#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-04

import numpy as np
import niceplots as nice
import matplotlib.pyplot as plt

vcm_mins = [0.05, 0.15, 0.25, 0.35]
colors = {0.05:'k', 0.15:'r', 0.25:'b', 0.35:'gray'}

def main(infile='tropic_width_40.npz'):
    npz = np.load(infile)
    tmin, tmax, time = npz['tmin'], npz['tmax'], npz['datetimes']
    
    tmin = np.array(tmin).item()
    tmax = np.array(tmax).item()
    
    
    plt.figure(figsize=[15,10])
    plt.subplot(2,1,1)
    for vcm_min in vcm_mins:
        this_tmin = np.array(tmin[vcm_min])
        this_tmin = np.ma.masked_where(this_tmin < -90, this_tmin)
        this_tmax = np.array(tmax[vcm_min])
        this_tmax = np.ma.masked_where(this_tmax < -90, this_tmax)
        plt.plot(time, this_tmin, colors[vcm_min])
        plt.plot(time, this_tmax, colors[vcm_min])
    plt.ylabel('Latitude')
    plt.legend(loc='center right')
    plt.grid()
    
    plt.subplot(2,1,2)
    for vcm_min in vcm_mins:
        this_tmin = np.array(tmin[vcm_min])
        this_tmin = np.ma.masked_where(this_tmin < -90, this_tmin)
        this_tmax = np.array(tmax[vcm_min])
        this_tmax = np.ma.masked_where(this_tmax < -90, this_tmax)
        plt.plot(time, this_tmax - this_tmin, colors[vcm_min])
    plt.ylabel('Tropics meridional height')
    plt.grid()
    
    nice.savefig(infile[:-4] + '.png')
    
    plt.show()
    

if __name__ == '__main__':
    import plac
    plac.call(main)
