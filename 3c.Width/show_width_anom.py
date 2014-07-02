#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-04

import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import niceplots as nice
from show_width_avg import average_year

vcm_mins = [0.05, 0.15, 0.25, 0.35]
vcm_x = {0.05:datetime(2007,7,5), 0.15:datetime(2007,6,24), 0.25:datetime(2007,6,1), 0.35:datetime(2007,5,1)}
vcm_y = {0.05:30, 0.15:25, 0.25:18, 0.35:5}
colors = {0.05:'b', 0.35:'g'}

fmt = mdates.DateFormatter('%b')

def anomalies(time, tmin, tmax, newdates, tmin_amean, tmax_amean):
    tmin_anom = dict()
    tmax_anom = dict()
    tsize_anom = dict()
    for vcm_min in vcm_mins:
        tminl = tmin[vcm_min]
        tmaxl = tmax[vcm_min]
        tmina = []
        tmaxa = []
        tsizea = []
        for i, dt in enumerate(time):
            print dt
            jday = dt.timetuple().tm_yday
            for j, ndt in enumerate(newdates):
                njday = ndt.timetuple().tm_yday
                if njday == jday:
                    print 'found : ', ndt
                    if tminl[i] > -90:
                        tmina.append(tminl[i] - tmin_amean[vcm_min][j])
                    else:
                        tmina.append(np.nan)
                    if tmaxl[i] > -90:
                        tmaxa.append(tmaxl[i] - tmax_amean[vcm_min][j])
                    else:
                        tmaxa.append(np.nan)
                    if tminl[i] > -90 and tmaxl[i] > -90:
                        s = tmaxl[i] - tminl[i]
                        sa = tmax_amean[vcm_min][j] - tmin_amean[vcm_min][j]
                        tsizea.append(s - sa)
                    else:
                        tsizea.append(np.nan)
        tmin_anom[vcm_min] = tmina
        tmax_anom[vcm_min] = tmaxa
        tsize_anom[vcm_min] = tsizea
    return tmin_anom, tmax_anom ,tsize_anom
    

def main(infile='tropic_width_40.npz'):
    npz = np.load(infile)
    tmin, tmax, time = npz['tmin'], npz['tmax'], npz['datetimes']
    
    tmin = np.array(tmin).item()
    tmax = np.array(tmax).item()
    
    newdates = []
    for dt in time:
        if dt.year == 2007:
            newdates.append(dt)
            
    newdates, tmin_amean, tmax_amean, tsize_amean = average_year(time, tmin, tmax)
    tmin_anom, tmax_anom, tsize_anom = anomalies(time, tmin, tmax, newdates, tmin_amean, tmax_amean)
        
    fig = plt.figure()
    plt.subplot(3,1,1)
    for vcm_min in [0.05, 0.35]:
        tmin = np.ma.masked_invalid(tmin_anom[vcm_min])
        plt.fill_between(time, 0, tmin, alpha=0.3, label=vcm_min, color=colors[vcm_min])
    plt.ylim(-10, 15)
    plt.legend()
    plt.title('North boundary anomaly')
    plt.grid()
        
    plt.subplot(3,1,2)
    for vcm_min in [0.05, 0.35]:
        tmax = np.ma.masked_invalid(tmax_anom[vcm_min])
        plt.fill_between(time, 0, tmax, alpha=0.3, color=colors[vcm_min])
    plt.ylim(-10, 10)
    plt.grid()
    plt.title('South boundary anomaly')
    
    plt.subplot(3,1,3)
    for vcm_min in [0.05, 0.35]:
        tsize = np.ma.masked_invalid(tsize_anom[vcm_min])
        plt.fill_between(time, 0, tsize, alpha=0.3, color=colors[vcm_min])
    plt.ylim(-10, 10)
    plt.grid()
    plt.title('North-South Size')
    fig.autofmt_xdate()
    plt.show()
    
    
    

if __name__ == '__main__':
    import plac
    plac.call(main)
