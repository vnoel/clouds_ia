#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-02

import numpy as np
import dimarray as da
import matplotlib.pyplot as plt
import tropic_width


def pcolor_zonal(x, y, vcmarray, title=None):

    plt.figure(figsize=[15,5])
    plt.contourf(x, y, vcmarray.T, np.r_[0:0.8:0.05])
    plt.colorbar()
    if title is not None:
        plt.title(title)
    plt.clim(0,0.8)
    plt.xlim(-82,82)
    plt.xticks(np.r_[-90:90+30:30])
    plt.axhline(y=16, ls='--', color='w')
    latrange = tropic_width.tropic_width(x, y, vcmarray)
    plt.axvline(x=latrange[0], ls='--', color='w')
    plt.axvline(x=latrange[1], ls='--', color='w')
    
    cover_top = tropic_width.cloud_cover_top(y, vcmarray)
    plt.plot(x, cover_top, lw=2, color='w', alpha=0.5)
    
    print 'lat range : ', latrange
    print 'lat width : ', latrange[1]-latrange[0]
    

    lat = x[:-100]
    altchange = cover_top[100:] - cover_top[:-100]

    ilat = (lat > -40) & (lat < 10)
    ilatup = (altchange[ilat] > 1.)
    latup = np.min(lat[ilat][ilatup])
    ilat = (lat > 10) & (lat < 40)
    ilatdown = (altchange[ilat] < -1)
    latdown = np.max(lat[ilat][ilatdown])

    plt.figure(figsize=[15,5])
    plt.plot(x, cover_top)
    plt.axvline(x=latup1)
    plt.axvline(x=latdown1)
    plt.axvline(x=latup2)
    plt.axvline(x=latdown2)
    
    plt.figure(figsize=[15,5])
    plt.plot(lat, altchange)
    plt.axvline(x=latup1)
    plt.axvline(x=latdown1)
    plt.axvline(x=latup2)
    plt.axvline(x=latdown2)
    plt.ylim(-2,2)
    plt.xlim(-40, 40)
    
    print 'lat range, second method : ', latup1, latup2, latdown1, latdown2
    


def aggregate_arrays_from_files(files, array_name, summed_along=None):
    
    aggregated = None

    files.sort()
    prevmax = 0

    for f in files:

        data = da.read_nc(f)
        if array_name not in data:
            continue
        array = data[array_name]

        if summed_along is not None:
            array = array.sum(axis=summed_along)            
        if aggregated is None:
            aggregated = 1. * array
        else:
            aggregated += array
        
        if aggregated.max() < prevmax:
            print 'PROBLEME !'
            print 'Previous maximum = ', prevmax, ', current max = ', aggregated.max()

    return aggregated


def show_files(files, title):
    
    vcm_prof = aggregate_arrays_from_files(files, 'vcm_csat+cal333-80')
    nprof = aggregate_arrays_from_files(files, 'vcm_csat+cal333-80_cprof')
    
    cf_lat = vcm_prof.values.T / nprof.values
    cf_lat = cf_lat.T
    cf_lat = np.ma.masked_invalid(cf_lat)
    
    pcolor_zonal(vcm_prof.labels[0], vcm_prof.labels[1], cf_lat, 'Cloud fraction ' + title)


def main(mask='./out/2007/vcm_zonal_2007*.nc4'):
    
    import glob
    
    grid_files = glob.glob(mask)
    grid_files.sort()

    show_files(grid_files, '2007-01')
    
    plt.show()
    

if __name__ == '__main__':
    import plac
    plac.call(main)
