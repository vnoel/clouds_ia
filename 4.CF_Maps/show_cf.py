#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-04-28

import numpy as np
import niceplots as nice
import matplotlib.pyplot as plt
from vcm import aggregate_arrays_from_files


vcm_name = 'cal333+cal05+cal20+cal80+csat'


def pcolor_cf(x, y, vcmarray, title=None):

    from mpl_toolkits.basemap import Basemap

    m = Basemap()

    plt.figure(figsize=[10,5])
    m.pcolormesh(x, y, vcmarray.T)
    m.drawcoastlines()
    m.drawparallels(np.r_[-90:90:30], labels=[1,0,0,0])
    plt.colorbar()
    # plt.clim(0, 1.)
    if title is not None:
        plt.title(title)


def zonal(lat, v, title=None):
    
    print lat.shape, v.shape
    
    plt.figure(figsize=[10,5])
    plt.plot(lat, v)
    plt.title(title)
    plt.xlim(-90,90)
    plt.xticks(np.r_[-90:90:30])
    plt.ylabel('CF')
    plt.ylim(0,80)    
    plt.grid()


def show_files(files, layer, title, period):
    
    cprof, nprof = aggregate_arrays_from_files(files, [vcm_name + '_cprof_' + layer, 'nprof'])
    
    cf = np.ma.masked_where(nprof.values==0, 100. * cprof.values / nprof.values)
    cf = np.ma.masked_invalid(cf)
    
    pcolor_cf(cprof.labels[0], cprof.labels[1], cprof.values, title=title + ' - cloud counts')
    nice.savefig('cc_%s_2008_%s.png' % (layer, period))
    pcolor_cf(cprof.labels[0], cprof.labels[1], nprof.values, title=title + ' - total counts')
    nice.savefig('tc_%s_2008_%s.png' % (layer, period))
    pcolor_cf(cprof.labels[0], cprof.labels[1], cf, title=title + ' - cloud fraction')
    nice.savefig('cf_%s_2008_%s.png' % (layer, period))
    
    cfzonal = 100. * cprof.sum(axis='lon') / nprof.sum(axis='lon')
    zonal(cprof.labels[1], cfzonal, title=title + ' - cloud fraction')
    #plt.clim(0,100)


def main(layer='high', period='jja'):
    
    import glob
    
    months = {'jja':[6,7,8], 'djf':[12,1,2]}
    
    files = []
    base = 'out.daily/2008%02d/*nc4'
    for month in months[period]:
        x = glob.glob(base % month)
        files.extend(x)
    assert len(files) > 0
    show_files(files, layer, '2008 - ' + layer + ' - '+ period, period)
    
    plt.show()
    

if __name__ == '__main__':
    import plac
    plac.call(main)
