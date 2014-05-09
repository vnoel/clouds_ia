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
    
    if len(files) == 0:
        return None
    
    out = da.Dataset()

    for f in files:
        
        data = da.read_nc(f)

        if fields is None:
            fields = data.keys()
        
        for field in fields:
            if field not in out:
                out[field] = data[field]
            else:
                out[field] += data[field]
        print data['vcm_05km'].sum()

    print out['vcm_05km'].sum(), data['vcm_05km'].sum() * len(files)

    return out


def process_vcm_grids_period(start, end, where):

    if not os.path.isdir(where):
        print 'Creating dir ' + where
        os.mkdir(where)

    current = start
    while current <= end:
        
        inpath = './in/%04d%02d/' % (current.year, current.month)
        mask = 'vcm_lat_%04d-%02d-%02d*.nc4' % (current.year, current.month, current.day)
        vcm_files = glob.glob(inpath + mask)
        outpath = where + '%04d%02d/' % (current.year, current.month)
        
        if not os.path.isdir(outpath):
            print 'Creating ' + outpath
            os.mkdir(outpath)
            
        outfile = 'vcm_lat_%04d-%02d-%02d.nc4' % (current.year, current.month, current.day)
        print inpath, mask, current, len(vcm_files)
        aggregated = aggregate_arrays_from_files(vcm_files)
        if aggregated is not None:
            aggregated.write_nc(outpath + outfile, mode='w')
        
        current += timedelta(days=1)


def main(year=2009, month=None, day=None, where='out/'):

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

    process_vcm_grids_period(start, end, where)


def test_day_run():
    
    grid_files = glob.glob('in/200901/vcm_2009-01-01*.nc4')
    main(2009,1,1,where='out.test/')
    day_files = glob.glob('out.test/200901/vcm_lat_*.nc4')
        
    assert False
    
    
if __name__=='__main__':
    import plac
    plac.call(main)