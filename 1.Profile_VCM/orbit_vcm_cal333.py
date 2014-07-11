#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel 2014-05-20 13:09

import numpy as np
from calipso import level2
import dimarray as da

# altitude vector
vcm_alt = np.r_[0:19.5:0.03]
nalt = vcm_alt.shape[0]


def vcm_from_layers(nl, base, top, ltype):
    
    nprof = base.shape[0]
    vcm = np.zeros([nprof, nalt], dtype='int8')
    basecopy = base.copy()
        
    for i in xrange(nprof):
        for j in xrange(nl[i]):            
            idx = (vcm_alt >= basecopy[i,j]) & (vcm_alt < top[i,j])
            vcm[i, idx] = 1
    
    del basecopy
    
    return vcm


def downscale_333m_to_1km(time, lon, lat, vcm):
    
    # the time of a 1km profile is the time of the first 333m profile used for aggregation
    
    nprof = time.shape[0]
    nprof2 = np.int(1. * nprof / 3.)
    vcm2 = np.zeros([nprof2, nalt], dtype='int8')
    lon2 = np.zeros([nprof2])
    lat2 = np.zeros([nprof2])
    time2 = np.zeros([nprof2])
    for i in xrange(nprof2):
        i2 = i * 3
        time2[i] = time[i2]
        lon2[i] = np.mean(lon[i2:i2+3])
        lat2[i] = np.mean(lat[i2:i2+3])
        vcm2[i] = np.sum(vcm[i2:i2+3,:], axis=0)
    return time2, lon2, lat2, vcm2


def vcm_dataset_from_l2_orbit(filename):
    
    # print 'Creating vcm from l2 file ' + filename
    
    try:
        l2 = level2.Cal2(filename)
    except:
        return None
    
    lon, lat = l2.coords()
    tai_time = l2.time()
    nl, base, top = l2.layers()
    ltype = l2.layer_type()
    l2.close()
    
    vcm = vcm_from_layers(nl, base, top, ltype)
    tai_time, lon, lat, vcm = downscale_333m_to_1km(tai_time, lon, lat, vcm)

    dset = {'time':tai_time, 'altitude':vcm_alt, 'cal333':vcm, 'lon':lon, 'lat':lat}

    return dset
    

# test functions
# to run tests : py.test orbit_vcm.py
    
def test_vcm_nprof():
    
    test333 = '/homedata/noel/Data/333mCLay/2008/2008_01_01/CAL_LID_L2_333mCLay-ValStage1-V3-01.2008-01-01T01-30-23ZN.hdf'
    vcm = vcm_dataset_from_l2_orbit(test333)
    nprof = vcm['lon'].shape[0]
    assert nprof == 55920
    assert vcm['cal333'].shape[0] == nprof
    assert vcm['cal333'].shape[1] == 650
    print nprof
    assert np.all(np.isfinite(vcm['cal333'][:,:]))
