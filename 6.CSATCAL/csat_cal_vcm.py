#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel on 2014-07-15

import vcm
import dimarray as da
import numpy as np

def check_out_dir(where):
    import os
    if not os.path.isdir(where):
        print 'Creating ' + where
        os.mkdir(where)

def csat_no_cal(files, outname, where):
    
    v = vcm.VCM(files, verbose=False)
    cal = v.get_vcm('cal333+cal05+cal20+cal80')
    csat = v.get_vcm('csat')
    
    calcloudy = np.sum(cal, axis=1)    
    csatcloudy = np.sum(csat, axis=1)
    
    csatonly = np.where((csatcloudy > 0) & (calcloudy == 0))[0]
    print 100. * csatonly.shape[0] / calcloudy.shape[0]
    
    vcm_csatonly = np.zeros_like(csat)
    vcm_csatonly[csatonly,:] = csat[csatonly,:]
    csatcloudy[calcloudy > 0] = 0
    
    dset = da.Dataset()
    time_axis = da.Axis(v.time, 'tai_time')
    alt_axis = da.Axis(v.altitude, 'altitude')
    dset['lon'] = da.DimArray(v.lon, [time_axis])
    dset['lat'] = da.DimArray(v.lat, [time_axis])
    dset['csat'] = da.DimArray(vcm_csatonly, [time_axis, alt_axis]) 
    dset['cloudpts'] = da.DimArray(csatcloudy, [time_axis])
    
    check_out_dir(where)
    
    dset.write_nc(where + outname, 'w', zlib=True, complevel=9)
