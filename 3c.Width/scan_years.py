#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-02

import numpy as np
import dimarray as da
import matplotlib.pyplot as plt
from tropic_width import tropic_width3
from datetime import datetime


def month_tropic_width(monthfile):

    try:
        data = da.read_nc(monthfile)
    except:
        return None
    vcm = 1. * data['vcm_csat+cal333-80']
    nprof = 1. * data['vcm_csat+cal333-80_cprof']
    cf_lat = vcm.values.T / nprof.values
    cf_lat = cf_lat.T
    cf_lat = np.ma.masked_invalid(cf_lat)

    tropic_range = tropic_width3(vcm.labels[0], vcm.labels[1], cf_lat)
    
    return tropic_range
    

def scan_years(years, where='./out/'):
    
    import glob, os
    
    datetimes = []
    tropic_min = []
    tropic_max = []

    months = np.r_[1:13]

    for year in years:
        for month in months:
        
            monthfile = 'in/%04d/vcm_zonal_%04d%02d.nc4' % (year, year, month)
        
            tropic_range = month_tropic_width(monthfile)
            if tropic_range is None:
                continue
            datetimes.append(datetime(year, month, 15))
            tropic_min.append(tropic_range[0])
            tropic_max.append(tropic_range[1])
            
            print datetimes[-1], tropic_min[-1], tropic_max[-1]

    np.savez('tropic_width.npz', tmin=tropic_min, tmax=tropic_max, datetimes=datetimes)

def main():
    
    years = np.r_[2006:2014]        
    scan_years(years)
    

if __name__ == '__main__':
    import plac
    plac.call(main)
