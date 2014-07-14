#!/usr/bin/env python
#encoding:utf-8

# Created by V. Noel [LMD/CNRS] on 2014-06-24

import vcm
import numpy as np
import dimarray as da

names = ['cal333+cal05+cal20+cal80+csat']
lstep = 1.
lonbins = np.r_[-180:180+lstep:lstep]


def cflon(f, altmin, latbounds):

    # altmin is an array
    
    v = vcm.VCM(f, verbose=False)
    out = da.Dataset()

    lon_axis = da.Axis(lonbins[:-1], 'lon')

    # number of profiles per lon bin
    h, xx = np.histogram(v.lon, bins=lonbins)
    out['nprof'] = da.DimArray(h, [lon_axis])
    out['nprof'].longname = 'Number of measured profiles'
    
    for n in names:
        
        cv = v.get_vcm(n)
        assert cv is not None
        
        # clip latitudes
        latidx = (v.lat >= latbounds[0]) & (v.lat < latbounds[1])
        cv = np.take(cv, latidx, axis=0)
        lon = np.take(v.lon, latidx, axis=0)
        
        outdict = dict()
        
        for a in altmin:
            
            idx = np.where(v.altitude >= a)[0]
            cloudy = np.take(cv, idx, axis=1)
            cloudy = np.sum(cloudy, axis=1)
            np.clip(cloudy, 0, 1, out=cloudy)
            
            h, xx = np.histogram(v.lon, bins=lonbins, weights=cloudy)
            outdict[a] = da.DimArray(h, [lon_axis,])
        
        outname = n + '_cprof'
        out[outname] = da.stack(outdict, axis='altmin')
        out[outname].longname = 'Number of cloudy profiles from cloud mask = ' + n
    
    return out


def cflon_files(files, altmin, latbounds, outname, where):
    
    import os
    
    dataset = cflon(files, altmin, latbounds)
    if not os.path.isdir(where):
        print('Creating output dir ' + where)
        os.mkdir(where)
    
    print('Saving ' + where + outname)
    dataset.write_nc(where + outname, mode='w', zlib=True, complevel=9)
    