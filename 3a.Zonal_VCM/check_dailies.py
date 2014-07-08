#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-07-07

import glob
import dimarray as da

def main(mask = 'out/200912/*nc4'):

    files = glob.glob(mask)

    for f in files:
        d = da.read_nc(f)
        cf = 100. * d['cal333+cal05+cal20+cal80+csat_cprof'].sum() / d['nprof'].sum()
        print f, d['nprof'].sum(), d['cal333+cal05+cal20+cal80+csat_cprof'].sum(), cf
    
    

if __name__ == '__main__':
    import plac
    plac.call(main)