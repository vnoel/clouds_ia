#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-07-15

import dimarray as da
import numpy as np
import matplotlib.pyplot as plt

lonbins = np.r_[-180:180:2.]
latbins = np.r_[-90:90:2.]

def map_show(lon, lat, h, nprof):
    
    from mpl_toolkits.basemap import Basemap
    
    fraction = np.ma.masked_invalid(100. * h / nprof)
    
    m = Basemap()
    x, y = m(lon, lat)
    m.pcolormesh(x, y, fraction.T, cmap='PuRd')
    m.drawcoastlines()
    plt.clim(0,3)
    cb = plt.colorbar()
    cb.set_label('Percents')
    plt.title('Fraction of cloudy csat-only profiles')
    plt.savefig('map.pdf')
    plt.show()
    

def main(mask='out/200607/*nc4'):
    
    dset = da.read_nc(mask, ['lon', 'lat', 'cloudpts'], axis='tai_time')
    cloudy = 1 * (dset['cloudpts'] > 0)
    h, xx, yy = np.histogram2d(dset['lon'].values, dset['lat'].values, bins=[lonbins, latbins], weights=cloudy)
    nprof, xx, yy = np.histogram2d(dset['lon'].values, dset['lat'].values, bins=[lonbins, latbins])
    map_show(lonbins, latbins, h, nprof)



if __name__ == '__main__':
    import plac
    plac.call(main)