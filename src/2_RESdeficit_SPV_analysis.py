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
import CREBfunctions as creb


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
fileName= 'SPV/PEON/H_ERA5_ECMW_T639_SPV_0000m_Pecd_PEON_S198001010000_E202112312300_CFR_TIM_01h_NA-_noc_org_NA_NA---_NA---_PhM01.csv'


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
ds_Clim['Daily'], MOD = creb.Climatology_MOD(ds, 'NL01')
ds_Clim['Hourly'], OH = creb.Climatology_Hourly(ds, 'NL01')
ds_Clim['RolDay42'], MOD = creb.Climatology_MOD_Rolling(ds, 'NL01', RollingWindow=1008)
ds_Clim['RolHour42'], OH = creb.Climatology_Hourly_Rolling(ds, 'NL01', RollingWindow=42)



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

axes[0].set_ylim(-450,100)
axes[1].set_ylim(-450,100)

# make it look better
plt.tight_layout()

plt.savefig(FOLDER_project+'results/figures/Fig_CUMSUM_ClimComparison_SPV.png')

plt.show()

#%%
# =============================================================================
# Now we do a yearly running sum of cumsum of capacity factor
# =============================================================================

# First we define the yearly cumsum
da_YCS = ds_AnomRolHourly.groupby(ds_AnomRolHourly.time.dt.year).cumsum()


#%%

# ds_AnomRolHourly.groupby(ds_AnomRolHourly.time.dt.year).cumsum().plot()
# ds_AnomRolHourly.groupby(ds_AnomRolHourly.time.dt.year).cumsum().groupby('OrdinalHour').quantile(0.1, method='closest_observation').plot()

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16,6), sharey=True)

axes[0].fill_between(
    ds_Clim.OrdinalHour, 
    da_YCS.groupby('OrdinalHour').quantile(0, method='closest_observation'),
    da_YCS.groupby('OrdinalHour').quantile(1, method='closest_observation'),
    color='dodgerblue', alpha=0.1, label='min-max'
    )

axes[0].fill_between(
    ds_Clim.OrdinalHour, 
    da_YCS.groupby('OrdinalHour').quantile(0.1, method='closest_observation'),
    da_YCS.groupby('OrdinalHour').quantile(0.9, method='closest_observation'),
    color='dodgerblue', alpha=0.2, label='10-90%'
    )

axes[0].fill_between(
    ds_Clim.OrdinalHour, 
    da_YCS.groupby('OrdinalHour').quantile(0.25, method='closest_observation'),
    da_YCS.groupby('OrdinalHour').quantile(0.75, method='closest_observation'),
    color='dodgerblue', alpha=0.4, label='25-75%'
    )

axes[0].plot(da_YCS.groupby('OrdinalHour').quantile(0.5, method='closest_observation'), color='dodgerblue', label='50%')

#EXPERIMENTAL 
# axes[1].plot(ds_AnomHourly.OrdinalHour.sel(time='1990'),ds_AnomHourly.sel(time='1990').cumsum().values, color='red')
# axes[1].plot(ds_AnomHourly.OrdinalHour.sel(time='1995'),ds_AnomHourly.sel(time='1995').cumsum().values, color='green')
axes[1].plot(ds_AnomHourly.OrdinalHour.sel(time='2003'),ds_AnomHourly.sel(time='2003').cumsum().values, color='red', label='2003')
axes[1].plot(ds_AnomHourly.OrdinalHour.sel(time='2010'),ds_AnomHourly.sel(time='2010').cumsum().values, color='purple', label='2010')

axes[1].fill_between(
    ds_Clim.OrdinalHour, 
    da_YCS.groupby('OrdinalHour').quantile(0.1, method='closest_observation'),
    da_YCS.groupby('OrdinalHour').quantile(0.9, method='closest_observation'),
    color='dodgerblue', alpha=0.2, label='10-90%'
    )

axes[1].fill_between(
    ds_Clim.OrdinalHour, 
    da_YCS.groupby('OrdinalHour').quantile(0.25, method='closest_observation'),
    da_YCS.groupby('OrdinalHour').quantile(0.75, method='closest_observation'),
    color='dodgerblue', alpha=0.4, label='25-75%'
    )

axes[1].plot(da_YCS.groupby('OrdinalHour').quantile(0.5, method='closest_observation'), color='dodgerblue', label='50%')


