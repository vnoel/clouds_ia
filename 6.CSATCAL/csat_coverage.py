#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-07-15

from datetime import datetime, timedelta
import glob
import vcm
import numpy as np


def csat_coverage(files):
    
    v = vcm.VCM(files, verbose=False, cleanup_cloudsat=False)
    csat = v.get_vcm('csat')
    idx = np.any(csat < 0, axis=1)
    coverage = 100. * (v.nprof - np.sum(idx)) / v.nprof
    return coverage


def process_vcm_orbits_period(start, end):

    coverage = []
    dates = []
    
    current = start
    while current < end:
        
        inpath = './in/%04d%02d/' % (current.year, current.month)
        mask = 'vcm_%04d-%02d-%02d*_v2.0.nc4' % (current.year, current.month, current.day)
        vcm_files = glob.glob(inpath + mask)
        print inpath + mask + ' : %d files' % (len(vcm_files))
        if len(vcm_files) > 0:        
            day_coverage = csat_coverage(inpath + mask)
            print 'CloudSat coverage : ', day_coverage, '%'
        else:
            day_coverage = -1

        dates.append(current)
        coverage.append(day_coverage)
        
        current += timedelta(days=1)
    
    np.savez('csat_coverage.npz', dates=dates, coverage=coverage)


def main(year=2007, month=None, day=None):

    if day is not None and month is not None:
        year, month, day = int(year), int(month), int(day)
        start = datetime(year, month, day)
        end = start + timedelta(days=1)
    elif day is None and month is not None:
        year, month = int(year), int(month)
        start = datetime(year, month, 1)
        end = start + timedelta(days=31)
    else:
        if '-' in year:
            year_start, year_end = year.split('-')
            start = datetime(int(year_start), 1, 1)
            end = datetime(int(year_end) + 1, 1, 1)
        else:
            year = int(year)
            start = datetime(year, 1, 1)
            end = datetime(year+1, 1, 1)

    process_vcm_orbits_period(start, end)


if __name__=='__main__':
    import plac
    plac.call(main)
