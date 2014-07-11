#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-07-10

import netCDF4
import glob
from datetime import datetime

day = datetime(2007, 2, 3)

# 14 files

# compression levels = 9 - 1 file = 1.1MB
# warm cache : 3.3 seconds
# cold cache : 3.7 seconds

# compression level = 6 - 1 file = 1.4MB

# compression level = 4 (default) - 1 file = 1.8MB
# warm cache : 3s
# cold cache : 4.1s

# il y a un leger gain en lecture quand on compresse moins, mais rien de bien extravagant
# C'est genre 10% speedup.
# Par comparaison, utiliser netCDF4 directement vs dimarray c'est 300% speedup.

flist = glob.glob('out/%04d%02d/vcm_%04d-%02d-%02d*.nc4' % (day.year, day.month, day.year, day.month, day.day))
for f in flist:
    nc = netCDF4.Dataset(f, 'r')
    time = nc.variables['tai_time'][:]
    lon = nc.variables['lon'][:]
    lat = nc.variables['lat'][:]
    altitude = nc.variables['altitude'][:]
    cal333 = nc.variables['cal333'][:]
    csat = nc.variables['csat'][:]
    nc.close()
    
