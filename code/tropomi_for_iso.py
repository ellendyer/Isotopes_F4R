import os
import numpy as np
import matplotlib.pyplot as plt
import sys         
import xarray as xr
import NooneCurves as NC 
import pandas as pd
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import gc
import pickle

tlist = []
for Y in range(2018,2020):
    print('running year: ',str(Y))
    tin = xr.open_dataset("/Volumes/ESA_F4R/tropomi/merged/TROPOMI_merged_"+str(Y)+".nc")
    tlist.append(tin.where((tin.lat < 12.) & (tin.lat > 5.) & (tin.lon < 31.) & (tin.lon > 10.),drop=True).load())
    #tlist.append(tin.where((tin.lat < 5.) & (tin.lat > -5.) & (tin.lon < 29.) & (tin.lon > 8.),drop=True).load())
    #tlist.append(tin.where((tin.lat < -5.) & (tin.lat > -15.) & (tin.lon < 31.) & (tin.lon > 12.),drop=True).load())
    tin.close()
    del tin
tropomi = xr.concat(tlist,dim='time')
print('concated')
del tlist
tropN = pickle.dump(tropomi,'/Users/ellendyer/Documents/GitHub/Isotopes_F4R/data/tropomi_iso_band_N.pkl')
#tropomi.to_netcdf('/Users/ellendyer/Documents/GitHub/Isotopes_F4R/data/tropomi_iso_band_N.nc')
