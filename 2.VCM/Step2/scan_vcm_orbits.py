#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-04-28

from datetime import datetime, timedelta
from grid_vcm import grid_vcm_file_from_vcm_orbit
import glob
    

def process_vcm_orbits_period(start, end):

    current = start
    while current <= end:
        
        inpath = './in/%04d%02d/' % (current.year, current.month)
        mask = 'vcm_%04d-%02d-%02d*.nc4' % (current.year, current.month, current.day)
        vcm_files = glob.glob(inpath + mask)
        print inpath, mask, current, len(vcm_files)
        for vcm_file in vcm_files:
            grid_vcm_file_from_vcm_orbit(vcm_file, where='out/%04d%02d/' % (current.year, current.month))
        
        current += timedelta(days=1)


def main(year=2009, month=None, day=None):

    if day is not None and month is not None:
        year, month, day = int(year), int(month), int(day)
        start = datetime(year, month, day)
        end = start
    elif day is None and month is not None:
        year, month = int(year), int(month)
        start = datetime(year, month, 1)
        end = start + timedelta(days=31)
    else:
        year = int(year)
        start = datetime(year, 1, 1)
        end = datetime(year, 12, 31)

    process_vcm_orbits_period(start, end)


def test_day_run():
    
    orbit_files = glob.glob('in/200901/vcm_2009-01-01*.nc4')
    main(2009,1,1)
    grid_files = glob.glob('out/200901/vcm_lat_*.nc4')
        
    assert len(orbit_files)==len(grid_files)
    assert False
        