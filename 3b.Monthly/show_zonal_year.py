#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-05

import numpy as np
import dimarray as da
import matplotlib.pyplot as plt
import tropic_width
import niceplots as nice


def pcolor_zonal(x, y, vcmarray, title=None):

    plt.contourf(x, y, vcmarray.T, np.r_[0:0.8:0.05])
    plt.colorbar()
    if title is not None:
        plt.title(title)
    plt.clim(0,0.8)
    plt.xlim(-82,82)
    plt.xticks(np.r_[-90:90+30:30])
    plt.axhline(y=16, ls='--', color='w')
    # latrange = tropic_width(x, y, vcmarray)
    # plt.axvline(x=latrange[0], ls='--', color='w')
    # plt.axvline(x=latrange[1], ls='--', color='w')
    latup, latdown = tropic_width.tropic_width2(x, y, vcmarray)
    plt.axvline(x=latup, ls='--', color='w')
    plt.axvline(x=latdown, ls='--', color='w')
    # print 'lat range : ', latrange
    # print 'lat width : ', latrange[1]-latrange[0]


def cf_zonal(filename):
    
    data = da.read_nc(filename)
    vcm_prof = data['vcm_csat+cal333-80']
    nprof = data['vcm_csat+cal333-80_cprof']

    cf_lat = 1. * vcm_prof.values.T / nprof.values
    cf_lat = cf_lat.T
    cf_lat = np.ma.masked_invalid(cf_lat)
    
    return vcm_prof.labels[0], vcm_prof.labels[1], cf_lat
    

def show_files(files, title):
    
    plt.figure(figsize=[12,12])
    
    for i, filename in enumerate(files):

        lat, alt, cf_lat = cf_zonal(filename)
        plt.subplot(6,2,i+1)
        pcolor_zonal(lat, alt, cf_lat, filename.split('/')[-1])


def main(year=2007):
    
    import glob
    
    year = int(year)
    mask = './out/%04d/*nc4' % (year)
    
    grid_files = glob.glob(mask)
    grid_files.sort()

    show_files(grid_files, '2007')
    
    nice.savefig('zonal_cf_%04d.png' % (year))
    plt.show()
    

if __name__ == '__main__':
    import plac
    plac.call(main)