#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel Thu Apr 24 17:07:38 2014

import numpy as np
import calipso_l2
import dimarray as da

# altitude vector
vcm_alt = np.r_[0:22.3:0.3]
nalt = vcm_alt.shape[0]

# averaging levels to include
havgs_vcm = [5, 20, 80]


def vcm_from_layers(nl, base, top, havg, ltype, only_havg=None):
    
    nprof = base.shape[0]
    vcm = np.zeros([nprof, nalt], dtype='uint8')
    
    # clean up unwanted layers first
    
    # for clouds, feature type == layer_type == 2
    base[ltype != 2] = -9999.
    # keep only requested havg
    if only_havg is not None:
        base[havg != only_havg] = -9999.
    
    for i in xrange(nprof):
        
        if nl[i] == 0:
            continue
        
        for j in xrange(nl[i]):
            
            if base[i,j] < 0:
                continue

            idx = (vcm_alt >= base[i,j]) & (vcm_alt < top[i,j])
            vcm[i, idx] = 1
    
    return vcm
    

def vcm_dataset_from_l2_orbit(filename):
    
    print 'Creating vcm dataset from l2 file ' + filename
    
    l2 = calipso_l2.Cal2(filename)
    lon, lat = l2.coords()
    tai_time = l2.time()
    nl, base, top = l2.layers()
    havg = l2.horizontal_averaging()
    ltype = l2.layer_type()
    
    vertical_cloud_masks = da.Dataset()
    
    time_axis = ('tai_time', tai_time)
    alt_axis = ('altitude', vcm_alt)
    
    for havg_vcm in havgs_vcm:
        vcm = vcm_from_layers(nl, base, top, havg, ltype, only_havg=havg_vcm)
        vcm_name = 'vcm_%02dkm' % (havg_vcm)
        vertical_cloud_masks[vcm_name] = da.DimArray(vcm, (time_axis, alt_axis))
    
    vertical_cloud_masks['lon'] = da.DimArray(lon, (time_axis,))
    vertical_cloud_masks['lat'] = da.DimArray(lat, (time_axis,))

    outname = 'vcm_' + l2.id + '.nc4'
    return vertical_cloud_masks, outname
    
    
def vcm_file_from_l2_orbit(filename, where='./'):
    
    import os
    
    vcm, outname = vcm_dataset_from_l2_orbit(filename)
    # check if where exists, fix it if not
    if not os.path.isdir(where):
        print 'Creating dir ' + where
        os.mkdir(where)
    vcm.write_nc(where + outname, mode='w')
    
    
# test functions
# to run tests : py.test orbit_vcm.py
    
def test_vcm_nprof():
    
    import calipso_local
    import glob
    
    out = './test.out'
    
    l2files = calipso_local.l2_night_files(2009,1,1)
    vcm, outname = vcm_dataset_from_l2_orbit(l2files[0])
    # assert vcm['altitude'].shape[0] == vcm_alt.shape[0]
    nprof = vcm['lon'].shape[0]
    assert nprof > 0
    assert vcm['vcm_05km'].shape[0] == nprof
    print vcm['vcm_05km'].ix[0,:]
    assert np.all(np.isfinite(vcm['vcm_05km'][:,:]))
    
    
def test_vcm_creation_for_a_day():
    
    import calipso_local
    import glob
    
    out = './test.out/'
    
    l2files = calipso_local.l2_night_files(2009,1,1)
    assert l2files != []
    
    for l2file in l2files:
        vcm_file_from_l2_orbit(l2file, where=out)
    
    outfiles = glob.glob(out + '*.nc4')

    assert len(outfiles)==len(l2files)
    
    
def main(l2file):
    
    vcm_file_from_l2_orbit(l2file, where='./')


if __name__ == '__main__':
    import plac
    plac.call(main)