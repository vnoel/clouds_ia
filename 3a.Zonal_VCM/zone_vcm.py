#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-02

import numpy as np
import dimarray as da
import vcm

latstep = 0.1
latbins = np.r_[-82:82+latstep:latstep]

vcm_names = ['cal333+cal05+cal20+cal80+csat']

def zone_vcm_from_vcm_orbit(vcm_orbit, latbins=latbins):
    
    # read data
    print 'opening ' + vcm_orbit
    v = vcm.VCM(vcm_orbit, verbose=False)
    
    nlat = latbins.shape[0]
    nalt = v.altitude.shape[0]
    
    out = da.Dataset()

    # ilatbins = vector with nprof indexes containing bin numbers
    ilatbins = np.digitize(v.lat, latbins)
    lat_axes = da.Axis(latbins[:-1], 'lat')

    nprof, xx = np.histogram(v.lat, bins=latbins)
    out['nprof'] = da.DimArray(nprof * 3, [lat_axes])

    alt_axes = da.Axis(v.altitude, 'altitude')

    for name in vcm_names:
        
        this_vcm = v.get_vcm(name)
        zone_vcm = np.zeros([nlat-1, nalt], dtype='uint16')
        
        prof_is_cloudy = np.sum(this_vcm, axis=1)
        np.clip(prof_is_cloudy, 0, 3, out=prof_is_cloudy)
        cprof, xx = np.histogram(v.lat, bins=latbins, weights=prof_is_cloudy)
        out[name + '_cprof'] = da.DimArray(cprof, [lat_axes])
        
        for i,ilatbin in enumerate(ilatbins[:-1]):
            if prof_is_cloudy[i] > 0:
                zone_vcm[ilatbin,:] += np.take(this_vcm, i, axis=0)
        out[name] = da.DimArray(zone_vcm, [lat_axes, alt_axes], longname='Number of cloudy points in lat-z bin, considering ' + name)
    
    return out


def zone_vcm_file_from_vcm_orbits(vcm_orbits, outname, where='./out'):
    
    import os

    dataset = zone_vcm_from_vcm_orbit(vcm_orbits)
    if dataset is None:
        return
        
    dataset.author = 'Vincent Noel, LMD/CNRS'
        
    if not os.path.isdir(where):
        print 'Creating dir ' + where
        os.mkdir(where)
        
    dataset.write_nc(where + outname, mode='w', zlib=True, complevel=9)
