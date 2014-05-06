#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-04-28

import dimarray as da
import matplotlib.pyplot as plt


def pcolor_vcm(vcm):

    from mpl_toolkits.basemap import Basemap

    m = Basemap()

    plt.figure()
    m.pcolormesh(vcm.labels[0], vcm.labels[1], vcm.values.T, cmap='BuPu')
    m.drawcoastlines()
    plt.colorbar()


def show_file(filename):
    
    data = da.read_nc(filename)
    vcm05 = data['vcm_05km']
    vcm_lonlat = vcm05.sum(axis='altitude')
    
    pcolor_vcm(vcm_lonlat)


def aggregate_arrays_from_files(files, array_name, summed_along=None):
    
    aggregated = None

    for f in files:

        data = da.read_nc(f)
        array = data[array_name]

        if summed_along is not None:
            array = array.sum(axis=summed_along)
            
        if aggregated is None:
            aggregated = array
        else:
            aggregated += array

    return aggregated


def show_files(files):
    
    vcm = aggregate_arrays_from_files(files, 'vcm_05km', 'altitude')
    nprof = aggregate_arrays_from_files(files, 'nprof')
    cf = vcm / nprof
    pcolor_vcm(cf)


def main(year=2009, month=1, day=1):
    
    import glob
    
    mask = 'out/%04d%02d/vcm_lat_%04d-%02d-%02d*.nc4' % (year, month, year, month, day)
    grid_files = glob.glob(mask)
    
    show_file(grid_files[0], 'orbit = ' + grid_files[0])
    show_files(grid_files, 'date = %04d-%02d-%02d' % (year, month, day))
    
    mask = 'out/%04d%02d/vcm_lat_%04d-%02d*.nc4' % (year, month, year, month)
    grid_files = glob.glob(mask)
    show_files(grid_files, 'month = %04d-%02d' % (year, month))
    
    plt.show()
    

if __name__ == '__main__':
    import plac
    plac.call(main)