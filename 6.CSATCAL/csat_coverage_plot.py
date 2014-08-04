#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-07-16

import numpy as np
import matplotlib.pyplot as plt

def main(datafile='csat_coverage.npz'):
    
    npz = np.load(datafile)
    dates = npz['dates']
    coverage = npz['coverage']
    coverage = np.ma.masked_where(coverage < 0, coverage)
    
    plt.figure(figsize=[12,4])
    plt.plot(dates, coverage, lw=0.5)
    plt.yticks(np.r_[0:120:20])
    plt.ylim(0, 110)
    plt.grid()

    plt.ylabel('Coverage [%]')
    plt.title('CloudSAT coverage in dataset')
    
    plt.show()
    


if __name__ == '__main__':
    import plac
    plac.call(main)