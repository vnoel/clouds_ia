#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel Fri May 09 15h

import os
from geoprof import GeoProf


def find_geoprof_file(year, month, day, cal_l2_file):
    
    orbit_id = cal_l2_file[-25:-4]
    
    path = '/bdd/CFMIP/OBS_LOCAL/ATRAIN_COLOC/CLOUDSAT_COLOC/GEOPROF-LIDAR/%04d/' % year
    folder = '%04d_%02d_%02d/' % (year, month, day)
    
    geofile = path + folder + 'CALTRACK-5km_CS-2B-GEOPROF_V1-00_' + orbit_id + '.hdf'
    
    if os.path.isfile(geofile):
        return geofile
    else:
        return None
    
    
def geoprof_cm_on_altitudes(geo, altitudes):
    pass


def vcm_from_geoprof_orbit():
    pass


    
def test_finding():
    
    geofile = find_geoprof_file(2007,1,1,'CAL_LID_L2_05kmCLay-Prov-V3-01.2007-01-01T00-22-49ZN.hdf')
    assert geofile == '/bdd/CFMIP/OBS_LOCAL/ATRAIN_COLOC/CLOUDSAT_COLOC/GEOPROF-LIDAR/2007/2007_01_01/CALTRACK-5km_CS-2B-GEOPROF_V1-00_2007-01-01T00-22-49ZN.hdf'
    
    