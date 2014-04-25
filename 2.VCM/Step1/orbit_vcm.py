#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel Thu Apr 24 17:07:38 2014

import numpy as np
import calipso_l2
import dimarray as da

vcm_alt = np.r_[0:22.3:0.3]


def vcm_from_layers(nl, base, top, havg, ltype, only_havg=None):
    # FIXME
    pass

    # for clouds, feature type == layer_type == 2



def vcm_dataset_from_l2_orbit(filename):
    
    print 'Creating vcm dataset from l2 file ' + filename
    
    l2 = calipso_l2.Cal2(filename)
    lon, lat = l2.coords()
    tai_time = l2.time()
    nl, base, top = l2.layers()
    havg = l2.horizontal_averaging()
    ltype = l2.layer_type()
    
    havgs_vcm = [5, 20, 80]
    vertical_cloud_masks = da.Dataset()
    
    time_axis = ('tai_time', tai_time)
    alt_axis = ('altitude', vcm_alt)
    
    for havg_vcm in havgs_vcm:
        vcm = vcm_from_layers(nl, base, top, havg, ltype, only_havg=havg_vcm)
        vcm_name = 'vcm_' + '%02d' % (havg_vcm)
        vertical_cloud_masks[vcm_name] = da.DimArray(vcm, (time_axis, alt_axis))
    
    vertical_cloud_masks['lon'] = da.DimArray(lon, (time_axis,))
    vertical_cloud_masks['lat'] = da.DimArray(lat, (time_axis,))

    outname = 'vcm_' + l2.orbit + '.nc4'
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
    
def test_vcm_creation_for_a_day():
    
    import calipso_local
    import glob
    
    out = './test.out/'
    
    l2files = calipso_local.l2_night_files(2009,1,1)
    assert l2files != []
    
    for l2file in l2files:
        vcm_file_from_l2_orbit(l2file, where=out)
    
    outfiles = glob.glob(out + '/*.nc4')
    assert len(outfiles)==len(l2files)
    
    
def main(l2file):
    
    vcm_file_from_l2_orbit(l2file, where='./')


if __name__ == '__main__':
    import plac
    plac.call(main)