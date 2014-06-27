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
        self.altitude = self.data['cal333'].altitude
        
    
    def get_vcm(self, mask):
        
        # mask = 'cal333+cal05+cal20+cal80+csat' for instance
        
        if '+' not in mask:
            output = np.clip(self.data[mask].values, 0, 1)
        else:
            names = mask.split('+')
            if not all(name in self.data for name in names):
                print 'Warning : some requested vcms are not present in file. Contained data :'
                print self.data
                return None        

            # this is waaaay slower
            # output = np.sum([self.data[name].values for name in names], axis=0)

            # need to clip this between 0,1
            # missing data in a vcm is flagged with -1

            # this can happen e.g. for csat when there are no files.
            # it does *not* happen when the are no colocated profile, as far as I know.
            # need to do sthing better than that ?
            output = np.clip(self.data[names[0]].values, 0, 1)
            for name in names[1:]:
                output += np.clip(self.data[name].values, 0, 1)
            output = np.clip(output, 0, 1)

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