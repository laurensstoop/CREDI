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
# from matplotlib.dates import DateFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable


#%%


# Define some folders
FOLDER_project='/Users/3986209/Library/CloudStorage/OneDrive-UniversiteitUtrecht/Projects/ccmetrics/'
FOLDER_pecd = '/Users/3986209/Desktop/PECD/'
FOLDER_hist = FOLDER_pecd+'HIST/ENER/'
FOLDER_proj = FOLDER_pecd+'PROJ/ENER/EERO/RCP45/'

# file name
fileNameHIST= 'WON/PEON/H_ERA5_ECMW_T639_WON_NA---_Pecd_PEON_S198001010000_E202112312300_CFR_TIM_01h_NA-_noc_org_30_NA---_NA---_PhM01.csv'
fileNamePROJ= 'WON/PEON/P_EUCX_KNMI_EERO_WON_NA---_Pecd_PEON_S200601010000_E206512312300_CFR_TIM_01h_NA-_noc_org_30_RCP45_NA---_PhM01.csv'


# Open the file and set the index as the date
df_hist = pd.read_csv(FOLDER_hist+fileNameHIST, header=52, parse_dates=True, index_col='Date')
df_proj = pd.read_csv(FOLDER_proj+fileNamePROJ, header=52, parse_dates=True, index_col='Date')

df_hist.index = df_hist.index.rename('time')
df_proj.index = df_proj.index.rename('time')
ds_hist = df_hist.to_xarray()
ds_proj = df_proj.to_xarray()

#%%
# =============================================================================
# Getting the right climatology (that includes the 29th)
# =============================================================================

# we want a function of in which the 29t of february is counted correctly

# for not leap years we get the information (HISTORICAL)
H_not_leap_year = xr.DataArray(~ds_hist.indexes['time'].is_leap_year, coords=ds_hist.coords)
H_march_or_later = ds_hist.time.dt.month >= 3
H_ordinal_day = ds_hist.time.dt.dayofyear
H_modified_ordinal_day = H_ordinal_day + (H_not_leap_year & H_march_or_later)
H_modified_ordinal_day = H_modified_ordinal_day.rename('modified_ordinal_day')


# for not leap years we get the information (PROJECTION)
P_not_leap_year = xr.DataArray(~ds_proj.indexes['time'].is_leap_year, coords=ds_proj.coords)
P_march_or_later = ds_proj.time.dt.month >= 3
P_ordinal_day = ds_proj.time.dt.dayofyear
P_modified_ordinal_day = P_ordinal_day + (P_not_leap_year & P_march_or_later)
P_modified_ordinal_day = P_modified_ordinal_day.rename('modified_ordinal_day')
  
#%%
# =============================================================================
# Basic anomaly calculation
# =============================================================================

# we can use this new modified ordinal day definition to get the correct climatology
ds_hist_clim = ds_hist.groupby(H_modified_ordinal_day).mean('time')
ds_proj_clim = ds_proj.groupby(P_modified_ordinal_day).mean('time')

# determine the anomaly
ds_hist_anom = ds_hist_clim - ds_hist.groupby(H_modified_ordinal_day)
ds_proj_anom_Chist = ds_hist_clim - ds_proj.groupby(P_modified_ordinal_day)
ds_proj_anom_Cproj = ds_proj_clim - ds_proj.groupby(P_modified_ordinal_day)


#%%
# =============================================================================
# Now we do a slow moving climatology calculation                               ONLY FOR  THE NL01 zone
# =============================================================================

# for a dutch zone, we take the rolling centroid meand of 10 days (240 hours)
dsr_hist = ds_hist.NL01.rolling(time=1008,center=True).mean()
dsr_proj = ds_proj.NL01.rolling(time=1008,center=True).mean()

# from the multi-day rolling mean we calculate the climatology
dsr_hist_clim = dsr_hist.groupby(H_modified_ordinal_day).mean('time')
dsr_proj_clim = dsr_proj.groupby(P_modified_ordinal_day).mean('time')


# To get the anomaly w.r.t climatology
dsr_hist_anom_CRhist = dsr_hist_clim - dsr_hist.groupby(H_modified_ordinal_day)
ds_hist_anom_CRhist = dsr_hist_clim - ds_hist.NL01.groupby(H_modified_ordinal_day)
ds_proj_anom_CRhist = dsr_hist_clim - ds_proj.NL01.groupby(P_modified_ordinal_day)



# we start a new figure
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14,12))

# first subplot is the climatology
# ds_hist_clim.NL01.plot(ax=axes[0,0],label='Daily historical climatology')
dsr_hist_clim.plot(ax=axes[0,0],label='Rolling historical climatology')
# ds_proj_clim.NL01.plot(ax=axes[0,0],label='Daily projected climatology')
dsr_proj_clim.plot(ax=axes[0,0],label='Rolling Projected climatology')


# second subplot is the historical daily vs rolling clima
ds_hist_anom.NL01.cumsum().plot(ax=axes[0,1], label='Daily climatology')
ds_hist_anom_CRhist.cumsum().plot(ax=axes[0,1], label= 'Rolling climatology')


