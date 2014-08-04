#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-06-25

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import date2num
import niceplots as nice

def pcolor_meridhov(time, lon, cf, title):
    plt.figure(figsize=[5,15])
    # time = date2num(time)
    time = np.r_[0:cf.shape[0]]
    ax = plt.gca()
    plt.pcolormesh(lon, time, cf)
    # ax.yaxis.axis_date()
    cb = plt.colorbar(orientation='horizontal', pad=0.05)
    cb.set_label('Cloud Fraction [%]')
    plt.xlim(-180, 180)
    plt.xlabel('Longitude')
    plt.clim(0,30)
    plt.ylim(time[0], time[-1])
    plt.title(title)
    # plt.tight_layout()

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
        pcolor_meridhov(time, lon, 100.*cf, 'Above %2d km' % (altmin[ialtmin]))
        nice.savefig('%s_above%02dkm.png' % (infile[:-4], altmin[ialtmin]))
    
    plt.show()

if __name__ == '__main__':
    import plac
    plac.call(main)