#!/usr/bin/env python
#encoding:utf-8

# Created by V. Noel [LMD/CNRS] on 2014-07-02

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import matplotlib.dates as mdates

fmt = mdates.DateFormatter('%b')

def average_year(dtlist, ceil):
    
    avg_dtlist = []
    for dt in dtlist:
        if dt.year == 2007:
            avg_dtlist.append(dt)
    
    avg_ceil = np.zeros([len(avg_dtlist), ceil.shape[1]])
    
    for i, avg_dt in enumerate(avg_dtlist):
        ajday = (avg_dt - datetime(avg_dt.year, 1, 1)).days
        n = 0
        for j, dt in enumerate(dtlist):
            jday = (dt - datetime(dt.year,1,1)).days
            if ajday == jday:
                if avg_dt == datetime(2007, 5, 21) and dt.year==2006:
                    continue
                avg_ceil[i,:] += ceil[j,:]
                n += 1
                
        if n > 0:
            avg_ceil[i,:] = 1. * avg_ceil[i,:] / n
        else:
            avg_ceil[i,:] = 0.
    
    return avg_dtlist, avg_ceil


def main():
    npz = np.load('ceilings_40.npz')
    dt = npz['datetimes']
    ceil = npz['ceilings']
    nprof = npz['nprof']
    lat = npz['lat']
    
    print nprof.shape

    ceil = ceil[0:len(dt),:]
    nprof = nprof[0:len(dt),:]

    # ceil = nprof

    dtnum = mdates.date2num(dt)

    plt.figure(figsize=[20,5])
    plt.pcolormesh(dtnum, lat, ceil.T)
    plt.xlim(dtnum[0], dtnum[-1])
    plt.ylim(lat[0], lat[-1])
    plt.ylim(-40, 60)
    plt.clim(10,18)
    # plt.clim(0,5000)
    # plt.clim(7,18)
    cb = plt.colorbar()
    cb.set_label('Altitude [km]')
    plt.gca().xaxis.axis_date()
    plt.ylabel('Latitude')
    plt.title('Highest altitude where CF > 0.05')
    
    plt.savefig('ceilings.png')

# datetime.datetime(2007, 5, 21, 0, 0) is weird

    avgdt, avgceil = average_year(dt, ceil)

    plt.figure(figsize=[10,5])
    avgdtnum = mdates.date2num(avgdt)
    plt.pcolormesh(avgdtnum, lat, avgceil.T)
    plt.ylim(-40,60)
    plt.clim(10,18)
    cb = plt.colorbar()
    cb.set_label('Altitude [km]')
    plt.xlim(datetime(2007,1,1), datetime(2007,12,31))
    plt.gca().xaxis.axis_date()
    plt.gca().xaxis.set_major_formatter(fmt)
    plt.ylabel('Latitude')
    plt.title('Highest altitude where CF > 0.05')

    plt.savefig('ceilings_avg.png')

        

    plt.show()


if __name__ == '__main__':
    main()

