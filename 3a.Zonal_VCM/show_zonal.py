#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-02

import numpy as np
import dimarray as da
import matplotlib.pyplot as plt
import vcm


def pcolor_cf(x, y, vcmarray, title=None):

    plt.figure(figsize=[15,5])
    plt.contourf(x, y, vcmarray.T, np.r_[0:105:5])
    plt.colorbar()
    if title is not None:
        plt.title(title)
    plt.clim(0,100)
    plt.xlim(-82,82)


def show_files(files):
    
    dset = vcm.sum_arrays_from_files(files)
    
    nprof = dset['nprof'] * 3.
    cprof = dset['cal333+cal05+cal20+cal80+csat']
    cf_lat = np.ma.masked_invalid(100. * cprof.values.T / nprof.values)
    cf_lat = cf_lat.T
    
    pcolor_cf(cprof.lat, cprof.altitude, cf_lat, 'Cloud fraction ')


def main(mask='out/200607/vcm_zonal*.nc4'):
    
    show_files(mask)    
    plt.show()
    

if __name__ == '__main__':
    import plac
    plac.call(main)
