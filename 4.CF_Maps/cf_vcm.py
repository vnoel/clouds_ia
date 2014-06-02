#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-04-28

import numpy as np
import dimarray as da

vcm_names = 'vcm_csat+cal333-5', 'vcm_csat+cal333-20', 'vcm_csat+cal333-80', 'vcm_cal333'

def cf_from_vcm_orbit(vcm_orbit, lstep=2.):
    
    # create vcm_3d grid
    lonbins = np.r_[-180:180+lstep:lstep]
    latbins = np.r_[-90:90+lstep:lstep]
    nlon, nlat = lonbins.shape[0], latbins.shape[0]
    
    # read data
    data = da.read_nc(vcm_orbit)
    plon = data['lon'].values
    plat = data['lat'].values
    
    if not all(name in data for name in vcm_names):
        print 'Warning : some vcms are not present in file. Contained data :'
        print data
        return None
    
    altitude = data[vcm_names[0]].labels[1]
    nalt = altitude.shape[0]
    
    out = da.Dataset()

    for vcm_name in vcm_names:
        
        this_vcm = data[vcm_name].values
        nprof = np.zeros([nlon, nlat], dtype='uint16')
        cprof = np.zeros([nlon, nlat], dtype='uint16')
        
        for ilon, lon in enumerate(lonbins):
            
            idxlon = (plon >= lon) & (plon < (lon + lstep))
            if idxlon.sum() == 0:
                continue
            
            vcm_slice = this_vcm[idxlon,:]
            lat_slice = plat[idxlon]
            
            for ilat, lat in enumerate(latbins):
            
                idx = (lat_slice >= lat) & (lat_slice < (lat + lstep))
                this_nprof = np.sum(idx)
                if this_nprof == 0:
                    continue
            
                # number of profiles in the box
                nprof[ilon, ilat] = this_nprof
                
                # number of cloudy profiles in the box
                cloudyprofileflags = np.sum(vcm_slice[idx,:], axis=1) > 0
                cprof[ilon, ilat] = np.sum(cloudyprofileflags)
                
        
        out[vcm_name + '_cprof'] = da.DimArray(cprof, labels=[lonbins, latbins], dims=['lon', 'lat'])
        if 'nprof' not in out:
            out['nprof'] = da.DimArray(nprof, labels=[lonbins, latbins], dims=['lon', 'lat'])
    
    return out


def cf_file_from_vcm_orbit(vcm_orbit, where='./out/'):
    
    import os
    
    dataset = cf_from_vcm_orbit(vcm_orbit)
    
    outname = 'cf_' + vcm_orbit[-25:]
    if not os.path.isdir(where):
        print 'Creating dir ' + where
        os.mkdir(where)
    dataset.write_nc(where + outname, mode='w', zlib=True, complevel=9)


def cf_file_from_vcm_orbits(vcm_orbits, outname, where='./out'):
    
    import os
    
    dataset = None
    for vcm_orbit in vcm_orbits:
        out = cf_from_vcm_orbit(vcm_orbit)
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
    dataset.write_nc(where + outname, mode='w', zlib=True, complevel=9)


def test_orbits():
    
    import glob, os

    vcm_orbits = glob.glob('./in/200701/vcm_2007-01-01*.nc4')
    assert len(vcm_orbits) > 1

    cf_file_from_vcm_orbits(vcm_orbits, 'cf_2007-01-01.nc4', where='./test.out/')
    
    assert os.path.isfile('./test.out/cf_2007-01-01.nc4')
