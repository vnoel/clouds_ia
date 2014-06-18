#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-02

import numpy as np
import dimarray as da
import matplotlib.pyplot as plt


def plot_ctop(dt, ctopsum, nclouds):
    
    ctops = 1. * ctopsum / nclouds
    
    plt.figure(figsize=[15,5])
    plt.plot(dt, ctops)
    plt.xlabel('Latitude')
    plt.ylabel('Average Tropical Cloud Top')
    

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


def tropic_ctop_from_file(filename, bounds):
    
    data = da.read_nc(filename)
    ctopsum = data['cal333+cal05+cal20+cal80+csat_ctopsum']
    nclouds = data['cal333+cal05+cal20+cal80+csat_nclouds']
    lat = ctopsum.labels[0]
    idx = (lat > bounds[0]) & (lat < bounds[1])
    ctopsum = np.sum(ctopsum.ix[idx])
    nclouds = np.sum(nclouds.ix[idx])
    ctop = np.ma.masked_invalid(1. * ctopsum / nclouds)    
    
    return ctopsum, nclouds
    

def main():
    
    import os
    import datetime
    
    npz = np.load('in_width/tropic_width.npz')
    tropic_min = npz['tmin']
    tropic_max = npz['tmax']
    tropic_dt = npz['datetimes']
    
    years = range(2006,2013)
    tropic_ctopssum = []
    topic_nclouds = []
    dt = []
    
    for year in years:
        for month in range(13):
            filename = 'out/{:04d}/ctop_zonal_{:04d}{:02d}.nc4'.format(year, year, month)
            if not os.path.isfile(filename):
                print(filename + ' does not exist, skipping')
                continue
        
            this_dt = datetime.datetime(year, month, 15)
            i = (tropic_dt == this_dt)
            bounds = tropic_min[i][0], tropic_max[i][0]
            print(filename + ' - tropics bounds {:5.5f} - {:5.5f}'.format(*bounds))
        
            ctopsum, nclouds = tropic_ctop_from_file(filename, bounds)
            tropic_ctopsum.append(ctopsum)
            tropic_nclouds.append(nclouds)
            
            dt.append(this_dt)
    
    plot_ctop(dt, tropic_ctopsum, tropic_nclouds)
    plt.show()
    

if __name__ == '__main__':
    import plac
    plac.call(main)
