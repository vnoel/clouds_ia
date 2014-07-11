#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel Thu Apr 24 17:07:38 2014

import numpy as np
import calipso.level2 as calipso_l2
import dimarray as da

# altitude vector
vcm_alt = np.r_[0:19.5:0.03]
nalt = vcm_alt.shape[0]

# averaging levels to include
havgs_vcm = [5, 20, 80]


def vcm_from_layers(nl, base, top, havg, ltype, tropo, only_havg=None):
    
    nprof = base.shape[0]
    vcm = np.zeros([nprof, nalt], dtype='int8')
    
    # clean up unwanted layers first
    
    basecopy = base.copy()
    
    # for clouds, feature type == layer_type == 2
    basecopy[ltype != 2] = -9999.
    # keep only requested havg
    if only_havg is not None:
        basecopy[havg != only_havg] = -9999.

    tropo += 1.
    # remove layer that overlap with stratosphere
    for i in xrange(nprof):
        for j in xrange(nl[i]):
            if top[i,j] > (tropo[i]):
                basecopy[i,j] = -9999.
    
    for i in xrange(nprof):
        for j in xrange(nl[i]):
            if basecopy[i,j] < 0:
                continue
            idx = (vcm_alt >= basecopy[i,j]) & (vcm_alt < top[i,j])
            vcm[i, idx] = 1
    
    del basecopy
    
    return vcm
    

def vcm_dataset_from_l2_orbit(filename):
    
    #print 'Creating vcm dataset from l2 file ' + filename
    
    l2 = calipso_l2.Cal2(filename)
    lon, lat = l2.coords()
    tai_time = l2.time()
    nl, base, top = l2.layers()
    havg = l2.horizontal_averaging()
    ltype = l2.layer_type()
    tai_time_min, tai_time_max = l2.time_bounds()
    tropo = l2.tropopause_height()
    l2.close()
    
    tropo[lat < -60] = 11.
    tropo[lat > 60] = 11.
    
    dset = da.Dataset()
    
    time_axis = ('tai_time', tai_time)
    alt_axis = ('altitude', vcm_alt)
    
    for havg_vcm in havgs_vcm:
        vcm = vcm_from_layers(nl, base, top, havg, ltype, tropo, only_havg=havg_vcm)
        vcm_name = 'cal%02d' % (havg_vcm)
        dset[vcm_name] = da.DimArray(vcm, (time_axis, alt_axis))
    
    dset['lon'] = da.DimArray(lon, (time_axis,))
    dset['lat'] = da.DimArray(lat, (time_axis,))
    dset['time_min'] = da.DimArray(tai_time_min, (time_axis,))
    dset['time_max'] = da.DimArray(tai_time_max, (time_axis,))

    return dset
    
    
def vcm_file_from_l2_orbit(filename, where='./'):
    
    import os
    
    vcm = vcm_dataset_from_l2_orbit(filename)
    
    # check if where exists, fix it if not
    if not os.path.isdir(where):
        print 'Creating dir ' + where
        os.mkdir(where)
    vcm.write_nc(where + 'cal5_test_' + os.path.basename(filename[:-4]) + '.nc4', mode='w')
    
    
# test functions
# to run tests : py.test orbit_vcm.py
    
def test_vcm_nprof():
    
    import calipso_local
    import glob
    
    out = './test.out'
    
    l2files = calipso_local.l2_night_files(2009,1,1)
    vcm = vcm_dataset_from_l2_orbit(l2files[0])
    nprof = vcm['lon'].shape[0]
    assert nprof > 0
    assert vcm['cal05'].shape[0] == nprof
    print vcm['cal05'].ix[0,:]
    assert np.all(np.isfinite(vcm['cal05'][:,:]))
    
    
def test_vcm_creation_for_a_day():
    
    import calipso_local
    import glob
    
    out = './test.out/'
    
    l2files = calipso_local.l2_night_files(2008,1,1)
    assert l2files != []
    
    for l2file in l2files:
        vcm_file_from_l2_orbit(l2file, where=out)
    
    outfiles = glob.glob(out + 'cal5_test*.nc4')

    assert len(outfiles)==len(l2files)
    
    
def main(l2file):
    
    vcm_file_from_l2_orbit(l2file, where='./')


if __name__ == '__main__':
    import plac
    plac.call(main)