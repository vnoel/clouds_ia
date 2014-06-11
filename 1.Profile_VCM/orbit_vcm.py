#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel Sat May 10 14:48:13 2014

import orbit_vcm_cal333
import orbit_vcm_cal5 
import orbit_vcm_csat
import dimarray as da
import calipso_local
import os
import numpy as np
import localpaths


def _find_orbit_id(cal_l2_file):
    '''
    finds identifiers for a calipso level 2 file
    '''
    
    orbit_id = cal_l2_file[-25:-4]
    year = int(cal_l2_file[-25:-21])
    month = int(cal_l2_file[-20:-18])
    day = int(cal_l2_file[-17:-15])
    
    return year, month, day, orbit_id    


def _find_cal5_file(year, month, day, orbit_id):
    '''
    find calipso level 2 5km file associated with an orbit identifier
    '''

    cal5file = calipso_local.l2_file_from_orbit(year, month, day, orbit_id)
    if cal5file is None:
        return None
    if os.path.isfile(cal5file):
        return cal5file
    else:
        return None    


def _find_geoprof_file(year, month, day, orbit_id):
    '''
    find geoprof file associated with a orbit identifier
    '''
    
    path = localpaths.caltrack_geoprof_dir[0] + '%04d/' % year
    folder = '%04d_%02d_%02d/' % (year, month, day)
    
    geofile = path + folder + 'CALTRACK-5km_CS-2B-GEOPROF_V1-00_' + orbit_id + '.hdf'
    
    if os.path.isfile(geofile):
        return geofile
    else:
        return None


def remap_profiles(values, n1, n2, nprof333):
    '''
    remap values on 333m profile indices
    '''
    
    out = np.zeros([nprof333, values.shape[1]], dtype='int8')
    for i in np.r_[0:values.shape[0]]:
        out[n1[i]:n2[i],:] = values[i,:]
    return out


def reindex_vcms(vcm, vcm5, vcmc):
    
    # vcmc can be None
    
    mintime5, maxtime5 = vcm5['time_min'].values, vcm5['time_max'].values
    
    nprof5 = mintime5.shape[0]
    time333 = vcm['cal333'].labels[0]
    
    # first find 333m profiles indexes for a given 5km profile
    n1, n2 = np.zeros(nprof5, 'int16'), np.zeros(nprof5, 'int16')
    n = 0
    for i in np.r_[0:nprof5]:
        n1[i] = n
        while time333[n] < maxtime5[i]:
            n += 1
        n2[i] = n-1

    # reindex all flags on the same 333m coordinates
    
    reindexed = da.Dataset()
    reindexed['lon'] = vcm['lon']
    reindexed['lat'] = vcm['lat']
    reindexed['cal333'] = vcm['cal333']
    
    # remap CALIPSO flag
    for vcm_name in 'cal05','cal20', 'cal80':
        this_vcm = remap_profiles(vcm5[vcm_name].values, n1, n2, time333.shape[0])
        reindexed[vcm_name] = da.DimArray(this_vcm, labels=vcm['cal333'].labels, dims=vcm['cal333'].dims)
    
    # remap cloudsat flag
    if vcmc is None:
        this_vcm = np.ones_like(reindexed['cal333'].values, 'int8') * -1.
    else:
        this_vcm = remap_profiles(vcmc.values, n1, n2, time333.shape[0])
    reindexed['csat'] = da.DimArray(this_vcm, labels=vcm['cal333'].labels, dims=vcm['cal333'].dims)
    
    # Now we have
    # cal333, cal05, cal20, cal80, csat in reindexed.
        
    return reindexed
    

def vcm_dataset_from_l2_orbits(cal333, cal5, csat, slow=False):
    '''
    create a vcm dataset containing cloud masks from calipso 333m, calipso 5km, and cloudsat data.
    '''
    
    # this function needs at least cal333 and cal5 to exist and contain valid data.
    # csat can be missing or contain invalid data, that's fine.
    
    if cal333 is None or cal5 is None:
        print 'Erreur - one or more input files missing'
        print 'cal 333 file : ', cal333
        print 'cal 5 file : ', cal5
        print 'csat file : ', csat
        return None
    
    vcm = orbit_vcm_cal333.vcm_dataset_from_l2_orbit(cal333)
    vcm5 = orbit_vcm_cal5.vcm_dataset_from_l2_orbit(cal5)

    if vcm is None or vcm5 is None:
        return None
    # make sure the 333m file has more profiles than the 5km one
    assert vcm['cal333'].shape[0] > (vcm5['cal05'].shape[0] * 10)    
    
    vcmc = orbit_vcm_csat.vcm_from_geoprof_file(csat, vcm['cal333'].labels[1])
    # here vcmc can be None if there is no file
    
    vcm = reindex_vcms(vcm, vcm5, vcmc)

    return vcm
    

