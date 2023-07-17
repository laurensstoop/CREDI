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
ds_Clim['Daily'], MOD = creb.Climatology_MOD(ds, 'NL01')
ds_Clim['Hourly'], OH = creb.Climatology_Hourly(ds, 'NL01')
ds_Clim['RolDay42'], MOD = creb.Climatology_MOD_Rolling(ds, 'NL01', RollingWindow=960)
ds_Clim['RolHour42'], OH = creb.Climatology_Hourly_Rolling(ds, 'NL01', RollingWindow=40)



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
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(14,6))

# first subplot is the climatology
# ds_AnomRolHourly.cumsum().plot(ax=axes[0], label='Initial hourly', color='grey')


# second subplot is the difference in cumalative sum
ds_AnomDaily.cumsum().plot(ax=axes, label='Daily', color='pink', alpha=0.7, linewidth=1)
ds_AnomHourly.cumsum().plot(ax=axes, label= 'Hourly', color='green',  alpha=0.7, linewidth=1)
ds_AnomRolHourly.cumsum().plot(ax=axes, label='Rolling Hourly', color='blue',  alpha=0.7, linewidth=1)

# set the legend, labels & titles of the subplots
axes.legend(fontsize='medium')

axes.set_ylabel('Wind CREDI [FLH]')
axes.set_xlabel('')

axes.set_ylim(-275,1450)

# make it look better
plt.tight_layout()

plt.savefig(FOLDER_project+'results/publication/supplementary/Fig_ClimComparison_WON.png')
plt.savefig(FOLDER_project+'results/publication/supplementary/Fig_ClimComparison_WON.pdf')

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

year_dates = pd.date_range('1990-01-01', periods=8784, freq='1h')

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16,6), sharey=True)
fig.autofmt_xdate()

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

axes[0].plot(ds_Clim.OrdinalHour,  da_YCS.groupby('OrdinalHour').quantile(0.5, method='closest_observation'), color='dodgerblue', label='50%')

#EXPERIMENTAL 
axes[1].plot(ds_AnomHourly.OrdinalHour.sel(time='1996'),ds_AnomHourly.sel(time='1996').cumsum().values, color='orange', label='1996')
axes[1].plot(ds_AnomHourly.OrdinalHour.sel(time='1998'),ds_AnomHourly.sel(time='1998').cumsum().values, color='green', label='1998')
axes[1].plot(ds_AnomHourly.OrdinalHour.sel(time='2003'),ds_AnomHourly.sel(time='2003').cumsum().values, color='red', label='2003')
axes[1].plot(ds_AnomHourly.OrdinalHour.sel(time='2010'),ds_AnomHourly.sel(time='2010').cumsum().values, color='purple', label='2010')

axes[1].fill_between(
    year_dates,
    da_YCS.groupby('OrdinalHour').quantile(0.1, method='closest_observation'),
    da_YCS.groupby('OrdinalHour').quantile(0.9, method='closest_observation'),
    color='dodgerblue', alpha=0.2, label='10-90%'
    )

axes[1].fill_between(
    year_dates,
    da_YCS.groupby('OrdinalHour').quantile(0.25, method='closest_observation'),
    da_YCS.groupby('OrdinalHour').quantile(0.75, method='closest_observation'),
    color='dodgerblue', alpha=0.4, label='25-75%'
    )

axes[1].plot(year_dates, da_YCS.groupby('OrdinalHour').quantile(0.5, method='closest_observation'), color='dodgerblue', label='50%')


# set the legend, labels & titles of the subplots
axes[0].legend(loc='lower left', fontsize='medium')
axes[1].legend(loc='lower left', fontsize='medium')

axes[0].set_ylabel('Wind CREDI [FLH]')
axes[0].set_ylim(-450,450)

# make it look better
plt.tight_layout()

plt.savefig(FOLDER_project+'results/figures_development/Fig_CUMSUM_Yearly_Distribution_WON_initialv2.pdf')
plt.savefig(FOLDER_project+'results/figures_development/Fig_CUMSUM_Yearly_Distribution_WON_initialv2.png')

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

for DA, SHIFT, SeasonName in zip([da_YCS_jan , da_YCS_feb, da_YCS_mar, da_YCS_apr, 
            da_YCS_may, da_YCS_jun, da_YCS_jul, da_YCS_aug, 
            da_YCS_sep, da_YCS_okt, da_YCS_nov, da_YCS_dec],
            [0,744,1416,2160,2880,3624,4344,5088,5832,6552,7296,8016],
            ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' ]):

    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(8,6))#, sharey=True)

    axes.fill_between(
        year_dates.shift(SHIFT), 
        DA.groupby('OrdinalHour').quantile(0, method='closest_observation'),
        DA.groupby('OrdinalHour').quantile(1, method='closest_observation'),
        color='dodgerblue', alpha=0.1, label='min-max'
        )
    
    axes.fill_between(
        year_dates.shift(SHIFT), 
        DA.groupby('OrdinalHour').quantile(0.1, method='closest_observation'),
        DA.groupby('OrdinalHour').quantile(0.9, method='closest_observation'),
        color='dodgerblue', alpha=0.2, label='10-90%'
        )
    
    axes.fill_between(
        year_dates.shift(SHIFT),
        DA.groupby('OrdinalHour').quantile(0.25, method='closest_observation'),
        DA.groupby('OrdinalHour').quantile(0.75, method='closest_observation'),
        color='dodgerblue', alpha=0.4, label='25-75%'
        )
    
    axes.plot(year_dates.shift(SHIFT),DA.groupby('OrdinalHour').quantile(0.5, method='closest_observation'), 
              color='dodgerblue', label='50%')

    
    
    
    # add the storylines
    axes.plot(year_dates.shift(SHIFT)[0:8760],DA.sel(time='1996'), color='red', label='1996', alpha=0.9, linewidth=1)
    axes.plot(year_dates.shift(SHIFT)[0:8760],DA.sel(time='1998'), color='green', label='1998', alpha=0.9, linewidth=1)
    axes.plot(year_dates.shift(SHIFT)[0:8760],DA.sel(time='2003'), color='purple', label='2003', alpha=0.9, linewidth=1)
    axes.plot(year_dates.shift(SHIFT)[0:8760],DA.sel(time='2016'), color='black', label='2016', alpha=0.9, linewidth=1)
    
    
    axes.set_ylabel('Wind CREDI [FLH]')
    axes.set_xlabel('')
    # axes.set_title(SeasonName)
    
    axes.legend(loc='lower left', fontsize='medium')

    plt.ylim(-450,450)
    
    
    xfmt_years = mdates.DateFormatter('%b')
    
    
    axes.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(3, 6, 9, 12)))
    axes.xaxis.set_minor_locator(mdates.MonthLocator())
    axes.xaxis.set_major_formatter(xfmt_years)


    # make it look better
    plt.tight_layout()

    plt.savefig(FOLDER_project+'results/publication/supplementary/Fig_CUMSUM_YearStart_'+SeasonName+'.pdf')
    plt.savefig(FOLDER_project+'results/publication/supplementary/Fig_CUMSUM_YearStart_'+SeasonName+'.png')

    plt.show()






