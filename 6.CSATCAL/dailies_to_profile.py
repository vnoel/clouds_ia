#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-07-15

import dimarray as da
import numpy as np
import matplotlib.pyplot as plt

lats = {'tropics':[0,30], 'midlat':[30,60], 'polar':[60,90]}

def profile_plot(cprofl, altitude):
    
    plt.figure(figsize=[5,9])
    for l in cprofl:
        plt.plot(cprofl[l], altitude, label=l, lw=0.5)
    plt.xlabel('Cloudsat-only cloud fraction')
    plt.ylabel('Altitude [km]')
    plt.legend()
    plt.show()


def gather(mask):
    import glob
    
    flist = glob.glob(mask)
    for f in flist:
        print f
        dset = da.read_nc(f, ['csat', 'lat', 'cloudpts'])
        csat = dset['csat'].values
        lat = dset['lat'].values
        altitude = dset['csat'].altitude
        idx = (dset['cloudpts'].values > 0)
        del dset
        cpts = dict()
        nprof = dict()
        for l in lats:
            idx1 = np.where((lat >= lats[l][0]) & (lat < lats[l][1]))[0]
            idx2 = np.where((lat >= -lats[l][1]) & (lat < -lats[l][0]))[0]
            idx = np.concatenate([idx1, idx2])
            if l in cpts:
                nprof[l] = nprof[l] + idx.shape[0]
                cpts[l] = cpts[l] + np.take(csat, idx, axis=0).sum(axis=0)
            else:
                nprof[l] = np.sum(idx)
                cpts[l] = np.take(csat, idx, axis=0).sum(axis=0)
    cprofl = dict()
    for l in lats:
        cprofl[l] = 100. * cpts[l] / nprof[l]
        
    return cprofl, altitude
        

def main(mask='out/200607/*nc4'):
    
    cprofl, altitude = gather(mask)
    profile_plot(cprofl, altitude)
    


if __name__ == '__main__':
    import plac
    plac.call(main)