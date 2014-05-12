#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-04-28

from datetime import datetime, timedelta
import dimarray as da
import glob
import os
    

def aggregate_arrays_from_files(files):
    
    files.sort()
    fields = None
    
    out = da.Dataset()

    for f in files:
        
        data = da.read_nc(f)

        if fields is None:
            fields = data.keys()
        
        for field in fields:
            if field not in data:
                continue
            if field not in out:
                out[field] = data[field] * 1.
            else:
                out[field] += data[field]

    return out


def process_vcm_grids_period(start, end, cycle, where):

    if not os.path.isdir(where):
        print 'Creating dir ' + where
        os.mkdir(where)

    current = start
    while current <= end:
        
        cycle_start = current
        cycle_files = []
        
        for i in range(cycle):
            
            inpath = './in/%04d%02d/' % (current.year, current.month)
            dayfile = 'vcm_lat_%04d-%02d-%02d.nc4' % (current.year, current.month, current.day)
            cycle_files.append(inpath + dayfile)
            
            current += timedelta(days=1)
            
        aggregated = aggregate_arrays_from_files(cycle_files)
        
        outfile = where + 'vcm_grid_%04d-%02d-%02d_%ddays.nc4' % (cycle_start.year, cycle_start.month, cycle_start.day, cycle)
        aggregated.write_nc(outfile, mode='w')


def main(year=2007, month=None, day=None, cycle=15, where='out/'):

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

    process_vcm_grids_period(start, end, cycle, where)


def test_day_run():
    
    grid_files = glob.glob('in/200901/vcm_2009-01-01*.nc4')
    main(2009,1,1,where='out.test/')
    day_files = glob.glob('out.test/200901/vcm_lat_*.nc4')
        
    assert False
    
    
if __name__=='__main__':
    import plac
    plac.call(main)