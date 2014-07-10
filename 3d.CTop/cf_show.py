#!/usr/bin/env python
#encoding:utf-8

# Created by V. Noel [LMD/CNRS] on 2014-07-02

import numpy as np
import niceplots as nice
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

fmt = mdates.DateFormatter('%b')


def anomalies(dtavg, avg, dtval, val):
    
    anom = np.zeros_like(val)
    for i, dt in enumerate(dtval):
        jday = (dt - datetime(dt.year, 1, 1)).days
        for j, thisavgdt in enumerate(dtavg):
            ajday = (thisavgdt - datetime(thisavgdt.year, 1, 1)).days
            if ajday==jday:
                anom[i] = val[i] - avg[j]
                break
    return anom
                
            
def average_year(dtlist, val):
    
    avg_dtlist = []
    for dt in dtlist:
        if dt.year == 2007:
            avg_dtlist.append(dt)
    
    avg = np.zeros([len(avg_dtlist)])
    
    for i, avg_dt in enumerate(avg_dtlist):
        ajday = (avg_dt - datetime(avg_dt.year, 1, 1)).days
        n = 0
        for j, dt in enumerate(dtlist):
            jday = (dt - datetime(dt.year,1,1)).days
            if ajday == jday:
                avg[i] += val[j]
                n += 1
                
        if n > 0:
            avg[i] = 1. * avg[i] / n
        
    return avg_dtlist, avg


def main():
    
    npz = np.load('ceilings_40.npz')
    dt = npz['datetimes']
    nprof = npz['nprof']
    cprof = npz['cprof']
    lat = npz['lat']

    idx = (lat > -82) & (lat < 82)
    nprof = nprof[0:len(dt),idx]
    cprof = cprof[0:len(dt),idx]
    lat = lat[idx]
    nprof = nprof.sum(axis=1)
    cprof = cprof.sum(axis=1)

    plt.figure(figsize=[20,5])
    plt.plot(dt, nprof, label='Total profiles')
    plt.plot(dt, cprof, label='Cloudy profiles')
    plt.legend()
    plt.grid()

    cf = 100.*cprof/nprof
    badidx = (cf < 57) | (nprof < 1.7e7)

    plt.figure(figsize=[24,4])
    plt.plot(dt, cf)
    plt.plot(dt[badidx], cf[badidx], 'r*')
    plt.grid()
    plt.ylabel('Cloud Fraction [%]')
    plt.title('2006-2014')
    nice.savefig('cf.png')

    avgdt, avgnprof = average_year(dt, nprof)
    avgdt, avgcprof = average_year(dt, cprof)
    avgcf = 100. * avgcprof / avgnprof
    
    plt.figure(figsize=[10,5])
    plt.plot(avgdt, avgcf)
    plt.grid()
    plt.ylabel('Cloud Fraction [%]')
    plt.title('Average 2006-2014')
    nice.savefig('cf_avg.png')
    plt.gca().xaxis.set_major_formatter(fmt)
    
    cfanom = anomalies(avgdt, avgcf, dt, cf)
    cfanom = np.ma.masked_where(badidx, cfanom)
    
    plt.figure(figsize=[24,4])
    plt.plot(dt, cfanom)
    plt.fill_between(dt, 0, cfanom, alpha=0.2)
    plt.grid()
    plt.ylabel('Cloud Fraction Anomalies [%]')
    plt.title('2006-2014')
    nice.savefig('cf_anom.png')


    plt.figure(figsize=[24,4])
    plt.plot(dt, cf, label='Cloud Fraction')
    plt.plot(dt, cf - cfanom, color='grey', label='Average 2006-2014')
    cfavg = cf - cfanom
    cfred = np.ma.masked_where(cfanom < 0, cf)
    plt.fill_between(dt, cfred, cfred-cfanom, color='red', alpha=0.2)
    cfblue = np.ma.masked_where(cfanom > 0, cf)
    plt.fill_between(dt, cfblue, cfblue-cfanom, color='blue', alpha=0.2)
    plt.grid()
    plt.legend()
    plt.ylabel('Cloud Fraction [%]')
    plt.title('2006-2014')
    nice.savefig('cf_anom_bluered.png')


    plt.show()


if __name__ == '__main__':
    main()

