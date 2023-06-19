# -*- coding: utf-8 -*-
"""
Spyder Editor

Created on 2023-03-07

Updated on 2023-06-19

@author: Laurens P. Stoop
"""


# load the dependencies
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import sys
from datetime import datetime
import matplotlib.dates as mdates

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



# Solar
colour_solar = 'burlywood' # 0.03
colour_solar_clim = 'grey' # 1
colour_solar_hrw = 'tab:red' # 0.7
colour_solar_credi = 'orange'

# Wind
colour_wind = 'skyblue' # 0.03
colour_wind_clim = 'grey' # 1
colour_wind_hrw = 'dodgerblue' # 0.7
colour_wind_credi = 'steelblue'


# COLOURS = ['#ffffcc','#c7e9b4','#7fcdbb','#41b6c4','#2c7fb8','#253494']
# COLOURS = ['#66c2a5','#fc8d62','#8da0cb','#e78ac3','#a6d854','#ffd92f']

#%%
# =============================================================================
# Define file locations
# =============================================================================

# Define some folders
FOLDER_project='/Users/3986209/Library/CloudStorage/OneDrive-UniversiteitUtrecht/Projects/ccmetrics/'
FOLDER_pecd = '/Users/3986209/Library/CloudStorage/OneDrive-UniversiteitUtrecht/Data/PECD/'
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

plt.savefig(FOLDER_project+'results/figures_development/Fig_CUMSUM_ClimComparison_SPV.png')

plt.show()

#%%
# =============================================================================
# Now we do a yearly running sum of cumsum of capacity factor
# =============================================================================


ds_AnomRolHourly = ds_AnomRolHourly.sel(time=~((ds_AnomRolHourly.time.dt.month == 2) & (ds_AnomRolHourly.time.dt.day == 29))).sel(time=slice("1991-01-01", "2020-12-31"))

# First we define the yearly cumsum
da_YCS = ds_AnomRolHourly.groupby(ds_AnomRolHourly.time.dt.year).cumsum()


#%%

# ds_AnomRolHourly.groupby(ds_AnomRolHourly.time.dt.year).cumsum().plot()
# ds_AnomRolHourly.groupby(ds_AnomRolHourly.time.dt.year).cumsum().groupby('OrdinalHour').quantile(0.1, method='closest_observation').plot()


fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16,6), sharey=True)
fig.autofmt_xdate()

axes[0].fill_between(
    ds_Clim.OrdinalHour, 
    da_YCS.groupby('OrdinalHour').quantile(0, method='closest_observation'),
    da_YCS.groupby('OrdinalHour').quantile(1, method='closest_observation'),
    color='orange', alpha=0.1, label='min-max'
    )

axes[0].fill_between(
    ds_Clim.OrdinalHour, 
    da_YCS.groupby('OrdinalHour').quantile(0.1, method='closest_observation'),
    da_YCS.groupby('OrdinalHour').quantile(0.9, method='closest_observation'),
    color='orange', alpha=0.2, label='10-90%'
    )

axes[0].fill_between(
    ds_Clim.OrdinalHour, 
    da_YCS.groupby('OrdinalHour').quantile(0.25, method='closest_observation'),
    da_YCS.groupby('OrdinalHour').quantile(0.75, method='closest_observation'),
    color='orange', alpha=0.4, label='25-75%'
    )

axes[0].plot(da_YCS.groupby('OrdinalHour').quantile(0.5, method='closest_observation'), color='orange', label='50%')

#EXPERIMENTAL 
axes[1].plot(ds_AnomHourly.OrdinalHour.sel(time='1996'),ds_AnomHourly.sel(time='1996').cumsum().values, color='blue', label='1996')
axes[1].plot(ds_AnomHourly.OrdinalHour.sel(time='1998'),ds_AnomHourly.sel(time='1998').cumsum().values, color='green', label='1998')
axes[1].plot(ds_AnomHourly.OrdinalHour.sel(time='2003'),ds_AnomHourly.sel(time='2003').cumsum().values, color='red', label='2003')
axes[1].plot(ds_AnomHourly.OrdinalHour.sel(time='2010'),ds_AnomHourly.sel(time='2010').cumsum().values, color='purple', label='2010')

axes[1].fill_between(
    ds_Clim.OrdinalHour, 
    da_YCS.groupby('OrdinalHour').quantile(0.1, method='closest_observation'),
    da_YCS.groupby('OrdinalHour').quantile(0.9, method='closest_observation'),
    color='orange', alpha=0.2, label='10-90%'
    )

axes[1].fill_between(
    ds_Clim.OrdinalHour, 
    da_YCS.groupby('OrdinalHour').quantile(0.25, method='closest_observation'),
    da_YCS.groupby('OrdinalHour').quantile(0.75, method='closest_observation'),
    color='orange', alpha=0.4, label='25-75%'
    )

axes[1].plot(da_YCS.groupby('OrdinalHour').quantile(0.5, method='closest_observation'), color='orange', label='50%')


