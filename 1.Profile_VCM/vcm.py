#!/usr/bin/env python
#encoding:utf-8

# Created by V. Noel [LMD/CNRS] on 2014-06-24

import dimarray as da
import numpy as np


class VCM(object):
    
    def __init__(self, filename):

        self.filename = filename
        self.lon = da.read_nc(filename, 'lon').values
        self.lat = da.read_nc(filename, 'lat').values
        self.data = da.Dataset()
        self.data['cal333'] = da.read_nc(filename, 'cal333')
        self.altitude = self.data['cal333'].altitude
        
    
    def get_vcm(self, mask):
        
        # mask = 'cal333+cal05+cal20+cal80+csat' for instance
        
        if '+' in mask:
            names = mask.split('+')

            # this is waaaay slower
            # output = np.sum([self.data[name].values for name in names], axis=0)

            # negative data can happen e.g. for csat when there are no files.
            # it does *not* happen when the are no colocated profile, as far as I know.
            # need to do sthing better than that ?
            if names[0] not in self.data:
                self.data[names[0]] = da.read_nc(self.filename, names[0])
            output = np.clip(self.data[names[0]], 0, 1)
            for name in names[1:]:
                if name not in self.data:
                    self.data[name] = da.read_nc(self.filename, name)
                if 'csat' in name:
                    self.data[name] = np.clip(self.data[name], 0, 1)
                output += self.data[name]
            output = np.clip(output.values, 0, 1)
        else:
            if mask not in self.data:
                self.data[mask] = da.read_nc(self.filename, mask)
            output = np.clip(self.data[mask].values, 0, 1)

        return output


def aggregate_arrays_from_files(filemask, array_names, summed_along=None):
    
    aggregated = dict()
    
    for name in array_names:
        data = da.read_nc(filemask, name, axis='orbit')
        if summed_along:
            data = data.sum(axis=summed_along)
        aggregated[name] = data.sum(axis='orbit')
    
    data = [aggregated[array_name] for array_name in array_names]
    
    return data