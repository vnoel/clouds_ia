#!/usr/bin/env python
#encoding:utf-8

# Created by V. Noel [LMD/CNRS] on 2014-06-24

import vcm
import numpy as np
import dimarray as da

names = ['cal333+cal05+cal20+cal80+csat']
lstep = 1.
lonbins = np.r_[-180:180+lstep:lstep]


def cflon(f, altmin):

    # altmin is an array
    
    v = vcm.VCM(f)
    out = da.Dataset()

    # number of profiles per lon bin
    h, xx = np.histogram(v.lon.values, bins=lonbins)
    out['nprof'] = da.DimArray(h, labels=[lonbins[:-1]], dims=['lon',])
    out['nprof'].longname = 'Number of measured profiles'
    
    for n in names:
        
        cv = v.get_vcm(n)
        assert cv is not None
        
        outdict = dict()
        
        for a in altmin:
            
            idx = (v.altitude >= a) & (v.altitude < 22.5)
            cvslice = cv[:,idx]
            cloudy = np.sum(cvslice, axis=1)
            np.clip(cloudy, 0, 1, out=cloudy)
            
            h, xx = np.histogram(v.lon.values, bins=lonbins, weights=cloudy)
            outdict[a] = da.DimArray(h, labels=[lonbins[:-1]], dims=['lon',])
        
        outname = n + '_cprof'
        out[outname] = da.stack(outdict, axis='altmin')
        out[outname].longname = 'Number of cloudy profiles from cloud mask = ' + n
    
    return out


def cflon_files(files, altmin, outname, where):
    
    import os
    
    dataset = None
    for f in files:
        out = cflon(f, altmin)
        if out is None:
            return
        if dataset is None:
            dataset = out
            fields = dataset.keys()
        else:
            for field in fields:
                dataset[field] += out[field]
    
    if not os.path.isdir(where):
        print('Creating output dir ' + where)
        os.mkdir(where)
    
    print('Saving ' + where + outname)
    dataset.write_nc(where + outname, mode='w', zlib=True, complevel=9)
    