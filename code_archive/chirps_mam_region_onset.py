#%%
import sys
import xarray as xr
import numpy as np
from matplotlib import pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature
import geopandas as gpd
from shapely.geometry import mapping
from scipy.stats import spearmanr, pearsonr
import onset_cess_defs as ocd
import pandas as pd

#%%

Y1=2004
Y2=2015

prp = xr.open_mfdataset('/Volumes/blue_wd/chirps_daily/chirps-v2.0.*.days_p05.nc')['precip']
prp = prp.rename({'latitude':'lat','longitude':'lon'})
print(prp)
prp = prp.sel(lat=slice(-5,5),lon=slice(10,30),time=slice(str(Y1)+'-01-01',str(Y2)+'-12-31'))
prp = prp.mean(dim=('lat','lon'))

prp.plot()
plt.show()
plt.clf()

#%%
# #Create mask of relatively important (high mean) MAM rainfall
mam = prp.sel(time=np.in1d(prp['time.month'], [3,4,5])).mean('time')
jjas = prp.sel(time=np.in1d(prp['time.month'], [6,7,8,9])).mean('time')
ond = prp.sel(time=np.in1d(prp['time.month'], [10,11,12])).mean('time')
son = prp.sel(time=np.in1d(prp['time.month'], [9,10,11])).mean('time')
ondjjas = prp.sel(time=np.in1d(prp['time.month'], [6,7,8,9,10,11,12])).mean('time')
prp_mam = prp.where((mam>jjas) & (mam>ond),drop=True)
mam_seas_contour = prp_mam.mean('time')*0.0+1.0
#mam_seas_contour.to_netcdf('./dataf/chirps_mam_seas_contour.nc')
#mam_seas_contour = xr.open_dataset('./dataf/chirps_mam_seas_contour.nc')['precip']


#%%
## #Plot region where mam is greater than jjas and ond mean rainfall
## #Overlay with Kenya counties shapes
#data = gpd.read_file('/Users/ellendyer/Library/Mobile Documents/com~apple~CloudDocs/1SHARED_WORK/Work/shapefiles/kenyan-counties/County.shp')
#ax = plt.axes(projection=ccrs.PlateCarree())
#ax.coastlines()
#ax.add_feature(cartopy.feature.BORDERS)
#ax.add_feature(cartopy.feature.RIVERS)
#gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
#                  linewidth=1, color='black', alpha=0.5, linestyle='dotted')
#gl.top_labels = False
#gl.right_labels = False
#
#cmap = plt.get_cmap('cividis_r').copy()
#cmap.set_extremes(over='blue')
#cmap.set_extremes(under='orange')
#prp_mam.mean('time').plot(ax=ax,transform=ccrs.PlateCarree(),cmap=cmap,vmin=1,vmax=4,extend='both')
##data.plot(ax=ax, edgecolor='orange', facecolor='none',lw=2,zorder=2,linestyle='-')
#plt.title('MAM as main season compared to OND and JJAS')
#plt.savefig('./chirps_plots/mam_seas_contour.png',bbox_inches='tight',dpi=200)
#plt.show()
#plt.clf()

