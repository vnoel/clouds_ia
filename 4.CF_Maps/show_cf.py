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
    m.drawparallels(np.r_[-90:90:30], labels=[1,0,0,0])
    plt.colorbar()
    plt.clim(0, 1.)
    if title is not None:
        plt.title(title)


def aggregate_arrays_from_files(files, array_names, summed_along=None):
    
    aggregated = dict()

    files.sort()
    prevmax = 0

    for f in files:

        print f

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


def show_files(files, layer):
    
    cprof, nprof = aggregate_arrays_from_files(files, [vcm_name + '_cprof_' + layer, 'nprof'])
    
    cloudypoints = np.ma.masked_where(nprof.values==0, 1. * cprof.values / nprof.values)
    cloudypoints = np.ma.masked_invalid(cloudypoints)
    
    pcolor_cf(cprof.labels[0], cprof.labels[1], cloudypoints, title=layer)
    #plt.clim(0,100)


def main(layer='high'):
    
    import glob
    
    files = []
    base = 'out.daily/2008%02d/*nc4'
    for month in 6,7,8:
        x = glob.glob(base % month)
        files.extend(x)
    assert len(files) > 0
    show_files(files, layer)
    
    plt.show()
    

if __name__ == '__main__':
    import plac
    plac.call(main)
