#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-06-25

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import date2num
import niceplots as nice
import matplotlib.dates as mdates

fmt = mdates.DateFormatter('%b')

def pcolor_meridhov(time, lon, cf, title, anom=False):
    if anom:
        plt.figure(figsize=[7,10])
    else:
        plt.figure(figsize=[7,3])
    time = date2num(time)
    ax = plt.gca()
    if anom:
        plt.pcolormesh(lon, time, cf, cmap='RdBu_r')
        plt.clim(-0.05,0.05)
    else:
        plt.pcolormesh(lon, time, cf, shading='gouraud')
        plt.gca().yaxis.set_major_formatter(fmt)
        plt.ylim(datetime(2007,1,1), datetime(2007,12,31))
    ax.yaxis.axis_date()
        
    plt.colorbar()
    plt.xlim(-180, 180)
    plt.title(title)


def main(infile='series_40.npz'):
    
    npz = np.load(infile)
    nprof = npz['nprof']
    vcm = npz['vcm']
    time = npz['time']
    lon = npz['lon']
    altmin = npz['altmin']
    
    # exchange time and altmin axes
    vcm = vcm.swapaxes(0, 1)
    # now vcm[altmin,time,lon]
    
    # average year
    # find the vector of julian days for a typical year
    jdays = []
    time_avg = []
    for d in time:
        if d.year == 2007:
            jdays.append((d - datetime(2007,1,1)).days)
            time_avg.append(d)
    
    nprof_avg = np.zeros([len(jdays), vcm.shape[2]])
    vcm_avg = dict()
    for ialtmin in range(len(altmin)):
        vcm_avg[ialtmin] = np.zeros([len(jdays), vcm.shape[2]])
    cf_anom = np.zeros_like(vcm, dtype='float64')

    for i, jday in enumerate(jdays):
        
        idx = np.array([jday==(date - datetime(date.year, 1, 1)).days for date in time])
        print jday, ' - found {} days'.format(idx.sum())
        nprof_avg[i,:] = np.sum(nprof[idx,:], axis=0)
        
        for ialtmin in 0, 1, 2:
            
            vcm_avg[ialtmin][i,:] = np.sum(vcm[ialtmin,idx,:], axis=0)
            cf_avg = 1. * vcm_avg[ialtmin][i,:] / nprof_avg[i,:]
            actual_cf = 1. * vcm[ialtmin,idx,:] / nprof[idx,:]
            cf_anom[ialtmin,idx,:] = actual_cf - cf_avg

    for ialtmin in 0, 1, 2:

        cf = 1. * vcm_avg[ialtmin] / nprof_avg
        pcolor_meridhov(time_avg, lon, cf, 'clouds above > %2d km - Average year' % (altmin[ialtmin]))
        nice.savefig(infile[:-4] + '_avg_above%02dkm.png' % (altmin[ialtmin]))

        pcolor_meridhov(time, lon, cf_anom[ialtmin], 'clouds above > %2d km - Anomaly' % (altmin[ialtmin]), anom=True)
        nice.savefig(infile[:-4] + '_anom_above%02dkm.png' % (altmin[ialtmin]))
    
    plt.show()

if __name__ == '__main__':
    import plac
    plac.call(main)