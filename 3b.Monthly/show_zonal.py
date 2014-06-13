#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-02

import numpy as np
import dimarray as da
import matplotlib.pyplot as plt
import tropic_width


def pcolor_zonal(x, y, vcmarray, title=None):

    plt.figure(figsize=[15,5])
    plt.contourf(x, y, vcmarray.T, np.r_[0:0.8:0.05])
    plt.colorbar()
    if title is not None:
        plt.title(title)
    plt.clim(0,0.8)
    plt.xlim(-82,82)
    plt.xticks(np.r_[-90:90+30:30])
    
    cover_top = tropic_width.cloud_cover_top(y, vcmarray)
    plt.plot(x, cover_top, lw=2, color='w', alpha=0.5)
    
    latup, latdown, ceiling, height = tropic_width.tropic_width3(x, y, vcmarray)
    plt.figure(figsize=[15,5])
    plt.plot(x, cover_top)
    plt.axvline(x=latup)
    plt.axvline(x=latdown)
    plt.axhline(y=ceiling)
    plt.axhline(y=height)
        
    print 'lat range, second method : ', latup, latdown
    

def show_file(input, title):
    
    data = da.read_nc(input)
    vcm_prof = data['cal333+cal05+cal20+cal80+csat']
    nprof = data['cal333+cal05+cal20+cal80+csat_cprof']
    
    cf_lat = 1. * vcm_prof.values.T / nprof.values
    cf_lat = cf_lat.T
    cf_lat = np.ma.masked_invalid(cf_lat)
    
    pcolor_zonal(vcm_prof.labels[0], vcm_prof.labels[1], cf_lat, 'Cloud fraction ' + title)


def main(input='./out/2007/vcm_zonal_200701.nc4'):
    
    show_file(input, '2007-01')    
    plt.show()
    

if __name__ == '__main__':
    import plac
    plac.call(main)
