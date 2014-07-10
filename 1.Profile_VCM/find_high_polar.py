#!/usr/bin/env python
#encoding:utf-8

# Created by V. Noel [LMD/CNRS] on 2014-07-09


import glob
import numpy as np
from datetime import datetime
import dimarray as da

d = datetime(2008,9,2)

mask = 'out/%04d%02d/vcm_%04d-%02d-%02d*.nc4' % (d.year, d.month, d.year, d.month, d.day)
print mask
files = glob.glob(mask)

for f in files:
    print 'Looking in', f
    d = da.read_nc(f)
    lat = d['lat']
    idxlat = lat.values < -60
    # idxlat = (lat.values > -30) & (lat.values < 30)
    alt = d['cal333'].altitude
    idxalt = alt > 15
    for var in 'cal333', 'cal05', 'cal20', 'cal80', 'csat':
        cm = d[var].values
        cm = cm[idxlat,:]
        cm = cm[:,idxalt]
        if np.sum(cm) > 0:
            print 'high polar clouds found in ', var, np.sum(cm)
        