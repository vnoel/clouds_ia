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

    oldsum = 0

    for i,f in enumerate(files):

        data = da.read_nc(f)
        if array_name not in data:
            continue
        
        array = data[array_name].values

        if summed_along is not None:
            array = array.sum(axis=summed_along)
            
        if aggregated is None:
            aggregated = array
        else:
            oldsum = aggregated.sum()
            aggregated += array
            
        print array.sum(), oldsum, aggregated.sum()

    return aggregated


def show_file(filename, title):
    
    data = da.read_nc(filename)
    vcm05 = data['vcm_05km']
    vcm_lonlat = vcm05.sum(axis='altitude')
    
    pcolor_vcm(vcm_lonlat, title)


def show_files(files, title):
    
    #vcm = aggregate_arrays_from_files(files, 'vcm_05km', 'altitude')
    nprof = aggregate_arrays_from_files(files, 'nprof')
    #cloudypoints = vcm / nprof
    #cloudypoints[nprof==0] = 0
    #pcolor_vcm(nprof, 'cloudy points in profiles : ' + title)
    #plt.clim(0,50)


def main(year=2007, month=3, day=1):
    
    import glob
    
    year = int(year)
    month = int(month)
    day = int(day)
    
    mask = 'out/%04d%02d/vcm_lat_%04d-%02d-*.nc4' % (year, month, year, month)
    grid_files = glob.glob(mask)
    grid_files.sort()
    
    #show_file(grid_files[0], 'file = ' + grid_files[0])
    show_files(grid_files, 'month = %04d-%02d' % (year, month))
    
    mask = ['out/%04d%02d/vcm_lat_%04d-%02d*.nc4' % (year, m, year, m) for m in [1,2,3]]
    grid_files = glob.glob(mask[0]) + glob.glob(mask[1]) + glob.glob(mask[2])
    show_files(grid_files, '%04d %02d + %02d + %02d' % (year, 1, 2, 3))
    
    plt.show()
    

if __name__ == '__main__':
    import plac
    plac.call(main)