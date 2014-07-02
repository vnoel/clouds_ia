#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-04

import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import niceplots as nice

vcm_mins = [0.05, 0.15, 0.25, 0.35]
vcm_x = {0.05:datetime(2007,7,5), 0.15:datetime(2007,6,24), 0.25:datetime(2007,6,1), 0.35:datetime(2007,5,1)}
vcm_y = {0.05:30, 0.15:25, 0.25:18, 0.35:5}

fmt = mdates.DateFormatter('%b')


def average_year(time, tmin, tmax):
    
    # this feels so fortran ! *snif*
    
    newdates = []
    for dt in time:
        if dt.year == 2007:
            newdates.append(dt)
            
    tmin_amean = dict()
    tmax_amean = dict()
    tsize_amean = dict()
    
    for vcm_min in vcm_mins:
        tminl = tmin[vcm_min]
        tmaxl = tmax[vcm_min]
        tmina = []
        tmaxa = []
        tsizea = []
        for ndt in newdates:
            ta, tb, ts = 0, 0, 0
            na, nb, ns = 0, 0, 0
            njday = ndt.timetuple().tm_yday
            print ndt, njday
            for i, dt in enumerate(time):
                jday = dt.timetuple().tm_yday
                if njday == jday:
                    print 'found ', dt, njday
                    if tminl[i] > -90:
                        ta += tminl[i]
                        na += 1
                    if tmaxl[i] > -90:
                        tb += tmaxl[i]
                        nb += 1
                    if tminl[i] > -90 and tmaxl[i] > -90:
                        ts += (tmaxl[i] - tminl[i])
                        ns += 1
            if na > 0:
                tmina.append(1.*ta/na)
            else:
                tmina.append(np.nan)
            if nb > 0:
                tmaxa.append(1.*tb/nb)
            else:
                tmaxa.append(np.nan)
            if na > 0  and nb > 0:
                tsizea.append(1.*ts/ns)
            else:
                tsizea.append(np.nan)
        
        tmin_amean[vcm_min] = tmina
        tmax_amean[vcm_min] = tmaxa
        tsize_amean[vcm_min] = tsizea
        
    return newdates, tmin_amean, tmax_amean, tsize_amean
        

def main(infile='tropic_width_40.npz'):
    
    npz = np.load(infile)
    tmin, tmax, time = npz['tmin'], npz['tmax'], npz['datetimes']
    
    tmin = np.array(tmin).item()
    tmax = np.array(tmax).item()
    
    newdates, tmin_amean, tmax_amean, tsize_amean = average_year(time, tmin, tmax)
    
    fig = plt.figure()
    
    plt.subplot(2,1,1)
    
    for vcm_min in vcm_mins:
        tmin = np.ma.masked_invalid(tmin_amean[vcm_min])
        tmax = np.ma.masked_invalid(tmax_amean[vcm_min])
        plt.fill_between(newdates, tmin, tmax, alpha=0.3)
        plt.text(vcm_x[vcm_min], vcm_y[vcm_min], 'CF > %4.2f' % vcm_min)
    plt.gca().xaxis.set_major_formatter(fmt)
    plt.title('Average 2006-2014')
    plt.grid()
    fig.autofmt_xdate()
    
    plt.subplot(2,1,2)
    
    
    for vcm_min in vcm_mins:
        tsize = np.ma.masked_invalid(tsize_amean[vcm_min])
        plt.fill_between(newdates, tsize, alpha=0.3)
    plt.gca().xaxis.set_major_formatter(fmt)
    plt.title('Average 2006-2014')
    plt.grid()
    fig.autofmt_xdate()    
    
    nice.savefig('width_avg_year.pdf')

    plt.show()
    

if __name__ == '__main__':
    import plac
    plac.call(main)
