# -*- coding: utf-8 -*-
"""
Spyder Editor

Created on 2023-03-30

Updated on 2023-06-11

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
import matplotlib.transforms as mtransforms


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


## colour definitions

# Solar
colour_solar = 'burlywood' # 0.03
colour_solar_clim = 'grey' # 1
colour_solar_hrw = 'tab:red' # 0.7

# Wind
colour_wind = 'skyblue' # 0.03
colour_wind_clim = 'grey' # 1
colour_wind_hrw = 'dodgerblue' # 0.7


# COLOURS = ['#ffffcc','#c7e9b4','#7fcdbb','#41b6c4','#2c7fb8','#253494']
# COLOURS = ['#66c2a5','#fc8d62','#8da0cb','#e78ac3','#a6d854','#ffd92f']

#%%
# =============================================================================
# Define file locations
# =============================================================================


# Define some folders
FOLDER_drive='/Users/3986209/Library/CloudStorage/OneDrive-UniversiteitUtrecht/'
FOLDER_project=FOLDER_drive+'Projects/ccmetrics/'
FOLDER_pecd = FOLDER_drive+'Data/PECD/HIST/ENER/'
FOLDER_project=FOLDER_drive+'Projects/ccmetrics/'

# file name
fileName_SPV = 'SPV/PEON/H_ERA5_ECMW_T639_SPV_0000m_Pecd_PEON_S198001010000_E202112312300_CFR_TIM_01h_NA-_noc_org_NA_NA---_NA---_PhM01.csv'
fileName_WON = 'WON/PEON/H_ERA5_ECMW_T639_WON_NA---_Pecd_PEON_S198001010000_E202112312300_CFR_TIM_01h_NA-_noc_org_30_NA---_NA---_PhM01.csv'

#%%
# =============================================================================
# Get the PECDv4.0 
# =============================================================================


# Open the file and set the index as the date
df_SPV = pd.read_csv(FOLDER_pecd+fileName_SPV, header=52, parse_dates=True, index_col='Date')
df_WON = pd.read_csv(FOLDER_pecd+fileName_WON, header=52, parse_dates=True, index_col='Date')
df_SPV.index = df_SPV.index.rename('time')
df_WON.index = df_WON.index.rename('time')
ds_SPV = df_SPV.NL01.to_xarray()
ds_WON = df_WON.NL01.to_xarray()


#%%
# =============================================================================
# Fix time
# =============================================================================

# for easier figures we remove the leap days, see notes in RES-balance functions on how to keep this in
ds_SPV = ds_SPV.sel(time=~((ds_SPV.time.dt.month == 2) & (ds_SPV.time.dt.day == 29)))
ds_WON = ds_WON.sel(time=~((ds_WON.time.dt.month == 2) & (ds_WON.time.dt.day == 29)))

#%%
# =============================================================================
# Get the Climatology
# =============================================================================

# Open climatology from disk
ds_ClimSPV = xr.open_dataset(FOLDER_project+'data/processed/ERA5_SPV_clim-anom_PECD_PEON_hrwCLIM40.nc')
ds_ClimWON = xr.open_dataset(FOLDER_project+'data/processed/ERA5_WON_clim-anom_PECD_PEON_hrwCLIM40.nc')


#%%
# =============================================================================
# Figure for climatological behaviour
# =============================================================================


# we start a new figure
fig, axes = plt.subplot_mosaic([['a)', 'b)'], ['c)', 'd)']], figsize=(17,10))

# fix date-format
fig.autofmt_xdate()


# show years
year_dates = pd.date_range('1990-01-01', periods=8760, freq='1h')


### First set is the data + hourly clim

# we want to see all years
for year in np.arange(start=1991,stop=2021):
    
    # Show the data for all the years
    axes['a)'].plot(year_dates, ds_WON.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31')), color=colour_wind, alpha=0.03)
    axes['c)'].plot(year_dates[13:8760:24], ds_SPV.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[13:8760:24], color=colour_solar, alpha=0.03)

# show the hourly clim with all the years, only 13:00 for solar 
axes['a)'].plot(year_dates, ds_ClimWON.Hourly, color=colour_wind_clim, alpha=0.7)
axes['c)'].plot(year_dates[13:8760:24], ds_ClimSPV.Hourly[13:8760:24], color=colour_solar_clim, alpha=0.7)
  
axes['a)'].plot(year_dates[13:8760:24], ds_ClimWON.HRW40[13:8760:24], color=colour_wind_hrw, alpha=1)
axes['c)'].plot(year_dates[13:8760:24], ds_ClimSPV.HRW40[13:8760:24], color=colour_solar_hrw, alpha=1)

### show the chosen hourly clim for a smaller timeperiod

StartTime=2210
EndTime=2380
YearShowCase=2003

# and the raw data
axes['b)'].plot(year_dates[StartTime:EndTime], ds_WON.sel(time=slice(str(YearShowCase)+'-01-01', str(YearShowCase)+'-12-31'))[StartTime:EndTime], color=colour_wind,  label='Wind potential for '+str(YearShowCase), alpha=1)
axes['d)'].plot(year_dates[StartTime:EndTime], ds_SPV.sel(time=slice(str(YearShowCase)+'-01-01', str(YearShowCase)+'-12-31'))[StartTime:EndTime], color=colour_solar,  label='Solar potential for '+str(YearShowCase), alpha=1)

# add hourly clim
axes['b)'].plot(year_dates[StartTime:EndTime], ds_ClimWON.Hourly[StartTime:EndTime], label='Initial climatology', color=colour_wind_clim, alpha=1)
axes['d)'].plot(year_dates[StartTime:EndTime], ds_ClimSPV.Hourly[StartTime:EndTime], label='Initial climatology', color=colour_solar_clim, alpha=1)

# Add the Hourly Rolling Window climatology
axes['b)'].plot(year_dates[StartTime:EndTime], ds_ClimWON.HRW40[StartTime:EndTime], label='Hourly Rolling Window climatology', color=colour_wind_hrw, alpha=1)
axes['d)'].plot(year_dates[StartTime:EndTime], ds_ClimSPV.HRW40[StartTime:EndTime], label='Hourly Rolling Window climatology', color=colour_solar_hrw, alpha=1)




### Now fix the nice stuff

# Fix limits
axes['a)'].set_ylim(0,0.92)
axes['b)'].set_ylim(0,0.92)
axes['c)'].set_ylim(0,0.75)
axes['d)'].set_ylim(0,0.75)


# formate the date-axis 
for a in ['a)', 'c)']:
    axes[a].xaxis.set_major_locator(mdates.MonthLocator(bymonth=(3,6,9,12)))
    axes[a].xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
    axes[a].xaxis.set_major_formatter(mdates.DateFormatter('%B'))

for a in ['b)', 'd)']:
    axes[a].xaxis.set_major_locator(mdates.DayLocator(interval=3))
    axes[a].xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    axes[a].xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))



# set the legend and labels
axes['b)'].legend(loc='upper right', fontsize='medium')
axes['d)'].legend(loc='upper right', fontsize='medium')

# Fix labels
axes['a)'].set_ylabel('Wind potential [0-1]')
axes['c)'].set_ylabel('Solar potential [0-1]')
axes['b)'].set_ylabel('')
axes['d)'].set_ylabel('')

# make it look better
plt.tight_layout()


# print subplot names
for label, ax in axes.items():
    # label physical distance in and down:
    trans = mtransforms.ScaledTranslation(10/72, -8/72, fig.dpi_scale_trans)
    ax.text(0.0, 1.0, label, transform=ax.transAxes + trans,
            fontsize='xx-large', verticalalignment='top')

plt.savefig(FOLDER_project+'results/publication/Climatology_v2.png')
plt.savefig(FOLDER_project+'results/publication/Climatology_v2.pdf')

plt.show()
