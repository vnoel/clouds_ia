#!/usr/bin/env python
#encoding:utf-8

# Forked by V. Noel [LMD/CNRS] on 2014-06-23


from vcm import aggregate_arrays_from_files
import dimarray as da

vcm_name = 'cal333+cal05+cal20+cal80+csat'


def main(year='2008', month=None, indir='out.daily', outdir='out.monthly'):
    
    import glob
    import os
    
    year = int(year)

    print month

    if month is None:
        months = range(1,13)
    else:
        months = [int(month)]

    for month in months:
        filemask = indir + '/{:04d}{:02d}/*nc4'.format(year, month)
        if len(glob.glob(filemask))==0:
            print 'no dailies for {:04d}{:02d}, skipping'.format(year, month)
            continue
        cprof, nprof = aggregate_arrays_from_files(filemask, [vcm_name + '_cprof', 'nprof'])
        fulloutdir = outdir + '/{:04d}/'.format(year)
        if not os.path.isdir(fulloutdir):
            os.mkdir(fulloutdir)
        outpath = fulloutdir + '/cf_{:04d}-{:02d}.nc4'.format(year, month)
        aggregated = da.Dataset({vcm_name + '_cprof':cprof, 'nprof':nprof})
        print('Saving to ' + outpath)
        aggregated.write_nc(outpath, 'w')


if __name__ == '__main__':
    import plac
    plac.call(main)