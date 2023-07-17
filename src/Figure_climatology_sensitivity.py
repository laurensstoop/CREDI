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


#%% Set figure options
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

#%% Set file locations

# Define some folders
FOLDER_drive='/Users/3986209/Library/CloudStorage/OneDrive-UniversiteitUtrecht/'
FOLDER_project=FOLDER_drive+'Projects/ccmetrics/'
FOLDER_pecd = FOLDER_drive+'Data/PECD/HIST/ENER/'

# file name
fileName_SPV = 'SPV/PEON/H_ERA5_ECMW_T639_SPV_0000m_Pecd_PEON_S198001010000_E202112312300_CFR_TIM_01h_NA-_noc_org_NA_NA---_NA---_PhM01.csv'
fileName_WON = 'WON/PEON/H_ERA5_ECMW_T639_WON_NA---_Pecd_PEON_S198001010000_E202112312300_CFR_TIM_01h_NA-_noc_org_30_NA---_NA---_PhM01.csv'

#%% Open the data

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
ds_ClimSPV['RolHour10'], OH = creb.Climatology_Hourly_Rolling(ds_SPV, 'NL01', RollingWindow=10)
ds_ClimSPV['RolHour20'], OH = creb.Climatology_Hourly_Rolling(ds_SPV, 'NL01', RollingWindow=20)
ds_ClimSPV['RolHour60'], OH = creb.Climatology_Hourly_Rolling(ds_SPV, 'NL01', RollingWindow=60)
ds_ClimSPV['RolHour90'], OH = creb.Climatology_Hourly_Rolling(ds_SPV, 'NL01', RollingWindow=90)
ds_ClimSPV['RolHour120'], OH = creb.Climatology_Hourly_Rolling(ds_SPV, 'NL01', RollingWindow=120)
ds_ClimSPV['RolHour40'], OH = creb.Climatology_Hourly_Rolling(ds_SPV, 'NL01', RollingWindow=40)

# determine climatology for wind
ds_ClimWON['Hourly'], OH = creb.Climatology_Hourly(ds_WON, 'NL01')
ds_ClimWON['RolHour10'], OH = creb.Climatology_Hourly_Rolling(ds_WON, 'NL01', RollingWindow=10)
ds_ClimWON['RolHour20'], OH = creb.Climatology_Hourly_Rolling(ds_WON, 'NL01', RollingWindow=20)
ds_ClimWON['RolHour60'], OH = creb.Climatology_Hourly_Rolling(ds_WON, 'NL01', RollingWindow=60)
ds_ClimWON['RolHour90'], OH = creb.Climatology_Hourly_Rolling(ds_WON, 'NL01', RollingWindow=90)
ds_ClimWON['RolHour120'], OH = creb.Climatology_Hourly_Rolling(ds_WON, 'NL01', RollingWindow=120)
ds_ClimWON['RolHour40'], OH = creb.Climatology_Hourly_Rolling(ds_WON, 'NL01', RollingWindow=40)

#%% Figures with multiple methods full year


# we start a new figure
figW, axesW = plt.subplots(nrows=1, ncols=1, figsize=(10,5))
figS, axesS = plt.subplots(nrows=1, ncols=1, figsize=(10,5))

# fix date-format
figW.autofmt_xdate()
figS.autofmt_xdate()

# show years
year_dates = pd.date_range('1990-01-01', periods=8760, freq='1h')


### First set is the data + hourly clim

