#!/usr/bin/env python
#encoding:utf-8

# Created by V. Noel [LMD/CNRS] on 2014-06-23


from show_cf import aggregate_arrays_from_files
import dimarray as da

vcm_name = 'cal333+cal05+cal20+cal80+csat'


def main(year='2008', month=None):
    
    import glob
    import os
    
    year = int(year)

    if month is None:
        months = range(1,13)
    else:
        months = [month]

    for month in months:
        files = glob.glob('out/{:04d}{:02d}/*nc4'.format(year, month))
        if len(files)==0:
            print 'no dailies for {:04d}{:02d}, skipping'.format(year, month)
            continue
        cprof, nprof = aggregate_arrays_from_files(files, [vcm_name + '_cprof', 'nprof'])
        outdir = 'out/{:04d}/'.format(year)
        if not os.path.isdir(outdir):
            os.mkdir(outdir)
        outpath = outdir + 'cf_{:04d}-{:02d}.nc4'.format(year, month)
        aggregated = da.Dataset({vcm_name + '_cprof':cprof, 'nprof':nprof})
        aggregated.write_nc(outpath, 'w')


if __name__ == '__main__':
    main()