#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-02

import numpy as np
import dimarray as da
import matplotlib.pyplot as plt


def pcolor_ctop(x, y, vcmarray, title=None):

    from mpl_toolkits.basemap import Basemap

    m = Basemap()

    plt.figure(figsize=[10,5])
    m.pcolormesh(x, y, vcmarray.T)
    m.drawcoastlines()
    plt.colorbar()
    if title is not None:
        plt.title(title)


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
    
    ctopsum = aggregate_arrays_from_files(files, 'vcm_csat+cal333-80_ctopsum')
    nclouds = aggregate_arrays_from_files(files, 'vcm_csat+cal333-80_nclouds')
    
    print ctopsum, nclouds
    
    ctop = np.ma.masked_where(nclouds.values==0, 1. * ctopsum.values / nclouds.values)
    ctop = np.ma.masked_invalid(ctop)
    
    pcolor_ctop(ctopsum.labels[0], ctopsum.labels[1], ctop, 'Average cloud top ' + title)


def main(vcm_grid_file='./out/200707/ctop_2007-07-01.nc4'):
    
    import glob
    
    mask = 'test.out/ctop_*.nc4'
    grid_files = glob.glob(mask)
    # mask = 'out/200707/vcm_grid_*.nc4'
    # grid_files += glob.glob(mask)
    # mask = 'out/200708/vcm_grid_*.nc4'
    # grid_files += glob.glob(mask)
    grid_files.sort()

    show_files(grid_files, '2007 JJA')
    
    plt.show()
    

if __name__ == '__main__':
    import plac
    plac.call(main)
