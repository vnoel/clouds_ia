#!/usr/bin/env python
#encoding:utf-8

# Created by V. Noel [LMD/CNRS] on 2014-06-18

import dimarray as da


def dayfiles_sum_dataset(files):
    
    aggregated = da.Dataset()
    
    for f in files:

        data = da.read_nc(f)
        for array_name in data:
            
            # array = data[array_name]

            if array_name not in aggregated:
                aggregated[array_name] = data[array_name]
            else:
                aggregated[array_name] += data[array_name]
        
    return aggregated


def main(year=2006, months=None):
    
    import glob, os
    
    year = int(year)
    
    if months is None:
        months = range(13)
    else:
        months = [int(months)]
        
    for month in months:
        path = 'out/{}{:02d}/ctop_zonal*.nc4'.format(year, month)
        files = glob.glob(path)
        if len(files)==0:
            print(path + ': No dailies, skipping')
            continue
        print (path + ': {} files'.format(len(files)))
        outpath = 'out/{:04d}'.format(year)
        if not os.path.isdir(outpath):
            os.mkdir(outpath)
        outfile = outpath + '/ctop_zonal_{:04d}{:02d}.nc4'.format(year, month)
        
        month_sum = dayfiles_sum_dataset(files)
        month_sum.write_nc(outfile, 'w')
        
        
if __name__ == '__main__':
    import plac
    plac.call(main)