# subset the EMDNA according to lat/lon extent
import xarray as xr
import numpy as np
import pandas as pd
import os, sys

def generate_filelist(path, year, ens, suffix):
    num = ens[1] - ens[0] + 3 # include _mean and _spread
    filelist = [' '] * num
    for e in range(ens[0], ens[1]+1):
        filelist[e-1] = f'{path}/EMDNA_{year}.{e:03}{suffix}.nc4'
    filelist[-2] = f'{path}/EMDNA_{year}_mean{suffix}.nc4'
    filelist[-1] = f'{path}/EMDNA_{year}_spread{suffix}.nc4'
    return filelist

def read_EMDNA(file):
    with xr.open_dataset(file) as ds0:
        ds = ds0.copy()
        ds.coords['x'] = ds.longitude
        ds.coords['y'] = ds.latitude
        year = int(ds.date[0]/10000)
        ds.coords['time'] = pd.date_range(start=f'{year}-01-01', end=f'{year}-12-31', freq='1D')
    return ds


########################################################################################################################
# subsetting parameters

# parent path of EMDNA
emdna_path = '/project/rpp-kshook/Model_Output/ClimateForcingData/EMDNA/Estimate'
OI_path = '/project/rpp-kshook/Model_Output/ClimateForcingData/EMDNA/OI'

# outpath for saving the subset data
suffix = '.subset' # user defined suffix of output files
subset_path = '/scratch-deleted-2021-mar-20/gut428/test' # path where output files are written

# time period, region, and members
yearrange = [1979, 1979] # within [1979, 2018]
latrange = [27.8, 40.7] # within [5, 85]
lonrange = [-95.5, -86] # within [-180, -50]
ensrange = [1, 3] # within [1, 100]

# target variables: should be a subset of ['prcp','tmean','trange']
varout = ['prcp','tmean']

########################################################################################################################
# start extracting subsets
if not os.path.isdir(subset_path):
    os.mkdir(subset_path)

# extract probabilistic estimates
for year in range(yearrange[0], yearrange[1]+1):
    # input file list
    pathy_in = emdna_path + '/' + str(year)
    filelist_in = generate_filelist(pathy_in, year, ensrange, '')
    # output file list
    pathy_out = subset_path + '/' + str(year)
    if not os.path.isdir(pathy_out):
        os.mkdir(pathy_out)
    filelist_out = generate_filelist(pathy_out, year, ensrange, suffix)
    for filein, fileout in zip(filelist_in, filelist_out):
        # print information
        print('-'*100)
        print('InFile:',filein)
        print('OutFile:', fileout)
        if os.path.isfile(fileout):
            print('Outfile exists. Continue ...')
            continue
        # read raw EMDNA data
        datain = read_EMDNA(filein)
        # extract subset region
        dataout = datain.sel(y=slice(latrange[1], latrange[0]), x=slice(lonrange[0], lonrange[1]))
        # write data
        dataout = dataout[varout]
        encoding = {}
        for key in dataout.keys():
            encoding[key] = {'zlib': True, 'complevel': 5}
        dataout.to_netcdf(fileout, encoding=encoding)
        del dataout, datain

# extract deterministic outputs estimates
pathy_out = subset_path + '/EMDNA_deterministic'
if not os.path.isdir(pathy_out):
    os.mkdir(pathy_out)

for year in range(yearrange[0], yearrange[1]+1):
    filein = OI_path + '/OI_' + str(year) + '.nc4'
    fileout = pathy_out + '/OI_' + str(year) + '.nc4'
    # print information
    print('-' * 100)
    print('InFile:',filein)
    print('OutFile:', fileout)
    if os.path.isfile(fileout):
        print('Outfile exists. Continue ...')
        continue
    # read raw EMDNA data
    datain = read_EMDNA(filein)
    # extract subset region
    dataout = datain.sel(y=slice(latrange[1], latrange[0]), x=slice(lonrange[0], lonrange[1]))
    # write data
    dataout = dataout[varout]
    encoding = {}
    for key in dataout.keys():
        encoding[key] = {'zlib': True, 'complevel': 5}
    dataout.to_netcdf(fileout, encoding=encoding)
    del dataout, datain