# we want to see all years
for year in np.arange(start=1991,stop=2021):
    
    # Show the data for all the years
    axesW.plot(year_dates, ds_WON.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31')), color=colour_wind, alpha=0.03)
    axesS.plot(year_dates[13:8760:24], ds_SPV.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31'))[13:8760:24], color=colour_solar, alpha=0.03)

# show the hourly clim with all the years, only 13:00 for solar 
axesW.plot(year_dates, ds_ClimWON.Hourly, color=colour_wind_clim, alpha=1)
axesS.plot(year_dates[13:8760:24], ds_ClimSPV.Hourly[13:8760:24], color=colour_solar_clim, alpha=1)
  


### show the hourly clim with other climatologies  

# Hourly clim, now also 08 for solar
axesW.plot(year_dates[13:8760:24], ds_ClimWON.Hourly[13:8760:24], label='Initial climatology', color=colour_wind_clim, alpha=0.7)
axesS.plot(year_dates[13:8760:24], ds_ClimSPV.Hourly[13:8760:24], label='Initial climatology', color=colour_solar_clim, alpha=0.7)
    
# Rolling clim over 10 days
axesW.plot(year_dates[13:8760:24], ds_ClimWON.RolHour10[13:8760:24], label='HRW-10', color='purple', alpha=0.7)
axesS.plot(year_dates[13:8760:24], ds_ClimSPV.RolHour10[13:8760:24],label='HRW-10', color='purple', alpha=0.7)

# Rolling clim over 20 days
axesW.plot(year_dates[13:8760:24], ds_ClimWON.RolHour20[13:8760:24], label='HRW-20', color='green', alpha=0.7)
axesS.plot(year_dates[13:8760:24], ds_ClimSPV.RolHour20[13:8760:24],label='HRW-20', color='green', alpha=0.7)

# Rolling clim over 60 days
axesW.plot(year_dates[13:8760:24], ds_ClimWON.RolHour60[13:8760:24], label='HRW-60', color='yellow', alpha=0.7)
axesS.plot(year_dates[13:8760:24], ds_ClimSPV.RolHour60[13:8760:24],label='HRW-60', color='yellow', alpha=0.7)

# Rolling clim over 90 days
axesW.plot(year_dates[13:8760:24], ds_ClimWON.RolHour90[13:8760:24], label='HRW-90', color='black', alpha=0.7)
axesS.plot(year_dates[13:8760:24], ds_ClimSPV.RolHour90[13:8760:24],label='HRW-90', color='black', alpha=0.7)


# Rolling clim over 90 days
axesW.plot(year_dates[13:8760:24], ds_ClimWON.RolHour120[13:8760:24], label='HRW-120', color='orange', alpha=0.7)
axesS.plot(year_dates[13:8760:24], ds_ClimSPV.RolHour120[13:8760:24],label='HRW-120', color='orange', alpha=0.7)


# Rolling clim over 40 days
axesW.plot(year_dates[13:8760:24], ds_ClimWON.RolHour40[13:8760:24], label='HRW-40', color=colour_wind_hrw, alpha=0.7)
axesS.plot(year_dates[13:8760:24], ds_ClimSPV.RolHour40[13:8760:24],label='HRW-40', color=colour_solar_hrw, alpha=0.7)



### Now fix the nice stuff

# Fix limits
axesW.set_ylim(0,0.92)
axesS.set_ylim(0,0.75)


# formate the date-axis 
axesW.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(3,6,9,12)))
axesS.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(3,6,9,12)))
axesW.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
axesS.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
axesW.xaxis.set_major_formatter(mdates.DateFormatter('%B'))
axesS.xaxis.set_major_formatter(mdates.DateFormatter('%B'))



# set the legend and labels
axesW.legend(loc='upper right', fontsize='medium')
axesS.legend(loc='upper right', fontsize='medium')

# Fix labels
axesW.set_ylabel('Wind potential [0-1]')
axesS.set_ylabel('Solar potential [0-1]')


plt.tight_layout()
plt.savefig(FOLDER_project+'results/supplementary/Climatology_sensitivity_solar.png')
plt.savefig(FOLDER_project+'results/supplementary/Climatology_sensitivity_solar.pdf')
plt.show()


# make it look better & save
plt.figure(figW)
plt.tight_layout()
plt.savefig(FOLDER_project+'results/supplementary/Climatology_sensitivity_wind.png')
plt.savefig(FOLDER_project+'results/supplementary/Climatology_sensitivity_wind.pdf')
plt.show()

#%% Figures with multiple methods part only


# we start a new figure
figW, axesW = plt.subplots(nrows=1, ncols=1, figsize=(10,5))
figS, axesS = plt.subplots(nrows=1, ncols=1, figsize=(10,5))

# fix date-format
figW.autofmt_xdate()
figS.autofmt_xdate()

# show years
year_dates = pd.date_range('1990-01-01', periods=8760, freq='1h')


StartTime=1405
EndTime=4300
YearShowCase=2003


# and the raw data
axesW.plot(year_dates[StartTime:EndTime], ds_WON.NL01.sel(time=slice(str(YearShowCase)+'-01-01', str(YearShowCase)+'-12-31'))[StartTime:EndTime], color=colour_wind,  label='Wind potential for '+str(YearShowCase), alpha=1)
axesS.plot(year_dates[StartTime:EndTime:24], ds_SPV.NL01.sel(time=slice(str(YearShowCase)+'-01-01', str(YearShowCase)+'-12-31'))[StartTime:EndTime:24], color=colour_solar,  label='Solar potential for '+str(YearShowCase), alpha=1)


# show the hourly clim with all the years, only 13:00 for solar 
axesW.plot(year_dates[StartTime:EndTime:24], ds_ClimWON.Hourly[StartTime:EndTime:24], color=colour_wind_clim, alpha=1)
axesS.plot(year_dates[StartTime:EndTime:24], ds_ClimSPV.Hourly[StartTime:EndTime:24], color=colour_solar_clim, alpha=1)
  


### show the hourly clim with other climatologies  

