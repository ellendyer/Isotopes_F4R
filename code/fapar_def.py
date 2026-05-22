import sys
import xarray as xr
import numpy as np
from matplotlib import pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature
import geopandas as gpd
from shapely.geometry import mapping
from scipy.stats import spearmanr, pearsonr
import ts_onset_cess as ocd
import pandas as pd
import datetime

def fapar_read():
    fpl = []
    #Know the year range being analysed (could scrape the date from the filename but this is easier)
    #Loop through possible times and "try"
    #Know that there are three files per month
    for Y in range(2014,2025):
        for M in range(1,13):
            for D in [10,20,28,29,30,31]:
                try: 
                    if Y < 2020:
                        fname = '/Volumes/ESA_F4R/clms/clms_fapar_300m_v1_10daily/fapar300/central_africa/c_gls_FAPAR300_'+str(Y)+str("{:02d}".format(M))+str(D)+'0000_GLOBE_PROBAV_V1.0.1_central_africa.nc' 
                        fp = xr.open_mfdataset(fname)['FAPAR']
                        #assign a datetime value to each xarray based on the date in the filename
                        fp = fp.assign_coords({"time":datetime.datetime(Y,M,D)})
                    elif Y > 2020:
                        fname = '/Volumes/ESA_F4R/clms/clms_fapar_300m_v1_10daily/fapar300rt6/central_africa/c_gls_FAPAR300-RT6_'+str(Y)+str("{:02d}".format(M))+str(D)+'0000_GLOBE_OLCI_V1.1.2_central_africa.nc'
                        fp = xr.open_mfdataset(fname)['FAPAR']
                    else:
                        if M < 9:
                            fname = '/Volumes/ESA_F4R/clms/clms_fapar_300m_v1_10daily/fapar300/central_africa/c_gls_FAPAR300_'+str(Y)+str("{:02d}".format(M))+str(D)+'0000_GLOBE_PROBAV_V1.0.1_central_africa.nc' 
                            fp = xr.open_mfdataset(fname)['FAPAR']
                            fp = fp.assign_coords({"time":datetime.datetime(Y,M,D)})
                        if M > 8:
                            fname = '/Volumes/ESA_F4R/clms/clms_fapar_300m_v1_10daily/fapar300rt6/central_africa/c_gls_FAPAR300-RT6_'+str(Y)+str("{:02d}".format(M))+str(D)+'0000_GLOBE_OLCI_V1.1.2_central_africa.nc'
                            fp = xr.open_mfdataset(fname)['FAPAR']
                    fp = fp.sortby("lat", ascending=True)
                    fp = fp.sel(lat=slice(-15,12),lon=slice(8,31))
                    #append each xarray to a list
                    fpl.append(fp)
                except:
                    pass
    #concatenate all xarrays in list to one single dataarray
    fpt = xr.concat(fpl,dim='time')
    fpt = fpt.sortby('time')

    return fpt