#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-02

import numpy as np
import dimarray as da
from tropic_width import tropic_width3
from datetime import datetime

vcm_mins = [0.05, 0.15, 0.25, 0.35]

def month_tropic_width(monthfile):

    try:
        data = da.read_nc(monthfile)
    except:
        return None
    try:
        vcm = 1. * data['cal333+cal05+cal20+cal80+csat']
        nprof = 1. * data['cal333+cal05+cal20+cal80+csat_cprof']
    except KeyError:
        return None
        
    cf_lat = vcm.values.T / nprof.values
    cf_lat = cf_lat.T
    cf_lat = np.ma.masked_invalid(cf_lat)

    tropic_range = dict()
    for vcm_min in vcm_mins:
        tropic_range[vcm_min] = tropic_width3(vcm.labels[0], vcm.labels[1], cf_lat, vcm_min=vcm_min)
    
    return tropic_range
    

def scan_years(years, where='./out/'):
    
    datetimes = []
    tropic_min = dict()
    tropic_max = dict()
    for vcm_min in vcm_mins:
        tropic_min[vcm_min] = []
        tropic_max[vcm_min] = []

    months = np.r_[1:13]

    for year in years:
        for month in months:
        
            monthfile = 'in/%04d/vcm_zonal_%04d%02d.nc4' % (year, year, month)
        
            tropic_range = month_tropic_width(monthfile)
            if tropic_range is None:
                
                continue
            datetimes.append(datetime(year, month, 15))
            for vcm_min in vcm_mins:
                tropic_min[vcm_min].append(tropic_range[vcm_min][0])
                tropic_max[vcm_min].append(tropic_range[vcm_min][1])
            
            print datetimes[-1], tropic_min[0.05][-1], tropic_max[0.05][-1]

    np.savez('out/tropic_width.npz', tmin=tropic_min, tmax=tropic_max, datetimes=datetimes)

def main():
    
    years = np.r_[2006:2014]        
    scan_years(years)
    

if __name__ == '__main__':
    import plac
    plac.call(main)
