#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-04

import numpy as np
import matplotlib.pyplot as plt

def main(infile='out/tropic_width.npz'):
    npz = np.load(infile)
    tmin, tmax, time = npz['tmin'], npz['tmax'], npz['datetimes']
    
    plt.figure(figsize=[15,10])
    plt.subplot(2,1,1)
    plt.plot(time, tmin, label='South boundary')
    plt.plot(time, tmax, label='North boundary')
    plt.ylabel('Latitude')
    plt.legend(loc='center right')
    plt.grid()
    
    plt.subplot(2,1,2)
    plt.plot(time, tmax-tmin)
    plt.ylabel('Tropics meridional height')
    plt.grid()
    
    plt.show()
    

if __name__ == '__main__':
    import plac
    plac.call(main)
