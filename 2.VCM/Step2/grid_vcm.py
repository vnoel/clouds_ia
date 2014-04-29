#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-04-28

import numpy as np
import dimarray as da

def grid_vcm_from_vcm_orbit(vcm_orbit, lstep=2.):
    
    # FIXME : this is very slow apparently : 24 seconds for one vcm orbit. Not good.
    # ~8 seconds for 1 vcm_XXkm and there's three of those.
    
    # create vcm_3d grid
    lonbins = np.r_[-180:180+lstep:lstep]
    latbins = np.r_[-90:90+lstep:lstep]
    nlon, nlat = lonbins.shape[0], latbins.shape[0]
    
    # read data
    data = da.read_nc(vcm_orbit)
    plon = data['lon'].values
    plat = data['lat'].values
    
    altitude = data['vcm_05km'].labels[1]
    nalt = altitude.shape[0]
    
    dataset = da.Dataset()

    for field in ['vcm_05km']:
        if not field.startswith('vcm_'):
            continue
        this_vcm = data[field]
        vcm_3d = np.zeros([nlon, nlat, nalt], dtype='uint16')
        nprof = np.zeros([nlon, nlat], dtype='uint16')
        for ilon, lon in enumerate(lonbins):
            idxlon = (plon >= lon) & (plon < (lon + lstep))
            if idxlon.sum() == 0:
                continue
            vcm_slice = this_vcm.ix[idxlon,:]
            lat_slice = plat[idxlon]
            for ilat, lat in enumerate(latbins):
                idx = (lat_slice >= lat) & (lat_slice < (lat + lstep))
                vcm_3d[ilon, ilat, :] = np.sum(vcm_slice.ix[idx,:], axis=0)
                nprof[ilon, ilat] = np.sum(idx)
        dataset[field] = da.DimArray(vcm_3d, labels=[lonbins, latbins, altitude], dims=['lon', 'lat', 'altitude'])
        dataset['nprof_' + field] = da.DimArray(nprof, labels=[lonbins, latbins], dims=['lon', 'lat'])
    
    return dataset


def grid_vcm_file_from_vcm_orbit(vcm_orbit, where='./out/'):
    
    import os
    
    dataset = grid_vcm_from_vcm_orbit(vcm_orbit)
    
    outname = 'vcm_lat_' + vcm_orbit[-25:]
    if not os.path.isdir(where):
        print 'Creating dir ' + where
        os.mkdir(where)
    dataset.write_nc(where + outname, mode='w')


def test_orbit():
    
    vcm_orbit = './in/200901/vcm_2009-01-15T05-17-43ZN.nc4'
    grid_vcm_file_from_vcm_orbit(vcm_orbit)