# -*- coding: utf-8 -*-
"""
Spyder Editor

Created on 2023-02-01

@author: Laurens P. Stoop
"""


# load the dependencies
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
from datetime import datetime


#%%


# Define some folders
FOLDER_project='/Users/3986209/Library/CloudStorage/OneDrive-UniversiteitUtrecht/Projects/ccmetrics/'
FOLDER_pecd = '/Users/3986209/Desktop/PECD/'
FOLDER_hist = FOLDER_pecd+'HIST/ENER/'

# file name
fileName= 'WON/PEON/H_ERA5_ECMW_T639_WON_NA---_Pecd_PEON_S198001010000_E202112312300_CFR_TIM_01h_NA-_noc_org_30_NA---_NA---_PhM01.csv'


# Open the file and set the index as the date
df = pd.read_csv(FOLDER_hist+fileName, header=52, parse_dates=True, index_col='Date')
df.index = df.index.rename('time')
ds = df.to_xarray()

#%%
# =============================================================================
# Getting the right climatology
# =============================================================================

# we want a function of in which the 29t of february is counted correctly

# for not leap years we get the information
not_leap_year = xr.DataArray(~ds.indexes['time'].is_leap_year, coords=ds.coords)
march_or_later = ds.time.dt.month >= 3
ordinal_day = ds.time.dt.dayofyear
modified_ordinal_day = ordinal_day + (not_leap_year & march_or_later)
modified_ordinal_day = modified_ordinal_day.rename('modified_ordinal_day')


# we can use this new modified ordinal day definition to get the correct climatology
ds_clim = ds.groupby(modified_ordinal_day).mean('time')
  
#%%
# =============================================================================
# Basic anomaly calculation
# =============================================================================

# determine the anomaly
ds_anom = ds.groupby(modified_ordinal_day) - ds_clim

# Show the anomaly for a few zones
ds_anom_diff_NLES = ds_anom.NL01 - ds_anom.ES01

# Prep a figure
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(14,6), sharey=True)

# first subplot we set the NL zones
ds_anom.NL01.cumsum().plot(ax=axes[0])
ds_anom.NL02.cumsum().plot(ax=axes[0])
ds_anom.NL03.cumsum().plot(ax=axes[0])
ds_anom.NL04.cumsum().plot(ax=axes[0])

# second subplot we set the ES zones
ds_anom.ES01.cumsum().plot(ax=axes[1])
ds_anom.ES02.cumsum().plot(ax=axes[1])
ds_anom.ES03.cumsum().plot(ax=axes[1])
ds_anom.ES04.cumsum().plot(ax=axes[1])
ds_anom.ES05.cumsum().plot(ax=axes[1])
ds_anom.ES06.cumsum().plot(ax=axes[1])
ds_anom.ES07.cumsum().plot(ax=axes[1])
ds_anom.ES08.cumsum().plot(ax=axes[1])
ds_anom.ES09.cumsum().plot(ax=axes[1])
ds_anom.ES10.cumsum().plot(ax=axes[1])
ds_anom.ES11.cumsum().plot(ax=axes[1])
ds_anom.ES12.cumsum().plot(ax=axes[1])

# third plot we set the diff between the zones
ds_anom_diff_NLES.cumsum().plot(ax=axes[2])


# set the labels & titles of the subplots
axes[0].set_title('NL zones')
axes[1].set_title('ES zones')
axes[2].set_title('NL01-ES01')

axes[0].set_ylabel('Cummalative sum of anomalies')
axes[1].set_ylabel('')

# make it look better
plt.tight_layout()
fig.suptitle('Cumsum for selected regions', fontsize=16, y=1.02)

plt.savefig(FOLDER_project+'results/figures/fig_cumsum_NLES.png')

plt.show()

#%%
# =============================================================================
# Now we do a slow moving climatology calculation
# =============================================================================

# for a dutch zone, we take the rolling centroid meand of 10 days (240 hours)
dsr_nl01 = ds.NL01.rolling(time=1008,center=True).mean()

# from the multi-day rolling mean we calculate the climatology
dsr_nl01_clim = dsr_nl01.groupby(modified_ordinal_day).mean('time')

# To get the anomaly w.r.t climatology
dsr_nl01_anom = dsr_nl01.groupby(modified_ordinal_day) - dsr_nl01_clim
ds_nl01_anom = ds.NL01.groupby(modified_ordinal_day) - dsr_nl01_clim


# we start a new figure
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12,6))

# first subplot is the climatology
ds_clim.NL01.plot(ax=axes[0],label='Daily climatology')
dsr_nl01_clim.plot(ax=axes[0],label='Rolling climatology')


# second subplot is the difference in cumalative sum
ds_anom.NL01.cumsum().plot(ax=axes[1], label='Daily climatology')
ds_nl01_anom.cumsum().plot(ax=axes[1], label= 'Rolling climatology')
dsr_nl01_anom.cumsum().plot(ax=axes[1], label='Rolling climatology, rolling data')

# set the legend, labels & titles of the subplots
axes[0].legend()
axes[1].legend()

axes[0].set_title('Climatology')
axes[1].set_title('Cumalative sum')

axes[0].set_ylabel('Daily average capacity factor')
axes[1].set_ylabel('Cumsum')

# make it look better
plt.tight_layout()
fig.suptitle('Cumsum for selected regions', fontsize=16, y=1.02)

plt.savefig(FOLDER_project+'results/figures/fig_climatology.png')

plt.show()

#%%
# =============================================================================
# Now we do a yearly running sum of cumsum of capacity factor
# =============================================================================


fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(14,12), sharey=True)

for year in np.arange(start=1980,stop=2021):
    
    axes[0,0].plot(ds_nl01_anom.sel(time=slice(str(year)+'-01-01', str(year+1)+'-12-31')).cumsum())
    axes[0,1].plot(ds_nl01_anom.sel(time=slice(str(year)+'-02-01', str(year+1)+'-01-31')).cumsum())
    axes[0,2].plot(ds_nl01_anom.sel(time=slice(str(year)+'-03-01', str(year+1)+'-02-28')).cumsum())
    axes[1,0].plot(ds_nl01_anom.sel(time=slice(str(year)+'-04-01', str(year+1)+'-03-31')).cumsum())
    axes[1,1].plot(ds_nl01_anom.sel(time=slice(str(year)+'-05-01', str(year+1)+'-04-30')).cumsum())
    axes[1,2].plot(ds_nl01_anom.sel(time=slice(str(year)+'-06-01', str(year+1)+'-05-31')).cumsum())


plt.savefig(FOLDER_project+'results/figures/fig_yearlyCumsum_startdate.png')




#%%
# df_clim = df.groupby(cum_data.index.dayofyear).mean()