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


def show_files(files):
    
    vcm_lonlat = None
    for f in files:
        data = da.read_nc(f)
        vcm05 = data['vcm_05km']
        if vcm_lonlat is None:
            vcm_lonlat = vcm05.sum(axis='altitude')
        else:
            vcm_lonlat += vcm05.sum(axis='altitude')
    
    pcolor_vcm(vcm_lonlat)


def main(year=2009, month=1, day=1):
    
    import glob
    
    mask = 'out/%04d%02d/vcm_lat_%04d-%02d-%02d*.nc4' % (year, month, year, month, day)
    grid_files = glob.glob(mask)
    
    show_file(grid_files[0])
    show_files(grid_files)
    
    mask = 'out/%04d%02d/vcm_lat_%04d-%02d*.nc4' % (year, month, year, month)
    show_files(grid_files)
    
    plt.show()
    

if __name__ == '__main__':
    import plac
    plac.call(main)