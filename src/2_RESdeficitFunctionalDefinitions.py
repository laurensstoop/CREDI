#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 12:21:57 2023

@author: Laurens P. Stoop
"""


# Load the dependencies
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr

#%%
# =============================================================================
# Functional definition of climatology based on the Modified Ordinal Day
# =============================================================================


# we want a function of climatology in which the 29t of february is counted correctly
def Climatology_MOD(InputDataSet, SelectedZone):

    # Method to get a neat definition of the day of the year, based on https://github.com/pydata/xarray/issues/1844#issuecomment-418188977
    not_leap_year = xr.DataArray(~InputDataSet.indexes['time'].is_leap_year, coords=InputDataSet.coords)
    march_or_later = InputDataSet.time.dt.month >= 3
    ordinal_day = InputDataSet.time.dt.dayofyear
    modified_ordinal_day = ordinal_day + (not_leap_year & march_or_later)
    modified_ordinal_day = modified_ordinal_day.rename('Modified Ordinal Day')
    
    # we can use this new modified ordinal day definition to get the correct climatology
    OutputDataArray = InputDataSet[SelectedZone].groupby(modified_ordinal_day).mean('time')
    
    # Now we return the output dataset that provides the anomaly 
    return OutputDataArray


# we want a function of in which the 29t of february is counted correctly
def Climatology_MOD_Rolling(InputDataSet, SelectedZone, RollingWindow=1008):

    # Method to get a neat definition of the day of the year, based on https://github.com/pydata/xarray/issues/1844#issuecomment-418188977
    not_leap_year = xr.DataArray(~InputDataSet.indexes['time'].is_leap_year, coords=InputDataSet.coords)
    march_or_later = InputDataSet.time.dt.month >= 3
    ordinal_day = InputDataSet.time.dt.dayofyear
    modified_ordinal_day = ordinal_day + (not_leap_year & march_or_later)
    modified_ordinal_day = modified_ordinal_day.rename('Modified Ordinal Day')
    
    # For the requested zone, we take the rolling centroid mean of 42 days (1008 hours)
    OutputDataArray = InputDataSet[SelectedZone].rolling(time=RollingWindow,center=True).mean()
    
    # On this smooth data we determine the climatology
    OutputDataArray = OutputDataArray.groupby(modified_ordinal_day).mean('time')
    

    return OutputDataArray

#%%
# =============================================================================
# 
# =============================================================================