# Hourly clim, now also 08 for solar
axesW.plot(year_dates[StartTime:EndTime:24], ds_ClimWON.Hourly[StartTime:EndTime:24], label='Initial climatology', color=colour_wind_clim, alpha=1)
axesS.plot(year_dates[StartTime:EndTime:24], ds_ClimSPV.Hourly[StartTime:EndTime:24], label='Initial climatology', color=colour_solar_clim, alpha=1)
# axes['e)'].plot(year_dates[8:8760:24], ds_ClimSPV.Hourly[8:8760:24], color='burlywood', alpha=1)
    
# Rolling clim over 10 days
axesW.plot(year_dates[StartTime:EndTime:24], ds_ClimWON.RolHour10[StartTime:EndTime:24], label='HRW-10', color='purple', alpha=0.7)
axesS.plot(year_dates[StartTime:EndTime:24], ds_ClimSPV.RolHour10[StartTime:EndTime:24],label='HRW-10', color='purple', alpha=0.7)
# axes['e)'].plot(year_dates[8:8760:24], ds_ClimSPV.RolHour10[8:8760:24], color='peachpuff', alpha=0.3)

# Rolling clim over 20 days
axesW.plot(year_dates[StartTime:EndTime:24], ds_ClimWON.RolHour20[StartTime:EndTime:24], label='HRW-20', color='green', alpha=0.7)
axesS.plot(year_dates[StartTime:EndTime:24], ds_ClimSPV.RolHour20[StartTime:EndTime:24],label='HRW-20', color='green', alpha=0.7)
# axes['e)'].plot(year_dates[8:8760:24], ds_ClimSPV.RolHour20[8:8760:24], color='peachpuff', alpha=0.3)

# Rolling clim over 60 days
axesW.plot(year_dates[StartTime:EndTime:24], ds_ClimWON.RolHour60[StartTime:EndTime:24], label='HRW-60', color='yellow', alpha=0.7)
axesS.plot(year_dates[StartTime:EndTime:24], ds_ClimSPV.RolHour60[StartTime:EndTime:24],label='HRW-60', color='yellow', alpha=0.7)
# axes['e)'].plot(year_dates[8:8760:24], ds_ClimSPV.RolHour60[8:8760:24], color='yellow', alpha=0.3)

# Rolling clim over 90 days
axesW.plot(year_dates[StartTime:EndTime:24], ds_ClimWON.RolHour90[StartTime:EndTime:24], label='HRW-90', color='black', alpha=0.7)
axesS.plot(year_dates[StartTime:EndTime:24], ds_ClimSPV.RolHour90[StartTime:EndTime:24],label='HRW-90', color='black', alpha=0.7)
# axes['e)'].plot(year_dates[8:8760:24], ds_ClimSPV.RolHour90[8:8760:24], color='yellow', alpha=0.3)


# Rolling clim over 120 days
axesW.plot(year_dates[StartTime:EndTime:24], ds_ClimWON.RolHour120[StartTime:EndTime:24], label='HRW-120', color='orange', alpha=0.7)
axesS.plot(year_dates[StartTime:EndTime:24], ds_ClimSPV.RolHour120[StartTime:EndTime:24],label='HRW-120', color='orange', alpha=0.7)

# Rolling clim over 40 days
axesW.plot(year_dates[StartTime:EndTime:24], ds_ClimWON.RolHour40[StartTime:EndTime:24], label='HRW-40', color=colour_wind_hrw, alpha=0.7)
axesS.plot(year_dates[StartTime:EndTime:24], ds_ClimSPV.RolHour40[StartTime:EndTime:24],label='HRW-40', color=colour_solar_hrw, alpha=0.7)
# axes['e)'].plot(year_dates[8:8760:24], ds_ClimSPV.RolHour40[8:8760:24], color='red', alpha=0.3)


### Now fix the nice stuff

# Fix limits
axesW.set_ylim(0,0.92)
axesS.set_ylim(0,0.75)



axesW.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
axesS.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
axesW.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
axesS.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
axesW.xaxis.set_major_formatter(mdates.DateFormatter('%B'))
axesS.xaxis.set_major_formatter(mdates.DateFormatter('%B'))



# set the legend and labels
axesW.legend(loc='upper right', fontsize='medium')
axesS.legend(loc='lower right', fontsize='medium')

# Fix labels
axesW.set_ylabel('Wind potential [0-1]')
axesS.set_ylabel('Solar potential [0-1]')


plt.tight_layout()
plt.savefig(FOLDER_project+'results/supplementary/Climatology_sensitivity_zoom_solar.png')
plt.savefig(FOLDER_project+'results/supplementary/Climatology_sensitivity_zoom_solar.pdf')
plt.show()


# make it look better & save
plt.figure(figW)
plt.tight_layout()
plt.savefig(FOLDER_project+'results/supplementary/Climatology_sensitivity_zoom_wind.png')
plt.savefig(FOLDER_project+'results/supplementary/Climatology_sensitivity_zoom_wind.pdf')
plt.show()
