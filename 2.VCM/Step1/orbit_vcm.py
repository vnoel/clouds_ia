#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel Thu Apr 24 17:07:38 2014

import numpy as np
import calipso_local

vcm_alt = np.r_[0:22:0.3]


def vcm_from_layers():
    # FIXME
    pass


def vcm_dataset_from_l2_orbit(filename):
    
    l2 = Cal2(filename)
    lon, lat = l2.coords()
    tai_time = l2.time()
    nl, base, top = l2.layers()
    havg = l2.horizontal_averaging()
    # for clouds, feature type == layer_type == 2
    ltype = l2.layer_type()
    
    havgs_vcm = [5, 20, 80]
    vertical_cloud_masks = da.Dataset()
    
    for havg_vcm in havgs_vcm:
        vcm = vcm_from_layers(nl, base, top, havg, only_havg=havg_vcm)
        vcm_name = 'vcm_' + '%02d' % (havg_vcm)
        vertical_cloud_masks[vcn_name] = da.DimArray(vcm, axes=[('tai_time', tai_time), ('altitude', vcm_alt))
    
    vertical_cloud_masks['lon'] = da.DimArray(lon, axes=('tai_time', tai_time))
    vertical_cloud_masks['lat'] = da.DimArray(lat, axes=('tai_time', tai_time))

    outname = 'vcm_' + l2.orbit + '.nc4'
    return vertical_cloud_masks, outname
    
    
def vcm_file_from_l2_orbit(filename, where='./'):
    
    vcm, outname = vcm_dataset_from_l2_orbit(filename)
    # check if where exists, fix it if not
    vcm.write_nc(where + outname)
    
    
def main(l2file='bla'):
    
    vcm_file_from_l2_orbit(l2file, where='./')


if __name__ == '__main__':
    import plac
    plac.call(main)