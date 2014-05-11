#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel Sat May 10 14:48:13 2014

import orbit_vcm_cal 
import orbit_vcm_csat
import dimarray as da


def vcm_dataset_from_l2_orbit(filename):
    '''
    create a vcm dataset containing cloud masks from calipso and cloudsat data,
    based on a calipso orbit file.
    '''
    # 1st create Dataset from CALIPSO data
    vcm, outname = orbit_vcm_cal.vcm_dataset_from_l2_orbit(filename)
    # 2nd add CloudSat data to Dataset
    # geo_vcm is a numpy array
    geo_vcm = orbit_vcm_csat.vcm_from_cal_orbit(filename, vcm['vcm_05km'].labels[1])
    vcm['vcm_csat'] = da.DimArray(geo_vcm, labels=vcm['vcm_05km'].labels, dims=vcm['vcm_05km'].dims)
    return vcm, outname
    

def vcm_file_from_l2_orbit(filename, where='./'):
    '''
    saves a vcm dataset in a file containing cloud masks from calipso and cloudsat data,
    based on a calipso orbit file.
    '''
    
    vcm, outname = vcm_dataset_from_l2_orbit(filename)
    # check if path exists, fix it if not
    vcm.write_nc(where + outname, mode='w')
    

def test_vcm_dataset_from_l2_orbit():
    
    import calipso_local

    l2files = calipso_local.l2_night_files(2007,1,1)
    vcm, outname = vcm_dataset_from_l2_orbit(l2files[0])
    print vcm
    