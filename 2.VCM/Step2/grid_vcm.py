#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-04-28

import numpy as np
import dimarray as da


def grid_vcm_from_vcm_orbit(vcm_orbit, lstep=2.):
    
    # create vcm_3d grid
    lonbins = np.r_[-180:180+lstep:lstep]
    latbins = np.r_[-90:90+lstep:lstep]
    nlon, nlat = lonbins.shape[0], latbins.shape[0]
    
    # read data
    data = da.read_nc(vcm_orbit)
    plon = data['lon'].values
    plat = data['lat'].values
    
    altitude = data['vcm_cal05'].labels[1]
    nalt = altitude.shape[0]
    
    out = da.Dataset()

    for field in data:
        
        if not field.startswith('vcm_'):
            continue
        
        this_vcm = data[field].values
        # we're binning profiles at 5km res
        # for one day, no chance to get more than ~50 5km profiles in a 2x2 box.
        # no guarantees for other resolutions or periods !
        vcm_3d = np.zeros([nlon, nlat, nalt], dtype='uint8')
        nprof = np.zeros([nlon, nlat], dtype='uint8')
        
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
            
                nprof[ilon, ilat] = this_nprof
                vcm_3d[ilon, ilat, :] = np.sum(vcm_slice[idx,:], axis=0)
        
        out[field] = da.DimArray(vcm_3d, labels=[lonbins, latbins, altitude], dims=['lon', 'lat', 'altitude'])
        if 'nprof' not in out:
            out['nprof'] = da.DimArray(nprof, labels=[lonbins, latbins], dims=['lon', 'lat'])
    
    return out


def grid_vcm_file_from_vcm_orbit(vcm_orbit, where='./out/'):
    
    import os
    
    dataset = grid_vcm_from_vcm_orbit(vcm_orbit)
    
    outname = 'vcm_grid_' + vcm_orbit[-25:]
    if not os.path.isdir(where):
        print 'Creating dir ' + where
        os.mkdir(where)
    dataset.write_nc(where + outname, mode='w', zlib=True, complevel=9)


def grid_vcm_file_from_vcm_orbits(vcm_orbits, outname, where='./out'):
    
    import os
    
    dataset = None
    for vcm_orbit in vcm_orbits:
        out = grid_vcm_from_vcm_orbit(vcm_orbit)
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


def test_orbit():
    
    import os
    
    vcm_orbit = './in/200701/vcm_2007-01-01T00-22-49ZN.nc4'
    grid_vcm_file_from_vcm_orbit(vcm_orbit, where='./test.out/')
    
    assert os.path.isfile('./test.out/vcm_grid_2007-01-01T00-22-49ZN.nc4')
    
    
def test_orbits():
    
    import glob, os

    vcm_orbits = glob.glob('./in/200701/vcm_2007-01-01*.nc4')
    assert len(vcm_orbits) > 1

    grid_vcm_file_from_vcm_orbits(vcm_orbits, 'vcm_grid_2007-01-01.nc4', where='./test.out/')
    
    assert os.path.isfile('./test.out/vcm_grid_2007-01-01.nc4')