# third subplot is the projected historical vs projected clima
ds_proj_anom_Chist.NL01.cumsum().plot(ax=axes[1,0], label='Historical climatology')
ds_proj_anom_Cproj.NL01.cumsum().plot(ax=axes[1,0], label='Projected climatology')

# the fourth subplot is rolling historical rolling vs daily
ds_proj_anom_CRhist.cumsum().plot(ax=axes[1,1], label='Historical rolling climatology')
ds_proj_anom_Chist.NL01.cumsum().plot(ax=axes[1,1], label='Historical climatology')

# set the legend, labels & titles of the subplots
axes[0,0].legend()
axes[0,1].legend()
axes[1,0].legend()
axes[1,1].legend()

# axes[0].set_title('Climatology')
# axes[1].set_title('Cumalative sum')

# axes[0].set_ylabel('Climatology of RES-potential')
# axes[1].set_ylabel('Cumalative sum of RES-potential deficit')

# # make it look better
# plt.tight_layout()

plt.savefig(FOLDER_project+'results/figures/fig_climatology_proj.png')

# plt.show()

#%%
# =============================================================================
# Now we make the figure for the ICEM abstract
# =============================================================================


fig, axes = plt.subplots(constrained_layout=True,nrows=1, ncols=3, figsize=(12,4))

# first subplot is the climatology
ds_hist_clim.NL01.plot(ax=axes[0],label='Daily historical climatology')
dsr_hist_clim.plot(ax=axes[0],label='Rolling historical climatology')


# for the second subplot we do yearly cumsums coloured with the year

# make a colorrange
color = plt.cm.plasma(np.linspace(0, 1, 59))

for year, c in zip(np.arange(start=2006,stop=2065), color):    
     axes[1].plot(ds_proj_anom_CRhist.sel(time=slice(str(year)+'-04-01', str(year+1)+'-03-31')).cumsum(), c=c, linewidth=1, alpha=0.5)

sm = plt.cm.ScalarMappable(cmap=plt.cm.plasma, norm=plt.Normalize(vmin=2006, vmax=2065))
# fig.colorbar(sm, ax=axes.ravel().tolist())
fig.colorbar(sm, ax=axes[1], location='right', label='Year')

# third subplot is the cumalative sum over the whole timerange
ds_hist_anom_CRhist.cumsum().plot(ax=axes[2], label= 'Reanalysis')
ds_proj_anom_CRhist.cumsum().plot(ax=axes[2], label= 'Projection data')

# # set the legend, labels & titles of the subplots
axes[0].set_title('A) Historical climatology')
axes[1].set_title('B) Cumulative sum per year')
axes[2].set_title('C) Cumulative sum ')

axes[0].legend()
axes[2].legend()

axes[0].set_ylabel('WON-potential [0-1]')
axes[1].set_ylabel('RES-potential deficit')
axes[2].set_ylabel('RES-potential deficit')

axes[0].set_xlabel('Day of the year')
axes[1].set_xlabel('Hourse since April 1st')
axes[2].set_xlabel('Year')

plt.savefig(FOLDER_project+'results/figures/fig_combination.png')

# #%%
# # =============================================================================
# # Now we do a yearly running sum of cumsum of capacity factor
# # =============================================================================


# # now for a different approach
# fig = plt.figure(constrained_layout=True, figsize=(16,12))#, sharey=True)


# # make a colorrange
# color = plt.cm.RdBu_r(np.linspace(0, 1, 41))

# # Rearrange the subplots so we have 1 big and 1 small graph
# gs = plt.GridSpec(nrows=2,ncols=3, figure=fig)
# ax1 = fig.add_subplot(gs[0,0])
# ax2 = fig.add_subplot(gs[0,1:3])
# ax3 = fig.add_subplot(gs[1,0:3])

# for year, c in zip(np.arange(start=1980,stop=2021), color):
    
#     ax1.plot(dsr_anom.sel(time=slice(str(year)+'-05-01', str(year+1)+'-04-30')).cumsum(), c=c, linewidth=1)
#     ax2.plot(dsr_anom.sel(time=slice(str(year)+'-05-01', str(year+2)+'-04-30')).cumsum(), c=c, linewidth=1)
#     ax3.plot(dsr_anom.sel(time=slice(str(year)+'-05-01', str(year+3)+'-04-30')).cumsum(), c=c, linewidth=1)

# # set the legend, labels & titles of the subplots
# ax1.set_title('One year')
# ax2.set_title('Two year')
# ax3.set_title('Three years')

# ax1.set_ylim([-600,600])
# ax2.set_ylim([-600,600])
# ax3.set_ylim([-600,600])

# ax1.set_ylabel('Cumsum of RES deficit')
# ax3.set_ylabel('Cumsum of RES deficit')

# sm = plt.cm.ScalarMappable(cmap=plt.cm.RdBu_r, norm=plt.Normalize(vmin=1980, vmax=2021))
# fig.colorbar(sm, ax=ax3, location='bottom')

# # # make it loog better
# # plt.tight_layout()


# if ROLLING is True: 
#     plt.savefig(FOLDER_project+'results/figures/fig_multiyear_Cumsum.png')
# elif ROLLING is False:
#     plt.savefig(FOLDER_project+'results/figures/fig_multiyear_Cumsum_rolling.png')


#%%
# df_clim = df.groupby(cum_data.index.dayofyear).mean()