#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-02

import numpy as np
import dimarray as da
import matplotlib.pyplot as plt


def plot_ctop(ctop_avg):
    
    plt.figure(figsize=[15,5])
    for year in ctop_avg:
        plt.plot(ctop_avg[year].labels[0], ctop_avg[year], label=year)
    plt.xlabel('Latitude')
    plt.ylabel('Average Cloud Top')
    
    plt.legend()
    

def aggregate_arrays_from_files(files, array_names):
    
    aggregated = dict()

    files.sort()
    prevmax = 0

    for f in files:

        data = da.read_nc(f)
        if any(array_name not in data for array_name in array_names):
            continue
            
        for array_name in array_names:

            array = data[array_name]

            if array_name not in aggregated:
                aggregated[array_name] = 1. * array
            else:
                aggregated[array_name] += array
        
            if aggregated[array_name].max() < prevmax:
                print 'PROBLEME !'
                print 'Previous maximum = ', prevmax, ', current max = ', aggregated[array_name].max()

    data = [aggregated[key] for key in array_names]

    return data


def ctop_avg_for_files(files):
    
    ctopsum, nclouds = aggregate_arrays_from_files(files, ['cal333+cal05+cal20+cal80+csat_ctopsum', 'cal333+cal05+cal20+cal80+csat_nclouds'])    
    ctop = np.ma.masked_where(nclouds.values==0, 1. * ctopsum.values / nclouds.values)
    ctop = np.ma.masked_invalid(ctop)
    ctop = da.DimArray(ctop, labels=ctopsum.labels, dims=ctopsum.dims)
    
    return ctop
    

def main():
    
    import glob
    
    years = range(2006,2013)
    ctop_avg = dict()
    
    for year in years:
        mask = 'out/{:04d}/ctop_zonal*.nc4'.format(year)
        files = glob.glob(mask)
        if len(files)==0:
            print(mask + ' : no monthlies, skipping')
            continue
        print(mask + ' : {} files'.format(len(files)))
        ctop_avg[year] = ctop_avg_for_files(files)
    
    plot_ctop(ctop_avg)
    plt.show()
    

if __name__ == '__main__':
    import plac
    plac.call(main)
