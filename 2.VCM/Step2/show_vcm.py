#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-04-28

import dimarray as da
import matplotlib.pyplot as plt

def main(input='out/vcm_lat_2009-01-15T05-17-43ZN.nc4'):
    
    data = da.read_nc(input)
    vcm05 = data['vcm_05km']
    vcm_lonlat = vcm05.sum(axis='altitude')
    
    plt.figure()
    plt.pcolormesh(vcm05.labels[0], vcm05.labels[1], vcm_lonlat.values.T)
    plt.colorbar()
    plt.show()
    


if __name__ == '__main__':
    import plac
    plac.call(main)