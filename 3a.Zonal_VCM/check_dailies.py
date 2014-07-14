#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-07-07

import glob
import dimarray as da

def main(mask='out/200607/*.nc4'):

    print mask
    files = glob.glob(mask)
    print len(files)

    for f in files:
        d = da.read_nc(f)
        print f
        for n in 'cal333+cal05+cal20+cal80+csat_cprof', 'cal333+cal05+cal20+cal80_cprof':
            cf = 100. * d[n].sum() / d['nprof'].sum()
            print '    ', n, d['nprof'].sum(), d[n].sum(), cf
    
    

if __name__ == '__main__':
    import plac
    plac.call(main)