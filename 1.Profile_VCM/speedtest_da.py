#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-07-10

import vcm as vcm
import glob
from datetime import datetime

day = datetime(2007, 2, 13)
# 14 files of 1.1 MB = 15.4 MB
# warm cache : 9 seconds
# cold cache : 10 seconds
flist = glob.glob('out/%04d%02d/vcm_%04d-%02d-%02d*.nc4' % (day.year, day.month, day.year, day.month, day.day))
for f in flist:
    v = vcm.VCM(f)
    cal333 = v.get_vcm('cal333')
    csat = v.get_vcm('csat')
    
