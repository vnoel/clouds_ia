#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-04-28

import numpy as np
import dimarray as da
import matplotlib.pyplot as plt


vcm_name = 'cal333+cal05+cal20+cal80+csat'


def pcolor_cf(x, y, vcmarray, title=None):

    from mpl_toolkits.basemap import Basemap

    m = Basemap()

    plt.figure(figsize=[10,5])
    m.pcolormesh(x, y, vcmarray.T)
    m.drawcoastlines()
    plt.colorbar()
    plt.clim(0, 1.)
    if title is not None:
        plt.title(title)


def aggregate_arrays_from_files(files, array_names, summed_along=None):
    
    aggregated = dict()

    files.sort()
    prevmax = 0

    for f in files:

        data = da.read_nc(f)
        if any(array_name not in data for array_name in array_names):
            print 'Missing data'
            continue
        for array_name in array_names:

            array = data[array_name]

            if summed_along is not None:
                array = array.sum(axis=summed_along)            
            if array_name not in aggregated:
                aggregated[array_name] = 1. * array
            else:
                aggregated[array_name] += array
        
            if aggregated[array_name].max() < prevmax:
                print 'PROBLEME !'
                print 'Previous maximum = ', prevmax, ', current max = ', aggregated[array_name].max()

    data = [aggregated[array_name] for array_name in array_names]
    return data


def show_files(files, title):
    
    cprof, nprof = aggregate_arrays_from_files(files, [vcm_name + '_cprof', 'nprof'])
    
    cloudypoints = np.ma.masked_where(nprof.values==0, 1. * cprof.values / nprof.values)
    cloudypoints = np.ma.masked_invalid(cloudypoints)
    
    pcolor_cf(cprof.labels[0], cprof.labels[1], cloudypoints, 'cloud fraction ' + title)
    #plt.clim(0,100)


def main(vcm_grid_file='./out/200707/vcm_grid_2007-07-01.nc4'):
    
    import glob
    
    #show_file(vcm_grid_file, vcm_grid_file)
    
    mask = 'out/200706/cf*.nc4'
    grid_files = glob.glob(mask)
    mask = 'out/200707/cf*.nc4'
    grid_files += glob.glob(mask)
    mask = 'out/200708/cf*.nc4'
    grid_files += glob.glob(mask)
    grid_files.sort()

    show_files(grid_files, '2007 JJA')
    
    plt.show()
    

if __name__ == '__main__':
    import plac
    plac.call(main)
