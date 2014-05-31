#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel Fri May 09 15h

import numpy as np
from caltrack.geoprof import GeoProf
from scipy.interpolate import interp1d
import dimarray as da
    
    
def _geoprof_vcm_on_altitudes(geo_vcm, geo_alt, altitudes):
    
    nprof = geo_vcm.shape[0]
    nalt = altitudes.shape[0]

    vcm = np.zeros([nprof, nalt], dtype='uint8')
    for i in np.arange(nprof):
        if np.max(geo_alt[i,:]) < 20:
            continue
        f = interp1d(geo_alt[i,::-1], geo_vcm[i,::-1], kind='nearest')
        vcm[i,:] = f(altitudes)
    vcm = (vcm >= 20)
    
    return vcm


def _geoprof_vcm_from_geoprof_file(geoprof_file):
    
    try:
        geo = GeoProf(geoprof_file)
    except TypeError:
        print 'Warning, cannot open ' + geoprof_file
        return None, None
    geovcm = geo.cloudmask()
    geoalt = geo.altitude()
    geotime = geo.time()
    geo.close()
    return geovcm, geoalt, geotime
    

def vcm_from_geoprof_file(geoprof_file, vcm_alt):
    
    geoprof_vcm, geoprof_alt, geoprof_time = _geoprof_vcm_from_geoprof_file(geoprof_file)
    if geoprof_vcm is None:
        return None
    vcm = _geoprof_vcm_on_altitudes(geoprof_vcm, geoprof_alt, vcm_alt)
    vcm_da = da.DimArray(vcm, labels=(geoprof_time, vcm_alt), dims=['tai_time', 'altitude'])

    return vcm_da
    

def vcm_from_cal_orbit(cal_l2_file, vcm_alt):
    
    geoprof_file = _find_geoprof_file(cal_l2_file)
    if geoprof_file is None:
        return None

    vcm = vcm_from_geoprof_file(geoprof_file, vcm_alt)

    return vcm

# Tests
        

def test_geoprof_vcm_from_geoprof_file():
    
    geofile = '/bdd/CFMIP/OBS_LOCAL/ATRAIN_COLOC/CLOUDSAT_COLOC/CALTRACK-GEOPROF/2007/2007_01_01/CALTRACK-5km_CS-2B-GEOPROF_V1-00_2007-01-01T00-22-49ZN.hdf'
    vcm, alt, time = _geoprof_vcm_from_geoprof_file(geofile)    
    assert vcm.shape == (3728, 125)
    assert alt.shape == (3728, 125)
    assert time.shape == (3728,)
    
    
def test_geoprof_vcm_on_altitudes():
    
    geofile = '/bdd/CFMIP/OBS_LOCAL/ATRAIN_COLOC/CLOUDSAT_COLOC/CALTRACK-GEOPROF/2007/2007_01_01/CALTRACK-5km_CS-2B-GEOPROF_V1-00_2007-01-01T00-22-49ZN.hdf'
    geo_vcm, geo_alt, geo_time = _geoprof_vcm_from_geoprof_file(geofile)    
    
    altitudes = np.r_[0:19.5+0.03:0.03]
    vcm = _geoprof_vcm_on_altitudes(geo_vcm, geo_alt, altitudes)
    assert vcm.shape[1] == altitudes.shape[0]
    
    # pour info : first cloudy profile = 8

    cloudyprofs0 = (geo_vcm >= 20).sum(axis=1)
    cloudyprofs0[cloudyprofs0 > 1] = 1
    cloudyprofs1 = (vcm > 0).sum(axis=1)
    cloudyprofs1[cloudyprofs1 > 1] = 1

    assert cloudyprofs0.sum() == cloudyprofs1.sum()
    