#!/usr/bin/env python
#encoding:utf-8

# Created by V. Noel [LMD/CNRS] on 2014-06-24

import dimarray as da
import numpy as np


class VCM(object):
    
    def __init__(self, filename):
    
        self.data = da.read_nc(filename)
        self.lon = self.data['lon']
        self.lat = self.data['lat']
        
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

    