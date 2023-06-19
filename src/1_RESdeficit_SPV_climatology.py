# -*- coding: utf-8 -*-
"""
Spyder Editor

Created on 2023-03-02

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
ds_Clim['RolClim10'], MOD = creb.Climatology_MOD_Rolling(ds, 'NL01', RollingWindow=240)
ds_Clim['RolClim20'], MOD = creb.Climatology_MOD_Rolling(ds, 'NL01', RollingWindow=480)
ds_Clim['RolClim30'], MOD = creb.Climatology_MOD_Rolling(ds, 'NL01', RollingWindow=720)
ds_Clim['RolClim42'], MOD = creb.Climatology_MOD_Rolling(ds, 'NL01', RollingWindow=960)
ds_Clim['RolClim60'], MOD = creb.Climatology_MOD_Rolling(ds, 'NL01', RollingWindow=1920)
ds_Clim['RolClim90'], MOD = creb.Climatology_MOD_Rolling(ds, 'NL01', RollingWindow=2880)


ds_Clim['Hourly'], MOH = creb.Climatology_Hourly(ds, 'NL01')

ds_Clim['RolMOH42'], MOH = creb.Climatology_MOH_Rolling(ds, 'NL01', RollingWindow=42)

ds_Clim['RolHour20'], OH = creb.Climatology_Hourly_Rolling(ds, 'NL01', RollingWindow=20)
ds_Clim['RolHour60'], OH = creb.Climatology_Hourly_Rolling(ds, 'NL01', RollingWindow=60)
ds_Clim['RolHour42'], OH = creb.Climatology_Hourly_Rolling(ds, 'NL01', RollingWindow=40)



#%%
# =============================================================================
# Harmonic mean
# =============================================================================

# Determin Fourier T
fft_D, freq_D = creb.fourier_transform(ds_Clim.Daily.values, 1/366.)
fft_H, freq_H = creb.fourier_transform(ds_Clim.Hourly.values, 1/8764.)

# Get the frequency spectrum information
spd_D, pos_freqs_D = creb.spectrum(fft_D, freq_D) #, scaling='power')
spd_H, pos_freqs_H = creb.spectrum(fft_H, freq_H) #, scaling='power')

# quickly plot the frequency spectrum for the Daily version
f, ax = plt.subplots(1,1)
ax.plot(pos_freqs_D, spd_D)
ax.set_xlabel('Frequency(units: cycles per length of domain)', fontsize=14)
ax.set_title('Spectral density', fontsize=16)


# quickly plot the frequency spectrum for the hourly version
f, ax = plt.subplots(1,1)
ax.plot(pos_freqs_H, spd_H)
ax.set_xlabel('Frequency(units: cycles per length of domain)', fontsize=14)
ax.set_title('Spectral density', fontsize=16)
# ax.set_xlim(0,750)

# Harmonics based on daily data
ds_Clim['Harmonic3']  = xr.DataArray(np.real(creb.inverse_fourier_transform(fft_D, freq_D, max_freq=3)), coords={'ModifiedOrdinalDay': ds_Clim.ModifiedOrdinalDay}, dims=['ModifiedOrdinalDay'])


# Harmonics based on Houlry data
ds_Clim['HourHarm3']  = xr.DataArray(np.real(creb.inverse_fourier_transform(fft_H, freq_H, max_freq=3)), coords={'ModifiedOrdinalHour': ds_Clim.ModifiedOrdinalHour}, dims=['ModifiedOrdinalHour'])
ds_Clim['HourHarm750']  = xr.DataArray(np.real(creb.inverse_fourier_transform(fft_H, freq_H, max_freq=750)), coords={'ModifiedOrdinalHour': ds_Clim.ModifiedOrdinalHour}, dims=['ModifiedOrdinalHour'])




#%%
# =============================================================================
# Now we do a comparison of climatology
# =============================================================================



# we start a new figure
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14,12))


# fix date-format
fig.autofmt_xdate()


# year_dates = pd.date_range('1990-05-01', periods=8760, freq='1h')
year_dates = pd.date_range('1990-01-01', periods=8760, freq='1h')
# 
# first subplot is the climatology comparison
ds_Clim.Daily.plot(ax=axes[0,0], label='Initial Daily', alpha=0.5, color='grey')
ds_Clim.RolClim30.plot(ax=axes[0,0],label='HRW-30', color='red')
ds_Clim.Harmonic3.plot(ax=axes[0,0],label='Harmonic 3rd', color='black')

# Comparison of rolling climatology
ds_Clim.Daily.plot(ax=axes[0,1], label='Initial Daily', alpha=0.2, color='grey')
ds_Clim.RolClim10.plot(ax=axes[0,1],label='HRW-10')
ds_Clim.RolClim20.plot(ax=axes[0,1],label='HRW-20', color='green')
ds_Clim.RolClim30.plot(ax=axes[0,1],label='HRW-30',color='red')
ds_Clim.RolClim42.plot(ax=axes[0,1],label='HRW-40', color='black')
ds_Clim.RolClim60.plot(ax=axes[0,1],label='HRW-60')
ds_Clim.RolClim90.plot(ax=axes[0,1],label='HRW-90')

# Comparison of rolling hours
axes[1,0].plot(year_dates[8:8760:24], ds_Clim.Hourly[8:8760:24],  alpha=0.5, color='grey')
axes[1,0].plot(year_dates[13:8760:24], ds_Clim.Hourly[13:8760:24],  label='Initial hourly', alpha=0.5, color='grey')
axes[1,0].plot(year_dates[8:8760:24], ds_Clim.RolHour42[8:8760:24],  color='black')
axes[1,0].plot(year_dates[8:8760:24], ds_Clim.RolHour42[13:8760:24], label='HRW-40', color='black')

# Comparison of Hourly version
axes[1,1].plot(year_dates[8:8760:24], ds_Clim.Hourly[8:8760:24],  alpha=0.5, color='tab:red')
axes[1,1].plot(year_dates[13:8760:24], ds_Clim.Hourly[13:8760:24], label='Initial hourly', alpha=0.5, color='grey')
axes[1,1].plot(year_dates[8:8760:24], ds_Clim.HourHarm750[8:8760:24], alpha=0.5, color='purple')
axes[1,1].plot(year_dates[13:8760:24], ds_Clim.HourHarm750[13:8760:24], label='750th Harmonic H',  alpha=0.5, color='purple')
axes[1,1].plot(year_dates[8:8760:24], ds_Clim.RolMOH42[8:8760:24], label='HRW-30 MOH', color='red')
axes[1,1].plot(year_dates[8:8760:24], ds_Clim.RolHour20[8:8760:24], color='green')
axes[1,1].plot(year_dates[13:8760:24], ds_Clim.RolHour20[13:8760:24], label='RHRW-20', color='green')
axes[1,1].plot(year_dates[8:8760:24], ds_Clim.RolHour42[8:8760:24],  color='black')
axes[1,1].plot(year_dates[13:8760:24], ds_Clim.RolHour42[13:8760:24], label='HRW-40', color='black')
axes[1,1].plot(year_dates[8:8760:24], ds_Clim.RolHour60[8:8760:24], color='pink')
axes[1,1].plot(year_dates[13:8760:24], ds_Clim.RolHour60[13:8760:24], label='HRW-60', color='pink')


# set the legend and labels
axes[0,0].legend(loc='upper right', fontsize='medium')
axes[0,1].legend(loc='upper right', fontsize='medium')
axes[1,0].legend(loc='upper right', fontsize='medium')
axes[1,1].legend(loc='upper right', fontsize='medium')

# axes[0,0].set_title('Daily climatology')
# axes[1,0].set_title('Hourly comparison')
# axes[0,1].set_title('Rolling comparison')
# axes[1,1].set_title('Hourly 2 comparison')



axes[0,0].set_xlabel('')
axes[0,1].set_xlabel('')
axes[1,0].set_xlabel('')
axes[1,1].set_xlabel('')


axes[0,0].set_ylabel('Solar potential [0-1]')
axes[0,1].set_ylabel('')
axes[1,0].set_ylabel('Solar potential [0-1]')
axes[1,1].set_ylabel('')


# formate the date-axis 
xfmt_years = mdates.DateFormatter('%b')
for a, b in [[0,0], [0,1], [1,0], [1,1]]:
    axes[a,b].xaxis.set_major_locator(mdates.MonthLocator(bymonth=(3, 6, 9, 12)))
    axes[a,b].xaxis.set_minor_locator(mdates.MonthLocator())
    axes[a,b].xaxis.set_major_formatter(xfmt_years)

# make it look better
plt.tight_layout()

plt.savefig(FOLDER_project+'results/publication/supplementary/Fig_ClimatologyComparison_SPV.png')
plt.savefig(FOLDER_project+'results/publication/supplementary/Fig_ClimatologyComparison_SPV.pdf')

plt.show()


#%%
# =============================================================================
# Final choice
# =============================================================================

# we start a new figure
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(14,6), sharey=True)

# selected hours
ds_Clim.Hourly[8:8760:24].plot(ax=axes[0], alpha=0.5, color='tab:red')
ds_Clim.Hourly[13:8760:24].plot(ax=axes[0], label='Initial daily', alpha=0.5, color='tab:red')
ds_Clim.RolHour42[8:8760:24].plot(ax=axes[0],  color='black')
ds_Clim.RolHour42[13:8760:24].plot(ax=axes[0], label='HRW-40', color='black')

# All hours
ds_Clim.Hourly[6:8760:24].plot(ax=axes[1], alpha=0.5, color='grey')
ds_Clim.Hourly[7:8760:24].plot(ax=axes[1], alpha=0.5, color='grey')
ds_Clim.Hourly[8:8760:24].plot(ax=axes[1], alpha=0.5, color='grey')
ds_Clim.Hourly[9:8760:24].plot(ax=axes[1], alpha=0.5, color='grey')
ds_Clim.Hourly[10:8760:24].plot(ax=axes[1], alpha=0.5, color='grey')
ds_Clim.Hourly[11:8760:24].plot(ax=axes[1], alpha=0.5, color='grey')
ds_Clim.Hourly[12:8760:24].plot(ax=axes[1], alpha=0.5, color='grey')
ds_Clim.Hourly[13:8760:24].plot(ax=axes[1], label='Initial hourly', alpha=0.5, color='grey')
ds_Clim.RolHour42[6:8760:24].plot(ax=axes[1],  color='tab:red')
ds_Clim.RolHour42[7:8760:24].plot(ax=axes[1],  color='tab:red')
ds_Clim.RolHour42[8:8760:24].plot(ax=axes[1],  color='tab:red')
ds_Clim.RolHour42[9:8760:24].plot(ax=axes[1],  color='tab:red')
ds_Clim.RolHour42[10:8760:24].plot(ax=axes[1],  color='tab:red')
ds_Clim.RolHour42[11:8760:24].plot(ax=axes[1],  color='tab:red')
ds_Clim.RolHour42[12:8760:24].plot(ax=axes[1],  color='tab:red')
ds_Clim.RolHour42[13:8760:24].plot(ax=axes[1], label='HRO-40', color='tab:red')



for year in np.arange(start=1980,stop=2021):
    axes[2].plot(ds.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31')), color='yellow', alpha=0.1)
ds_Clim.Hourly.plot(ax=axes[2], label='Initial hourly', alpha=0.5, color='tab:red')
ds_Clim.RolHour42.plot(ax=axes[2], label='HRW-40', linestyle='dashed', color='black')

axes[2].set_xlim(1200,1600)

# set the legend and labels
axes[0].legend(loc='upper right', fontsize='medium')


axes[0].set_ylabel('Climatology of RES-potential')
axes[1].set_ylabel('')
axes[2].set_ylabel('')

# make it look better
plt.tight_layout()

plt.savefig(FOLDER_project+'results/publication/supplementary/Fig_ClimatologyChoice_SPV.png')
plt.savefig(FOLDER_project+'results/publication/supplementary/Fig_ClimatologyChoice_SPV.pdf')

plt.show()