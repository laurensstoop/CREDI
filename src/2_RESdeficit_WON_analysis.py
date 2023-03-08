# -*- coding: utf-8 -*-
"""
Spyder Editor

Created on 2023-03-07

@author: Laurens P. Stoop
"""


# load the dependencies
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import sys
from datetime import datetime

# The scripts
sys.path.append('/Users/3986209/Library/CloudStorage/OneDrive-UniversiteitUtrecht/Projects/ccmetrics/src/')
import RESdeficitFunctions as resFunc


#%%
import matplotlib.pylab as pylab
params = {'legend.fontsize': 'xx-large',
          'figure.figsize': (15, 5),
         'axes.labelsize': 'xx-large',
         'axes.titlesize':'xx-large',
         'xtick.labelsize':'xx-large',
         'ytick.labelsize':'xx-large'}
pylab.rcParams.update(params)


# COLOURS = ['#ffffcc','#c7e9b4','#7fcdbb','#41b6c4','#2c7fb8','#253494']
# COLOURS = ['#66c2a5','#fc8d62','#8da0cb','#e78ac3','#a6d854','#ffd92f']

#%%
# =============================================================================
# Define file locations
# =============================================================================

# Define some folders
FOLDER_project='/Users/3986209/Library/CloudStorage/OneDrive-UniversiteitUtrecht/Projects/ccmetrics/'
FOLDER_pecd = '/Users/3986209/Desktop/PECD/'
FOLDER_hist = FOLDER_pecd+'HIST/ENER/'

# file name
fileName= 'WON/PEON/H_ERA5_ECMW_T639_WON_NA---_Pecd_PEON_S198001010000_E202112312300_CFR_TIM_01h_NA-_noc_org_30_NA---_NA---_PhM01.csv'


#%%
# =============================================================================
# Get the data to open
# =============================================================================

# Open the file and set the index as the date
df = pd.read_csv(FOLDER_hist+fileName, header=52, parse_dates=True, index_col='Date')
df.index = df.index.rename('time')
ds = df.to_xarray()

#%%
# =============================================================================
# Functional definition call of climatology
# =============================================================================

# Make the Climatology dataset
ds_Clim = xr.Dataset()

# determine climatology
ds_Clim['Daily'], MOD = resFunc.Climatology_MOD(ds, 'NL01')
ds_Clim['Hourly'], OH = resFunc.Climatology_Hourly(ds, 'NL01')
ds_Clim['RolDay42'], MOD = resFunc.Climatology_MOD_Rolling(ds, 'NL01', RollingWindow=1008)
ds_Clim['RolHour42'], OH = resFunc.Climatology_Hourly_Rolling(ds, 'NL01', RollingWindow=42)



# determine the anomaly
ds_AnomHourly = ds.NL01.groupby(OH) - ds_Clim.Hourly
ds_AnomRolHourly = ds.NL01.groupby(OH) - ds_Clim.RolHour42
ds_AnomDaily = ds.NL01.groupby(MOD) - ds_Clim.Daily
ds_AnomRolDaily = ds.NL01.groupby(MOD) - ds_Clim.RolDay42

ds_AnomdiffD = ds_AnomRolHourly.cumsum() - ds_AnomDaily.cumsum()
ds_AnomdiffRD = ds_AnomRolHourly.cumsum() - ds_AnomRolDaily.cumsum()
ds_AnomdiffH = ds_AnomRolHourly.cumsum() - ds_AnomHourly.cumsum()

#%%
# =============================================================================
# Many year analysis
# =============================================================================



# we start a new figure
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14,6))

# first subplot is the climatology
ds_AnomRolHourly.cumsum().plot(ax=axes[0], label='Rolling Hourly', color='black')


# second subplot is the difference in cumalative sum
ds_AnomDaily.cumsum().plot(ax=axes[1], label='Daily', color='blue')
ds_AnomHourly.cumsum().plot(ax=axes[1], label= 'Hourly', color='orange')
ds_AnomRolHourly.cumsum().plot(ax=axes[1], label='Rolling Hourly', color='black')
ds_AnomRolDaily.cumsum().plot(ax=axes[1], label='Rolling Daily', color='purple')

# set the legend, labels & titles of the subplots
axes[1].legend(fontsize='medium')

axes[0].set_ylabel('Cumalative sum of RES-potential anomaly')

axes[0].set_ylim(-275,1450)
axes[1].set_ylim(-275,1450)

# make it look better
plt.tight_layout()

plt.savefig(FOLDER_project+'results/figures/Fig_CUMSUM_ClimComparison_WON.png')

plt.show()

#%%
# =============================================================================
# Now we do a yearly running sum of cumsum of capacity factor
# =============================================================================


# ds_AnomRolHourly.groupby(ds_AnomRolHourly.time.dt.year).cumsum().plot()
# ds_AnomRolHourly.groupby(ds_AnomRolHourly.time.dt.year).cumsum().groupby('OrdinalHour').quantile(0.1, method='closest_observation').plot()

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16,6), sharey=True)

