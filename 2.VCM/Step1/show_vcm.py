#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-04-28

import dimarray as da
import matplotlib.pyplot as plt


def main(input='test.out/200701/vcm_2007-01-01T00-22-49ZN.nc4'):
    
    fig = plt.figure(figsize=[12,12])
    vcm = da.read_nc(input)
    i = 1
    for field in vcm:
        if field.startswith('vcm'):
            plt.subplot(3, 2, i)
            va = vcm[field]
            plt.pcolormesh(va.labels[0], va.labels[1], va.values.T, cmap=plt.cm.gray_r)
            plt.title(field)
            i += 1
    plt.show()


if __name__ == '__main__':
    import plac
    plac.call(main)