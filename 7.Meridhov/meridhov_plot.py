#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-06-25

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import date2num
import niceplots as nice

def pcolor_meridhov(time, lon, cf, title):
    plt.figure()
    time = date2num(time)
    ax = plt.gca()
    plt.pcolormesh(lon, time, cf)
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
    vcm = vcm.swapaxes(0, 1)

    pcolor_meridhov(time, lon, nprof, 'Number of profiles')
    nice.savefig('%s_nprof.png' % (infile[:-4]))

    for ialtmin in 0,1,2:
        cf = 1. * vcm[ialtmin,...] / nprof
        pcolor_meridhov(time, lon, cf, 'clouds above > %5f km' % (altmin[ialtmin]))
        nice.savefig('%s_above%02dkm.png' % (infile[:-4], altmin[ialtmin]))
    
    plt.show()

if __name__ == '__main__':
    import plac
    plac.call(main)