#%%
##Plot Kenya MAM using rio clip
#mam_ke = mam.rio.clip(data.geometry.apply(mapping),data.crs)
#ax = plt.axes(projection=ccrs.PlateCarree())
#ax.coastlines()
#ax.add_feature(cartopy.feature.BORDERS)
#ax.add_feature(cartopy.feature.RIVERS)
#gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
#                  linewidth=1, color='black', alpha=0.5, linestyle='dotted')
#gl.top_labels = False
#gl.right_labels = False
#mam_ke.plot(ax=ax,transform=ccrs.PlateCarree())
#plt.show()
#plt.clf()
#
##%%
##Create mam correlation map using degree of correlation between
##seasonal mean MAM in Kenya and the rest of GHA MAM rainfall
#data = gpd.read_file('/Users/ellendyer/Library/Mobile Documents/com~apple~CloudDocs/1SHARED_WORK/Work/shapefiles/kenyan-counties/County.shp')
#mam_ts = prp.sel(time=np.in1d(prp['time.month'], [3,4,5]))
#mam_ke_ts = mam_ts.rio.clip(data.geometry.apply(mapping),data.crs)
##mam_ke_ts = mam_ts.sel(lat=slice(0,5),lon=slice(12,20))
#mam_ke_ts = mam_ke_ts.mean(dim=('lat','lon')).groupby('time.year').mean('time')
#mam_map_ts = mam_ts.groupby('time.year').mean('time')
#print(mam_map_ts)
#print(mam_ke_ts)
## 2D array first
#correl, pvalue = np.apply_along_axis(spearmanr,0,mam_map_ts,mam_ke_ts)
#corrs = xr.DataArray(correl, coords=[mam_map_ts.lat.values, mam_map_ts.lon.values], \
#                      dims=['lat', 'lon']) #making xarray
#pvals = xr.DataArray(pvalue, coords=[mam_map_ts.lat.values, mam_map_ts.lon.values], \
#                      dims=['lat', 'lon']) #making xarray
#sig_p=corrs.where((pvals < 0.10) & (np.abs(corrs) > 0.4))#, drop=True)
##sig_p=corrs.where((pvals < 0.10), drop=True)
#
#mam_corr_contour = sig_p*0.0+1.0
## mam_corr_contour.to_netcdf('./dataf/chirps_mam_corr_contour.nc')
## mam_corr_contour = xr.open_dataset('./dataf/chirps_mam_corr_contour.nc')['__xarray_dataarray_variable__']
#
#ax = plt.axes(projection=ccrs.PlateCarree())
#ax.coastlines()
#ax.add_feature(cartopy.feature.BORDERS)
#ax.add_feature(cartopy.feature.RIVERS)
#gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
#                  linewidth=1, color='black', alpha=0.5, linestyle='dotted')
#gl.top_labels = False
#gl.right_labels = False
#sig_p.plot(ax=ax,transform=ccrs.PlateCarree(),vmin=0.4,vmax=1.0,extend='both',cmap=plt.cm.magma_r)
#plt.title('MAM Kenya regional correl (seasonal)')
#plt.savefig('./chirps_plots/mam_corr_contour.png',bbox_inches='tight',dpi=200)
#plt.show()
#plt.clf()

#%%
#Calculate seasonal onset and cessations for full dataset
#can mask regionally first
power_ratio,on1,ce1,on2,ce2,on3,ce3,on1_years,ce1_years,on2_years,ce2_years,on3_years,ce3_years = ocd.xarray_on_cess(prp)
power_ratio.to_netcdf('./onsetf/pr.nc')
on1.to_netcdf('./onsetf/chirps/on1.nc')
on2.to_netcdf('./onsetf/chirps/on2.nc')
on3.to_netcdf('./onsetf/chirps/on3.nc')
ce1.to_netcdf('./onsetf/chirps/ce1.nc')
ce2.to_netcdf('./onsetf/chirps/ce2.nc')
ce3.to_netcdf('./onsetf/chirps/ce3.nc')
on1_years.to_netcdf('./onsetf/chirps/on1_years.nc')
on2_years.to_netcdf('./onsetf/chirps/on2_years.nc')
on3_years.to_netcdf('./onsetf/chirps/on3_years.nc')
ce1_years.to_netcdf('./onsetf/chirps/ce1_years.nc')
ce2_years.to_netcdf('./onsetf/chirps/ce2_years.nc')
ce3_years.to_netcdf('./onsetf/chirps/ce3_years.nc')

ce1_years = xr.open_dataset('./onsetf/chirps/ce1_years.nc')['precip']
on1_years = xr.open_dataset('./onsetf/chirps/on1_years.nc')['precip']
power_ratio = xr.open_dataset('./onsetf/chirps/pr.nc')['precip']

sys.exit()

#%%
# #Plot first season onset dates
# #Overlay with mam seasonal def contour and mam correlation def contour
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
ax.add_feature(cartopy.feature.BORDERS)
ax.add_feature(cartopy.feature.RIVERS)
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='black', 
                  alpha=0.5, linestyle='dotted')
gl.top_labels = False
gl.right_labels = False
cmap = plt.cm.get_cmap("viridis").copy()
im = on1_years.mean('year').plot.pcolormesh(ax=ax,extend='neither',
                                            cmap=cmap,
                                            vmin=60,vmax=130,
                                            transform=ccrs.PlateCarree(),
                                            add_colorbar=False)
im.cmap.set_over("white")
cb = plt.colorbar(im)
cb.set_ticks(np.arange(60,130,20))
cb.set_ticklabels(pd.to_datetime(np.arange(60,130,20), \
          unit='D').strftime('%d-%b'))
mam_corr_contour.where(mam_corr_contour==1.,0.).plot.contour(ax=ax,
                        levels=[0],colors=['red'],alpha=1,
                        linewidths=1,transform=ccrs.PlateCarree())
