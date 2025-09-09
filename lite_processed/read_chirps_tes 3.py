import sys
import os
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import pickle

# read in tes netcdf
tes_ds = xr.open_dataset('./all_tes_cb.nc')

## read in chirps netcdf
#lat1,lat2 = -5,5
#lon1,lon2 = 10,30
#Y1=1981
#Y2=2020
#for Y in range(Y1,Y2+1):
#  pr_daily_in = xr.open_dataset("/Volumes/passport_ellen/chirps_daily/chirps-v2.0."+str(Y)+".days_p05.nc")['precip']
#  pr_daily_in = pr_daily_in.rename({'latitude':'lat'})
#  pr_daily_in = pr_daily_in.rename({'longitude':'lon'})
#  pr_daily_in = pr_daily_in.sel(lat=slice(lat1,lat2),
#                                lon=slice(lon1,lon2))
#  pr_daily_in = pr_daily_in.interp(lat=np.arange(lat1,lat2+1,1), 
#                lon=np.arange(lon1,lon2+1,1),method='linear')
#  if Y == Y1:
#    chirps_df = pr_daily_in
#  else:
#    chirps_df = xr.concat([chirps_df, pr_daily_in], 'time')
#  del pr_daily_in
#
#sfile = open('file_out.pkl','wb')
#pickle.dump(chirps_df,sfile,protocol=pickle.HIGHEST_PROTOCOL)

f = open('file_out.pkl', 'rb')
chirps_df = pickle.load(f)

#chirps_ts = chirps_df.where(chirps_df > 0,drop=True)
#chirps_times = chirps_ts.time.values
#
##tes_sel = tes_ds.where(tes_ds.date==chirps_times,drop=True)
#tes_sel = tes_ds.sel(timedatum = np.in1d( tes_ds['date'], chirps_times))
#tes_sel = tes_sel.dropna(dim='timedatum',how='all')

#tes sel - select pressure 
tes_sel = tes_ds.where((tes_ds.pressure <= 850.) & (tes_ds.pressure >= 500.))

print(tes_sel.pressure.values)
#print(tes_sel.date.values)
#print(tes_sel.timedatum.values)
#print(tes_sel.HDO[:,5].values)

#plt.scatter(tes_sel['lon'][:], tes_sel['lat'][:], c=tes_sel['HDO'][:,5], s=5)
#plt.show()
#plt.clf()

# write out dataset to netcdf
tes_sel.to_netcdf(path='./sel_tes_cb.nc',mode='w',format='NETCDF4',engine='netcdf4')


