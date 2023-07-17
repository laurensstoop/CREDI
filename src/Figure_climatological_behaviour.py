# -*- coding: utf-8 -*-
"""
Spyder Editor

Created on 2023-03-30

Updated on 2023-07-17

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




# Region selection
REGION = 'NL01'
# REGION = 'SK00'
# REGION = 'SE02' 
# REGION = 'FR10'


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

ds_SPV = df_SPV[REGION].to_xarray()
ds_WON = df_WON[REGION].to_xarray()


#%%
# =============================================================================
# Fix time
# =============================================================================

# for easier figures we remove the leap days, see notes in RES-balance functions on how to keep this in
ds_SPV = ds_SPV.sel(time=~((ds_SPV.time.dt.month == 2) & (ds_SPV.time.dt.day == 29)))
ds_WON = ds_WON.sel(time=~((ds_WON.time.dt.month == 2) & (ds_WON.time.dt.day == 29)))



#%%
# =============================================================================
# Figure for climatological behaviour
# =============================================================================








# we start a new figure
# fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(17,10))
fig, axes = plt.subplot_mosaic([['a)', 'b)', 'c)'], ['d)', 'e)', 'f)']], figsize=(17,10))

# fix date-format
fig.autofmt_xdate()

# show year
ds_WON.sel(time=slice("2002-01-01", "2004-06-15")).plot(ax=axes['a)'], alpha=1, linewidth=0.25, color=colour_wind)
ds_SPV.sel(time=slice("2002-01-01", "2004-06-15")).plot(ax=axes['d)'], alpha=1, linewidth=0.25, color=colour_solar)

# Show subseasonal
ds_WON.sel(time=slice("2003-02-15", "2003-05-15")).plot(ax=axes['b)'], alpha=1, linewidth=0.5, color=colour_wind)
ds_SPV.sel(time=slice("2003-02-15", "2003-05-15")).plot(ax=axes['e)'], alpha=1, linewidth=0.5, color=colour_solar)

# show diurnal
ds_WON.sel(time=slice("2003-04-03", "2003-04-10")).plot(ax=axes['c)'], alpha=1, color=colour_wind)
ds_SPV.sel(time=slice("2003-04-03", "2003-04-10")).plot(ax=axes['f)'], alpha=1, color=colour_solar)


### Fix limits
axes['a)'].set_ylim(0,0.92)
axes['b)'].set_ylim(0,0.92)
axes['c)'].set_ylim(0,0.92)
axes['d)'].set_ylim(0,0.8)
axes['e)'].set_ylim(0,0.8)
axes['f)'].set_ylim(0,0.8)


## formate the date-axis 
# years
for a in ['a)', 'd)']:
    axes[a].xaxis.set_major_locator(mdates.YearLocator(base=1))
    axes[a].xaxis.set_minor_locator(mdates.MonthLocator(bymonth=(1,4,7,10)))
    axes[a].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    
# months
for a in ['b)', 'e)']:
    axes[a].xaxis.set_major_locator(mdates.MonthLocator(bymonth=(3,4,5)))
    axes[a].xaxis.set_minor_locator(mdates.DayLocator(interval=3))
    axes[a].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# Dates
for a in ['c)', 'f)']:
    axes[a].xaxis.set_major_locator(mdates.DayLocator(interval=3))
    axes[a].xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    axes[a].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

### Fix labels
# y-label
axes['a)'].set_ylabel('Wind potential [0-1]')
axes['d)'].set_ylabel('Solar potential [0-1]')
axes['b)'].set_ylabel('')
axes['e)'].set_ylabel('')
axes['c)'].set_ylabel('')
axes['f)'].set_ylabel('')

# x-label
axes['a)'].set_xlabel('')
axes['b)'].set_xlabel('')
axes['c)'].set_xlabel('')
axes['d)'].set_xlabel('')
axes['e)'].set_xlabel('')
axes['f)'].set_xlabel('')

# make it look better
plt.tight_layout()

# print subplot names
for label, ax in axes.items():
    # label physical distance in and down:
    trans = mtransforms.ScaledTranslation(10/72, -8/72, fig.dpi_scale_trans)
    ax.text(0.0, 1.0, label, transform=ax.transAxes + trans,
            fontsize='xx-large', verticalalignment='top')


if REGION == 'NLO1':
    plt.savefig(FOLDER_project+'results/publication/Climatological_Behaviour.png')
    plt.savefig(FOLDER_project+'results/publication/Climatological_Behaviour.pdf')
else:
    plt.savefig(FOLDER_project+'results/additional_regions/Climatological_Behaviour_'+REGION+'.png')
    plt.savefig(FOLDER_project+'results/additional_regions/Climatological_Behaviour_'+REGION+'.pdf')
plt.show()
