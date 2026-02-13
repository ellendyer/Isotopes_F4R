# %% [markdown]
# ## Read in TROPESS

# %%
import sys
import os
import numpy as np
import xarray as xr
import pandas as pd
import datetime

import matplotlib as mpl
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')


# %%
xls = []
arr = os.listdir('/Users/ellendyer/Documents/GitHub/Isotopes_F4R/forward/central_test/')
print(arr)
for I,F in enumerate(arr):
    print(F)
    x = xr.open_dataset('/Users/ellendyer/Documents/GitHub/Isotopes_F4R/forward/central_test/'+F,
                        engine="netcdf4",
                        drop_variables=['x_h2o_col_p_error','x_h2o_col_p','dd_004','dd_col_p',
                                        'dd_col_p_error','datetime_utc','datetime_utc_dim', 
                                        'altitude','level','target_idx','target_id','year_fraction'])
    
    x = x.rename({'latitude':'lat','longitude':'lon','x_h2o':'H2O','x':'ratio'})
    x = x.assign_coords({'level':x.level})
    x = x.assign_coords({'time':x.time})
    x = x.assign_coords({"target": pd.MultiIndex.from_arrays(
        [x.time.values, x.lat.values, x.lon.values],
        names=["time", "lon", "lat"])}).unstack("target")
    xls.append(x)
    x.close()
print(xls)

# %%
#targets = []
#for i in range(0,len(xls)):
#    #print(xls[i].target.values)
#    if i==0:
#        targets=xls[i].target.data.tolist()
#    else:
#        targets = targets + xls[i].target.data.tolist() 
##print(targets)
#print("len targets", len(targets))
#print("len set", len(set(targets)))

#ds = xr.concat(xls,dim='time',data_vars="all")
print('before combine')
ds = xr.combine_by_coords(xls)
print('after combine')
#ds = xr.combine_nested(xls,concat_dim=["time"])
#ds = xr.merge(xls)
print(ds)

# %%

ds = ds.assign_coords({"target": pd.MultiIndex.from_arrays(
    [ds.time.values, ds.lat.values, ds.lon.values],
    names=["time", "lon", "lat"])}).unstack("target")
ds = ds.transpose("time", "level", "lon", "lat")

# %%
lon_meshgrid, lat_meshgrid = np.meshgrid(ds.lon.values, ds.lat.values, indexing='ij')

ds_out = xr.Dataset(
    data_vars=dict(
    ratio=(["time","level","x","y"], ds.ratio.data),
    H2O=(["time","level","x","y"], ds.H2O.data),
    
),
    coords=dict(
    time=(["time"], ds.time.data),
    level=(["level"], ds.level.data),
    lon=(["x","y"], lon_meshgrid),
    lat=(["x","y"], lat_meshgrid),
),
)

print(ds)

# %%
print(np.nanmax(ds.ratio.sel(level = 825,method='nearest').values))
print(np.nanmin(ds.ratio.sel(level = 825,method='nearest').values))

# %%
# calculate deltaD
R = ds.ratio
# use this RSMOW for molecules of water
Rvsmow = 3.11*10**(-4)
dD = (R/Rvsmow - 1)*1000.
ds['deltaD'] = dD

# %%
print(np.nanmax(ds.deltaD.sel(level = 825,method='nearest').values))
print(np.nanmin(ds.deltaD.sel(level = 825,method='nearest').values))

# %%
import cartopy.crs as ccrs
import cartopy.feature
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
ax.add_feature(cartopy.feature.OCEAN)
ds['deltaD'].mean('time').sel(level = 825,method='nearest').plot(ax=ax,transform=ccrs.PlateCarree(),
                                       add_colorbar=True,
                                       #vmin=0,vmax=2,
                                       alpha=1,
                                       cmap=plt.cm.RdBu,
                                       extend="both")

ax.set_extent([-20, 20, -20, 60])
#ax.set_extent([7, 32, -15, 12])
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='black', alpha=0.5, linestyle='dotted')
gl.top_labels = False
gl.right_labels = False
#ax.set_title()
#plt.savefig()
plt.show()
plt.clf()

# %%
cb_tropess = ds.where((ds.lat>-5)&(ds.lat<5)&(ds.lon>10)&(ds.lon<28), drop=True)

print(cb_tropess)

# %%

cb_tropess.to_netcdf(path='/Users/ellendyer/Documents/GitHub/Isotopes_F4R/iso_prepped/tropess_airs_cb.nc',mode='w',format='NETCDF4',engine='netcdf4')


