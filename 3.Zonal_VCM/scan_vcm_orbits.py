#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-02

from datetime import datetime, timedelta
from zone_vcm import zone_vcm_file_from_vcm_orbits
import glob
import os
    

def process_vcm_orbits_period(start, end, where):

    if not os.path.isdir(where):
        print 'Creating dir ' + where
        os.mkdir(where)

    current = start
    while current < end:
        
        
        inpath = './in/%04d%02d/' % (current.year, current.month)
        mask = 'vcm_%04d-%02d-%02d*.nc4' % (current.year, current.month, current.day)
        vcm_files = glob.glob(inpath + mask)
        if len(vcm_files) < 1:
            current += timedelta(days=1)
            continue

        print current, ' : %d files' % (len(vcm_files))
        
        outpath = where + '%04d%02d/' % (current.year, current.month)
        outname = 'vcm_zonal_%04d-%02d-%02d.nc4' % (current.year, current.month, current.day)
        
        zone_vcm_file_from_vcm_orbits(vcm_files, outname, where=outpath)
        
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


def test_day_grid_for_orbits():
    
    import os
    
    orbit_files = glob.glob('in/200701/vcm_2007-07-07*.nc4')
    main(2007,1,1,where='test.out/')
    assert os.path.isfile('test.out/200701/vcm_zonal_2007-01-01.nc4')
        

if __name__=='__main__':
    import plac
    plac.call(main)