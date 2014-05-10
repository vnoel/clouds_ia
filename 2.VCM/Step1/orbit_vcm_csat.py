#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel Fri May 09 15h

import numpy as np
import os
from geoprof import GeoProf
from scipy.interpolate import interp1d


def _find_geoprof_file(year, month, day, cal_l2_file):
    
    orbit_id = cal_l2_file[-25:-4]
    
    path = '/bdd/CFMIP/OBS_LOCAL/ATRAIN_COLOC/CLOUDSAT_COLOC/GEOPROF-LIDAR/%04d/' % year
    folder = '%04d_%02d_%02d/' % (year, month, day)
    
    geofile = path + folder + 'CALTRACK-5km_CS-2B-GEOPROF_V1-00_' + orbit_id + '.hdf'
    
    if os.path.isfile(geofile):
        return geofile
    else:
        return None
    
    
    
def _geoprof_vcm_on_altitudes(geo_vcm, geo_alt, altitudes):
    
    nprof = geo_vcm.shape[0]
    nalt = altitudes.shape[0]

    vcm = np.zeros([nprof, nalt], dtype='uint8')
    for i in np.arange(nprof):
        f = interp1d(geo_alt[i,::-1], geo_vcm[i,::-1], kind='nearest')
        vcm[i,:] = f(altitudes)
    
    return vcm


def _geoprof_vcm_from_geoprof_file(geoprof_file):
    
    geo = GeoProf(geoprof_file)
    geovcm = geo.cloudmask()
    geoalt = geo.altitude()
    geo.close()
    return geovcm, geoalt
    

def vcm_from_cal_orbit(year, month, day, cal_l2_file, vcm_alt):
    
    geoprof_file = _find_geoprof_file(year, month, day, cal_l2_file)
    geoprof_vcm, geoprof_alt = _geoprof_vcm_from_geoprof_file(geoprof_file)
    vcm = _geoprof_vcm_on_altitudes(geoprof_vcm, geoprof_alt, vcm_alt)
    return vcm

# Tests
    
def test_find_geoprof_file():
    
    geofile = _find_geoprof_file(2007,1,1,'CAL_LID_L2_05kmCLay-Prov-V3-01.2007-01-01T00-22-49ZN.hdf')
    assert geofile == '/bdd/CFMIP/OBS_LOCAL/ATRAIN_COLOC/CLOUDSAT_COLOC/GEOPROF-LIDAR/2007/2007_01_01/CALTRACK-5km_CS-2B-GEOPROF_V1-00_2007-01-01T00-22-49ZN.hdf'
    

def test_geoprof_vcm_from_geoprof_file():
    
    geofile = '/bdd/CFMIP/OBS_LOCAL/ATRAIN_COLOC/CLOUDSAT_COLOC/GEOPROF-LIDAR/2007/2007_01_01/CALTRACK-5km_CS-2B-GEOPROF_V1-00_2007-01-01T00-22-49ZN.hdf'
    vcm, alt = _geoprof_vcm_from_geoprof_file(geofile)    
    assert vcm.shape == (3728, 125)
    assert alt.shape == (3728, 125)
    
    
def test_geoprof_vcm_on_altitudes():
    
    geofile = '/bdd/CFMIP/OBS_LOCAL/ATRAIN_COLOC/CLOUDSAT_COLOC/GEOPROF-LIDAR/2007/2007_01_01/CALTRACK-5km_CS-2B-GEOPROF_V1-00_2007-01-01T00-22-49ZN.hdf'
    geo_vcm, geo_alt = _geoprof_vcm_from_geoprof_file(geofile)    
    
    altitudes = np.r_[0:19.5+0.03:0.03]
    vcm = _geoprof_vcm_on_altitudes(geo_vcm, geo_alt, altitudes)
    assert vcm.shape[1] == altitudes.shape[0]
    
    # pour info : first cloudy profile = 8

    cloudyprofs0 = (geo_vcm > 20).sum(axis=1)
    cloudyprofs0[cloudyprofs0 > 1] = 1
    cloudyprofs1 = (vcm > 20).sum(axis=1)
    cloudyprofs1[cloudyprofs1 > 1] = 1

    assert cloudyprofs0.sum() == cloudyprofs1.sum()
    