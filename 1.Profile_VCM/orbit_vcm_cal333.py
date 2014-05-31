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
    vcm = np.zeros([nprof, nalt], dtype='uint8')
    basecopy = base.copy()
        
    # clean up unwanted layers first
    # for clouds, feature type == layer_type == 2
    #basecopy[ltype != 2] = -9999.
    
    for i in xrange(nprof):
        
        for j in xrange(nl[i]):
            
            if basecopy[i,j] < 0:
                continue

            idx = (vcm_alt >= basecopy[i,j]) & (vcm_alt < top[i,j])
            vcm[i, idx] = 1
    
    del basecopy
    
    return vcm


def vcm_dataset_from_l2_orbit(filename):
    
    print 'Creating vcm from l2 file ' + filename
    
    try:
        l2 = level2.Cal2(filename)
    except:
        return None
    
    lon, lat = l2.coords()
    tai_time = l2.time()
    nl, base, top = l2.layers()
    ltype = l2.layer_type()
    
    vertical_cloud_masks = da.Dataset()
    
    time_axis = ('tai_time', tai_time)
    alt_axis = ('altitude', vcm_alt)
    
    vcm = vcm_from_layers(nl, base, top, ltype)
    vertical_cloud_masks['vcm_cal333'] = da.DimArray(vcm, (time_axis, alt_axis))
    vertical_cloud_masks['lon'] = da.DimArray(lon, (time_axis,))
    vertical_cloud_masks['lat'] = da.DimArray(lat, (time_axis,))

    return vertical_cloud_masks
    

# test functions
# to run tests : py.test orbit_vcm.py
    
def test_vcm_nprof():
    
    import calipso_local
    import glob
    
    out = './test.out'
    test333 = '/homedata/noel/Data/333mCLay/2008/2008_01_01/CAL_LID_L2_333mCLay-ValStage1-V3-01.2008-01-01T01-30-23ZN.hdf'
    vcm = vcm_dataset_from_l2_orbit(test333)
    nprof = vcm['lon'].shape[0]
    assert nprof == 55920
    assert vcm['vcm_cal333'].shape[0] == nprof
    assert vcm['vcm_cal333'].shape[1] == 650
    print nprof
    assert np.all(np.isfinite(vcm['vcm_cal333'][:,:]))
