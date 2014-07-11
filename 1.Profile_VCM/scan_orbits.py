#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-04-24

from orbit_vcm import vcm_file_from_333_orbits, vcm_file_from_333_orbit
from datetime import datetime, timedelta
import calipso_local
import os

dayflag = 'night'

l2func = {'night':calipso_local.l2_night_files, 'day':calipso_local.l2_day_files}[dayflag]


def process_l2_orbits_period(start, end, where):
    
    current = start
    while current < end:
        outpath = where + '/%04d%02d/' % (current.year, current.month)
        l2files = l2func(current.year, current.month, current.day, havg=0.333)
        l2files.sort()
        for l2file in l2files:
            vcm_file_from_333_orbit(current, l2file, where=outpath)        
        # vcm_file_from_333_orbits(current, l2files, where=outpath)
        current += timedelta(days=1)


def main(year=2008, month=None, day=None, where='./out'):

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

    process_l2_orbits_period(start, end, where)
    

def test_day_run():
    
    import glob
    
    main(2008, 1, 1, where='./test.out/')
    outfiles = glob.glob('./test.out/200801/*.nc4')
    assert len(outfiles) > 0


if __name__ == '__main__':
    import plac
    plac.call(main)