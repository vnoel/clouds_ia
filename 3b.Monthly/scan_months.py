#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-02

import numpy as np
import dimarray as da
import matplotlib.pyplot as plt


def dayfiles_sum_dataset(files):
    
    aggregated = da.Dataset()
    
    for f in files:

        data = da.read_nc(f)
        for array_name in data:
            
            array = data[array_name]

            if array_name not in aggregated:
                aggregated[array_name] = 1. * array
            else:
                aggregated[array_name] += array
        
    return aggregated


def dayfiles_to_monthfile(files, outfile):
    
    monthly_sum = dayfiles_sum_dataset(files)
    monthly_sum.write_nc(outfile, 'w')


def scan_months(year, months):
    
    import glob
    
    for month in months:
        mask = 'in/%04d%02d/*.nc4' % (year, month)
        dayfiles = glob.glob(mask)
        dayfiles.sort()
        outfile = 'out/vcm_zonal_%04d%02d.nc4' % (year, month)
        dayfiles_to_monthfile(dayfiles, outfile)
    

def main(year=2007, month=None):
    
    if month is None:
        months = np.r_[1:13]
    else:
        months = [int(month)]
    year = int(year)
        
    scan_months(year, months)
    

if __name__ == '__main__':
    import plac
    plac.call(main)
