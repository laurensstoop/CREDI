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

#%%
# =============================================================================
# Get the data to open
# =============================================================================


# Store to disk
ds_SPVanom = xr.open_dataset(FOLDER_project+'data/processed/ERA5_SPVanom_PECD_PEON_hrwCLIM42.nc')
ds_WONanom = xr.open_dataset(FOLDER_project+'data/processed/ERA5_WONanom_PECD_PEON_hrwCLIM42.nc')


# fix date-format for plotting
ds_SPVanom['time'] = ds_SPVanom.indexes['time'].to_datetimeindex()
ds_WONanom['time'] = ds_WONanom.indexes['time'].to_datetimeindex()




#%%
# =============================================================================
# Build pandas dataframe
# =============================================================================

# Initialize the dataframe
df_CREBI = pd.DataFrame()


# we want to see all years
for year in np.arange(start=1991,stop=2021):
    
    # Show the data for all the years
    if year == 1991:
        df_CREBI[str(year)] = ds_SPVanom.NL01.sel(time=slice(str(year)+'-11-01', str(year+1)+'-10-31')).cumsum().to_numpy()
    else:
        df_CREBI[str(year)] = ds_SPVanom.NL01.sel(time=slice(str(year)+'-11-01', str(year+1)+'-10-31')).cumsum().values

#%%
# =============================================================================
# Figure for interannual behaviour
# =============================================================================

# colour = 'dodgerblue'
colour = 'orange'


# we start a new figure
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(13,5), sharey=True)


# fix date-format
fig.autofmt_xdate()

### First plot the initial yearly energy balance index and additional lines 

# show years
year_dates = pd.date_range('1990-11-01', periods=8760, freq='1h')

# we want to see all years
for year in np.arange(start=1991,stop=2021):
    
    # Show the data for all the years
    axes[0].plot(year_dates, df_CREBI[str(year)], color=colour, alpha=0.4, linewidth=1)
    
    
axes[0].plot(year_dates,df_CREBI['1996'], color='red', label='1996', alpha=0.9, linewidth=1)
axes[0].plot(year_dates,df_CREBI['2003'], color='purple', label='2003', alpha=0.9, linewidth=1)
    

axes[1].fill_between(
    year_dates, 
    df_CREBI.quantile(0,  axis=1),
    df_CREBI.quantile(1,  axis=1),
    color=colour, alpha=0.1, label='min-max'
    )

axes[1].fill_between(
    year_dates, 
    df_CREBI.quantile(0.1,  axis=1),
    df_CREBI.quantile(0.9,  axis=1),
    color=colour, alpha=0.2, label='10-90%'
    )

axes[1].fill_between(
    year_dates, 
    df_CREBI.quantile(0.25,  axis=1),
    df_CREBI.quantile(0.75,  axis=1),
    color=colour, alpha=0.4, label='25-75%'
    )

axes[1].plot(year_dates,df_CREBI.quantile(0.5,  axis=1), color=colour, label='50%')

axes[1].plot(year_dates,df_CREBI['1996'], color='red', label='1996', alpha=0.9, linewidth=1)
axes[1].plot(year_dates,df_CREBI['2003'], color='purple', label='2003', alpha=0.9, linewidth=1)

   
# # Add a line through zero
# axes[0].axhline(y=0.0, color='gray', linestyle='--')
# axes[1].axhline(y=0.0, color='gray', linestyle='--')

# # add window markers
# axes[0].vlines(x=['1991-01-01', '2020-12-31'], ymin=0, ymax=900, color='gray', alpha=0.6, linestyle='-.',  label='Climatology period')
# axes[1].vlines(x=['1991-01-01', '2020-12-31'], ymin=-250, ymax=0, color='gray', alpha=0.6, linestyle='-.', label='Climatology period')





## Now fix the nice stuff

# formate the date-axis 
xfmt_years = mdates.DateFormatter('%b')
for a in [0,1]:
    axes[a].xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 4, 7, 10)))
    axes[a].xaxis.set_minor_locator(mdates.MonthLocator())
    axes[a].xaxis.set_major_formatter(xfmt_years)




# # set the legend and labels
axes[1].legend(loc='lower left', fontsize='medium')



# # Fix labels
# axes[0].set_ylabel('Wind Energy Balance index')
axes[0].set_ylabel('Solar Energy Balance index')



# # make it look better
plt.tight_layout()

plt.savefig(FOLDER_project+'results/publication/Annual_SEBI_Nov.png')
plt.savefig(FOLDER_project+'results/publication/Annual_SEBI_Nov.pdf')

plt.show()
