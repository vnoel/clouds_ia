#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-04-28

import numpy as np
# import niceplots as nice
import matplotlib.pyplot as plt
from vcm import sum_arrays_from_files


vcm_name = 'cal333+cal05+cal20+cal80+csat'


def pcolor_cf(x, y, vcmarray, title=None, label=None):

    from mpl_toolkits.basemap import Basemap

    m = Basemap()
    m.pcolormesh(x, y, vcmarray.T)
    m.drawcoastlines()
    m.drawparallels(np.r_[-90:90:30], labels=[1,0,0,0])
    plt.clim(0, 100)
    cb = plt.colorbar()
    if label is not None:
        cb.set_label(label)
    # plt.clim(0, 1.)
    if title is not None:
        plt.title(title + ' - average %5.2f %%' % (np.mean(vcmarray)))


def zonal(lat, v, title=None):
    
    print lat.shape, v.shape
    
    plt.plot(lat, v)
    plt.title(title)
    plt.xlim(-90,90)
    plt.xticks(np.r_[-90:90:30])
    plt.ylabel('CF')
    plt.ylim(0,80)    
    plt.grid()


def show_files(files):
    
    dset = sum_arrays_from_files(files)
    plt.figure(figsize=[10,8])
    print np.max(dset['nprof'])
    for i,layer in enumerate(['low', 'mid', 'high', 'total']):
        nprof = dset['nprof']
        cprof = dset[vcm_name + '_cprof_' + layer]
        cf = np.ma.masked_invalid(100. * cprof.values / nprof.values)    
        plt.subplot(2,2,i+1)
        pcolor_cf(cprof.lon, cprof.lat, cf, title='cloud fraction - ' + layer, label='Cloud Fraction [%]')
    plt.suptitle(files)
    plt.savefig('maps.png')


def main(mask='out.daily/200607/*nc4'):
    
    show_files(mask)    
    plt.show()
    

if __name__ == '__main__':
    import plac
    plac.call(main)