# set the legend, labels & titles of the subplots
axes[0].legend(fontsize='medium')
axes[1].legend(fontsize='medium')

axes[0].set_ylabel('Cumalative sum of SPV-potential anomaly')
axes[0].set_ylim(-150,150)

# make it look better
plt.tight_layout()

plt.savefig(FOLDER_project+'results/figures/Fig_CUMSUM_Yearly_Distribution_SPV_initialv2.png')

plt.show()





#%%
# =============================================================================
# Start point determination
# =============================================================================


# First we define the yearly cumsum
da_YCS_jan = ds_AnomRolHourly.groupby(ds_AnomRolHourly.time.dt.year).cumsum()
da_YCS_feb = ds_AnomRolHourly.shift(time=744).groupby(ds_AnomRolHourly.time.dt.year).cumsum()
da_YCS_mar = ds_AnomRolHourly.shift(time=1440).groupby(ds_AnomRolHourly.time.dt.year).cumsum()
da_YCS_apr = ds_AnomRolHourly.shift(time=2184).groupby(ds_AnomRolHourly.time.dt.year).cumsum()
da_YCS_may = ds_AnomRolHourly.shift(time=2904).groupby(ds_AnomRolHourly.time.dt.year).cumsum()
da_YCS_jun = ds_AnomRolHourly.shift(time=3648).groupby(ds_AnomRolHourly.time.dt.year).cumsum()
da_YCS_jul = ds_AnomRolHourly.shift(time=4368).groupby(ds_AnomRolHourly.time.dt.year).cumsum()
da_YCS_aug = ds_AnomRolHourly.shift(time=5112).groupby(ds_AnomRolHourly.time.dt.year).cumsum()
da_YCS_sep = ds_AnomRolHourly.shift(time=5856).groupby(ds_AnomRolHourly.time.dt.year).cumsum()
da_YCS_okt = ds_AnomRolHourly.shift(time=6576).groupby(ds_AnomRolHourly.time.dt.year).cumsum()
da_YCS_nov = ds_AnomRolHourly.shift(time=7320).groupby(ds_AnomRolHourly.time.dt.year).cumsum()
da_YCS_dec = ds_AnomRolHourly.shift(time=8040).groupby(ds_AnomRolHourly.time.dt.year).cumsum()


#%%

for DA, SeasonName in zip([da_YCS_jan , da_YCS_feb, da_YCS_mar, da_YCS_apr, 
            da_YCS_may, da_YCS_jun, da_YCS_jul, da_YCS_aug, 
            da_YCS_sep, da_YCS_okt, da_YCS_nov, da_YCS_dec],
            ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'okt', 'nov', 'dec' ]):

    fig = plt.figure(figsize=(8,6))#, sharey=True)

    plt.fill_between(
        ds_Clim.OrdinalHour, 
        DA.groupby('OrdinalHour').quantile(0, method='closest_observation'),
        DA.groupby('OrdinalHour').quantile(1, method='closest_observation'),
        color='dodgerblue', alpha=0.1, label='min-max'
        )
    
    plt.fill_between(
        ds_Clim.OrdinalHour, 
        DA.groupby('OrdinalHour').quantile(0.1, method='closest_observation'),
        DA.groupby('OrdinalHour').quantile(0.9, method='closest_observation'),
        color='dodgerblue', alpha=0.2, label='10-90%'
        )
    
    plt.fill_between(
        ds_Clim.OrdinalHour, 
        DA.groupby('OrdinalHour').quantile(0.25, method='closest_observation'),
        DA.groupby('OrdinalHour').quantile(0.75, method='closest_observation'),
        color='dodgerblue', alpha=0.4, label='25-75%'
        )
    
    plt.plot(DA.groupby('OrdinalHour').quantile(0.5, method='closest_observation'), color='dodgerblue', label='50%')

    
    
    plt.ylabel('Cummalative sum of SPV-potential deficit')
    plt.title(SeasonName)
    
    plt.legend(fontsize='medium')

    plt.ylim(-125,150)

    # make it look better
    plt.tight_layout()

    plt.savefig(FOLDER_project+'results/figures/Fig_CUMSUM_YearStart_SPV_'+SeasonName+'.png')

    plt.show()






