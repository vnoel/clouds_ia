#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-07-09

import matplotlib.pyplot as plt
import dimarray as da
from calipso.level2 import Cal2

f = 'out/200809/vcm_2008-09-02T10-14-57ZN.nc4'
c2f = '/DATA/LIENS/CALIOP/05kmCLay/2008/2008_09_02/CAL_LID_L2_05kmCLay-Prov-V3-01.2008-09-02T18-29-23ZN.hdf'

c = Cal2(c2f)

nl, base, top = c.layers()
lon, lat = c.coords()
havg = c.horizontal_averaging()
flag = c.flag()
ltype = c.layer_type()
lstype = c.layer_subtype()

base[base < 0] = 0
top[top < 0] = 0

ilat = (lat < -60)
print lat[ilat]

plt.plot(lat[ilat], base[ilat,:])
plt.plot(lat[ilat], top[ilat,:])
plt.show()

print flag.shape
idx = (top[ilat,:] > 15)
print ltype[ilat,:][idx]
print lstype[ilat,:][idx]
print flag[ilat,:][idx]