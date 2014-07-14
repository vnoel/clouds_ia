#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-04-28

import numpy as np
import dimarray as da
import vcm

vcm_names = ['cal333+cal05+cal20+cal80+csat']

# create grid
lstep = 2.
lonbins = np.r_[-180:180+lstep:lstep]
latbins = np.r_[-90:90+lstep:lstep]

# vcm_orbit can be a file, a file list or a file mask
def cf_from_vcm_orbit(vcm_orbit, layers):
    
    print 'Creating vcm from ', vcm_orbit
    
    # read data
    v = vcm.VCM(vcm_orbit, verbose=False)
        
    print '%d profiles' % (v.lon.shape[0])
    
    lon_axis = da.Axis(lonbins[:-1], 'lon')
    lat_axis = da.Axis(latbins[:-1], 'lat')

    # gridded number of profiles
    h, xx, yy = np.histogram2d(v.lon, v.lat, bins=(lonbins, latbins))

    out = da.Dataset()
    out['nprof'] = da.DimArray(h * 3, [lon_axis, lat_axis])
    out['nprof'].longname = 'Number of measured profiles'

    for layer in layers:
        
        altrange = layers[layer]
        altidx = np.where((v.altitude >= altrange[0]) & (v.altitude < altrange[1]))[0]
        
        for vcm_name in vcm_names:
        
            # number of cloudy profiles in grid and altitude range

            this_vcm = v.get_vcm(vcm_name)
            assert this_vcm is not None
        
            if layer == 'total':
                t = this_vcm
            else:
                t = np.take(this_vcm, altidx, axis=1)
            cloudy_profile = np.sum(t, axis=1)
            np.clip(cloudy_profile, 0, 3, out=cloudy_profile)
        
            h, xx, yy = np.histogram2d(v.lon, v.lat, bins=(lonbins, latbins), weights=cloudy_profile)
            outname = vcm_name + '_cprof_%s' % (layer)
            out[outname] = da.DimArray(h, [lon_axis, lat_axis])
            out[outname].longname = 'Number of cloudy profiles from cloud mask = ' + vcm_name + ' at altitudes %5.2f - %5.2f' % (altrange[0], altrange[1])
    
    return out

# vcm_orbits can be a filelist or a file mask
def cf_file_from_vcm_orbits(vcm_orbits, layers, outname, where='./out'):
    
    import os
    
    dataset = cf_from_vcm_orbit(vcm_orbits, layers)

    if not os.path.isdir(where):
        print 'Creating dir ' + where
        os.mkdir(where)
    
    print('Saving ' + where + outname)
    dataset.write_nc(where + outname, mode='w', zlib=True, complevel=9)
