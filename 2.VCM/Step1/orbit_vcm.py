#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel Sat May 10 14:48:13 2014

import orbit_vcm_cal 
import orbit_vcm_csat
import dimarray as da


def vcm_dataset_from_l2_orbits(calfilename):
    '''
    create a vcm dataset containing cloud masks from calipso and cloudsat data,
    based on a calipso orbit file.
    '''
    # 1st create Dataset from CALIPSO data
    vcm, outname = orbit_vcm_cal.vcm_dataset_from_l2_orbit(calfilename)
    # 2nd add CloudSat data to Dataset
    # geo_vcm is a numpy array
    geo_vcm = orbit_vcm_csat.vcm_from_cal_orbit(calfilename, vcm['vcm_cal05'].labels[1])
    if geo_vcm is None:
        return None, None
    vcm['vcm_csat'] = da.DimArray(geo_vcm, labels=vcm['vcm_cal05'].labels, dims=vcm['vcm_cal05'].dims)
    #vcm['vcm_csat_cal05'] = vcm['vcm_csat'] + vcm['vcm_cal05']
    #idx = vcm['vcm_csat_cal05'] > 1
    #vcm['vcm_csat_cal05'].ix[idx] = 1
    return vcm, outname
    

def vcm_file_from_l2_orbits(calfilename, where='./'):
    '''
    saves a vcm dataset in a file containing cloud masks from calipso and cloudsat data,
    based on a calipso orbit file.
    '''
    
    import os
    
    vcm, outname = vcm_dataset_from_l2_orbits(calfilename)
    if vcm is None:
        return
    
    # check if path exists, fix it if not
    if not os.path.isdir(where):
        print 'Creating dir ' + where
        os.mkdir(where)

    vcm.write_nc(where + outname, mode='w', zlib=True, complevel=9)
    

# TESTS

def test_vcm_dataset_from_l2_orbit():
    
    calfile = '/bdd/CALIPSO/Lidar_L2/05kmCLay.v2.01/2007/2007_01_01/CAL_LID_L2_05kmCLay-Prov-V2-01.2007-01-01T00-22-49ZN.hdf'
    vcm, outname = vcm_dataset_from_l2_orbits(calfile)
    assert outname=='vcm_2007-01-01T00-22-49ZN.nc4'
    assert 'vcm_csat' in vcm
    
    
def test_vcm_file_from_l2_orbit():
    
    import os
    
    testpath = './test.out/'
    calfile = '/bdd/CALIPSO/Lidar_L2/05kmCLay.v2.01/2007/2007_01_01/CAL_LID_L2_05kmCLay-Prov-V2-01.2007-01-01T00-22-49ZN.hdf'
    vcm_file_from_l2_orbits(calfile, where=testpath)
    assert os.path.isfile(testpath + 'vcm_2007-01-01T00-22-49ZN.nc4')