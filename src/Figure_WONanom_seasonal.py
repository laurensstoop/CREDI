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
FOLDER_drive='/Users/3986209/Library/CloudStorage/OneDrive-UniversiteitUtrecht/'
FOLDER_project=FOLDER_drive+'Projects/ccmetrics/'
FOLDER_pecd = FOLDER_drive+'Data/PECD/HIST/ENER/'

# file name
fileName_SPV = 'SPV/PEON/H_ERA5_ECMW_T639_SPV_0000m_Pecd_PEON_S198001010000_E202112312300_CFR_TIM_01h_NA-_noc_org_NA_NA---_NA---_PhM01.csv'
fileName_WON = 'WON/PEON/H_ERA5_ECMW_T639_WON_NA---_Pecd_PEON_S198001010000_E202112312300_CFR_TIM_01h_NA-_noc_org_30_NA---_NA---_PhM01.csv'



# fix date-format for plotting
ds_SPVanom['time'] = ds_SPVanom.indexes['time'].to_datetimeindex()
ds_WONanom['time'] = ds_WONanom.indexes['time'].to_datetimeindex()


#%%
# =============================================================================
# Go to pandas
# =============================================================================

df_WONanom = ds_WONanom.NL01.to_pandas()
df_SPVanom = ds_SPVanom.NL01.to_pandas()


# Create a Seasonal Dictionary that will map months to seasons
SeasonDict = {11: 'Winter', 12: 'Winter', 1: 'Winter', 2: 'Winter', 3: 'Winter', 4: 'None', 5: 'Summer', 6: 'Summer', 7: 'Summer', \
8: 'Summer', 9: 'Summer', 10: 'None'}

# Write a function that will be used to group the data
def GroupFunc(x):
    return SeasonDict[x.month]


Grouped = df_WONanom.groupby(GroupFunc)




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
        df_CREBI[str(year)] = ds_WONanom.NL01.sel(time=slice(str(year)+'-11-01', str(year+1)+'-03-31')).to_numpy()
    else:
        df_CREBI[str(year)] = ds_WONanom.NL01.sel(time=slice(str(year)+'-11-01', str(year+1)+'-03-31')).values


# df_anom['Season'] = df_anom['time'].dt.month.apply(lambda x : MonthToSeason(x))

#%%
# =============================================================================
# Figure for interannual behaviour
# =============================================================================

colour = 'dodgerblue'
# colour = 'orange'


# we start a new figure
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(13,5), sharey=True)


# fix date-format
fig.autofmt_xdate()

### First plot the initial yearly energy balance index and additional lines 

# show years
year_dates = pd.date_range('1991-11-01', periods=3624, freq='1h')

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
    axes[a].xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 2, 3, 4, 11, 12)))
    axes[a].xaxis.set_minor_locator(mdates.MonthLocator())
    axes[a].xaxis.set_major_formatter(xfmt_years)




# # set the legend and labels
axes[1].legend(loc='lower left', fontsize='medium')



# # Fix labels
axes[0].set_ylabel('Wind Energy anomaly')
# axes[0].set_ylabel('Solar Energy Balance index')



# # make it look better
plt.tight_layout()

plt.savefig(FOLDER_project+'results/publication/Seasonal_winter_WEBI.png')
plt.savefig(FOLDER_project+'results/publication/Seasonal_winter_WEBI.pdf')

plt.show()
