#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-04-28

import numpy as np
import dimarray as da
import matplotlib.pyplot as plt


def zonal_vcm(vcm, title=None):

    plt.figure(figsize=[10,5])
    #plt.pcolormesh(vcm.labels[0], vcm.labels[1], vcm.values.T)
    vcm.T.pcolor()
    plt.colorbar()
    plt.clim(0, 8000)
    if title is not None:
        plt.title(title)


def aggregate_arrays_from_files(files, array_name, summed_along=None, bounds=None):
    
    aggregated = None

    files.sort()

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
        
        print aggregated.max()

    return aggregated


def show_file(filename, title):
    
    data = da.read_nc(filename)
    vcm05 = data['vcm_cal333']
    vcm_lonlat = 1. * vcm05.sum(axis='altitude') / data['nprof']
    
    zonal_vcm(vcm_lonlat, title)


def show_files(files, title):
    
    vcm = aggregate_arrays_from_files(files, 'vcm_cal333', 'lon')
    nprof = aggregate_arrays_from_files(files, 'nprof', 'lon')
    #cloudypoints = da.DimArray(vcm / nprof, labels=vcm.labels, dims=vcm.dims)
    zonal_vcm(vcm, 'cloudy points in profiles : ' + title)
    #plt.clim(0,100)


def main(vcm_grid_file='./out/200707/vcm_grid_2007-07-01.nc4'):
    
    import glob
    
    mask = 'out/200707/vcm_grid_*.nc4'
    grid_files = glob.glob(mask)
    grid_files.sort()

    show_files(grid_files, '200701-200703')
    
    plt.show()
    

if __name__ == '__main__':
    import plac
    plac.call(main)
