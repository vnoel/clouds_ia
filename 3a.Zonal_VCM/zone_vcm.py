#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-02

import numpy as np
import dimarray as da
import vcm

latstep = 0.01
latbins = np.r_[-82:82+latstep:latstep]

# vcm_names = 'cal333', 'cal333+cal05', 'cal333+cal05+cal20', 'cal333+cal05+cal20+cal80', 'cal333+cal05+cal20+cal80+csat'
vcm_names = ['cal333+cal05+cal20+cal80+csat', 'cal333+cal05+cal20+cal80']

def zone_vcm_from_vcm_orbit(vcm_orbit, latbins=latbins):
    
    # read data
    v = vcm.VCM(vcm_orbit)
    
    nlat = latbins.shape[0]
    nalt = v.altitude.shape[0]
    
    out = da.Dataset()

    # ilatbins = vector with nprof indexes containing bin numbers
    ilatbins = np.digitize(v.lat, latbins)

    nprof = np.zeros([nlat], dtype='uint16')
    h, xx = np.histogram(v.lat, bins=latbins)
    nprof[:-1] = h
    out['nprof'] = da.DimArray(nprof, labels=[latbins,], dims=['lat',])
    ialt1 = (v.altitude > 1)

    for name in vcm_names:
        
        this_vcm = v.get_vcm(name)
        zone_vcm = np.zeros([nlat, nalt], dtype='uint16')
        cprof = np.zeros([nlat], dtype='uint16')
        
        prof_is_cloudy = (np.sum(this_vcm, axis=1) > 0)
        h, xx = np.histogram(v.lat, bins=latbins, weights=1 * prof_is_cloudy)
        cprof[:-1] = h
        out[name + '_cprof'] = da.DimArray(cprof, labels=[latbins], dims=['lat',])
        
        # prof_is_cloudy = (np.sum(this_vcm[:,ialt1], axis=1) > 0)
        # h, xx = np.histogram(v.lat, bins=latbins, weights=1 * prof_is_cloudy)
        # cprof[:-1] = h
        # out[name + '_cprof1km'] = da.DimArray(cprof, labels=[latbins], dims=['lat',])
        
        for i,ilatbin in enumerate(ilatbins):
            if prof_is_cloudy[i]:
                np.add(zone_vcm[ilatbin,:], this_vcm[i,:], out=zone_vcm[ilatbin,:])
        out[name] = da.DimArray(zone_vcm, labels=[latbins, v.altitude], dims=['lat', 'altitude'], longname='Number of cloudy points in lat-z bin, considering ' + name)
    
    return out


def zone_vcm_file_from_vcm_orbits(vcm_orbits, outname, where='./out'):
    
    import os
    
    dataset = None
    for vcm_orbit in vcm_orbits:
        out = zone_vcm_from_vcm_orbit(vcm_orbit)
        if out is None:
            continue
        if dataset is None:
            dataset = out
            fields = dataset.keys()
        else:
            for field in fields:
                dataset[field] += out[field]
        
    if dataset is None:
        return
        
    dataset.author = 'Vincent Noel, LMD/CNRS'
        
    if not os.path.isdir(where):
        print 'Creating dir ' + where
        os.mkdir(where)
        
    dataset.write_nc(where + outname, mode='w', zlib=True, complevel=9)


def test_orbits():
    
    import glob, os

    vcm_orbits = glob.glob('./in/200701/vcm_2007-01-01*.nc4')
    assert len(vcm_orbits) > 1

    zone_vcm_file_from_vcm_orbits(vcm_orbits, 'zone_vcm_grid_2007-01-01.nc4', where='./test.out/')
    
    assert os.path.isfile('./test.out/zone_vcm_grid_2007-01-01.nc4')
