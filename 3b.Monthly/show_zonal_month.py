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
    ctop = tropic_width.cloud_cover_top(y, vcmarray, 0.05)
    latup, latdown, ceiling, height = tropic_width.tropic_width3(x, y, vcmarray)
    plt.axvline(x=latup, ls='--', color='w')
    plt.axvline(x=latdown, ls='--', color='w')
    plt.axhline(y=ceiling, ls='--')
    plt.axhline(y=height, ls='--')
    plt.plot(x, ctop, ls='--', color='w', alpha=0.5)


def cf_zonal(filename):
    
    data = da.read_nc(filename)
    print filename
    try:
        vcm_prof = data['cal333+cal05+cal20+cal80+csat']
        nprof = data['cal333+cal05+cal20+cal80+csat_cprof']
    except KeyError:
        return None, None, None
        
    cf_lat = 1. * vcm_prof.values.T / nprof.values
    cf_lat = cf_lat.T
    cf_lat = np.ma.masked_invalid(cf_lat)
    
    return vcm_prof.labels[0], vcm_prof.labels[1], cf_lat
    

def show_files(files, title):
    
    plt.figure(figsize=[12,12])
    
    for i, filename in enumerate(files):

        lat, alt, cf_lat = cf_zonal(filename)
        if cf_lat is None:
            continue
        plt.subplot(3,2,i+1)
        pcolor_zonal(lat, alt, cf_lat, filename.split('/')[-1])


def main(year, month):
    
    import glob
    
    year = int(year)
    month = int(month)
    mask = './out.40/%04d/vcm_zonal_%04d%02d*.nc4' % (year, year, month)
    
    grid_files = glob.glob(mask)
    assert len(grid_files) > 0  
    grid_files.sort()

    show_files(grid_files, 'bof')
    
    nice.savefig('zonal_cf_%04d%02d.png' % (year, month))
    plt.show()
    

if __name__ == '__main__':
    import plac
    plac.call(main)
