#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-07-15

from datetime import datetime, timedelta
from csat_cal_vcm import csat_no_cal
import glob
import os
    

def process_vcm_orbits_period(start, end, where):

    if not os.path.isdir(where):
        print 'Creating dir ' + where
        os.mkdir(where)

    current = start
    while current < end:
        
        inpath = './in/%04d%02d/' % (current.year, current.month)
        mask = 'vcm_%04d-%02d-%02d*_v2.0.nc4' % (current.year, current.month, current.day)
        vcm_files = glob.glob(inpath + mask)
        if len(vcm_files) < 1:
            current += timedelta(days=1)
            continue

        print inpath + mask + ' : %d files' % (len(vcm_files))
        
        outpath = where + '%04d%02d/' % (current.year, current.month)
        outname = 'vcm_csatcal_%04d-%02d-%02d.nc4' % (current.year, current.month, current.day)
        
        csat_no_cal(inpath + mask, outname, where=outpath)
        
        current += timedelta(days=1)


def main(year=2007, month=None, day=None, where='out/'):

    if day is not None and month is not None:
        year, month, day = int(year), int(month), int(day)
        start = datetime(year, month, day)
        end = start + timedelta(days=1)
    elif day is None and month is not None:
        year, month = int(year), int(month)
        start = datetime(year, month, 1)
        end = start + timedelta(days=31)
    else:
        year = int(year)
        start = datetime(year, 1, 1)
        end = datetime(year+1, 1, 1)

    process_vcm_orbits_period(start, end, where)


if __name__=='__main__':
    import plac
    plac.call(main)
