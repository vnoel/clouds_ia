#!/usr/bin/env python
#encoding:utf-8

# Forked by VNoel on 2014-06-02

import numpy as np
import dimarray as da

latstep = 0.01
latbins = np.r_[-82:82+latstep:latstep]
nlat = latbins.shape[0]

vcm_names = 'cal333', 'cal333+cal05', 'cal333+cal05+cal20', 'cal333+cal05+cal20+cal80', 'cal333+cal05+cal20+cal80+csat'


def combine_vcms(origin, target_name):
    
    if '+' not in target_name:
        output = origin[target_name]
    else:
        
        names = target_name.split('+')
        if not all(name in origin for name in names):
            print 'Warning : some vcms are not present in file. Contained data :'
            print origin
            return None        
        output = origin[names[0]]
        for name in names[1:]:
            output += origin[name]
        # FIXME : need to check cloudsat data here
        np.clip(output, -1, 1, out=output.values)
    return output
    

def ctop_from_vcm_orbit(vcm_orbit):
        
    # read data
    data = da.read_nc(vcm_orbit)
    if data is None:
        return None
        
    plat = data['lat'].values
    altitude = data[vcm_names[0]].labels[1]
    
    # only keep cloud tops > 10 km, for fun
    ialt = (altitude > 10)
    
    out = da.Dataset()
    
    # vector with nprof indexes containing bin numbers
    ilatbins = np.digitize(plat, latbins)

    for name in vcm_names:
        
        this_vcm = combine_vcms(data, name)
        this_vcm = this_vcm.values
        
        cloudtopsum = np.zeros([nlat])
        nclouds = np.zeros([nlat], dtype='uint16')
        nprof = np.zeros([nlat], dtype='uint16')
        
        for i, ilatbin in enumerate(ilatbins):
            if 'nprof' not in out:
                nprof[ilatbin] += 1
            if np.sum(this_vcm[i,ialt]) > 0:
                nclouds[ilatbin] += 1
                cloudtopsum[ilatbin] += np.max(altitude * this_vcm[i,:])
        
        if 'nprof' not in out:
            out['nprof'] = da.DimArray(nprof, labels=[latbins,], dims=['lat',])
        out[name+'_ctopsum'] = da.DimArray(cloudtopsum, labels=[latbins,], dims=['lat',])
        out[name+'_nclouds'] = da.DimArray(nclouds, labels=[latbins,], dims=['lat',])
                    
    return out


def ctop_file_from_vcm_orbits(vcm_orbits, outname, where='./out'):
    
    import os
    
    dataset = None
    for vcm_orbit in vcm_orbits:
        out = ctop_from_vcm_orbit(vcm_orbit)
        if out is None:
            return
        if dataset is None:
            dataset = out
            fields = dataset.keys()
        else:
            for field in fields:
                dataset[field] += out[field]
        
    if not os.path.isdir(where):
        print 'Creating dir ' + where
        os.mkdir(where)
    dataset.write_nc(where + outname, mode='w', zlib=True, complevel=9)


def test_orbits():
    
    import glob, os

    vcm_orbits = glob.glob('./in/200701/vcm_2007-01-01*.nc4')
    assert len(vcm_orbits) > 1

    ctop_file_from_vcm_orbits(vcm_orbits[0:1], 'ctop_zonal_2007-01-01.nc4', where='./test.out/')
    
    assert os.path.isfile('./test.out/ctop_zonal_2007-01-01.nc4')
