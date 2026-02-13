#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 14:54:29 2022

@author: ellendyer
"""

###############################
# Start of file:
# Author(s): Ellen Dyer (2021)
# Contact: ellen.dyer@ouce.ox.ac.uk
# calculation of wet season onset and cessation
###############################
#    These functions find the onset and cessation of the wet season/s
#    The methodology is based on that of Liebmann et al. (2012) Journal of Climate
#    This methodology closely follows on the methodology described in Dunning et al. (2016)
#import sys
import xarray as xr
import matplotlib.pyplot as plt
import onset_cess_defs as ocd
import numpy as np
import pandas as pd
from shapely.geometry import mapping
import geopandas as gpd
from scipy.stats import linregress, kendalltau, theilslopes

#-------------------------
def q_slope(qarr,x):

        slope, intercept, r, p, se = linregress(x, qarr)

        return slope, p, intercept

def kt_slope(qarr,x):

        correl, p = kendalltau(x, qarr)

        return correl, p  

def ts_slope(x, qarr):

        slope, incpt, lslope, uslope = theilslopes(x, qarr)

        return slope, incpt, lslope, uslope



reg = 'Central Africa'
Y1=2004
Y2=2015

prt = xr.open_mfdataset('/Volumes/blue_wd/chirps_daily/chirps-v2.0.*.days_p05.nc')['precip']
prt = prt.rename({'latitude':'lat','longitude':'lon'})
prt = prt.sel(lat=slice(-5,5),lon=slice(10,30),time=slice(str(Y1)+'-01-01',str(Y2)+'-12-31'))
prt = prt.mean(dim=('lat','lon'))

power_ratio,on1,ce1,on2,ce2,on3,ce3,on1_years,ce1_years,on2_years,ce2_years,on3_years,ce3_years = ocd.xarray_on_cess_point(prt)
print(reg)
#print(on1,ce1)
#print('ON1_years',on1_years)
#print('CE1_years',ce1_years)

#%%
fig, ax = plt.subplots()
o =  plt.scatter(on1_years.year.values,on1_years.values,c='darkblue')
c =  plt.scatter(ce1_years.year.values,ce1_years.values,c='coral')  
for i in range(0, len(on1_years)):
    plt.plot([on1_years[i].year,on1_years[i].year], \
           [on1_years[i]+5,ce1_years[i]-5], '-', \
           color='green', linewidth=4)
ax.set_yticks(np.arange(100,330,20))
ax.set_ylim([90,330])
hl = plt.hlines(y=152, xmin=Y1, xmax=Y2, colors='black', linestyles='dotted',
           lw=2, alpha=0.5, zorder=10,label='June 1')
vl1 = plt.vlines(x=1996,ymin=100,ymax=320,colors='red', linestyles='--',
           lw=1, alpha=0.5, zorder=10,label='1996')
vl2 = plt.vlines(x=2013,ymin=100,ymax=320,colors='purple', linestyles='--',
           lw=1, alpha=0.5, zorder=10,label='2013')
plt.ylabel('Day of year')
twin_ax = ax.twinx()
twin_ax.set_ylim([90,330])
twin_ax.set_yticks(np.arange(100,330,20))    
twin_ax.set_yticklabels(pd.to_datetime(np.arange(100,330,20), \
          unit='D').strftime('%d-%b'),rotation=350)
plt.title(reg+' CHIRPS') 
plt.legend((o,c,hl,vl1,vl2),
          ('Onset','Cessation','June 1','1996','2013'),
          scatterpoints=1,
          loc='upper left',
          ncol=1,
          fontsize=8)
plt.savefig('plots/rainseason_duration_CHIRPS_'+reg+'.png',
            bbox_inches='tight',dpi=200)
plt.show()
plt.clf()

#%%

#ps = prt.sel(year=slice(Y1+1,Y2-2)).groupby('time.year').sum('time')/10.
#pm = prt.sel(year=slice(Y1+1,Y2-2)).groupby('time.year').quantile(0.9)*30.
#pm = prt.groupby('time.year').mean('time')*30.
lens = ce1_years - on1_years
mean1 = lens.sel(year=slice(1981,1996)).mean()
mean2 = lens.sel(year=slice(1997,2012)).mean()
mean3 = lens.sel(year=slice(2013,2022)).mean()
print(mean1.values,mean2.values,mean3.values)


mean1 = on1_years.sel(year=slice(1981,1996)).mean()
mean2 = on1_years.sel(year=slice(1997,2012)).mean()
mean3 = on1_years.sel(year=slice(2013,2022)).mean()
print(mean1.values,mean2.values,mean3.values)

seasval = on1_years

ktc,ktp = kt_slope(seasval,seasval.year)
print('kt correl of onset:',round(ktc,2),round(ktp,2))
lrs,lrp,lri = q_slope(seasval,seasval.year)
print('lr slope of onset:',round(lrs,2),round(lrp,2))
tss, incpt, lslope, uslope = ts_slope(seasval,seasval.year)
print('ts slope of onset:',round(tss,2),round(incpt,2),round(lslope,2),round(uslope,2))

tsvals = list(incpt + tss * np.arange(Y1+1,Y2))
lrvals = list(lri + lrs * np.arange(Y1+1,Y2))

upvals = tsvals[0] + uslope * (np.arange(Y1+1,Y2)-1982)
lwvals = tsvals[0] + lslope * (np.arange(Y1+1,Y2)-1982)

fig = plt.figure()
ax = fig.add_subplot(111)
sp = plt.scatter(np.arange(Y1+1,Y2),seasval,label='Onset day')
tsp = plt.plot(np.arange(Y1+1,Y2), tsvals, 'k-',label='Theil slope')
plt.plot(np.arange(Y1+1,Y2), upvals, 'k--')
plt.plot(np.arange(Y1+1,Y2), lwvals, 'k--')
lsp = plt.plot(np.arange(Y1+1,Y2), lrvals, 'g-',label='Linear reg')
hl = plt.hlines(y=152, xmin=Y1, xmax=Y2, colors='coral', linestyles='-',
           lw=3, alpha=0.5, zorder=10,label='June 1')
vl1 = plt.vlines(x=1996,ymin=120,ymax=160,colors='red', linestyles='--',
           lw=2, alpha=0.5, zorder=10,label='1996')
vl2 = plt.vlines(x=2013,ymin=110,ymax=180,colors='purple', linestyles='--',
           lw=2, alpha=0.5, zorder=10,label='2013')
plt.title('CHIRPS wet season onset (KT p='+str(round(ktp,2))+
          ', LR p='+str(round(lrp,2))+')')
plt.legend(scatterpoints=1,
          loc='upper left',
          ncol=2,
          fontsize=10)
plt.savefig('plots/onset_ts_CHIRPS_'+reg+'.png',
            bbox_inches='tight',dpi=200)
plt.show()
plt.clf()