# mam_seas_contour.where(mam_seas_contour==1.,0.).plot.contour(ax=ax,
#                         levels=[0],colors=['orange'],alpha=1,
#                         linewidths=1,transform=ccrs.PlateCarree())
plt.title('MAM mean onset')
plt.savefig('./chirps_plots/on1_mam_mean_onset.png',bbox_inches='tight',dpi=200)
plt.show()
plt.clf()

#%%
# #Plot the power ratio of the region
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
ax.add_feature(cartopy.feature.BORDERS)
ax.add_feature(cartopy.feature.RIVERS)
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='black', alpha=0.5, 
                  linestyle='dotted')
gl.top_labels = False
gl.right_labels = False
im = power_ratio.plot.pcolormesh(vmin=0,vmax=2,levels=3,
                                 extend='both',add_colorbar=False)
cb = plt.colorbar(im)
cb.set_ticks([0,1,2])
plt.title('Power ratio')
plt.savefig('./chirps_plots/power_ratio.png',bbox_inches='tight',dpi=200)
plt.show()
plt.clf()

#%%
# To capture failed seasons (according to algorithm) replace nan onset with 
# the latest onset date for that grid point
on1_years_c = on1_years.fillna(on1_years.max(dim='year'))
# print(on1_years.mean(dim='year'))
# cmap = plt.get_cmap('viridis').copy()
# cmap.set_extremes(under='pink', over='pink')
# on1_years.mean(dim='year').plot.pcolormesh(cmap=cmap,vmin=30,vmax=120)
# plt.show()
# plt.clf()

# Select and create MAM seasonal avgs for same years as onset
prp_mam_agg = prp.sel(time=np.in1d(prp['time.month'], 
                        [3,4,5])).groupby('time.year').mean('time')[1:]
# Loop through correlation calculation for each grid point
# between onset and mean rainfall
# fillna only for pearson
# on1_years = on1_years.fillna(0.0)
# prp_mam_agg = prp_mam_agg.fillna(0.0)
co_agg = np.empty(np.shape(prp_mam_agg[0,:,:]))
pv_agg = np.empty(np.shape(prp_mam_agg[0,:,:]))
for i,iv in enumerate(prp_mam_agg.lat):
    for j,jv in enumerate(prp_mam_agg.lon):
        co_agg[i,j],pv_agg[i,j] = spearmanr(prp_mam_agg.sel(lat=iv,lon=jv),
                                            on1_years_c.sel(lat=iv,lon=jv),
                                            nan_policy='omit')
# Put correl and pvalue back into xarrays
co_agg = xr.DataArray(co_agg, coords=[prp_mam_agg.lat.values, 
                                      prp_mam_agg.lon.values],
                              dims=['lat', 'lon'])
pv_agg = xr.DataArray(pv_agg, coords=[prp_mam_agg.lat.values, 
                                      prp_mam_agg.lon.values],
                              dims=['lat', 'lon'])
# Mask correlations for stat sig 95% and for where there is an onset
# that means there isn't really a MAM season (onset later than day 120)
# or last day of April
sig_p = co_agg.where((pv_agg < 0.05), drop=True)
sig_p = sig_p.where(on1_years.mean(dim='year') < 120)
print('regional mean: r=',sig_p.mean(dim=('lat','lon')).values)
print('regional min: r=',sig_p.min(dim=('lat','lon')).values)
print('regional max: r=',sig_p.max(dim=('lat','lon')).values)

ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
ax.add_feature(cartopy.feature.BORDERS)
ax.add_feature(cartopy.feature.RIVERS)
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='black', alpha=0.5, 
                  linestyle='dotted')
gl.top_labels = False
gl.right_labels = False
cmap = plt.get_cmap('plasma').copy()
cmap.set_extremes(over='green')
im = sig_p.plot.pcolormesh(cmap=cmap,extend='both',vmin=-1.0,vmax=-0.4)
# mam_corr_contour.where(mam_corr_contour==1.,0.).plot.contour(ax=ax,
#                         levels=[0],colors=['blue'],alpha=1,linestyles='-',
#                         linewidths=1,transform=ccrs.PlateCarree())
# mam_seas_contour.where(mam_seas_contour==1.,0.).plot.contour(ax=ax,
#                         levels=[0],colors=['lime'],alpha=1,linestyles='dotted',
#                         linewidths=2,transform=ccrs.PlateCarree())
plt.title('Correlation between MAM \n onset and seasonal rainfall')
plt.savefig('./chirps_plots/on1_mam_pr_correl_spearman.png',bbox_inches='tight',dpi=200)
plt.show()
plt.clf()

#%%
# To capture failed seasons (according to algorithm) replace nan cessation  with 
# the earliest cessation date for that grid point
ce1_years_c = ce1_years.fillna(ce1_years.min(dim='year'))

