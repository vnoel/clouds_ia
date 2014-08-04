#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-06-24

import dimarray as da
import datetime
import numpy as np
import netCDF4

vcm_name = 'cal333+cal05+cal20+cal80+csat_cprof'


def filename_to_datetime(filename):
    year = int(filename[-8:-4])
    month = int(filename[-4:-2])
    day = int(filename[-2:])
    dt = datetime.datetime(year=year, month=month, day=day)
    return dt


def main(window):
    window = int(window)
    years = range(2006,2015)
    fullvcm = []
    fullnprof = []
    for year in years:
        mask = 'out.{:02d}/{:04d}/*.nc4'.format(window, year)
        print mask
        try:
            vcm = da.read_nc(mask, vcm_name, axis='file')
        except ValueError:
            print 'No monthlies for {:04d}, skipping'.format(year)
            continue
        # vcm.reset_axis(filename_to_datetime, 'file')
        nprof = da.read_nc(mask, 'nprof', axis='file')
        # nprof.reset_axis(filename_to_datetime, 'file')
        fullvcm.append(vcm)
        fullnprof.append(nprof)
    vcm = da.concatenate(fullvcm, axis='file')
    nprof = da.concatenate(fullnprof, axis='file')
    print vcm, nprof
    
    np.savez('series_%d.npz' % window, vcm=vcm, nprof=nprof, altmin=vcm.labels[1], time=vcm.labels[0], lon=vcm.labels[2])
    

if __name__ == '__main__':
    import plac
    plac.call(main)