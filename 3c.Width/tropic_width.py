#!/usr/bin/env python
#encoding:utf-8

# Created by V. Noel [LMD/CNRS] on 2014-06-04

import numpy as np

def tropic_width(lat, alt, vcm, height=16.):
    
    ialt = np.argmin(np.abs(alt-16.))
    print 'Using alt = ', alt[ialt]
    vcmslice = vcm[:,ialt]
    idx = (vcmslice > 0.05) & (lat > -60) & (lat < 60)
    
    latrange = [np.min(lat[idx]), np.max(lat[idx])]
    return latrange
    
def cloud_cover_top(alt, vcm):
    
    nlat = vcm.shape[0]
    cloud_top = np.zeros(nlat)
    
    for ilat in np.arange(nlat):
        vcmslice = vcm[ilat,:]
        idx = (vcmslice > 0.05) & (alt < 19)
        try:
            cloud_top[ilat] = np.max(alt[idx])
        except ValueError:
            cloud_top[ilat] = -1
            
    return cloud_top