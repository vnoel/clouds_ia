#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-04-28

import dimarray as da
import matplotlib.pyplot as plt


def main(input='out/200901/vcm_2009-01-01T00-07-47ZN.nc4'):
    
    vcm = da.read_nc(input)
    vcm05 = vcm['vcm_05km']
    plt.pcolormesh(vcm05.labels[0], vcm05.labels[1], vcm05.values.T)
    plt.colorbar()
    plt.show()


if __name__ == '__main__':
    import plac
    plac.call(main)