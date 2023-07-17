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
import CREDIfunctions as credi


REGION = 'NL01'

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


#%%
# =============================================================================
# Removing the 29th of febuary for simplicity
# =============================================================================

# for easier figures we remove the leap days, see notes in RES-balance functions on how to keep this in
ds_SPV = ds_SPV.sel(time=~((ds_SPV.time.dt.month == 2) & (ds_SPV.time.dt.day == 29))).sel(time=slice("1991-01-01", "2021-12-31"))
ds_WON = ds_WON.sel(time=~((ds_WON.time.dt.month == 2) & (ds_WON.time.dt.day == 29))).sel(time=slice("1991-01-01", "2021-12-31"))




#%%
# =============================================================================
# Getting a climatology definition
# =============================================================================

# Make the Climatology dataset
ds_ClimSPV = xr.Dataset()
ds_ClimWON = xr.Dataset()


# determine climatology for solar
ds_ClimSPV['Hourly'], OH = credi.Climatology_Hourly(ds_SPV, REGION)
ds_ClimSPV['HRW40'], OH = credi.Climatology_Hourly_Rolling(ds_SPV, REGION, RollingWindow=40)

# determine climatology for wind
ds_ClimWON['Hourly'], OH = credi.Climatology_Hourly(ds_WON, REGION)
ds_ClimWON['HRW40'], OH = credi.Climatology_Hourly_Rolling(ds_WON, REGION, RollingWindow=40)


#%%
# =============================================================================
# Calculating the anomaly & saving the data
# =============================================================================


# the anomaly is the potential - climatology
ds_SPV_save = xr.Dataset()
ds_WON_save = xr.Dataset()

# determine HRW anomaly 
ds_SPV_save['anom'] = ds_SPV[REGION].groupby(credi.Ordinal_Hour(ds_SPV)) - ds_ClimSPV.HRW40
ds_WON_save['anom'] = ds_WON[REGION].groupby(credi.Ordinal_Hour(ds_WON)) - ds_ClimWON.HRW40

# determine Hourly anomaly 
ds_SPV_save['anom_hourly'] = ds_SPV[REGION].groupby(credi.Ordinal_Hour(ds_SPV)) - ds_ClimSPV.Hourly
ds_WON_save['anom_hourly'] = ds_WON[REGION].groupby(credi.Ordinal_Hour(ds_WON)) - ds_ClimWON.Hourly

# Add the climatologies
ds_SPV_save['Hourly'] = ds_ClimSPV['Hourly']
ds_WON_save['Hourly'] = ds_ClimWON['Hourly']
ds_SPV_save['HRW40'] = ds_ClimSPV['HRW40']
ds_WON_save['HRW40'] = ds_ClimWON['HRW40']

# Add the base value
ds_SPV_save['SPV'] = ds_SPV.NL01
ds_WON_save['WON'] = ds_WON.NL01




#%%
# =============================================================================
# Saving the anomaly data
# =============================================================================

# Store to disk
ds_SPV_save.to_netcdf(FOLDER_project+'data/processed/ERA5_SPV_clim-anom_PECD_PEON_hrwCLIM40_additionalYear.nc')
ds_WON_save.to_netcdf(FOLDER_project+'data/processed/ERA5_WON_clim-anom_PECD_PEON_hrwCLIM40_additionalYear.nc')


