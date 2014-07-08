#!/usr/bin/env python
#encoding:utf-8

# Created by V. Noel [LMD/CNRS] on 2014-07-02

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import niceplots as nice

fmt = mdates.DateFormatter('%b')

def average_year(dtlist, nprof, cprof):
    
    avg_dtlist = []
    for dt in dtlist:
        if dt.year == 2007:
            avg_dtlist.append(dt)
    
    avg_nprof = np.zeros([len(avg_dtlist), nprof.shape[1]])
    avg_cprof = np.zeros_like(avg_nprof)
    avg_cf = np.zeros_like(avg_cprof)
    
    for i, avg_dt in enumerate(avg_dtlist):
        ajday = (avg_dt - datetime(avg_dt.year, 1, 1)).days
        n = 0
        for j, dt in enumerate(dtlist):
            jday = (dt - datetime(dt.year,1,1)).days
            if ajday == jday:
                avg_nprof[i,:] += nprof[j,:]
                avg_cprof[i,:] += cprof[j,:]
                n += 1
                
        if n > 0:
            avg_cf[i,:] = 100. * avg_cprof[i,:] / avg_nprof[i,:]
        else:
            avg_cf[i,:] = 0.
        
    avg_cf = np.ma.masked_invalid(avg_cf)
        
    return np.array(avg_dtlist), avg_cf


def anomalies(dtavg, avg, dtval, val):
    
    anom = np.zeros_like(val)
    for i, dt in enumerate(dtval):
        jday = (dt - datetime(dt.year, 1, 1)).days
        for j, thisavgdt in enumerate(dtavg):
            ajday = (thisavgdt - datetime(thisavgdt.year, 1, 1)).days
            if ajday==jday:
                anom[i,:] = val[i,:] - avg[j,:]
                break
    return anom

def main():
    
    npz = np.load('ceilings_40.npz')
    dt = npz['datetimes']
    nprof = npz['nprof']
    cprof = npz['cprof']
    lat = npz['lat']

    dtnum = mdates.date2num(dt)

    nprof = nprof[0:len(dt),:]
    cprof = cprof[0:len(dt),:]
    
    nproft = np.sum(nprof, axis=1)
    cft = 100.*np.sum(cprof, axis=1)/nproft
    badidx = (cft < 57) | (nproft < 1.7e7)

    cf = 100. * cprof / nprof
    cf[badidx,:] = np.nan
    cf = np.ma.masked_where(nprof==0, cf)
    cf = np.ma.masked_invalid(cf)
    
    print dtnum.shape, lat.shape, cf.shape
    avgdt, avgcf = average_year(dt, nprof, cprof)
    avgdtnum = mdates.date2num(avgdt)

    plt.figure(figsize=[24,4])
    plt.pcolormesh(dtnum, lat, cf.T)
    plt.xlim(dtnum[0], dtnum[-1])
    plt.ylim(-60,60)
    plt.gca().xaxis.axis_date()
    plt.grid()
    plt.clim(30, 100)
    plt.title('Cloud Fraction')
    plt.colorbar()
    nice.savefig('cfz.png')

    plt.figure(figsize=[10,5])
    plt.pcolormesh(avgdtnum, lat, avgcf.T)
    plt.xlim(avgdtnum[0], avgdtnum[-1])
    plt.ylim(-60,60)
    plt.gca().xaxis.axis_date()
    plt.gca().xaxis.set_major_formatter(fmt)
    plt.clim(30, 100)
    plt.title('Cloud Fraction average 2006-2014')
    plt.colorbar()
    plt.grid()
    nice.savefig('cfz_avg.png')
    
    anom = anomalies(avgdt, avgcf, dt, cf)

    plt.figure(figsize=[24,4])
    plt.pcolormesh(dtnum, lat, anom.T, cmap='RdBu_r')
    plt.xlim(dtnum[0], dtnum[-1])
    plt.ylim(-60,60)
    plt.gca().xaxis.axis_date()
    plt.grid()
    plt.clim(-10,10)
    plt.title('Cloud Fraction Anomalies [%]')
    plt.colorbar()
    nice.savefig('cfz_anom.png')

    
    plt.show()



if __name__ == '__main__':
    main()

