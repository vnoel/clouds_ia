#!/usr/bin/env python
#encoding:utf-8

# Created by V. Noel [LMD/CNRS] on 2014-06-24

import dimarray as da
import numpy as np


class VCM(object):
    
    def __init__(self, filename):
    
        self.data = da.read_nc(filename)
        self.lon = self.data['lon'].values
        self.lat = self.data['lat'].values
        
        self.altitude = self.data['cal333'].labels[1]
        
    
    def get_vcm(self, mask):
        
        # mask = 'cal333+cal05+cal20+cal80+csat' for instance
        
        if '+' not in mask:
            output = self.data[mask]
        else:
            names = mask.split('+')
            if not all(name in self.data for name in names):
                print 'Warning : some requested vcms are not present in file. Contained data :'
                print self.data
                return None        
        
            output = self.data[names[0]].values
            for name in names[1:]:
                output += self.data[name].values

            np.clip(output, 0, 1, out=output)

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