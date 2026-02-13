import sys
import os
import numpy as np
import h5py
import xarray as xr
import pandas as pd

import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Open file.
#FILE_NAME = './data/TES-Aura_L2-HDO-Nadir_2010-03_v007_Lite-v02.00.nc'
#arr = os.listdir('./data/')
arr = os.listdir('/Volumes/passport_ellen/lite_006/063100509211111/')
for I,F in enumerate(arr):
  #print(F)
  #FILE_NAME = './data/'+F
  FILE_NAME = '/Volumes/passport_ellen/lite_006/063100509211111/'+F
  #DATAFIELD_NAME = 'Retrieval/HDO_H2O'
  DATAFIELD_NAME = 'Species'
  with h5py.File(FILE_NAME, mode='r') as f:
   # Read dataset.
   dset = f[DATAFIELD_NAME]
   data = dset[:]
  
   # Handle fill value.
   data[data == dset.fillvalue] = np.nan
   data = np.ma.masked_where(np.isnan(data), data)
   # hdo is stored in first 17 levels and h2o next 17
   hdo = data[:,0:17]
   h2o = data[:,17:]
  
   # Get the geolocation data
   gridt = f['Grid_Targets'][:]
   gridp = np.arange(0,17)
   lat = f['Latitude'][:]
   lon = f['Longitude'][:]
   daynight = f['DayNightFlag'][:]
   time = f['Time'][:]
   pressurei = f['Pressure'][:]
   # mask for pressures that are negative
   pressurei[pressurei < 0.0] = np.nan
   pressurei = np.ma.masked_where(np.isnan(pressurei), pressurei)
   # only need one set of pressures to work with both hdo and h2o
   pressure = pressurei[:,0:17]
#   # quality flag only in v007
#   quality = f['Quality'][:]
#
#   # quality flag only in v007
#   # mask bad quality columns (bad=0)
#   hdo[quality==0,:] = np.nan
#   hdo = np.ma.masked_where(np.isnan(hdo), hdo)
#   h2o[quality==0,:] = np.nan
#   h2o = np.ma.masked_where(np.isnan(h2o), h2o)
#   pressure[quality==0,:] = np.nan
#   pressure = np.ma.masked_where(np.isnan(pressure), pressure)
#   lat[quality==0] = np.nan
#   lat = np.ma.masked_where(np.isnan(lat), lat)
#   lon[quality==0] = np.nan
#   lon = np.ma.masked_where(np.isnan(lon), lon)
   # mask night time columns (night=0)
   hdo[daynight==0,:] = np.nan
   hdo = np.ma.masked_where(np.isnan(hdo), hdo)
   h2o[daynight==0,:] = np.nan
   h2o = np.ma.masked_where(np.isnan(h2o), h2o)
   pressure[daynight==0,:] = np.nan
   pressure = np.ma.masked_where(np.isnan(pressure), pressure)
   lat[daynight==0] = np.nan
   lat = np.ma.masked_where(np.isnan(lat), lat)
   lon[daynight==0] = np.nan
   lon = np.ma.masked_where(np.isnan(lon), lon)

   # calculate deltaD
   R = hdo/h2o
   # use this RSMOW for molecules of water
   Rvsmow = 3.11*10**(-4)
   dD = (R/Rvsmow - 1)*1000.

   # Time is second from TAI93.
   # See 4-25 of "TES Science Data Processing Standard and Special Observation
   # Data Products Specification" [1].
   timebase = datetime.datetime(1993, 1, 1, 0, 0, 0)
   timedatum = []
   for i,t in enumerate(time):
     delta = datetime.timedelta(days=time[i]/86400.0)
     timedatum.append(timebase + delta)
  
##-- test scatter plot with TES input data
#   m = Basemap(projection='cyl', resolution='l',
#               llcrnrlat=-90, urcrnrlat=90,
#               llcrnrlon=-180, urcrnrlon=180)
#   m.drawcoastlines(linewidth=0.5)
#   m.drawparallels(np.arange(-90, 91, 45))
#   m.drawmeridians(np.arange(-180, 180, 45), labels=[True,False,False,True])
#   m.scatter(lon, lat, c=hdo[:,5], s=5, cmap=plt.cm.jet,
#           edgecolors=None, linewidth=0)
#   cb = m.colorbar()
#   fig = plt.gcf()
#   plt.show()

  
   lat = xr.DataArray(lat, coords=[timedatum], dims=["timedatum"])
   lon = xr.DataArray(lon, coords=[timedatum], dims=["timedatum"])
   hdo = xr.DataArray(hdo, coords=[timedatum,gridp], dims=["timedatum", "gridp"])
   h2o = xr.DataArray(h2o, coords=[timedatum,gridp], dims=["timedatum", "gridp"])
   dD = xr.DataArray(dD, coords=[timedatum,gridp], dims=["timedatum", "gridp"])
   pressure = xr.DataArray(pressure, coords=[timedatum,gridp], dims=["timedatum", "gridp"])
   ds = xr.Dataset({'lat':lat,'lon':lon,'HDO':hdo, 'H2O':h2o, 'deltaD':dD, 'pressure':pressure})
   # create a date for each measurement rounded to the day for comp with other data
   ds['date'] = ds["timedatum"].dt.floor("D")
 
   ds = ds.where(ds!=-999.)

   if I == 0:
     tes_ds = ds
   else:
     tes_ds = xr.concat([tes_ds, ds], dim="timedatum")

# organise dataset data by the dateitime timedatum stamps
tes_ds = tes_ds.sortby(tes_ds['timedatum'])
# select basic congo basin region
tes_ds = tes_ds.where((tes_ds.lat < 5.) & (tes_ds.lat > -5.),drop=True)
tes_ds = tes_ds.where((tes_ds.lon < 30.) & (tes_ds.lon > 10.),drop=True)

# write out dataset to netcdf
tes_ds.to_netcdf(path='/Users/ellendyer/Documents/GitHub/Isotopes_F4R/iso_prepped/all_tes_cb.nc',mode='w',format='NETCDF4',engine='netcdf4')

## read in netcdf for test plot
#tes_ds = xr.open_dataset('./all_tes_cb.nc')

##---------------------
#plt.scatter(tes_ds['lon'][:], tes_ds['lat'][:], c=tes_ds['HDO'][:,5], s=5)
#plt.show()
#plt.clf()
#
#tes_ds = tes_ds.where((tes_ds.lat < 5.) & (tes_ds.lat > -5.),drop=True)
#tes_ds = tes_ds.where((tes_ds.lon < 30.) & (tes_ds.lon > 10.),drop=True)
#plt.scatter(tes_ds['lon'][:], tes_ds['lat'][:], c=tes_ds['HDO'][:,5], s=5)
#plt.show()
#plt.clf()

