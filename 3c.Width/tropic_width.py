#!/usr/bin/env python
#encoding:utf-8

# Created by V. Noel [LMD/CNRS] on 2014-06-04

import numpy as np
import matplotlib.pyplot as plt

def tropic_width(lat, alt, vcm, height=16.):
    
    ialt = np.argmin(np.abs(alt-16.))
    print 'Using alt = ', alt[ialt]
    vcmslice = vcm[:,ialt]
    idx = (vcmslice > 0.05) & (lat > -60) & (lat < 60)
    
    latrange = [np.min(lat[idx]), np.max(lat[idx])]
    return latrange
 
    
def tropic_width3(lat, alt, vcm, vcm_min=0.05):
    
    cover_top = cloud_cover_top(alt, vcm, vcm_min=0.05)
    idx = (lat > -30) & (lat < 30)
    
    # sorted cover tops between + and - 30 degrees
    # 6000 points = 60 degrees = 6000 km
    # 100km average = 100 highest points
    sorted_tops = np.sort(cover_top[idx])
    trop_ceiling = np.mean(sorted_tops[-100:])
    height = trop_ceiling - 2.
    
    print('Tropic ceiling = {} km'.format(trop_ceiling))
    print('Cutting tropic hat at {} km'.format(height))

    cover_top2 = cloud_cover_top(alt, vcm, vcm_min=vcm_min)
    idx = (cover_top2 > height) & (lat > -40) & (lat < 40)
    
    if np.sum(idx) == 0:
        tropmin = -1
        tropmax = -1
    else:
        tropmin = np.min(lat[idx])
        tropmax = np.max(lat[idx])
    
    return tropmin, tropmax, trop_ceiling, height
    
    
def tropic_width2(lat, alt, vcm):
    
    cover_top = cloud_cover_top(alt, vcm)
    
    thislat = lat[:-100]
    altchange = cover_top[100:] - cover_top[:-100]

    ilat = (thislat > -40) & (thislat < 10)
    ilatup = (altchange[ilat] > 1.)
    latup = np.min(thislat[ilat][ilatup])
    ilat = (thislat > 10) & (thislat < 40)
    ilatdown = (altchange[ilat] < -1)
    if np.sum(ilatdown)==0:
        latdown = thislat[ilat][np.argmin(altchange[ilat])]
    else:
        latdown = np.max(thislat[ilat][ilatdown])
    return latup, latdown
    
    
def cloud_cover_top(alt, vcm, vcm_min=0.05):
    
    nlat = vcm.shape[0]
    cloud_top = np.zeros(nlat)
    
    for ilat in np.arange(nlat):
        vcmslice = vcm[ilat,:]
        idx = (vcmslice > vcm_min) & (alt < 19)
        try:
            cloud_top[ilat] = np.max(alt[idx])
        except ValueError:
            cloud_top[ilat] = -1
            
    return cloud_top