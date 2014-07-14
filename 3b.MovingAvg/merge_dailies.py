#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-02

from datetime import datetime, timedelta
import numpy as np
import dimarray as da
import netCDF4


def sum_dailies(files):

    dset = da.read_nc(files, axis='day', verbose=False)
    dset.sum(axis='day')
    return dset


def dayfiles_to_windows(files, outfile):
    
    window_sum = sum_dailies(files)
    print 'Saving ' + outfile
    print '   cf = ', 100. * np.sum(window_sum['cal333+cal05+cal20+cal80+csat_cprof']) / np.sum(window_sum['nprof'])
    window_sum.write_nc(outfile, 'w')


def scan_period(start, end, window=40, step=7, where='./out.{:02d}/', indir='./in/'):
    
    import glob, os
    
    current = start
    while current < end:
        
        # create list of files for current averaging window        
        this_start = current - timedelta(days=window/2)
        this_end = current + timedelta(days=window/2)
        c = this_start
        files = []
        while c < this_end:
            this_mask = indir + '/{:04d}{:02d}/vcm_zonal_{:04d}-{:02d}-{:02d}.nc4'.format(c.year, c.month, c.year, c.month, c.day)
            files += glob.glob(this_mask)
            c += timedelta(days=1)
            
        if len(files)==0:
            print 'no dailies for {:04d}{:02d}, skipping'.format(c.year, c.month)
            current += timedelta(days=step)
            continue
        
        where = where.format(window)
        if not os.path.isdir(where):
            print('Creating '+where)
            os.mkdir(where)
        if not os.path.isdir(where + '%04d' % current.year):
            print('Creating '+where + '%04d' % current.year)
            os.mkdir(where + '%04d' % current.year)
        outfile = where + '%04d/vcm_zonal_%04d%02d%02d.nc4' % (current.year, current.year, current.month, current.day)
        print current.date(), ' : aggregating %d files, ' % len(files), this_start.date(), this_end.date()
        dayfiles_to_windows(files, outfile)
        
        current += timedelta(days=step)
    

def main(year, month=None):
    
    year = int(year)
    start = datetime(year, 1, 1)
    end = datetime(year + 1, 1, 1)
        
    scan_period(start, end)
    

if __name__ == '__main__':
    import plac
    plac.call(main)
