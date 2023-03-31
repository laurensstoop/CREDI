# -*- coding: utf-8 -*-
"""
Spyder Editor

Created on 2023-03-30

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
fileName_SPV = 'SPV/PEON/H_ERA5_ECMW_T639_SPV_0000m_Pecd_PEON_S198001010000_E202112312300_CFR_TIM_01h_NA-_noc_org_NA_NA---_NA---_PhM01.csv'
fileName_WON = 'WON/PEON/H_ERA5_ECMW_T639_WON_NA---_Pecd_PEON_S198001010000_E202112312300_CFR_TIM_01h_NA-_noc_org_30_NA---_NA---_PhM01.csv'


#%%
# =============================================================================
# Get the data to open
# =============================================================================

# Open the file and set the index as the date
df_SPV = pd.read_csv(FOLDER_hist+fileName_SPV, header=52, parse_dates=True, index_col='Date')
df_WON = pd.read_csv(FOLDER_hist+fileName_WON, header=52, parse_dates=True, index_col='Date')
df_SPV.index = df_SPV.index.rename('time')
df_WON.index = df_WON.index.rename('time')

ds_SPV = df_SPV.to_xarray()
ds_WON = df_WON.to_xarray()

# for easier figures we remove the leap days, see notes in RES-balance functions on 
# ds_SPV = ds_SPV.sel(time=~((ds_SPV.time.dt.month == 2) & (ds_SPV.time.dt.day == 29)))
# ds_WON = ds_WON.sel(time=~((ds_WON.time.dt.month == 2) & (ds_WON.time.dt.day == 29)))
ds_SPV = ds_SPV.convert_calendar('noleap').sel(time=slice("1991-01-01", "2020-12-31"))
ds_WON = ds_WON.convert_calendar('noleap').sel(time=slice("1991-01-01", "2020-12-31"))



# Make the Climatology dataset
ds_ClimSPV = xr.Dataset()
ds_ClimWON = xr.Dataset()

# determine climatology for solar
ds_ClimSPV['Hourly'], OH = creb.Climatology_Hourly(ds_SPV, 'NL01')
ds_ClimSPV['RolHour10'], OH = creb.Climatology_Hourly_Rolling(ds_SPV, 'NL01', RollingWindow=10)
ds_ClimSPV['RolHour20'], OH = creb.Climatology_Hourly_Rolling(ds_SPV, 'NL01', RollingWindow=20)
ds_ClimSPV['RolHour60'], OH = creb.Climatology_Hourly_Rolling(ds_SPV, 'NL01', RollingWindow=60)
ds_ClimSPV['RolHour90'], OH = creb.Climatology_Hourly_Rolling(ds_SPV, 'NL01', RollingWindow=90)
ds_ClimSPV['RolHour42'], OH = creb.Climatology_Hourly_Rolling(ds_SPV, 'NL01', RollingWindow=42)

# determine climatology for wind
ds_ClimWON['Hourly'], OH = creb.Climatology_Hourly(ds_WON, 'NL01')
ds_ClimWON['RolHour10'], OH = creb.Climatology_Hourly_Rolling(ds_WON, 'NL01', RollingWindow=10)
ds_ClimWON['RolHour20'], OH = creb.Climatology_Hourly_Rolling(ds_WON, 'NL01', RollingWindow=20)
ds_ClimWON['RolHour60'], OH = creb.Climatology_Hourly_Rolling(ds_WON, 'NL01', RollingWindow=60)
ds_ClimWON['RolHour90'], OH = creb.Climatology_Hourly_Rolling(ds_WON, 'NL01', RollingWindow=90)
ds_ClimWON['RolHour42'], OH = creb.Climatology_Hourly_Rolling(ds_WON, 'NL01', RollingWindow=42)

#%%
# =============================================================================
# Figure for climatological behaviour
# =============================================================================


# we start a new figure
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(17,10))

# fix date-format
fig.autofmt_xdate()


# show years
year_dates = pd.date_range('1990-01-01', periods=8760, freq='1h')


### First set is the data + hourly clim

# we want to see all years
for year in np.arange(start=1991,stop=2021):
    
    # Show the data for all the years
    axes[0,0].plot(year_dates, ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31')), color='dodgerblue', alpha=0.03)
    axes[1,0].plot(year_dates[13:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[13:8760:24], color='orange', alpha=0.03)

# show the hourly clim with all the years, only 13:00 for solar 
axes[0,0].plot(year_dates, ds_ClimWON.Hourly, color='lightslategray', alpha=1)
axes[1,0].plot(year_dates[13:8760:24], ds_ClimSPV.Hourly[13:8760:24], color='burlywood', alpha=1)
  


### show the hourly clim with other climatologies  

# Hourly clim, now also 08 for solar
axes[0,1].plot(year_dates[13:8760:24], ds_ClimWON.Hourly[13:8760:24], label='Hourly climatology', color='lightslategray', alpha=1)
axes[1,1].plot(year_dates[13:8760:24], ds_ClimSPV.Hourly[13:8760:24], label='Hourly climatology', color='burlywood', alpha=1)
axes[1,1].plot(year_dates[8:8760:24], ds_ClimSPV.Hourly[8:8760:24], color='burlywood', alpha=1)
    
# Rolling clim over 10 days
axes[0,1].plot(year_dates[13:8760:24], ds_ClimWON.RolHour10[13:8760:24], label='Rolling hourly 10', color='cornflowerblue', alpha=0.3)
axes[1,1].plot(year_dates[13:8760:24], ds_ClimSPV.RolHour10[13:8760:24],label='Rolling hourly 10', color='peachpuff', alpha=0.3)
axes[1,1].plot(year_dates[8:8760:24], ds_ClimSPV.RolHour10[8:8760:24], color='peachpuff', alpha=0.3)

# Rolling clim over 20 days
axes[0,1].plot(year_dates[13:8760:24], ds_ClimWON.RolHour20[13:8760:24], label='Rolling hourly 20', color='cornflowerblue', alpha=0.3)
axes[1,1].plot(year_dates[13:8760:24], ds_ClimSPV.RolHour20[13:8760:24],label='Rolling hourly 20', color='peachpuff', alpha=0.3)
axes[1,1].plot(year_dates[8:8760:24], ds_ClimSPV.RolHour20[8:8760:24], color='peachpuff', alpha=0.3)

# Rolling clim over 60 days
axes[0,1].plot(year_dates[13:8760:24], ds_ClimWON.RolHour60[13:8760:24], label='Rolling hourly 60', color='navy', alpha=0.3)
axes[1,1].plot(year_dates[13:8760:24], ds_ClimSPV.RolHour60[13:8760:24],label='Rolling hourly 60', color='yellow', alpha=0.3)
axes[1,1].plot(year_dates[8:8760:24], ds_ClimSPV.RolHour60[8:8760:24], color='yellow', alpha=0.3)

# Rolling clim over 90 days
axes[0,1].plot(year_dates[13:8760:24], ds_ClimWON.RolHour90[13:8760:24], label='Rolling hourly 90', color='purple', alpha=0.3)
axes[1,1].plot(year_dates[13:8760:24], ds_ClimSPV.RolHour90[13:8760:24],label='Rolling hourly 90', color='orange', alpha=0.3)
axes[1,1].plot(year_dates[8:8760:24], ds_ClimSPV.RolHour90[8:8760:24], color='yellow', alpha=0.3)

# Rolling clim over 42 days
axes[0,1].plot(year_dates[13:8760:24], ds_ClimWON.RolHour42[13:8760:24], label='Rolling hourly 42', color='blue', alpha=0.3)
axes[1,1].plot(year_dates[13:8760:24], ds_ClimSPV.RolHour42[13:8760:24],label='Rolling hourly 42', color='red', alpha=0.3)
axes[1,1].plot(year_dates[8:8760:24], ds_ClimSPV.RolHour42[8:8760:24], color='red', alpha=0.3)



### show the chosen hourly clim for a smaller timeperiod

StartTime=2210
EndTime=2380
YearShowCase=2003

# and the raw data
axes[0,2].plot(year_dates[StartTime:EndTime], ds_WON.NL01.sel(time=slice(str(YearShowCase)+'-01-01', str(YearShowCase)+'-12-31'))[StartTime:EndTime], color='dodgerblue',  label='Potential for '+str(YearShowCase), alpha=0.3)
axes[1,2].plot(year_dates[StartTime:EndTime], ds_SPV.NL01.sel(time=slice(str(YearShowCase)+'-01-01', str(YearShowCase)+'-12-31'))[StartTime:EndTime], color='orange',  label='Potential for '+str(YearShowCase), alpha=0.3)

# add hourly clim
axes[0,2].plot(year_dates[StartTime:EndTime], ds_ClimWON.Hourly[StartTime:EndTime], label='Hourly climatology', color='lightslategray', alpha=0.6)
axes[1,2].plot(year_dates[StartTime:EndTime], ds_ClimSPV.Hourly[StartTime:EndTime], label='Hourly climatology', color='burlywood', alpha=0.6)

# Add the 
axes[0,2].plot(year_dates[StartTime:EndTime], ds_ClimWON.RolHour42[StartTime:EndTime], label='Rolling hourly 42', color='blue', alpha=0.6)
axes[1,2].plot(year_dates[StartTime:EndTime], ds_ClimSPV.RolHour42[StartTime:EndTime], label='Rolling hourly 42', color='red', alpha=0.6)




### Now fix the nice stuff

# Fix limits
axes[0,0].set_ylim(0,0.92)
axes[0,1].set_ylim(0,0.92)
axes[0,2].set_ylim(0,0.92)
axes[1,0].set_ylim(0,0.75)
axes[1,1].set_ylim(0,0.75)
axes[1,2].set_ylim(0,0.75)


# formate the date-axis 
xfmt_years = mdates.DateFormatter('%b')
for a, b in [[0,0], [0,1], [1,0], [1,1]]:
    axes[a,b].xaxis.set_major_locator(mdates.MonthLocator(bymonth=(3, 6, 9, 12)))
    axes[a,b].xaxis.set_minor_locator(mdates.MonthLocator())
    axes[a,b].xaxis.set_major_formatter(xfmt_years)


xfmt_years = mdates.DateFormatter('%d-%m')
for a, b in [[0,2], [1,2]]:
    axes[a,b].xaxis.set_major_locator(mdates.DayLocator(interval=4))
    # axy.xaxis.set_minor_locator(mdates.MonthLocator())
    axes[a,b].xaxis.set_major_formatter(xfmt_years)



# set the legend and labels
axes[0,1].legend(loc='upper right', fontsize='medium')
axes[1,1].legend(loc='upper right', fontsize='medium')


axes[0,2].legend(loc='upper right', fontsize='medium')
axes[1,2].legend(loc='upper right', fontsize='medium')

# Fix labels
axes[0,0].set_ylabel('WON potential [0-1]')
axes[1,0].set_ylabel('SPV potential [0-1]')
axes[0,1].set_ylabel('')
axes[1,1].set_ylabel('')
axes[0,2].set_ylabel('')
axes[1,2].set_ylabel('')

# make it look better
plt.tight_layout()

plt.savefig(FOLDER_project+'results/publication/Climatology.png')
plt.savefig(FOLDER_project+'results/publication/Climatology.pdf')

plt.show()
