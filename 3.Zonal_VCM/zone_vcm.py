#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-02

import numpy as np
import dimarray as da
from numba import jit

latstep = 0.01
latbins = np.r_[-82:82+latstep:latstep]

vcm_names = 'vcm_csat+cal333-5', 'vcm_csat+cal333-20', 'vcm_csat+cal333-80', 'vcm_cal333'


def zone_vcm_from_vcm_orbit(vcm_orbit, latbins=latbins):
    
    # read data
    data = da.read_nc(vcm_orbit)    
    if not all(name in data for name in vcm_names):
        print 'Warning : some vcms are not present in file. Contained data :'
        print data
        return None
    
    # create zone_vcm grid
    nlat = latbins.shape[0]
    
    plat = data['lat'].values
    altitude = data[vcm_names[0]].labels[1]
    nalt = altitude.shape[0]
    
    out = da.Dataset()

    # ilatbins = vector with nprof indexes containing bin numbers
    ilatbins = np.digitize(plat, latbins)

    for vcm_name in vcm_names:
        
        print vcm_name
                
        this_vcm = data[vcm_name].values
        zone_vcm = np.zeros([nlat, nalt], dtype='uint16')
        if 'nprof' not in out:
            nprof = np.zeros([nlat], dtype='uint16')
        cprof = np.zeros([nlat], dtype='uint16')
        
        for i,ilatbin in enumerate(ilatbins):
            if 'nprof' not in out:
                nprof[ilatbin] += 1
            if np.sum(this_vcm[i,:]) > 0:
                cprof[ilatbin] += 1
                zone_vcm[ilatbin,:] += this_vcm[i,:]
        
        out[vcm_name] = da.DimArray(zone_vcm, labels=[latbins, altitude], dims=['lat', 'altitude'])
        out[vcm_name + '_cprof'] = da.DimArray(cprof, labels=[latbins], dims=['lat'])
        if 'nprof' not in out:
            out['nprof'] = da.DimArray(nprof, labels=[latbins], dims=['lat'])
    
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