# set the legend, labels & titles of the subplots
axes[0].legend(fontsize='medium')
axes[1].legend(fontsize='medium')

axes[0].set_ylabel('Cumalative sum of SPV-potential anomaly')
axes[0].set_ylim(-150,150)

# make it look better
plt.tight_layout()

plt.savefig(FOLDER_project+'results/figures_development/Fig_CUMSUM_Yearly_Distribution_SPV_initialv2.png')

plt.show()





#%%
# =============================================================================
# Start point determination
# =============================================================================


# subset the data
ds_AnomRolHourly = ds_AnomRolHourly.sel(time=~((ds_AnomRolHourly.time.dt.month == 2) & (ds_AnomRolHourly.time.dt.day == 29))).sel(time=slice("1991-01-01", "2020-12-31"))



# First we define the yearly cumsum
da_YCS_jan = ds_AnomRolHourly.groupby(ds_AnomRolHourly.time.dt.year).cumsum()
da_YCS_feb = ds_AnomRolHourly.shift(time=744).groupby(ds_AnomRolHourly.time.dt.year).cumsum()
da_YCS_mar = ds_AnomRolHourly.shift(time=1416).groupby(ds_AnomRolHourly.time.dt.year).cumsum()
da_YCS_apr = ds_AnomRolHourly.shift(time=2160).groupby(ds_AnomRolHourly.time.dt.year).cumsum()
da_YCS_may = ds_AnomRolHourly.shift(time=2880).groupby(ds_AnomRolHourly.time.dt.year).cumsum()
da_YCS_jun = ds_AnomRolHourly.shift(time=3624).groupby(ds_AnomRolHourly.time.dt.year).cumsum()
da_YCS_jul = ds_AnomRolHourly.shift(time=4344).groupby(ds_AnomRolHourly.time.dt.year).cumsum()
da_YCS_aug = ds_AnomRolHourly.shift(time=5088).groupby(ds_AnomRolHourly.time.dt.year).cumsum()
da_YCS_sep = ds_AnomRolHourly.shift(time=5832).groupby(ds_AnomRolHourly.time.dt.year).cumsum()
da_YCS_okt = ds_AnomRolHourly.shift(time=6552).groupby(ds_AnomRolHourly.time.dt.year).cumsum()
da_YCS_nov = ds_AnomRolHourly.shift(time=7296).groupby(ds_AnomRolHourly.time.dt.year).cumsum()
da_YCS_dec = ds_AnomRolHourly.shift(time=8016).groupby(ds_AnomRolHourly.time.dt.year).cumsum()


#%%

fig.autofmt_xdate()

year_dates = pd.date_range('1990-01-01', periods=8784, freq='1h')


for DA, SeasonName in zip([da_YCS_jan , da_YCS_feb, da_YCS_mar, da_YCS_apr, 
            da_YCS_may, da_YCS_jun, da_YCS_jul, da_YCS_aug, 
            da_YCS_sep, da_YCS_okt, da_YCS_nov, da_YCS_dec],
            ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' ]):

    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(8,6))#, sharey=True)

    axes.fill_between(
        year_dates, 
        DA.groupby('OrdinalHour').quantile(0, method='closest_observation'),
        DA.groupby('OrdinalHour').quantile(1, method='closest_observation'),
        color='orange', alpha=0.1, label='min-max'
        )
    
    axes.fill_between(
        year_dates, 
        DA.groupby('OrdinalHour').quantile(0.1, method='closest_observation'),
        DA.groupby('OrdinalHour').quantile(0.9, method='closest_observation'),
        color='orange', alpha=0.2, label='10-90%'
        )
    
    axes.fill_between(
        year_dates,
        DA.groupby('OrdinalHour').quantile(0.25, method='closest_observation'),
        DA.groupby('OrdinalHour').quantile(0.75, method='closest_observation'),
        color='orange', alpha=0.4, label='25-75%'
        )
    
    axes.plot(year_dates,DA.groupby('OrdinalHour').quantile(0.5, method='closest_observation'), 
              color='orange', label='50%')

    
    
    axes.set_ylabel('Solar CREDI [FLH]')
    axes.set_xlabel('')
    axes.set_title(SeasonName)
    
    axes.legend(loc='lower left', fontsize='medium')

    axes.set_ylim(-125,150)
    
    
    xfmt_years = mdates.DateFormatter('%b')
    
    
    axes.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(3, 6, 9, 12)))
    axes.xaxis.set_minor_locator(mdates.MonthLocator())
    axes.xaxis.set_major_formatter(xfmt_years)

    # make it look better
    plt.tight_layout()

    plt.savefig(FOLDER_project+'results/figures_development/Fig_CUMSUM_YearStart_SPV_'+SeasonName+'.pdf')
    plt.savefig(FOLDER_project+'results/figures_development/Fig_CUMSUM_YearStart_SPV_'+SeasonName+'.png')

    plt.show()



