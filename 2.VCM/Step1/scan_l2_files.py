#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-04-24

from orbit_vcm import vcm_file_from_l2_orbit

def main(year=2007, month=None, day=None):
    
    if day is not None and month is not None:
        start = datetime(year, month, day)
        end = start
    elif day is None and month is not None:
        start = datetime(year, month, 1)
        end = start + timedelta(days=31)
    else:
        start = datetime(year, 1, 1)
        end = datetime(year, 12, 31)

    current = start
    while current <= end:
        
        l2files = calipso_local.l2files(current.year, current.month, current.day)
        for l2file in l2files:
            vcm_file_from_l2_orbit(l2file, where='./out/%04d%02/' % (current.year, current.month))        
        
        current += timedelta(days=1)


if __name__ == '__main__':
    import plac
    plac.call(main)