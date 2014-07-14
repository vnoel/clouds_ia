#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-07-10

import netCDF4
import glob
from datetime import datetime
import dimarray as da
import vcm

day = datetime(2007, 2, 3)

# 14 files

# compression levels = 9 - 1 file = 1.1MB
# warm cache : 3.3 seconds
# cold cache : 3.7 seconds

# compression level = 6 - 1 file = 1.4MB

# compression level = 4 (default) - 1 file = 1.8MB
# warm cache : 3s
# cold cache : 4.1s

# il y a un leger gain en lecture quand on compresse moins, mais rien de bien extravagant
# C'est genre 10% speedup.
# Par comparaison, utiliser netCDF4 directement vs dimarray c'est 300% speedup.

f = glob.glob('out/200607/vcm_2006-07-01T*.nc4')[0]
def my_read_nc_lon(f=f):
    nc = netCDF4.Dataset(f, 'r')
    time = nc.variables['tai_time'][:]
    lon = nc.variables['lon'][:]
    nc.close()
    
    axis = da.Axis(time, 'time')
    d1 = da.DimArray(lon, axis)
    return d1

def my_read_nc_all(f=f):
    nc = netCDF4.Dataset(f, 'r')
    time = nc.variables['tai_time'][:]
    alt = nc.variables['altitude'][:]
    lon = nc.variables['lon'][:]
    lat = nc.variables['lat'][:]
    cal333 = nc.variables['cal333'][:]
    cal05 = nc.variables['cal05'][:]
    cal20 = nc.variables['cal20'][:]
    cal80 = nc.variables['cal80'][:]
    csat = nc.variables['csat'][:]
    
def my_read_vcm_nc(f=f):
    nc = netCDF4.Dataset(f, 'r')
    time = nc.variables['tai_time'][:]
    alt = nc.variables['altitude'][:]
    lon = nc.variables['lon'][:]
    lat = nc.variables['lat'][:]
    cal333 = nc.variables['cal333'][:]

    time_axis = da.Axis(time, 'time')
    alt_axis = da.Axis(alt, 'alt')
    lon = da.DimArray(lon, time_axis)
    lat = da.DimArray(lon, time_axis)
    cal333 = da.DimArray(cal333, [time_axis, alt_axis])
        
    
def my_read_vcm(f=f, verbose=False):
    filename = f
    lon = da.read_nc(filename, 'lon', verbose=verbose).values
    lat = da.read_nc(filename, 'lat', verbose=verbose).values
    data = da.Dataset()
    data['cal333'] = da.read_nc(filename, 'cal333', verbose=verbose)
    altitude = data['cal333'].altitude

def my_read_vcm_real(f=f):
    v = vcm.VCM(f, verbose=False)