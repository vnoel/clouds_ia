#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-07-15

import numpy as np
import dimarray as da
import matplotlib.pyplot as plt

def main(mask='out/200607/*nc4'):
    
    dset = da.read_nc(mask, ['cloudpts'], axis='tai_time')
    cpts = dset['cloudpts']
    cpts  = cpts/3.
    
    print 'Range of cloudy points in cloudsat-only cloudy profiles : ', np.min(cpts.values), np.max(cpts.values)
    
    plt.figure()
    cpts.plot(lw=0.5)
    plt.figure()
    plt.hist(cpts[cpts>0].values, 20)
    
    plt.show()


if __name__ == '__main__':
    import plac
    plac.call(main)