#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-04-28

import dimarray as da
import matplotlib.pyplot as plt


def pcolor_vcm(vcm, title=None):

    from mpl_toolkits.basemap import Basemap

    m = Basemap()

    plt.figure(figsize=[10,5])
    m.pcolormesh(vcm.labels[0], vcm.labels[1], vcm.values.T, cmap='BuPu')
    m.drawcoastlines()
    plt.colorbar()
    if title is not None:
        plt.title(title)


def aggregate_arrays_from_files(files, array_name, summed_along=None):
    
    aggregated = None

    files.sort()

    for f in files:

        data = da.read_nc(f)
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
    vcm05 = data['vcm_cal05']
    vcm_lonlat = vcm05.sum(axis='altitude')
    
    pcolor_vcm(vcm_lonlat, title)


def show_files(files, title):
    
    vcm = aggregate_arrays_from_files(files, 'vcm_cal05', 'altitude')
    nprof = aggregate_arrays_from_files(files, 'nprof')
    cloudypoints = vcm / nprof
    cloudypoints[nprof==0] = 0
    pcolor_vcm(cloudypoints, 'cloudy points in profiles : ' + title)
    plt.clim(0,120)


def main(vcm_grid_file='./test.out/vcm_grid_2007-01-01.nc4'):
    
    import glob
    
    show_file(vcm_grid_file, vcm_grid_file)
    
    mask = 'out/200701/vcm_grid_*.nc4'
    grid_files = glob.glob(mask)
    show_files(grid_files, '200701')
    
    plt.show()
    

if __name__ == '__main__':
    import plac
    plac.call(main)