# Select and create MAM seasonal avgs for same years as onset
prp_mam_agg = prp.sel(time=np.in1d(prp['time.month'], 
                        [3,4,5])).groupby('time.year').mean('time')[1:]
# Loop through correlation calculation for each grid point
# between onset and mean rainfall
# fillna only for pearson
# on1_years = on1_years.fillna(0.0)
# prp_mam_agg = prp_mam_agg.fillna(0.0)
co_agg = np.empty(np.shape(prp_mam_agg[0,:,:]))
pv_agg = np.empty(np.shape(prp_mam_agg[0,:,:]))
for i,iv in enumerate(prp_mam_agg.lat):
    for j,jv in enumerate(prp_mam_agg.lon):
        co_agg[i,j],pv_agg[i,j] = spearmanr(prp_mam_agg.sel(lat=iv,lon=jv),
                                            ce1_years_c.sel(lat=iv,lon=jv),
                                            nan_policy='propagate')
# Put correl and pvalue back into xarrays
co_agg = xr.DataArray(co_agg, coords=[prp_mam_agg.lat.values, 
                                      prp_mam_agg.lon.values],
                              dims=['lat', 'lon'])
pv_agg = xr.DataArray(pv_agg, coords=[prp_mam_agg.lat.values, 
                                      prp_mam_agg.lon.values],
                              dims=['lat', 'lon'])
# Mask correlations for stat sig 95% and for where there is an cessation
# that means there isn't really a MAM season (cessation before than day 90)
# or approx first day of April
sig_p = co_agg.where((pv_agg < 0.05), drop=True)
sig_p = sig_p.where(ce1_years.mean(dim='year') > 90)
print('regional mean: r=',sig_p.mean(dim=('lat','lon')).values)
print('regional min: r=',sig_p.min(dim=('lat','lon')).values)
print('regional max: r=',sig_p.max(dim=('lat','lon')).values)

ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
ax.add_feature(cartopy.feature.BORDERS)
ax.add_feature(cartopy.feature.RIVERS)
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='black', alpha=0.5, 
                  linestyle='dotted')
gl.top_labels = False
gl.right_labels = False
cmap = plt.get_cmap('plasma_r').copy()
cmap.set_extremes(under='green')
im = sig_p.plot.pcolormesh(cmap=cmap,extend='both',vmin=0.4,vmax=1.0)
# mam_corr_contour.where(mam_corr_contour==1.,0.).plot.contour(ax=ax,
#                         levels=[0],colors=['lime'],alpha=1,linestyles='-',
#                         linewidths=1,transform=ccrs.PlateCarree())
# mam_seas_contour.where(mam_seas_contour==1.,0.).plot.contour(ax=ax,
#                         levels=[0],colors=['lime'],alpha=1,linestyles='dotted',
#                         linewidths=2,transform=ccrs.PlateCarree())
plt.title('Correlation between MAM \n cessation and seasonal rainfall')
plt.savefig('./chirps_plots/ce1_mam_pr_correl_spearman.png',bbox_inches='tight',dpi=200)
plt.show()
plt.clf()


#%%
# Correlate Kenya mean onset  
# To capture failed seasons (according to algorithm) replace nan onset with 
# the latest onset date for that grid point and filter the region
on1_years = on1_years.fillna(on1_years.max(dim='year'))
on1_filter = on1_years.where(on1_years.mean(dim='year') < 120)
# Clip for a Kenya region
on1_ke = on1_filter.rio.clip(data.geometry.apply(mapping),data.crs)
prp_mam_ke = prp.sel(time=np.in1d(prp['time.month'], 
  [3,4,5])).groupby('time.year').mean('time')[1:].rio.clip(data.geometry.apply(mapping),data.crs)
# on1_ke.mean(dim='year').plot.pcolormesh(cmap=cmap,vmin=30,vmax=120)
# plt.show()
# plt.clf()
on1_ke_avg = on1_ke.mean(dim=('lat','lon'))
prp_ke_avg = prp_mam_ke.mean(dim=('lat','lon'))

on1_ke_rank = on1_ke_avg.sortby(on1_ke_avg)
prp_ke_rank = prp_ke_avg.reindex(year=on1_ke_rank.year)

prp_ond_ke = prp.sel(time=np.in1d(prp['time.month'], 
  [10,11,12])).groupby('time.year').mean('time')[:-1].rio.clip(data.geometry.apply(mapping),data.crs)
