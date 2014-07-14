#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-02

import numpy as np
import dimarray as da
import tropic_width
from datetime import datetime
import glob

vcm_mins = [0.05, 0.15, 0.25, 0.35]


def month_tropic_width(f):

    dset = da.read_nc(['cal333+cal05+cal20+cal80+csat', 'cal333+cal05+cal20+cal80+csat_cprof'])
    vcm = dset['cal333+cal05+cal20+cal80+csat']
    nprof = dset['nprof']

    cf_lat = np.ma.masked_invalid(1. * vcm.values.T / nprof.values)
    cf_lat = cf_lat.T
        
    tropic_range = dict()
    for vcm_min in vcm_mins:
        tropic_range[vcm_min] = tropic_width.tropic_width3(vcm.lat, vcm.altitude, cf_lat, vcm_min)
    
    return tropic_range
    

def scan_years(years, window=40):
    
    where='./in.%02d/' % (window)
    
    datetimes = []
    tropic_min = dict()
    tropic_max = dict()
    for vcm_min in vcm_mins:
        tropic_min[vcm_min] = []
        tropic_max[vcm_min] = []

    for year in years:

        mask = where + '{:04d}/*.nc4'.format(year)
        files = glob.glob(mask)
        
        if len(files)==0:
            print('No files for %d, skipping' % year)
            continue
        print '%d : %d files' % (year, len(files))
        
        for f in files:
                        
            tropic_range = month_tropic_width(f)
            if tropic_range is None:
                print 'tropic_range == None'
                continue
                
            year = int(f[-12:-8])
            month = int(f[-8:-6])
            day = int(f[-6:-4])
            
            datetimes.append(datetime(year, month, day))

            for vcm_min in vcm_mins:
                tropic_min[vcm_min].append(tropic_range[vcm_min][0])
                tropic_max[vcm_min].append(tropic_range[vcm_min][1])
        
            print datetimes[-1], tropic_min[0.05][-1], tropic_max[0.05][-1]

    np.savez('tropic_width_%02d.npz' % window, tmin=tropic_min, tmax=tropic_max, datetimes=datetimes)


def main():
    
    years = np.r_[2006:2015]        
    scan_years(years)
    

if __name__ == '__main__':
    import plac
    plac.call(main)