axes[0].fill_between(
    ds_Clim.OrdinalHour, 
    ds_AnomRolHourly.groupby(ds_AnomRolHourly.time.dt.year).cumsum().groupby('OrdinalHour').quantile(0, method='closest_observation'),
    ds_AnomRolHourly.groupby(ds_AnomRolHourly.time.dt.year).cumsum().groupby('OrdinalHour').quantile(1, method='closest_observation'),
    color='dodgerblue', alpha=0.1, label='min-max'
    )

axes[0].fill_between(
    ds_Clim.OrdinalHour, 
    ds_AnomRolHourly.groupby(ds_AnomRolHourly.time.dt.year).cumsum().groupby('OrdinalHour').quantile(0.1, method='closest_observation'),
    ds_AnomRolHourly.groupby(ds_AnomRolHourly.time.dt.year).cumsum().groupby('OrdinalHour').quantile(0.9, method='closest_observation'),
    color='dodgerblue', alpha=0.2, label='10-90%'
    )

axes[0].fill_between(
    ds_Clim.OrdinalHour, 
    ds_AnomRolHourly.groupby(ds_AnomRolHourly.time.dt.year).cumsum().groupby('OrdinalHour').quantile(0.25, method='closest_observation'),
    ds_AnomRolHourly.groupby(ds_AnomRolHourly.time.dt.year).cumsum().groupby('OrdinalHour').quantile(0.75, method='closest_observation'),
    color='dodgerblue', alpha=0.4, label='25-75%'
    )

axes[0].plot(ds_AnomRolHourly.groupby(ds_AnomRolHourly.time.dt.year).cumsum().groupby('OrdinalHour').quantile(0.5, method='closest_observation'), color='dodgerblue', label='50%')

#EXPERIMENTAL 
# axes[1].plot([ds_AnomRolHourly.OrdinalHour,ds_AnomRolHourly.groupby(ds_AnomRolHourly.time.dt.year).cumsum()])

# set the legend, labels & titles of the subplots
axes[0].legend(fontsize='medium')

axes[0].set_ylabel('Cumalative sum of RES-potential anomaly')

# axes[0].set_ylim(-275,1450)

# make it look better
plt.tight_layout()

plt.savefig(FOLDER_project+'results/figures/Fig_CUMSUM_Yearly_Distribution_WON.png')

plt.show()



# # #%%
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
    
#     ax1.plot(dsr_nl01_anom.sel(time=slice(str(year)+'-05-01', str(year+1)+'-04-30')).cumsum(), c=c, linewidth=1)
#     ax2.plot(dsr_nl01_anom.sel(time=slice(str(year)+'-05-01', str(year+2)+'-04-30')).cumsum(), c=c, linewidth=1)
#     ax3.plot(dsr_nl01_anom.sel(time=slice(str(year)+'-05-01', str(year+3)+'-04-30')).cumsum(), c=c, linewidth=1)

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


# #%%

# fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(17,12), sharey=True)

# # make a colorrange
# color = plt.cm.RdBu_r(np.linspace(0, 1, 41))

# for year, c in zip(np.arange(start=1980,stop=2021), color):
    
#     axes[0,0].plot(dsr_nl01_anom.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31')).cumsum(), c=c, linewidth=1)
#     axes[0,1].plot(dsr_nl01_anom.sel(time=slice(str(year)+'-05-01', str(year+1)+'-04-30')).cumsum(), c=c, linewidth=1)
#     axes[1,0].plot(dsr_nl01_anom.sel(time=slice(str(year)+'-09-01', str(year+1)+'-04-30')).cumsum(), c=c, linewidth=1)
#     axes[1,1].plot(dsr_nl01_anom.sel(time=slice(str(year)+'-10-01', str(year+1)+'-04-30')).cumsum(), c=c, linewidth=1)

# # set the legend, labels & titles of the subplots
# axes[0,0].set_title('January Start')
# axes[0,1].set_title('May Start')
# # axes[0,2].set_title('March Start')
# axes[1,0].set_title('Sept Start')
# axes[1,1].set_title('Okt Start')
# # axes[1,2].set_title('June Start')

# axes[0,0].set_ylabel('Cummalative sum of RES-potential deficit')
# axes[1,0].set_ylabel('Cummalative sum of RES-potential deficit')

# sm = plt.cm.ScalarMappable(cmap=plt.cm.RdBu_r, norm=plt.Normalize(vmin=1980, vmax=2021))
# fig.colorbar(sm, ax=axes.ravel().tolist())
# # make it loog better
# # plt.tight_layout()



# if ROLLING is True: 
#     plt.savefig(FOLDER_project+'results/figures/fig_yearlyCumsum_startdatev2.png')
# elif ROLLING is False:
#     plt.savefig(FOLDER_project+'results/figures/fig_yearlyCumsum_startdatev2_rolling.png')
# #%%
# # df_clim = df.groupby(cum_data.index.dayofyear).mean()