prp_ond_avg = prp_ond_ke.mean(dim=('lat','lon'))
prp_ond_rank = prp_ond_avg.reindex(year=on1_ke_rank.year.values-1)
print(spearmanr(prp_ke_avg,on1_ke_avg))
print(spearmanr(prp_ond_rank,on1_ke_rank))
print(spearmanr(prp_ond_avg,prp_ke_avg))
print(spearmanr(prp_ond_rank,prp_ke_rank))

plt.plot(on1_ke_rank.values/10.,label='onset')
plt.plot(prp_ke_rank.values,label='rain MAM')
plt.plot(prp_ond_rank.values,label='rain OND')
plt.legend()
plt.show()
plt.clf()

#%%
#Create mam correlation map using degree of correlation between
#MAM onset in Kenya and the rest of GHA MAM rainfall
data = gpd.read_file('/Users/ellendyer/Library/Mobile Documents/com~apple~CloudDocs/1SHARED_WORK/Work/shapefiles/kenyan-counties/County.shp')
mam_ts = on1_years
mam_ke_ts = mam_ts.rio.clip(data.geometry.apply(mapping),data.crs)
#mam_ke_ts = mam_ts.sel(lat=slice(5,8),lon=slice(38,45))
mam_ke_ts = mam_ke_ts.mean(dim=('lat','lon'))
mam_map_ts = mam_ts
print(mam_map_ts)
print(mam_ke_ts)
# 2D array first
correl, pvalue = np.apply_along_axis(spearmanr,0,mam_map_ts,mam_ke_ts)
corrs = xr.DataArray(correl, coords=[mam_map_ts.lat.values, mam_map_ts.lon.values], \
                      dims=['lat', 'lon']) #making xarray
pvals = xr.DataArray(pvalue, coords=[mam_map_ts.lat.values, mam_map_ts.lon.values], \
                      dims=['lat', 'lon']) #making xarray
sig_p=corrs.where((pvals < 0.10) & (np.abs(corrs) > 0.4))#, drop=True)
#sig_p=corrs.where((pvals < 0.10), drop=True)

ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
ax.add_feature(cartopy.feature.BORDERS)
ax.add_feature(cartopy.feature.RIVERS)
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='black', alpha=0.5, linestyle='dotted')
gl.top_labels = False
gl.right_labels = False
cmap = plt.get_cmap('magma_r').copy()
cmap.set_extremes(under='green')
sig_p.plot(ax=ax,transform=ccrs.PlateCarree(),vmin=0.4,vmax=1.0,extend='both',cmap=cmap)
plt.title('MAM onset Kenya regional correl (seasonal)')
plt.savefig('./chirps_plots/mam_onset_corr_contour.png',bbox_inches='tight',dpi=200)
plt.show()
plt.clf()


#%%
#Create mam correlation map using degree of correlation between
# MAM cessation in Kenya and the rest of GHA MAM rainfall
data = gpd.read_file('/Users/ellendyer/Library/Mobile Documents/com~apple~CloudDocs/1SHARED_WORK/Work/shapefiles/kenyan-counties/County.shp')
mam_ts = ce1_years
mam_ke_ts = mam_ts.rio.clip(data.geometry.apply(mapping),data.crs)
mam_ke_ts = mam_ke_ts.mean(dim=('lat','lon'))
mam_map_ts = mam_ts
print(mam_map_ts)
print(mam_ke_ts)
# 2D array first
correl, pvalue = np.apply_along_axis(spearmanr,0,mam_map_ts,mam_ke_ts)
corrs = xr.DataArray(correl, coords=[mam_map_ts.lat.values, mam_map_ts.lon.values], \
                      dims=['lat', 'lon']) #making xarray
pvals = xr.DataArray(pvalue, coords=[mam_map_ts.lat.values, mam_map_ts.lon.values], \
                      dims=['lat', 'lon']) #making xarray
sig_p=corrs.where((pvals < 0.10) & (np.abs(corrs) > 0.4))#, drop=True)
#sig_p=corrs.where((pvals < 0.10), drop=True)

ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
ax.add_feature(cartopy.feature.BORDERS)
ax.add_feature(cartopy.feature.RIVERS)
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='black', alpha=0.5, linestyle='dotted')
gl.top_labels = False
gl.right_labels = False
cmap = plt.get_cmap('magma_r').copy()
cmap.set_extremes(under='green')
sig_p.plot(ax=ax,transform=ccrs.PlateCarree(),vmin=0.4,vmax=1.0,extend='both',cmap=cmap)
plt.title('MAM cessation Kenya regional correl (seasonal)')
plt.savefig('./chirps_plots/mam_cess_corr_contour.png',bbox_inches='tight',dpi=200)
plt.show()
plt.clf()