def vcm_file_from_333_orbit(cal333_file, where='./'):
    '''
    saves a vcm dataset in a file containing cloud masks from calipso and cloudsat data,
    based on a calipso 333m orbit file.
    '''
    
    import os
    
    y, m, d, orbit_id = _find_orbit_id(cal333_file)
    geoprof_file = _find_geoprof_file(y, m, d, orbit_id)
    cal5_file = _find_cal5_file(y, m, d, orbit_id)

    vcm = vcm_dataset_from_l2_orbits(cal333_file, cal5_file, geoprof_file)
    if vcm is None:
        return
    
    outname = 'vcm_' + orbit_id + '.nc4'
    
    # check if path exists, fix it if not
    if not os.path.isdir(where):
        print 'Creating dir ' + where
        os.mkdir(where)

    vcm.write_nc(where + outname, mode='w', zlib=True, complevel=9)
    

# TESTS


def _test_files():

    from localpaths import hostname, icare_id, climserv_id

    if hostname.endswith(icare_id):
        print 'icare'
        cal333file = '/DATA/LIENS/CALIOP/333mCLay/2008/2008_01_01/CAL_LID_L2_333mCLay-ValStage1-V3-01.2008-01-01T01-30-23ZN.hdf'
        geofile = '/DATA/LIENS/CALIOP/CALTRACK-5km_CS-2B-GEOPROF/2008/2008_01_01/CALTRACK-5km_CS-2B-GEOPROF_V1-00_2008-01-01T01-30-23ZN.hdf'
        cal5file = '/DATA/LIENS/CALIOP/05kmCLay/2008/2008_01_01/CAL_LID_L2_05kmCLay-Prov-V3-01.2008-01-01T01-30-23ZN.hdf'
    elif hostname.endswith(climserv_id):
        print 'climserv'
        cal333file = '/homedata/noel/Data/333mCLay/2008/2008_01_01/CAL_LID_L2_333mCLay-ValStage1-V3-01.2008-01-01T01-30-23ZN.hdf'
        geofile = '/bdd/CFMIP/OBS_LOCAL/ATRAIN_COLOC/CLOUDSAT_COLOC/CALTRACK-GEOPROF/2008/2008_01_01/CALTRACK-5km_CS-2B-GEOPROF_V1-00_2008-01-01T01-30-23ZN.hdf'
        cal5file = '/bdd/CALIPSO/Lidar_L2/05kmCLay.v3.01/2008/2008_01_01/CAL_LID_L2_05kmCLay-Prov-V3-01.2008-01-01T01-30-23ZN.hdf'

    return cal333file, geofile, cal5file


def test_vcm_dataset():

    cal333file, geofile, cal5file = _test_files()
    vcm = vcm_dataset_from_l2_orbits(cal333file, cal5file, geofile)
    
    return vcm


def test_orbit_id():
    
    cal333file = 'CAL_LID_L2_333mCLay-ValStage1-V3-01.2008-01-01T01-30-23ZN.hdf'
    y, m, d, orbit_id = _find_orbit_id(cal333file)
    assert y==2008
    assert m==1
    assert d==1
    assert orbit_id=='2008-01-01T01-30-23ZN'


def test_find_geoprof_file():
    
    from localpaths import caltrack_geoprof_dir
    
    cal333file = 'CAL_LID_L2_333mCLay-ValStage1-V3-01.2008-01-01T01-30-23ZN.hdf'
    y, m, d, orbit_id = _find_orbit_id(cal333file)
    geofile = _find_geoprof_file(y, m, d, orbit_id)
    assert geofile == caltrack_geoprof_dir[0] + '2008/2008_01_01/CALTRACK-5km_CS-2B-GEOPROF_V1-00_2008-01-01T01-30-23ZN.hdf'


def test_find_cal5_file():
    
    from localpaths import l2dir
    
    cal333file = 'CAL_LID_L2_333mCLay-ValStage1-V3-01.2008-01-01T01-30-23ZN.hdf'
    y, m, d, orbit_id = _find_orbit_id(cal333file)
    cal5_file = _find_cal5_file(y, m, d, orbit_id)
    assert cal5_file == l2dir[2] + '/2008/2008_01_01/CAL_LID_L2_05kmCLay-Prov-V3-01.2008-01-01T01-30-23ZN.hdf'
    
    
def test_vcm_file_from_333_orbit():
    
    import os
    cal333file, _, _ = _test_files()
    assert os.path.isfile(cal333file)
    vcm_file_from_333_orbit(cal333file, where='./test.out/')
    assert os.path.isfile('./test.out/vcm_2008-01-01T01-30-23ZN.nc4')
    
def test_vcm_file_from_333_orbit_without_csat():
    
    import os
    cal333file = '/DATA/LIENS/CALIOP/333mCLay/2011/2011_05_01/CAL_LID_L2_333mCLay-ValStage1-V3-01.2011-05-01T14-53-38ZN.hdf'
    y, m, d, orbit_id = _find_orbit_id(cal333file)
    cal5file = _find_cal5_file(y, m, d, orbit_id)
    geofile = _find_geoprof_file(y, m, d, orbit_id)
    assert geofile is None
    vcm = vcm_dataset_from_l2_orbits(cal333file, cal5file, geofile)
    assert vcm['vcm_csat'].ix[0,0] == -9999.
    