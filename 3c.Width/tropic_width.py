#!/usr/bin/env python
#encoding:utf-8

# Created by V. Noel [LMD/CNRS] on 2014-06-04

import numpy as np

def tropic_width(lat, alt, vcm, height=16.):
    
    ialt = np.argmin(np.abs(alt-16.))
    vcmslice = vcm[:,ialt]
    idx = (vcmslice > 0.05)
    
    latrange = [np.min(lat[idx]), np.max(lat[idx])]
    return latrange