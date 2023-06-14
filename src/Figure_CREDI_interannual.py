# -*- coding: utf-8 -*-
"""
Spyder Editor

Created on 2023-03-30

@author: Laurens P. Stoop
"""


# load the dependencies
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import matplotlib.dates as mdates
import matplotlib.transforms as mtransforms



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

#%%
# =============================================================================
# Get the data to open
# =============================================================================


# Store to disk
ds_SPVanom = xr.open_dataset(FOLDER_project+'data/processed/ERA5_SPV_clim-anom_PECD_PEON_hrwCLIM40.nc')
ds_WONanom = xr.open_dataset(FOLDER_project+'data/processed/ERA5_WON_clim-anom_PECD_PEON_hrwCLIM40.nc')




#%%
# =============================================================================
# Calculate the cumalative sum over the whole time period (CREBI for full time period)
# =============================================================================


# Make a CREBI dataset
ds_SEBi = xr.Dataset()
ds_WEBi = xr.Dataset()


# Calculate the energy balance over the full period, but adjust to value on 1991-01-01
ds_SEBi = ds_SPVanom.sel(time=slice('1991-01-01', '2020-12-31')).cumsum()
ds_WEBi = ds_WONanom.sel(time=slice('1991-01-01', '2020-12-31')).cumsum()

#%%
# =============================================================================
# Figure for interannual behaviour
# =============================================================================


# we start a new figure
fig, axes = plt.subplot_mosaic([['a)'], ['b)']], figsize=(15,8))
# fig, axes = plt.subplot_mosaic([['a)','b)']], figsize=(20,7))


# show years
year_dates = pd.date_range('1990-01-01', periods=8760, freq='1h')


# fix date-format
fig.autofmt_xdate()

### First plot the energy balance index and additional lines 

# we want to see the energy balance for all years
axes['a)'].plot(ds_SPVanom.time.sel(time=slice('1991-01-01', '2020-12-31')), ds_WEBi.anom, color=colour_wind_credi)
axes['b)'].plot(ds_SPVanom.time.sel(time=slice('1991-01-01', '2020-12-31')), ds_SEBi.anom,  color=colour_solar_credi)


# Add a line through zero
axes['a)'].axhline(y=0.0, color='gray', linestyle='-.')
axes['b)'].axhline(y=0.0, color='gray', linestyle='-.')

# add window markers
# axes['a)'].vlines(x=['1991-01-01', '2020-12-31'], ymin=0, ymax=900, color='gray', alpha=0.6, linestyle='-.',  label='Climatology period')
# axes['b)'].vlines(x=['1991-01-01', '2020-12-31'], ymin=-250, ymax=0, color='gray', alpha=0.6, linestyle='-.', label='Climatology period')



## Now fix the nice stuff

# Fix limits
# axes['a)'].set_ylim(-1250,900)
# axes['b)'].set_ylim(-250,500)


# formate the date-axis 
axes['a)'].xaxis.set_major_locator(mdates.YearLocator(base=5))
axes['b)'].xaxis.set_major_locator(mdates.YearLocator(base=5))
axes['a)'].xaxis.set_minor_locator(mdates.YearLocator(base=1))
axes['b)'].xaxis.set_minor_locator(mdates.YearLocator(base=1))
axes['a)'].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
axes['b)'].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

# Fix labels
axes['a)'].set_ylabel('Wind CREDI [FLH]')
axes['b)'].set_ylabel('Solar CREDI [FLH]')


# print subplot names
for label, ax in axes.items():
    # label physical distance in and down:
    trans = mtransforms.ScaledTranslation(10/72, -8/72, fig.dpi_scale_trans)
    ax.text(0.0, 1.0, label, transform=ax.transAxes + trans,
            fontsize='xx-large', verticalalignment='top')

# make it look better
plt.tight_layout()

plt.savefig(FOLDER_project+'results/publication/CREDI_interannual.png')
plt.savefig(FOLDER_project+'results/publication/CREDI_interannual.pdf')

plt.show()
