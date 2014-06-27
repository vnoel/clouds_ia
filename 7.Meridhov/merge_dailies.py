#!/usr/bin/env python
#encoding:utf-8

# Forked by V. Noel [LMD/CNRS] on 2014-06-23

from datetime import datetime, timedelta
from vcm import aggregate_arrays_from_files
import dimarray as da


vcm_name = 'cal333+cal05+cal20+cal80+csat'

# window is the time in days over which to do the averaging
# step is the difference in weeks between each average

def main(year='2008', window=40, step=1, indir='out.daily'):
    
    import glob
    import os
    
    year = int(year)
    start = datetime(year, 1, 1)
    end = datetime(year+1, 1, 1)
    current = start
    
    outdir = 'out.{:02d}'.format(window)
    if not os.path.isdir(outdir):
        print 'Creating ' + outdir
        os.mkdir(outdir)

    while current < end:
        
        # create list of files for current averaging window
        c = current - timedelta(days=window/2)
        this_end = current + timedelta(days=window/2)
        files = []
        while c < this_end:
            this_mask = indir + '/{:04d}{:02d}/cflon_{:04d}-{:02d}-{:02d}*.nc4'.format(c.year, c.month, c.year, c.month, c.day)
            files += glob.glob(this_mask)
            c += timedelta(days=1)
            
        if len(files)==0:
            print 'no dailies for {:04d}{:02d}, skipping'.format(c.year, c.month)
            current += timedelta(weeks=step)
            continue

        # average files
        cprof, nprof = aggregate_arrays_from_files(files, [vcm_name + '_cprof', 'nprof'])
       
        # create output filename
        fulloutdir = outdir + '/{:04d}/'.format(year)
        if not os.path.isdir(fulloutdir):
            os.mkdir(fulloutdir)
            
        outname = 'cf_%04d%02d%02d.nc4' % (current.year, current.month, current.day)
        outpath = fulloutdir + outname
        aggregated = da.Dataset({vcm_name + '_cprof':cprof, 'nprof':nprof})
        print('Saving to ' + outpath)
        aggregated.write_nc(outpath, 'w')
        
        current += timedelta(weeks=step)


if __name__ == '__main__':
    import plac
    plac.call(main)