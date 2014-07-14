#!/usr/bin/env python
#encoding:utf-8

# Created by V. Noel [LMD/CNRS] on 2014-06-24

import dimarray as da
import numpy as np


class VCM(object):

    '''
    it is possible to read several orbit files at a time, using e.g. a glob pattern
    v = VCM('out/200701/vcm_2007-01-01T*_v2.0.nc4')
    or from a filelist
    v = VCM(glob.glob('out/200701/vcm_2007-01-01T*_v2.0.nc4'))
    '''
    
    def __init__(self, filename, verbose=True):

        import netCDF4

        self.filename = filename
        self.verbose = verbose
        dimarrays = da.read_nc(filename, ['lon', 'lat', 'cal333'], axis='tai_time', verbose=verbose)
        self.altitude = dimarrays['cal333'].altitude
        self.lon = dimarrays['lon'].values
        self.lat = dimarrays['lat'].values
        self.data = {'cal333':dimarrays['cal333'].values}
        
    
    def get_vcm(self, mask):
        
        # mask = 'cal333+cal05+cal20+cal80+csat' for instance
        
        if '+' in mask:
            names = mask.split('+')
            
            to_read = []
            for name in names:
                if name not in self.data:
                    to_read.append(name)
            ds = da.read_nc(self.filename, to_read, axis='tai_time', verbose=self.verbose)
            for name in to_read:
                self.data[name] = ds[name].values
            if 'csat' in names:
                self.data['csat'] = np.clip(self.data['csat'], 0, 3)

            # negative data can happen e.g. for csat when there are no files.
            # it does *not* happen when the are no colocated profile, as far as I know.
            # need to do sthing better than that ?
            output = self.data[names[0]]
            for name in names[1:]:
                output += self.data[name]
        else:
            if mask not in self.data:
                self.data[mask] = da.read_nc(self.filename, mask, axis='tai_time').values
            output = self.data[mask]

        output = np.clip(output, 0, 3)

        return output


def sum_arrays_from_files(filemask, array_names=None):
    
    import glob
    
    if array_names is None:
        datasets = da.read_nc(filemask, axis='day')
    else:
        datasets = da.read_nc(filemask, array_names, axis='day')
    datasets = datasets.sum(axis='day')
    return datasets
    
