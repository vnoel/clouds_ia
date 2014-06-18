#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-04-28

import dimarray as da
import matplotlib.pyplot as plt


def plot_vcm(vcm,field):
    va = vcm[field]
    plt.pcolormesh(va.labels[0][3000:5000], va.labels[1], va.values[3000:5000,:].T, cmap=plt.cm.gray_r)
    plt.title(field)
    plt.savefig('test.png')

    
def plot_vcms(vcm):
    
    i = 1
    print vcm
    
    for field in vcm:
        print field
        if field.startswith('cal') or field.startswith('csat'):
            print 'plotting'
            plt.subplot(3, 2, i)
            plot_vcm(vcm, field)
            i += 1
            

def main(input='test.out/200801/vcm_2008-01-01T01-30-23ZN.nc4'):
    
    fig = plt.figure(figsize=[12,12])
    vcm = da.read_nc(input)
    plot_vcms(vcm)
    plt.show()


if __name__ == '__main__':
    import plac
    plac.call(main)