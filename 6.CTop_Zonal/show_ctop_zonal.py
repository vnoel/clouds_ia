#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-02

import numpy as np
import dimarray as da
import matplotlib.pyplot as plt


def plot_zonal(lat, zonal, title=None):

    plt.figure(figsize=[10,5])
    plt.plot(lat, zonal)
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
    
    ctopsum = aggregate_arrays_from_files(files, 'cal333+cal05+cal20+cal80+csat_ctopsum')
    nclouds = aggregate_arrays_from_files(files, 'cal333+cal05+cal20+cal80+csat_nclouds')
    
    ctop = np.ma.masked_where(nclouds.values==0, 1. * ctopsum.values / nclouds.values)
    ctop = np.ma.masked_invalid(ctop)
    
    print 'Number of latitude points : ', len(ctop)
    
    plot_zonal(ctopsum.labels[0], nclouds, 'Number of cloudy profiles' + title)
    plot_zonal(ctopsum.labels[0], ctop, 'Average cloud top ' + title)


def main(mask=None):
    
    import glob
    
    if mask is None:
        mask = './test.out/200701/*.nc4'

    grid_files = glob.glob(mask)
    grid_files.sort()
    show_files(grid_files, mask)
    
    plt.show()
    

if __name__ == '__main__':
    import plac
    plac.call(main)
