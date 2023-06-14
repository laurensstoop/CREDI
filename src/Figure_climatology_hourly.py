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
colour_solar_clim = 'orange' # 1
colour_solar_hrw = 'tab:red' # 0.7

# Wind
colour_wind = 'skyblue' # 0.03
colour_wind_clim = 'lightsteelblue' # 1
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

# file name
fileName_SPV = 'SPV/PEON/H_ERA5_ECMW_T639_SPV_0000m_Pecd_PEON_S198001010000_E202112312300_CFR_TIM_01h_NA-_noc_org_NA_NA---_NA---_PhM01.csv'
fileName_WON = 'WON/PEON/H_ERA5_ECMW_T639_WON_NA---_Pecd_PEON_S198001010000_E202112312300_CFR_TIM_01h_NA-_noc_org_30_NA---_NA---_PhM01.csv'


#%%
# =============================================================================
# Get the data to open
# =============================================================================

# Open the file and set the index as the date
df_SPV = pd.read_csv(FOLDER_pecd+fileName_SPV, header=52, parse_dates=True, index_col='Date')
df_WON = pd.read_csv(FOLDER_pecd+fileName_WON, header=52, parse_dates=True, index_col='Date')
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
ds_ClimSPV['HRW40'], OH = creb.Climatology_Hourly_Rolling(ds_SPV, 'NL01', RollingWindow=40)

# determine climatology for wind
ds_ClimWON['Hourly'], OH = creb.Climatology_Hourly(ds_WON, 'NL01')
ds_ClimWON['HRW40'], OH = creb.Climatology_Hourly_Rolling(ds_WON, 'NL01', RollingWindow=40)

#%%
# =============================================================================
# Figure for climatological behaviour of each hour: solar
# =============================================================================


# we start a new figure
fig, axes = plt.subplots(nrows=4, ncols=6, figsize=(24,13), sharey=True, sharex=True )
# fig_won, axes_won = plt.subplots(nrows=4, ncols=6, figsize=(48,32))

# fix date-format
fig.autofmt_xdate()


# show years
year_dates = pd.date_range('1990-01-01', periods=8760, freq='1h')

