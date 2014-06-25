#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-06-25

import datetime
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import date2num
import niceplots as nice

def pcolor_meridhov(time, lon, cf, title, anom=False):
    if anom:
        plt.figure(figsize=[7,10])
    else:
        plt.figure()
    time = date2num(time)
    ax = plt.gca()
    if anom:
        plt.pcolormesh(lon, time, cf, cmap='RdBu_r')
        plt.clim(-0.1,0.1)
    else:
        plt.pcolormesh(lon, time, cf)
    ax.yaxis.axis_date()
        
    plt.colorbar()
    plt.xlim(-180, 180)
    plt.title(title)

def main(input='monthlies.npz'):
    
    npz = np.load(input)
    nprof = npz['nprof']
    vcm = npz['vcm']
    time = npz['time']
    lon = npz['lon']
    altmin = npz['altmin']
    # exchange time and altmin axes
    vcm = vcm.swapaxes(0, 1)
    # now vcm[altmin,time,lon]
    
    # average year
    vcm_avg = dict()
    for ialtmin in 0, 1, 2:
        vcm_avg[ialtmin] = np.zeros([13, vcm.shape[2]])
    nprof_avg = np.zeros([13, vcm.shape[2]])
    time_avg = []

    # anomalies
    vcm_anom = np.zeros_like(vcm)

    for month in range(1,13):
        
        time_avg.append(datetime.datetime(2010, month, 15))
        idx = np.array([month==date.month for date in time])
        nprof_avg[month,:] = np.sum(nprof[idx,:], axis=0)
        
        for ialtmin in 0, 1, 2:
            
            vcm_avg[ialtmin][month,:] = np.mean(vcm[ialtmin,idx,:], axis=0)
            vcm_anom[ialtmin,idx,:] = vcm[ialtmin,idx,:] - vcm_avg[ialtmin][month   ,:]

    time_avg[:0] = [datetime.datetime(2009,12,15)]
    nprof_avg[0,:] = nprof_avg[12,:]
    for ialtmin in 0, 1, 2:
        vcm_avg[ialtmin][0,:] = vcm_avg[ialtmin][12,:]

    for ialtmin in 0, 1, 2:

        cf = 1. * vcm_avg[ialtmin] / nprof_avg
        pcolor_meridhov(time_avg, lon, cf, 'clouds above > %2d km - Average year' % (altmin[ialtmin]))
        nice.savefig('cf_avg_above%02dkm.png' % (altmin[ialtmin]))

        cf = 1. * vcm_anom[ialtmin,:,:] / nprof
        pcolor_meridhov(time, lon, cf, 'clouds above > %2d km - Anomaly' % (altmin[ialtmin]), anom=True)
        nice.savefig('cf_anom_above%02dkm.png' % (altmin[ialtmin]))
    
    plt.show()

if __name__ == '__main__':
    import plac
    plac.call(main)