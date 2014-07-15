#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-07-15

import dimarray as da
import numpy as np
import matplotlib.pyplot as plt

latbins = np.r_[-90:90:1.]

def main(mask='out/200607/*nc4'):
    
    dset = da.read_nc(mask, ['lat', 'cloudpts'], axis='tai_time')
    npts = dset['cloudpts']
    lat = dset['lat']
    
    h_cprof, xx = np.histogram(lat, latbins, weights=1. * (npts > 0))
    h_nprof, xx = np.histogram(lat, latbins)
    fraction = h_cprof / (h_nprof)
    
    plt.figure(figsize=[10,3])
    plt.plot(latbins[:-1], 100. * fraction, lw=0.5)
    plt.grid()
    plt.xlabel('Latitude')
    plt.ylabel('Percents')
    plt.title('Fraction of cloudsat-only cloudy profiles')

    npts, xx = np.histogram(lat, latbins, weights = npts)
    npts_per_prof = 1. * npts / (h_cprof *3)

    plt.figure(figsize=[10,3])
    plt.plot(latbins[:-1], npts_per_prof, lw=0.5)
    plt.grid()
    plt.xlabel('Latitude')
    plt.title('Number of cloudy points in cloudsat-only cloudy profiles')
    
    plt.show()

if __name__ == '__main__':
    import plac
    plac.call(main)