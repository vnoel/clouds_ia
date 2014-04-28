#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-04-28

import dimarray as da
import matplotlib.pyplot as plt


def main(input='out/200901/vcm_2009-01-01T00-07-47ZN.nc4'):
    
    vcm = da.read_nc(input)
    i = 1
    for field in vcm:
        if field.startswith('vcm'):
            plt.subplot(4, 1, i)
            va = vcm[field]
            plt.pcolormesh(va.labels[0], va.labels[1], va.values.T)
            plt.title(field)
            i += 1
    plt.show()


if __name__ == '__main__':
    import plac
    plac.call(main)