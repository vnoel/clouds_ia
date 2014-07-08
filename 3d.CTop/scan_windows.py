#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-02

import numpy as np
import dimarray as da
import tropic_width
from datetime import datetime
import glob

vcm_mins = [0.05, 0.15, 0.25, 0.35]


def read_vars(f):
    print f
    try:
        vcm = da.read_nc(f, 'cal333+cal05+cal20+cal80+csat')
        cprof = da.read_nc(f, 'cal333+cal05+cal20+cal80+csat_cprof')
        nprof = da.read_nc(f, 'nprof')
    except KeyError:
        return None, None, None
        
    return vcm, cprof, nprof


def compute_cf(vcm, cprof, nprof):

    cf_lat = 1. * vcm.values.T / cprof.values
    cf_lat = np.ma.masked_invalid(cf_lat.T)

    cf_lat2 = 1. * vcm.values.T / nprof.values
    cf_lat2 = np.ma.masked_invalid(cf_lat2.T)

    return cf_lat, cf_lat2


def window_cloud_ceiling(f):

    vcm, cprof, nprof = read_vars(f)
    cf_lat, cf_lat2 = compute_cf(vcm, cprof, nprof)
        
    ceiling = tropic_width.cloud_cover_top(vcm.altitude, cf_lat)
    return ceiling, vcm.lat, cprof, nprof
    

def scan_years(years, window=40):
    
    where='./in.%02d/' % (window)
    
    datetimes = []
    ceilings = np.zeros([60*len(years), 16401])
    nprofs = np.zeros_like(ceilings, dtype='uint32')
    cprofs = np.zeros_like(ceilings, dtype='uint32')
    print ceilings.shape
    i = 0

    for year in years:

        mask = where + '{:04d}/*.nc4'.format(year)
        files = glob.glob(mask)
        if len(files)==0:
            print('No files for %d, skipping' % year)
            continue
            
        print '%d : %d files' % (year, len(files))
        for f in files:
                        
            ceiling, lat, cprof, nprof = window_cloud_ceiling(f)
            assert ceiling is not None
            
            year = int(f[-12:-8])
            month = int(f[-8:-6])
            day = int(f[-6:-4])            
            datetimes.append(datetime(year, month, day))
            
            ceilings[i,:] = ceiling
            nprofs[i,:] = nprof
            cprofs[i,:] = cprof

            print np.sum(nprof), np.sum(cprof), 100. * np.sum(cprof) / np.sum(nprof)
            
            i += 1

    np.savez('ceilings_%02d.npz' % window, ceilings=ceilings, datetimes=datetimes, lat=lat, cprof=cprofs, nprof=nprofs)

def main():
    
    years = np.r_[2006:2015]
    scan_years(years)
    

if __name__ == '__main__':
    import plac
    plac.call(main)