### First set is the data + hourly clim


    
# we want to see all years
for year in np.arange(start=1991,stop=2021):
    
    # Show the data for all the years
    # axes_won[0,0].plot(year_dates, ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31')), color='dodgerblue', alpha=ALPHA_SET)
    ALPHA_SET=0.03
        
    axes[0,0].plot(year_dates[00:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[00:8760:24], color=colour_solar, alpha=ALPHA_SET)
    axes[0,1].plot(year_dates[00:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[1:8760:24], color=colour_solar, alpha=ALPHA_SET)
    axes[0,2].plot(year_dates[00:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[2:8760:24], color=colour_solar, alpha=ALPHA_SET)
    axes[0,3].plot(year_dates[00:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[3:8760:24], color=colour_solar, alpha=ALPHA_SET)
    axes[0,4].plot(year_dates[00:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[4:8760:24], color=colour_solar, alpha=ALPHA_SET)
    axes[0,5].plot(year_dates[00:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[5:8760:24], color=colour_solar, alpha=ALPHA_SET)
    axes[1,0].plot(year_dates[00:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[6:8760:24], color=colour_solar, alpha=ALPHA_SET)
    axes[1,1].plot(year_dates[00:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[7:8760:24], color=colour_solar, alpha=ALPHA_SET)
    axes[1,2].plot(year_dates[00:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[8:8760:24], color=colour_solar, alpha=ALPHA_SET)
    axes[1,3].plot(year_dates[00:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[9:8760:24], color=colour_solar, alpha=ALPHA_SET)
    axes[1,4].plot(year_dates[00:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[10:8760:24], color=colour_solar, alpha=ALPHA_SET)
    axes[1,5].plot(year_dates[00:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[11:8760:24], color=colour_solar, alpha=ALPHA_SET)
    axes[2,0].plot(year_dates[00:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[12:8760:24], color=colour_solar, alpha=ALPHA_SET)
    axes[2,1].plot(year_dates[00:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[13:8760:24], color=colour_solar, alpha=ALPHA_SET)
    axes[2,2].plot(year_dates[00:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[14:8760:24], color=colour_solar, alpha=ALPHA_SET)
    axes[2,3].plot(year_dates[00:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[15:8760:24], color=colour_solar, alpha=ALPHA_SET)
    axes[2,4].plot(year_dates[00:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[16:8760:24], color=colour_solar, alpha=ALPHA_SET)
    axes[2,5].plot(year_dates[00:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[17:8760:24], color=colour_solar, alpha=ALPHA_SET)
    axes[3,0].plot(year_dates[00:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[18:8760:24], color=colour_solar, alpha=ALPHA_SET)
    axes[3,1].plot(year_dates[00:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[19:8760:24], color=colour_solar, alpha=ALPHA_SET)
    axes[3,2].plot(year_dates[00:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[20:8760:24], color=colour_solar, alpha=ALPHA_SET)
    axes[3,3].plot(year_dates[00:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[21:8760:24], color=colour_solar, alpha=ALPHA_SET)
    axes[3,4].plot(year_dates[00:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[22:8760:24], color=colour_solar, alpha=ALPHA_SET)
    if year == 2020:
        axes[3,5].plot(year_dates[00:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[23:8760:24], color=colour_solar, alpha=ALPHA_SET, label='PECDv4 timeseries')
    else: 
        axes[3,5].plot(year_dates[00:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[23:8760:24], color=colour_solar, alpha=ALPHA_SET)


# show the hourly climatology & the Hourly Rolling Window Climatology
axes[0,0].plot(year_dates[00:8760:24], ds_ClimSPV.Hourly[00:8760:24], color=colour_solar_clim, alpha=1)
axes[0,0].plot(year_dates[00:8760:24], ds_ClimSPV.HRW40[00:8760:24], color=colour_solar_hrw, alpha=0.7, linewidth=3)
axes[0,1].plot(year_dates[00:8760:24], ds_ClimSPV.Hourly[1:8760:24], color=colour_solar_clim, alpha=1)
axes[0,1].plot(year_dates[00:8760:24], ds_ClimSPV.HRW40[1:8760:24], color=colour_solar_hrw, alpha=0.7, linewidth=3)
axes[0,2].plot(year_dates[00:8760:24], ds_ClimSPV.Hourly[2:8760:24], color=colour_solar_clim, alpha=1)
axes[0,2].plot(year_dates[00:8760:24], ds_ClimSPV.HRW40[2:8760:24], color=colour_solar_hrw, alpha=0.7, linewidth=3)
axes[0,3].plot(year_dates[00:8760:24], ds_ClimSPV.Hourly[3:8760:24], color=colour_solar_clim, alpha=1)
axes[0,3].plot(year_dates[00:8760:24], ds_ClimSPV.HRW40[3:8760:24], color=colour_solar_hrw, alpha=0.7, linewidth=3)
axes[0,4].plot(year_dates[00:8760:24], ds_ClimSPV.Hourly[4:8760:24], color=colour_solar_clim, alpha=1)
axes[0,4].plot(year_dates[00:8760:24], ds_ClimSPV.HRW40[4:8760:24], color=colour_solar_hrw, alpha=0.7, linewidth=3)
axes[0,5].plot(year_dates[00:8760:24], ds_ClimSPV.Hourly[5:8760:24], color=colour_solar_clim, alpha=1)
axes[0,5].plot(year_dates[00:8760:24], ds_ClimSPV.HRW40[5:8760:24], color=colour_solar_hrw, alpha=0.7, linewidth=3)
axes[1,0].plot(year_dates[00:8760:24], ds_ClimSPV.Hourly[6:8760:24], color=colour_solar_clim, alpha=1)
axes[1,0].plot(year_dates[00:8760:24], ds_ClimSPV.HRW40[6:8760:24], color=colour_solar_hrw, alpha=0.7, linewidth=3)
axes[1,1].plot(year_dates[00:8760:24], ds_ClimSPV.Hourly[7:8760:24], color=colour_solar_clim, alpha=1)
axes[1,1].plot(year_dates[00:8760:24], ds_ClimSPV.HRW40[7:8760:24], color=colour_solar_hrw, alpha=0.7, linewidth=3)
axes[1,2].plot(year_dates[00:8760:24], ds_ClimSPV.Hourly[8:8760:24], color=colour_solar_clim, alpha=1)
axes[1,2].plot(year_dates[00:8760:24], ds_ClimSPV.HRW40[8:8760:24], color=colour_solar_hrw, alpha=0.7, linewidth=3)
axes[1,3].plot(year_dates[00:8760:24], ds_ClimSPV.Hourly[9:8760:24], color=colour_solar_clim, alpha=1)
axes[1,3].plot(year_dates[00:8760:24], ds_ClimSPV.HRW40[9:8760:24], color=colour_solar_hrw, alpha=0.7, linewidth=3)
axes[1,4].plot(year_dates[00:8760:24], ds_ClimSPV.Hourly[10:8760:24], color=colour_solar_clim, alpha=1)
axes[1,4].plot(year_dates[00:8760:24], ds_ClimSPV.HRW40[10:8760:24], color=colour_solar_hrw, alpha=0.7, linewidth=3)
axes[1,5].plot(year_dates[00:8760:24], ds_ClimSPV.Hourly[11:8760:24], color=colour_solar_clim, alpha=1)
axes[1,5].plot(year_dates[00:8760:24], ds_ClimSPV.HRW40[11:8760:24], color=colour_solar_hrw, alpha=0.7, linewidth=3)
axes[2,0].plot(year_dates[00:8760:24], ds_ClimSPV.Hourly[12:8760:24], color=colour_solar_clim, alpha=1)
axes[2,0].plot(year_dates[00:8760:24], ds_ClimSPV.HRW40[12:8760:24], color=colour_solar_hrw, alpha=0.7, linewidth=3)
axes[2,1].plot(year_dates[00:8760:24], ds_ClimSPV.Hourly[13:8760:24], color=colour_solar_clim, alpha=1)
axes[2,1].plot(year_dates[00:8760:24], ds_ClimSPV.HRW40[13:8760:24], color=colour_solar_hrw, alpha=0.7, linewidth=3)
axes[2,2].plot(year_dates[00:8760:24], ds_ClimSPV.Hourly[14:8760:24], color=colour_solar_clim, alpha=1)
axes[2,2].plot(year_dates[00:8760:24], ds_ClimSPV.HRW40[14:8760:24], color=colour_solar_hrw, alpha=0.7, linewidth=3)
axes[2,3].plot(year_dates[00:8760:24], ds_ClimSPV.Hourly[15:8760:24], color=colour_solar_clim, alpha=1)
axes[2,3].plot(year_dates[00:8760:24], ds_ClimSPV.HRW40[15:8760:24], color=colour_solar_hrw, alpha=0.7, linewidth=3)
axes[2,4].plot(year_dates[00:8760:24], ds_ClimSPV.Hourly[16:8760:24], color=colour_solar_clim, alpha=1)
axes[2,4].plot(year_dates[00:8760:24], ds_ClimSPV.HRW40[16:8760:24], color=colour_solar_hrw, alpha=0.7, linewidth=3)
axes[2,5].plot(year_dates[00:8760:24], ds_ClimSPV.Hourly[17:8760:24], color=colour_solar_clim, alpha=1)
axes[2,5].plot(year_dates[00:8760:24], ds_ClimSPV.HRW40[17:8760:24], color=colour_solar_hrw, alpha=0.7, linewidth=3)
axes[3,0].plot(year_dates[00:8760:24], ds_ClimSPV.Hourly[18:8760:24], color=colour_solar_clim, alpha=1)
axes[3,0].plot(year_dates[00:8760:24], ds_ClimSPV.HRW40[18:8760:24], color=colour_solar_hrw, alpha=0.7, linewidth=3)
axes[3,1].plot(year_dates[00:8760:24], ds_ClimSPV.Hourly[19:8760:24], color=colour_solar_clim, alpha=1)
axes[3,1].plot(year_dates[00:8760:24], ds_ClimSPV.HRW40[19:8760:24], color=colour_solar_hrw, alpha=0.7, linewidth=3)
axes[3,2].plot(year_dates[00:8760:24], ds_ClimSPV.Hourly[20:8760:24], color=colour_solar_clim, alpha=1)
axes[3,2].plot(year_dates[00:8760:24], ds_ClimSPV.HRW40[20:8760:24], color=colour_solar_hrw, alpha=0.7, linewidth=3)
axes[3,3].plot(year_dates[00:8760:24], ds_ClimSPV.Hourly[21:8760:24], color=colour_solar_clim, alpha=1)
axes[3,3].plot(year_dates[00:8760:24], ds_ClimSPV.HRW40[21:8760:24], color=colour_solar_hrw, alpha=0.7, linewidth=3)
axes[3,4].plot(year_dates[00:8760:24], ds_ClimSPV.Hourly[22:8760:24], color=colour_solar_clim, alpha=1)
axes[3,4].plot(year_dates[00:8760:24], ds_ClimSPV.HRW40[22:8760:24], color=colour_solar_hrw, alpha=0.7, linewidth=3)
axes[3,5].plot(year_dates[00:8760:24], ds_ClimSPV.Hourly[23:8760:24], color=colour_solar_clim, alpha=1, label='Hourly Climatology')
axes[3,5].plot(year_dates[00:8760:24], ds_ClimSPV.HRW40[23:8760:24], color=colour_solar_hrw, alpha=0.7, linewidth=3, label='Hourly Rolling Window Climatology')


# format labels
axes[0,0].set_ylabel('Solar potential [0-1]')
axes[1,0].set_ylabel('Solar potential [0-1]')
axes[2,0].set_ylabel('Solar potential [0-1]')
axes[3,0].set_ylabel('Solar potential [0-1]')

# format legend
axes[3,5].legend(fontsize='medium')


# formate the date-axis 
for a, b in [[3,0], [3,1], [3,2], [3,3], [3,4], [3,5]]:
    axes[a,b].xaxis.set_major_locator(mdates.MonthLocator(bymonth=(3,6,9,12)))
    axes[a,b].xaxis.set_minor_locator(mdates.MonthLocator(bymonth=(1,2,4,5,7,8,10,11)))
    axes[a,b].xaxis.set_major_formatter(mdates.DateFormatter('%B'))
    
    
# make it look better
plt.tight_layout()

plt.savefig(FOLDER_project+'results/publication/Climatology_solar_hourly.png')
plt.savefig(FOLDER_project+'results/publication/Climatology_solar_hourly.pdf')

plt.show()


#%%
# =============================================================================
# Figure for climatological behaviour of each hour: wind
# =============================================================================



# we start a new figure
fig, axes = plt.subplots(nrows=4, ncols=6, figsize=(24,13), sharey=True, sharex=True )
# fig_won, axes_won = plt.subplots(nrows=4, ncols=6, figsize=(48,32))

# fix date-format
fig.autofmt_xdate()


# show years
year_dates = pd.date_range('1990-01-01', periods=8760, freq='1h')

### First set is the data + hourly clim


    
# we want to see all years
for year in np.arange(start=1991,stop=2021):
    
    # Show the data for all the years
    # axes_won[0,0].plot(year_dates, ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31')), color='dodgerblue', alpha=ALPHA_SET)
    ALPHA_SET=0.03
        
    axes[0,0].plot(year_dates[00:8760:24], ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[00:8760:24], color=colour_wind, alpha=ALPHA_SET)
    axes[0,1].plot(year_dates[00:8760:24], ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[1:8760:24], color=colour_wind, alpha=ALPHA_SET)
    axes[0,2].plot(year_dates[00:8760:24], ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[2:8760:24], color=colour_wind, alpha=ALPHA_SET)
    axes[0,3].plot(year_dates[00:8760:24], ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[3:8760:24], color=colour_wind, alpha=ALPHA_SET)
    axes[0,4].plot(year_dates[00:8760:24], ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[4:8760:24], color=colour_wind, alpha=ALPHA_SET)
    axes[0,5].plot(year_dates[00:8760:24], ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[5:8760:24], color=colour_wind, alpha=ALPHA_SET)
    axes[1,0].plot(year_dates[00:8760:24], ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[6:8760:24], color=colour_wind, alpha=ALPHA_SET)
    axes[1,1].plot(year_dates[00:8760:24], ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[7:8760:24], color=colour_wind, alpha=ALPHA_SET)
    axes[1,2].plot(year_dates[00:8760:24], ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[8:8760:24], color=colour_wind, alpha=ALPHA_SET)
    axes[1,3].plot(year_dates[00:8760:24], ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[9:8760:24], color=colour_wind, alpha=ALPHA_SET)
    axes[1,4].plot(year_dates[00:8760:24], ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[10:8760:24], color=colour_wind, alpha=ALPHA_SET)
    axes[1,5].plot(year_dates[00:8760:24], ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[11:8760:24], color=colour_wind, alpha=ALPHA_SET)
    axes[2,0].plot(year_dates[00:8760:24], ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[12:8760:24], color=colour_wind, alpha=ALPHA_SET)
    axes[2,1].plot(year_dates[00:8760:24], ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[13:8760:24], color=colour_wind, alpha=ALPHA_SET)
    axes[2,2].plot(year_dates[00:8760:24], ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[14:8760:24], color=colour_wind, alpha=ALPHA_SET)
    axes[2,3].plot(year_dates[00:8760:24], ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[15:8760:24], color=colour_wind, alpha=ALPHA_SET)
    axes[2,4].plot(year_dates[00:8760:24], ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[16:8760:24], color=colour_wind, alpha=ALPHA_SET)
    axes[2,5].plot(year_dates[00:8760:24], ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[17:8760:24], color=colour_wind, alpha=ALPHA_SET)
    axes[3,0].plot(year_dates[00:8760:24], ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[18:8760:24], color=colour_wind, alpha=ALPHA_SET)
    axes[3,1].plot(year_dates[00:8760:24], ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[19:8760:24], color=colour_wind, alpha=ALPHA_SET)
    axes[3,2].plot(year_dates[00:8760:24], ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[20:8760:24], color=colour_wind, alpha=ALPHA_SET)
    axes[3,3].plot(year_dates[00:8760:24], ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[21:8760:24], color=colour_wind, alpha=ALPHA_SET)
    axes[3,4].plot(year_dates[00:8760:24], ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[22:8760:24], color=colour_wind, alpha=ALPHA_SET)
    if year == 2020:
        axes[3,5].plot(year_dates[00:8760:24], ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[23:8760:24], color=colour_wind, alpha=ALPHA_SET, label='PECDv4 timeseries')
    else: 
        axes[3,5].plot(year_dates[00:8760:24], ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[23:8760:24], color=colour_wind, alpha=ALPHA_SET)




# show the hourly climatology & the Hourly Rolling Window Climatology
axes[0,0].plot(year_dates[00:8760:24], ds_ClimWON.Hourly[00:8760:24], color=colour_wind_clim, alpha=1)
axes[0,0].plot(year_dates[00:8760:24], ds_ClimWON.HRW40[00:8760:24], color=colour_wind_hrw, alpha=0.7, linewidth=3)
axes[0,1].plot(year_dates[00:8760:24], ds_ClimWON.Hourly[1:8760:24], color=colour_wind_clim, alpha=1)
axes[0,1].plot(year_dates[00:8760:24], ds_ClimWON.HRW40[1:8760:24], color=colour_wind_hrw, alpha=0.7, linewidth=3)
axes[0,2].plot(year_dates[00:8760:24], ds_ClimWON.Hourly[2:8760:24], color=colour_wind_clim, alpha=1)
axes[0,2].plot(year_dates[00:8760:24], ds_ClimWON.HRW40[2:8760:24], color=colour_wind_hrw, alpha=0.7, linewidth=3)
axes[0,3].plot(year_dates[00:8760:24], ds_ClimWON.Hourly[3:8760:24], color=colour_wind_clim, alpha=1)
axes[0,3].plot(year_dates[00:8760:24], ds_ClimWON.HRW40[3:8760:24], color=colour_wind_hrw, alpha=0.7, linewidth=3)
axes[0,4].plot(year_dates[00:8760:24], ds_ClimWON.Hourly[4:8760:24], color=colour_wind_clim, alpha=1)
axes[0,4].plot(year_dates[00:8760:24], ds_ClimWON.HRW40[4:8760:24], color=colour_wind_hrw, alpha=0.7, linewidth=3)
axes[0,5].plot(year_dates[00:8760:24], ds_ClimWON.Hourly[5:8760:24], color=colour_wind_clim, alpha=1)
axes[0,5].plot(year_dates[00:8760:24], ds_ClimWON.HRW40[5:8760:24], color=colour_wind_hrw, alpha=0.7, linewidth=3)
axes[1,0].plot(year_dates[00:8760:24], ds_ClimWON.Hourly[6:8760:24], color=colour_wind_clim, alpha=1)
axes[1,0].plot(year_dates[00:8760:24], ds_ClimWON.HRW40[6:8760:24], color=colour_wind_hrw, alpha=0.7, linewidth=3)
axes[1,1].plot(year_dates[00:8760:24], ds_ClimWON.Hourly[7:8760:24], color=colour_wind_clim, alpha=1)
axes[1,1].plot(year_dates[00:8760:24], ds_ClimWON.HRW40[7:8760:24], color=colour_wind_hrw, alpha=0.7, linewidth=3)
axes[1,2].plot(year_dates[00:8760:24], ds_ClimWON.Hourly[8:8760:24], color=colour_wind_clim, alpha=1)
axes[1,2].plot(year_dates[00:8760:24], ds_ClimWON.HRW40[8:8760:24], color=colour_wind_hrw, alpha=0.7, linewidth=3)
axes[1,3].plot(year_dates[00:8760:24], ds_ClimWON.Hourly[9:8760:24], color=colour_wind_clim, alpha=1)
axes[1,3].plot(year_dates[00:8760:24], ds_ClimWON.HRW40[9:8760:24], color=colour_wind_hrw, alpha=0.7, linewidth=3)
axes[1,4].plot(year_dates[00:8760:24], ds_ClimWON.Hourly[10:8760:24], color=colour_wind_clim, alpha=1)
axes[1,4].plot(year_dates[00:8760:24], ds_ClimWON.HRW40[10:8760:24], color=colour_wind_hrw, alpha=0.7, linewidth=3)
axes[1,5].plot(year_dates[00:8760:24], ds_ClimWON.Hourly[11:8760:24], color=colour_wind_clim, alpha=1)
axes[1,5].plot(year_dates[00:8760:24], ds_ClimWON.HRW40[11:8760:24], color=colour_wind_hrw, alpha=0.7, linewidth=3)
axes[2,0].plot(year_dates[00:8760:24], ds_ClimWON.Hourly[12:8760:24], color=colour_wind_clim, alpha=1)
axes[2,0].plot(year_dates[00:8760:24], ds_ClimWON.HRW40[12:8760:24], color=colour_wind_hrw, alpha=0.7, linewidth=3)
axes[2,1].plot(year_dates[00:8760:24], ds_ClimWON.Hourly[13:8760:24], color=colour_wind_clim, alpha=1)
axes[2,1].plot(year_dates[00:8760:24], ds_ClimWON.HRW40[13:8760:24], color=colour_wind_hrw, alpha=0.7, linewidth=3)
axes[2,2].plot(year_dates[00:8760:24], ds_ClimWON.Hourly[14:8760:24], color=colour_wind_clim, alpha=1)
axes[2,2].plot(year_dates[00:8760:24], ds_ClimWON.HRW40[14:8760:24], color=colour_wind_hrw, alpha=0.7, linewidth=3)
axes[2,3].plot(year_dates[00:8760:24], ds_ClimWON.Hourly[15:8760:24], color=colour_wind_clim, alpha=1)
axes[2,3].plot(year_dates[00:8760:24], ds_ClimWON.HRW40[15:8760:24], color=colour_wind_hrw, alpha=0.7, linewidth=3)
axes[2,4].plot(year_dates[00:8760:24], ds_ClimWON.Hourly[16:8760:24], color=colour_wind_clim, alpha=1)
axes[2,4].plot(year_dates[00:8760:24], ds_ClimWON.HRW40[16:8760:24], color=colour_wind_hrw, alpha=0.7, linewidth=3)
axes[2,5].plot(year_dates[00:8760:24], ds_ClimWON.Hourly[17:8760:24], color=colour_wind_clim, alpha=1)
axes[2,5].plot(year_dates[00:8760:24], ds_ClimWON.HRW40[17:8760:24], color=colour_wind_hrw, alpha=0.7, linewidth=3)
axes[3,0].plot(year_dates[00:8760:24], ds_ClimWON.Hourly[18:8760:24], color=colour_wind_clim, alpha=1)
axes[3,0].plot(year_dates[00:8760:24], ds_ClimWON.HRW40[18:8760:24], color=colour_wind_hrw, alpha=0.7, linewidth=3)
axes[3,1].plot(year_dates[00:8760:24], ds_ClimWON.Hourly[19:8760:24], color=colour_wind_clim, alpha=1)
axes[3,1].plot(year_dates[00:8760:24], ds_ClimWON.HRW40[19:8760:24], color=colour_wind_hrw, alpha=0.7, linewidth=3)
axes[3,2].plot(year_dates[00:8760:24], ds_ClimWON.Hourly[20:8760:24], color=colour_wind_clim, alpha=1)
axes[3,2].plot(year_dates[00:8760:24], ds_ClimWON.HRW40[20:8760:24], color=colour_wind_hrw, alpha=0.7, linewidth=3)
axes[3,3].plot(year_dates[00:8760:24], ds_ClimWON.Hourly[21:8760:24], color=colour_wind_clim, alpha=1)
axes[3,3].plot(year_dates[00:8760:24], ds_ClimWON.HRW40[21:8760:24], color=colour_wind_hrw, alpha=0.7, linewidth=3)
axes[3,4].plot(year_dates[00:8760:24], ds_ClimWON.Hourly[22:8760:24], color=colour_wind_clim, alpha=1)
axes[3,4].plot(year_dates[00:8760:24], ds_ClimWON.HRW40[22:8760:24], color=colour_wind_hrw, alpha=0.7, linewidth=3)
axes[3,5].plot(year_dates[00:8760:24], ds_ClimWON.Hourly[23:8760:24], color=colour_wind_clim, alpha=1, label='Hourly Climatology')
axes[3,5].plot(year_dates[00:8760:24], ds_ClimWON.HRW40[23:8760:24], color=colour_wind_hrw, alpha=0.7, linewidth=3, label='Hourly Rolling Window Climatology')


# format labels
axes[0,0].set_ylabel('Wind potential [0-1]')
axes[1,0].set_ylabel('Wind potential [0-1]')
axes[2,0].set_ylabel('Wind potential [0-1]')
axes[3,0].set_ylabel('Wind potential [0-1]')

# format legend
axes[3,5].legend(fontsize='medium')


# formate the date-axis 
for a, b in [[3,0], [3,1], [3,2], [3,3], [3,4], [3,5]]:
    axes[a,b].xaxis.set_major_locator(mdates.MonthLocator(bymonth=(3,6,9,12)))
    axes[a,b].xaxis.set_minor_locator(mdates.MonthLocator(bymonth=(1,2,4,5,7,8,10,11)))
    axes[a,b].xaxis.set_major_formatter(mdates.DateFormatter('%B'))
    
    
# make it look better
plt.tight_layout()

plt.savefig(FOLDER_project+'results/publication/Climatology_wind_hourly.png')
plt.savefig(FOLDER_project+'results/publication/Climatology_wind_hourly.pdf')

plt.show()










