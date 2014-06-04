#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-02

import numpy as np
import dimarray as da
import matplotlib.pyplot as plt


def pcolor_ctop(x, y, vcmarray, title=None):

    plt.figure(figsize=[15,5])
    plt.contourf(x, y, vcmarray.T, np.r_[0:1.05:0.05])
    plt.colorbar()
    if title is not None:
        plt.title(title)
    plt.clim(0,0.7)
    plt.xlim(-82,82)


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
    
    pcolor_ctop(vcm_prof.labels[0], vcm_prof.labels[1], cf_lat, 'Cloud fraction ' + title)


def main(vcm_grid_file='./out/200707/ctop_2007-07-01.nc4'):
    
    import glob
    
    mask = 'out/200701/vcm_grid_*.nc4'
    grid_files = glob.glob(mask)
    # mask = 'out/200707/vcm_grid_*.nc4'
    # grid_files += glob.glob(mask)
    # mask = 'out/200708/vcm_grid_*.nc4'
    # grid_files += glob.glob(mask)
    grid_files.sort()

    show_files(grid_files, '2007-01')
    
    plt.show()
    

if __name__ == '__main__':
    import plac
    plac.call(main)
