#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-04-24

from orbit_vcm import vcm_file_from_l2_orbits
from datetime import datetime, timedelta
import calipso_local
import os


def process_l2_orbits_period(start, end, where):
    
    current = start
    while current < end:
        outpath = where + '/%04d%02d/' % (current.year, current.month)
        l2files = calipso_local.l2_night_files(current.year, current.month, current.day)
        for l2file in l2files:
            vcm_file_from_l2_orbits(l2file, where=outpath)
        
        current += timedelta(days=1)


def main(year=2007, month=None, day=None, where='./out'):

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

    process_l2_orbits_period(start, end, where)
    

def test_day_run():
    
    import glob
    
    main(2007, 1, 1, where='./test.out/')
    outfiles = glob.glob('./test.out/200701/*.nc4')
    assert len(outfiles) > 0


if __name__ == '__main__':
    import plac
    plac.call(main)