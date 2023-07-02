# -*- coding: utf-8 -*-
"""
Spyder Editor

Created on 2023-06-19

Updated on 2023-06-26

@author: Laurens P. Stoop
"""


# load the dependencies
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import matplotlib.dates as mdates
import matplotlib.transforms as mtransforms
from datetime import timedelta
import datetime



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
ds_SPVanom = xr.open_dataset(FOLDER_project+'data/processed/ERA5_SPV_clim-anom_PECD_PEON_hrwCLIM40_additionalYear.nc')
ds_WONanom = xr.open_dataset(FOLDER_project+'data/processed/ERA5_WON_clim-anom_PECD_PEON_hrwCLIM40_additionalYear.nc')


#%% WIND
# =============================================================================
# Winter WIND
# =============================================================================

# Initialize the dataframe
df_WsS = pd.DataFrame()
ds_WsSi = xr.Dataset()

# we want to see all years
for year in np.arange(start=1991,stop=2021):
    
    for seasonday in np.arange(1): #212
        # Show the data for all the years
        
        date_seasonday = datetime.datetime(year,9,1)+timedelta(days=int(seasonday))
        date_seasonday_14 = datetime.datetime(year,9,14,23)+timedelta(days=int(seasonday))
        
        if year == 1991:
            ds_WsSi[str(date_seasonday)] = ds_WONanom.anom.sel(
                time=slice(date_seasonday, date_seasonday_14)).cumsum()
        else:
            ds_WsSi[str(date_seasonday)] = ds_WONanom.anom.sel(
                time=slice(date_seasonday, date_seasonday_14)).cumsum().values

Dimension = start_date +& hours since initial



# xr.DataArray(data, coords=[times, locs], dims=["time", "space"])
# pd.date_range("2000-01-01", periods=4)
# ["IA", "IL", "IN"]


#%%

ds_subsW = xr.Dataset()

# show years
year_dates = pd.date_range('1999-09-01',periods=5088, freq='1h')

# we want to see all years




# we start a new figure
# fig, axes = plt.subplot_mosaic([['a)', 'b)']], figsize=(13,5))
fig, axes = plt.subplot_mosaic([['a)', 'b)', 'c)']], figsize=(18,5))


# fix date-format
fig.autofmt_xdate()

### First plot the initial yearly energy balance index and additional lines 


# we want to see all years
for year in np.arange(start=1991,stop=2021):
    
    # Show the data for all the years
    axes['a)'].plot(year_dates, df_WEBi[str(year)], color='dodgerblue', alpha=0.3, linewidth=1)
    
axes['a)'].plot(year_dates,df_WEBi['1996'], color='red', label='1996', alpha=0.9, linewidth=1)
axes['a)'].plot(year_dates,df_WEBi['1998'], color='green', label='1996', alpha=0.9, linewidth=1)
axes['a)'].plot(year_dates,df_WEBi['2003'], color='purple', label='2003', alpha=0.9, linewidth=1)
axes['a)'].plot(year_dates,df_WEBi['2016'], color='black', label='2016', alpha=0.9, linewidth=1)

axes['b)'].fill_between(
    year_dates, 
    df_WEBi.quantile(0,  axis=1),
    df_WEBi.quantile(1,  axis=1),
    color='dodgerblue', alpha=0.05, label='min-max'
    )

axes['b)'].fill_between(
    year_dates, 
    df_WEBi.quantile(0.1,  axis=1),
    df_WEBi.quantile(0.9,  axis=1),
    color='dodgerblue', alpha=0.1, label='10-90%'
    )

axes['b)'].fill_between(
    year_dates, 
    df_WEBi.quantile(0.25,  axis=1),
    df_WEBi.quantile(0.75,  axis=1),
    color='dodgerblue', alpha=0.2, label='25-75%'
    )

axes['b)'].plot(year_dates,df_WEBi.quantile(0.5,  axis=1), color='dodgerblue', label='50%')

axes['b)'].plot(year_dates,df_WEBi['1996'], color='red', alpha=0.9, linewidth=1)
# axes['b)'].plot(year_dates,df_WEBi['1998'], color='green', alpha=0.9, linewidth=1)
# axes['b)'].plot(year_dates,df_WEBi['2003'], color='purple', alpha=0.9, linewidth=1)
# axes['b)'].plot(year_dates,df_WEBi['2016'], color='black', label='2016', alpha=0.9, linewidth=1)


   
# # Add a line through zero
# axes['a)'].axhline(y=0.0, color='gray', linestyle='--')
# axes['b)'].axhline(y=0.0, color='gray', linestyle='--')

# # add window markers
# axes['a)'].vlines(x=['1991-01-01', '2020-12-31'], ymin=0, ymax=900, color='gray', alpha=0.6, linestyle='-.',  label='Climatology period')
# axes['b)'].vlines(x=['1991-01-01', '2020-12-31'], ymin=-250, ymax=0, color='gray', alpha=0.6, linestyle='-.', label='Climatology period')





# ## Now fix the nice stuff



# # formate the date-axis 
# xfmt_years = mdates.DateFormatter('%b')
# for a in ['a)', 'b)']:
#     axes[a].xaxis.set_major_locator(mdates.MonthLocator(interval=1))
#     axes[a].xaxis.set_minor_locator(mdates.MonthLocator())
#     axes[a].xaxis.set_major_formatter(xfmt_years)




# # # set the legend and labels
# # axes['a)'].legend(loc='lower right', fontsize='medium')
# axes['a)'].legend(loc='lower left', fontsize='medium')
# axes['b)'].legend(loc='lower left', fontsize='medium')



# axes['a)'].set_ylim(-410,410)
# axes['b)'].set_ylim(-410,410)

# # # Fix labels
# axes['a)'].set_ylabel('Wind CREDI [FLH]')
# # axes['b)'].set_ylabel('Solar Energy Balance index')



# # # make it look better
# plt.tight_layout()


# # print subplot names
# for label, ax in axes.items():
#     # label physical distance in and down:
#     trans = mtransforms.ScaledTranslation(10/72, -8/72, fig.dpi_scale_trans)
#     ax.text(0.0, 1.0, label, transform=ax.transAxes + trans,
#             fontsize='xx-large', verticalalignment='top')

# plt.savefig(FOLDER_project+'results/publication/WindCREDI_seasonal-winter.png')
# plt.savefig(FOLDER_project+'results/publication/WindCREDI_seasonal-winter.pdf')

plt.show()

