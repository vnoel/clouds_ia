#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-02

from datetime import datetime, timedelta
import meridhov
import glob
import os

altmin = [7, 10, 13]
latbounds = [-30, 30]

def process_vcm_orbits_period(start, end, where):

    if not os.path.isdir(where):
        print 'Creating dir ' + where
        os.mkdir(where)

    current = start
    while current < end:
        
        inpath = './in/%04d%02d/' % (current.year, current.month)
        mask = 'vcm_%04d-%02d-%02d*.nc4' % (current.year, current.month, current.day)
        vcm_files = glob.glob(inpath + mask)
        print inpath + mask + ' %d files' % len(vcm_files)
        if len(vcm_files) < 1:
            current += timedelta(days=1)
            continue
        
        outpath = where + '%04d%02d/' % (current.year, current.month)
        outname = 'cflon_%04d-%02d-%02d.nc4' % (current.year, current.month, current.day)
        
        meridhov.cflon_files(vcm_files, altmin, latbounds, outname, where=outpath)
        
        current += timedelta(days=1)


def main(year=2007, month=None, day=None, where='out.daily/'):

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
        end = datetime(year, 12, 31)

    process_vcm_orbits_period(start, end, where)


def test_day_grid_for_orbits():
    
    import os
    
    main('total',2008,1,1,where='test.out/')
    assert os.path.isfile('test.out/200801/cf_total_2008-01-01.nc4')
        

if __name__=='__main__':
    import plac
    plac.call(main)