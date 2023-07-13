# -*- coding: utf-8 -*-
"""
Spyder Editor

Created on 2023-03-30

Updated on 2023-06-14

@author: Laurens P. Stoop
"""


# load the dependencies
import numpy as np
import pandas as pd
import xarray as xr
import sys
from datetime import datetime


# The scripts
sys.path.append('/Users/3986209/Library/CloudStorage/OneDrive-UniversiteitUtrecht/Projects/ccmetrics/src/')
import CREBfunctions as creb


REGION = 'NL01'






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
ds_SPVanom = xr.open_dataset(FOLDER_project+'data/processed/ERA5_SPV_clim-anom_PECD_PEON_hrwCLIM40_additionalYear.nc').anom
ds_WONanom = xr.open_dataset(FOLDER_project+'data/processed/ERA5_WON_clim-anom_PECD_PEON_hrwCLIM40_additionalYear.nc').anom




#%%

ds_WS = xr.Dataset()

r = ds_WONanom.rolling(time=366)

ds_WS['anom_event'] = r.construct(time = "event_hour", stride=24)






#%%



r = ds_WONanom.rolling(time=366)

p = r.construct(time = "event_day", stride=24)









#%%
# =============================================================================
# Saving the anomaly data
# =============================================================================

# # Store to disk
# ds_SPV_save.to_netcdf(FOLDER_project+'data/processed/ERA5_SPV_clim-anom_PECD_PEON_hrwCLIM40_additionalYear.nc')
# ds_WON_save.to_netcdf(FOLDER_project+'data/processed/ERA5_WON_clim-anom_PECD_PEON_hrwCLIM40_additionalYear.nc')


