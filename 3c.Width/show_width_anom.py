#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-04

import numpy as np
import matplotlib.pyplot as plt

vcm_mins = [0.05, 0.15, 0.25, 0.35]
colors = {0.05:'k', 0.15:'r', 0.25:'b', 0.35:'gray'}

def main(infile='tropic_width_40.npz'):
    npz = np.load(infile)
    tmin, tmax, time = npz['tmin'], npz['tmax'], npz['datetimes']
    
    tmin = np.array(tmin).item()
    tmax = np.array(tmax).item()
    
    newdates = []
    for dt in time:
        if dt.year == 2007:
            newdates.append(dt)
            
    tmin_amean = dict()
    tmax_amean = dict()
    for vcm_min in vcm_mins:
        tmin = tmin[0.05]
        tmax = tmax[0.05]
        tmina = []
        tmaxa = []
        for ndt in newdates:
            ta = 0
            tb = 0
            n = 0
            for i, dt in enumerate(time):
                if dt.day==ndt.day and dt.month==ndt.month:
                    ta += tmin[i]
                    tb += tmax[i]
                    n += 1
            tmina.append(1.*ta/n)
            tmaxa.append(1.*tb/n)
        tmin_amean[vcm_min] = tmina
        tmax_amean[vcm_min] = tmaxa
    
    plt.figure()
    for vcm_min in vcm_mins:
        plt.plot(newdates, tmin_amean[vcm_min])
        plt.plot(newdates, tmax_amean[vcm_min])
    plt.show()
    

if __name__ == '__main__':
    import plac
    plac.call(main)
