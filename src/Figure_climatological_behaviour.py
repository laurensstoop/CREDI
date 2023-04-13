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



#%%
# =============================================================================
# Figure for climatological behaviour
# =============================================================================


# we start a new figure
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(17,10))

# fix date-format
fig.autofmt_xdate()

# show year
ds_WON.NL01[193000:215000].plot(ax=axes[0,0], alpha=0.5, color='dodgerblue')
ds_SPV.NL01[193000:215000].plot(ax=axes[1,0], alpha=0.5, color='orange')

# Show subseasonal
ds_WON.NL01[202500:205000].plot(ax=axes[0,1], alpha=0.5, color='dodgerblue')
ds_SPV.NL01[202500:205000].plot(ax=axes[1,1], alpha=0.5, color='orange')

# show diurnal
ds_WON.NL01[203834:204000].plot(ax=axes[0,2], alpha=0.5, color='dodgerblue')
ds_SPV.NL01[203834:204000].plot(ax=axes[1,2], alpha=0.5, color='orange')


### Fix limits
axes[0,0].set_ylim(0,0.92)
axes[0,1].set_ylim(0,0.92)
axes[0,2].set_ylim(0,0.92)
axes[1,0].set_ylim(0,0.75)
axes[1,1].set_ylim(0,0.75)
axes[1,2].set_ylim(0,0.75)

# set the legend and labels
# axes[0].legend(loc='upper right', fontsize='medium')



### formate the date-axis 
# years
for a, b in [[0,0], [1,0]]:
    axes[a,b].xaxis.set_major_locator(mdates.YearLocator(base=1))
    # axes[a,b].xaxis.set_minor_locator(mdates.MonthLocator())
    axes[a,b].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    
# months
for a, b in [[0,1], [1,1]]:
    axes[a,b].xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    axes[a,b].xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
    axes[a,b].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# Dates
for a, b in [[0,2], [1,2]]:
    axes[a,b].xaxis.set_major_locator(mdates.DayLocator(interval=3))
    axes[a,b].xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    axes[a,b].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

### Fix labels
# y-label
axes[0,0].set_ylabel('Wind potential')
axes[1,0].set_ylabel('Solar potential')
axes[0,1].set_ylabel('')
axes[1,1].set_ylabel('')
axes[0,2].set_ylabel('')
axes[1,2].set_ylabel('')

# x-label
axes[0,0].set_xlabel('')
axes[0,1].set_xlabel('')
axes[0,2].set_xlabel('')

# make it look better
plt.tight_layout()

plt.savefig(FOLDER_project+'results/publication/Climatological_Behaviour.png')
plt.savefig(FOLDER_project+'results/publication/Climatological_Behaviour.pdf')

plt.show()
