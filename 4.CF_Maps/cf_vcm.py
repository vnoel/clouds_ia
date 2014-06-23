#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-04-28

import numpy as np
import dimarray as da

vcm_names = ['cal333+cal05+cal20+cal80+csat']


def combine_vcms(origin, target_name, output_so_far=None):
    
    if '+' not in target_name:
        output = origin[target_name]
    else:
        names = target_name.split('+')
        if not all(name in origin for name in names):
            print 'Warning : some vcms are not present in file. Contained data :'
            print origin
            return None        
            
        # check if we are not simply adding a vcm to a sum already present
        if output_so_far is not None:
            previous_step = '+'.join(names[:-1])
            if previous_step in output_so_far:
                print previous_step + ' already cached'
                output = output_so_far[previous_step].values + origin[names[-1]]
                return output

        output = origin[names[0]].values
        for name in names[1:]:
            output += origin[name].values
        # FIXME : need to check cloudsat data here
        np.clip(output, -1, 1, out=output)

    return output


def cf_from_vcm_orbit(vcm_orbit, altrange, lstep=2.):
    
    # create vcm_3d grid
    lonbins = np.r_[-180:180+lstep:lstep]
    latbins = np.r_[-90:90+lstep:lstep]
    nlon, nlat = lonbins.shape[0]-1, latbins.shape[0]-1
    
    # read data
    data = da.read_nc(vcm_orbit)
    plon = data['lon'].values.astype('float32')
    plat = data['lat'].values.astype('float32')
        
    altitude = data['cal333'].labels[1]
    altidx = (altitude >= altrange[0]) & (altitude < altrange[1])
    
    out = da.Dataset()

    # number of profiles in grid
    h, xx, yy = np.histogram2d(plon, plat, bins=(lonbins, latbins))
    out['nprof'] = da.DimArray(h, labels=[lonbins[:-1], latbins[:-1]], dims=['lon', 'lat'])
    out['nprof'].longname = 'Number of measured profiles'

    for vcm_name in vcm_names:
        
        # number of cloudy profiles in grid and altitude range

        this_vcm = combine_vcms(data, vcm_name)
        assert this_vcm is not None
        
        vcm_slice = this_vcm[:, altidx]
        cloudy_profile = np.sum(vcm_slice, axis=1)
        np.clip(cloudy_profile, 0, 1, out=cloudy_profile)
        
        h, xx, yy = np.histogram2d(plon, plat, bins=(lonbins, latbins), weights=cloudy_profile)
        outname = vcm_name + '_cprof'
        out[outname] = da.DimArray(h, labels=[lonbins[:-1], latbins[:-1]], dims=['lon', 'lat'])
        out[outname].longname = 'Number of cloudy profiles from cloud mask = ' + vcm_name
    
    return out


def cf_file_from_vcm_orbit(vcm_orbit, where='./out/'):
    
    import os
    
    dataset = cf_from_vcm_orbit(vcm_orbit)
    
    outname = 'cf_' + vcm_orbit[-25:]
    if not os.path.isdir(where):
        print 'Creating dir ' + where
        os.mkdir(where)
    dataset.write_nc(where + outname, mode='w', zlib=True, complevel=9)


def cf_file_from_vcm_orbits(vcm_orbits, altrange, outname, where='./out'):
    
    import os
    
    dataset = None
    for vcm_orbit in vcm_orbits:
        out = cf_from_vcm_orbit(vcm_orbit, altrange)
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
    
    print('Saving ' + where + outname)
    dataset.altrange = '{:f} - {:f}'.format(altrange[0], altrange[1])
    dataset.write_nc(where + outname, mode='w', zlib=True, complevel=9)


def test_orbits():
    
    import glob, os

    vcm_orbits = glob.glob('./in/200701/vcm_2007-01-01*.nc4')
    assert len(vcm_orbits) > 1

    cf_file_from_vcm_orbits(vcm_orbits, 'cf_2007-01-01.nc4', where='./test.out/')
    
    assert os.path.isfile('./test.out/cf_2007-01-01.nc4')
