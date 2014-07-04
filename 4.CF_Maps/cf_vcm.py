#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-04-28

import numpy as np
import dimarray as da

vcm_names = ['cal333+cal05+cal20+cal80+csat']

# create grid
lonbins = np.r_[-180:180+lstep:lstep]
latbins = np.r_[-90:90+lstep:lstep]

def cf_from_vcm_orbit(vcm_orbit, layers, lstep=2.):
    
    # read data
    v = vcm.VCM(vcm_orbit)
    plon = v.lon.values
    plat = v.lat.values
        
    altitude = v.altitude
    
    for layer in layers:
        
        altrange = layers[layer]
        altidx = (altitude >= altrange[0]) & (altitude < altrange[1])
        
        out = da.Dataset()

        # gridded number of profiles
        h, xx, yy = np.histogram2d(plon, plat, bins=(lonbins, latbins))
        out['nprof'] = da.DimArray(h, labels=[lonbins[:-1], latbins[:-1]], dims=['lon', 'lat'])
        out['nprof'].longname = 'Number of measured profiles'

        for vcm_name in vcm_names:
        
            # number of cloudy profiles in grid and altitude range

            this_vcm = v.get_vcm(vcm_name)
            assert this_vcm is not None
        
            cloudy_profile = np.sum(this_vcm[:,altidx], axis=1)
            np.clip(cloudy_profile, 0, 1, out=cloudy_profile)
        
            h, xx, yy = np.histogram2d(plon, plat, bins=(lonbins, latbins), weights=cloudy_profile)
            outname = vcm_name + '_cprof_%s' % (layer)
            out[outname] = da.DimArray(h, labels=[lonbins[:-1], latbins[:-1]], dims=['lon', 'lat'])
            out[outname].longname = 'Number of cloudy profiles from cloud mask = ' + vcm_name + ' at altitudes %5.2f - %5.2f' % (*altrange)
    
    return out


def cf_file_from_vcm_orbit(vcm_orbit, where='./out/'):
    
    import os
    
    dataset = cf_from_vcm_orbit(vcm_orbit)
    
    outname = 'cf_' + vcm_orbit[-25:]
    if not os.path.isdir(where):
        print 'Creating dir ' + where
        os.mkdir(where)
    dataset.write_nc(where + outname, mode='w', zlib=True, complevel=9)


def cf_file_from_vcm_orbits(vcm_orbits, layers, outname, where='./out'):
    
    import os
    
    dataset = None
    for vcm_orbit in vcm_orbits:
        out = cf_from_vcm_orbit(vcm_orbit, layers)
        if out is None:
            return
        if dataset is None:
            dataset = out
            fields = dataset.keys()
        else:
            for field in fields:
                dataset[field] += out[field]
        
    if not os.path.isdir(where):
        print 'Creating dir ' + where
        os.mkdir(where)
    
    print('Saving ' + where + outname)
    dataset.write_nc(where + outname, mode='w', zlib=True, complevel=9)


def test_orbits():
    
    import glob, os

    vcm_orbits = glob.glob('./in/200701/vcm_2007-01-01*.nc4')
    assert len(vcm_orbits) > 1

    cf_file_from_vcm_orbits(vcm_orbits, 'cf_2007-01-01.nc4', where='./test.out/')
    
    assert os.path.isfile('./test.out/cf_2007-01-01.nc4')
