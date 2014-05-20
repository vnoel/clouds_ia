#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel Sat May 10 14:48:13 2014

import orbit_vcm_333
import orbit_vcm_cal 
import orbit_vcm_csat
import dimarray as da
import calipso_local
import os


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
    if os.path.isfile(cal5file):
        return cal5file
    else:
        return None    


def _find_geoprof_file(year, month, day, orbit_id):
    '''
    find geoprof file associated with a orbit identifier
    '''
    
    path = '/bdd/CFMIP/OBS_LOCAL/ATRAIN_COLOC/CLOUDSAT_COLOC/CALTRACK-GEOPROF/%04d/' % year
    folder = '%04d_%02d_%02d/' % (year, month, day)
    
    geofile = path + folder + 'CALTRACK-5km_CS-2B-GEOPROF_V1-00_' + orbit_id + '.hdf'
    
    if os.path.isfile(geofile):
        return geofile
    else:
        return None

def combine_vcms_slow(vcm, vcm5, vcms):
    # this is nifty but very slow. It will be nicer to do things myself.
    
    for vcm_name in 'vcm_cal05', 'vcm_cal20', 'vcm_cal80':
        this = vcm5[vcm_name]
        vcm[vcm_name] = this.reindex_axis(vcm['vcm_cal333'].labels[0], method='nearest')
    
    vcm['vcm_csat'] = vcmc.reindex_axis(vcm['vcm_cal333'].labels[0], method='nearest')


def combine_vcms(vcm, vcm5, vcmc, mintime5, maxtime5):
    
    nprof5 = mintime5.shape[0]
    time333 = vcm.labels[0]
    
    # first find 333m profiles indexes for a given 5km profile
    n1, n2 = np.zeros(nprof5), np.zeros(nprof5)
    n = 0
    for i in np.r_[nprof5]:
        n1[i] = n
        while time333[n] < maxtime5[i]:
            n += 1
        n2[i] = n-1
    
    # remap CALIPSO flag
    for vcm_name in 'vcm_cal05', 'vcm_cal20', 'vcm_cal80':
        this_vcm = np.zeros_like(vcm['vcm_cal333'].values)
        for i in np.r_[nprof5]:
            this_vcm[n1[i]:n2[i],:] = vcm5[vcm_name].ix[i,:]
        vcm[vcm_name] = da.DimArray(this_vcm)
    
    # remap cloudsat flag
    this_vcm = np.zeros_like(vcmc.values)
    for i in np.r_[nprof5]:
        this_vcm[n1[i]:n2[i],:] = vcmc.ix[i,:]
    vcm['vcm_csat'] = vcmc
    
    return vcm
    
    

def vcm_dataset_from_l2_orbits(cal333, cal5, csat):
    '''
    create a vcm dataset containing cloud masks from calipso 333m, calipso 5km, and cloudsat data.
    '''
    
    print cal333
    vcm = orbit_vcm_333.vcm_dataset_from_l2_orbit(cal333)
    if vcm is None:
        return
    
    print cal5
    vcm5 = orbit_vcm_cal.vcm_dataset_from_l2_orbit(cal5)
    if vcm5 is None:
        return
    
    print csat
    vcmc = orbit_vcm_csat.vcm_from_geoprof_file(csat, vcm['vcm_cal333'].labels[1])
    if vcmc is None:
        return
    
    vcm = combine_vcms(vcm, vcm5, vcms)

    return vcm, 'paf'
    

def vcm_file_from_l2_orbit(cal333_file, where='./'):
    '''
    saves a vcm dataset in a file containing cloud masks from calipso and cloudsat data,
    based on a calipso 333m orbit file.
    '''
    
    import os
    
    y, m, d, orbit_id = _find_orbit_id(cal333_file)
    geoprof_file = _find_geoprof_file(y, m, d, orbit_id)
    cal5_file = _find_cal5_file(y, m, d, orbit_id)

    vcm, outname = vcm_dataset_from_l2_orbits(cal333_file, cal5_file, geoprof_file)    
    
    # check if path exists, fix it if not
    if not os.path.isdir(where):
        print 'Creating dir ' + where
        os.mkdir(where)

    vcm.write_nc(where + outname, mode='w', zlib=True, complevel=9)
    

# TESTS

def test_vcm_dataset():
    
    cal333file = '/homedata/noel/Data/333mCLay/2008/2008_01_01/CAL_LID_L2_333mCLay-ValStage1-V3-01.2008-01-01T01-30-23ZN.hdf'
    geofile = '/bdd/CFMIP/OBS_LOCAL/ATRAIN_COLOC/CLOUDSAT_COLOC/CALTRACK-GEOPROF/2008/2008_01_01/CALTRACK-5km_CS-2B-GEOPROF_V1-00_2008-01-01T01-30-23ZN.hdf'
    cal5_file = '/bdd/CALIPSO/Lidar_L2/05kmCLay.v3.01/2008/2008_01_01/CAL_LID_L2_05kmCLay-Prov-V3-01.2008-01-01T01-30-23ZN.hdf'
    
    vcm = vcm_dataset_from_l2_orbits(cal333file, cal5_file, geofile)
    
    print vcm
    assert False
    


def test_orbit_id():
    
    cal333file = 'CAL_LID_L2_333mCLay-ValStage1-V3-01.2008-01-01T01-30-23ZN.hdf'
    y, m, d, orbit_id = _find_orbit_id(cal333file)
    assert y==2008
    assert m==1
    assert d==1
    assert orbit_id=='2008-01-01T01-30-23ZN'


def test_find_geoprof_file():
    
    cal333file = 'CAL_LID_L2_333mCLay-ValStage1-V3-01.2008-01-01T01-30-23ZN.hdf'
    y, m, d, orbit_id = _find_orbit_id(cal333file)
    geofile = _find_geoprof_file(y, m, d, orbit_id)
    assert geofile == '/bdd/CFMIP/OBS_LOCAL/ATRAIN_COLOC/CLOUDSAT_COLOC/CALTRACK-GEOPROF/2008/2008_01_01/CALTRACK-5km_CS-2B-GEOPROF_V1-00_2008-01-01T01-30-23ZN.hdf'


def test_find_cal5_file():
    
    cal333file = 'CAL_LID_L2_333mCLay-ValStage1-V3-01.2008-01-01T01-30-23ZN.hdf'
    y, m, d, orbit_id = _find_orbit_id(cal333file)
    cal5_file = _find_cal5_file(y, m, d, orbit_id)
    assert cal5_file == '/bdd/CALIPSO/Lidar_L2/05kmCLay.v3.01/2008/2008_01_01/CAL_LID_L2_05kmCLay-Prov-V3-01.2008-01-01T01-30-23ZN.hdf'
    
    
#def test_vcm_file_from_l2_orbit():
#    
#    import os
#    
#    testpath = './test.out/'
#    calfile = '/bdd/CALIPSO/Lidar_L2/05kmCLay.v2.01/2007/2007_01_01/CAL_LID_L2_05kmCLay-Prov-V2-01.2007-01-01T00-22-49ZN.hdf'
#    vcm_file_from_l2_orbits(calfile, where=testpath)
#    assert os.path.isfile(testpath + 'vcm_2007-01-01T00-22-49ZN.nc4')