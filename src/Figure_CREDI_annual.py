# -*- coding: utf-8 -*-
"""
Spyder Editor

Created on 2023-03-30

Updated on 2023-06-19

@author: Laurens P. Stoop
"""


# load the dependencies
import numpy as np
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
ds_SPVanom = xr.open_dataset(FOLDER_project+'data/processed/ERA5_SPV_clim-anom_PECD_PEON_hrwCLIM40_additionalYear.nc')
ds_WONanom = xr.open_dataset(FOLDER_project+'data/processed/ERA5_WON_clim-anom_PECD_PEON_hrwCLIM40_additionalYear.nc')


#%% WIND
# =============================================================================
# Build pandas dataframe
# =============================================================================

# Initialize the dataframe
df_WEBi = pd.DataFrame()


# we want to see all years
for year in np.arange(start=1991,stop=2021):
    
    # Show the data for all the years
    if year == 1991:
        df_WEBi[str(year)] = ds_WONanom.anom.sel(time=slice(str(year)+'-05-01', str(year+1)+'-04-30')).cumsum().to_numpy()
    else:
        df_WEBi[str(year)] = ds_WONanom.anom.sel(time=slice(str(year)+'-05-01', str(year+1)+'-04-30')).cumsum().values

#%%
# =============================================================================
# Figure for interannual behaviour
# =============================================================================


# we start a new figure
# fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(13,5), sharey=True)
fig, axes = plt.subplot_mosaic([['a)', 'b)']], figsize=(13,5))


# fix date-format
fig.autofmt_xdate()

### First plot the initial yearly energy balance index and additional lines 

# show years
year_dates = pd.date_range('1990-05-01', periods=8760, freq='1h')

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
axes['a)'].axhline(y=0.0, color='gray', linestyle='--')
axes['b)'].axhline(y=0.0, color='gray', linestyle='--')

# # add window markers
# axes['a)'].vlines(x=['1991-01-01', '2020-12-31'], ymin=0, ymax=900, color='gray', alpha=0.6, linestyle='-.',  label='Climatology period')
# axes['b)'].vlines(x=['1991-01-01', '2020-12-31'], ymin=-250, ymax=0, color='gray', alpha=0.6, linestyle='-.', label='Climatology period')





# ## Now fix the nice stuff



# formate the date-axis 
xfmt_years = mdates.DateFormatter('%b')
for a in ['a)', 'b)']:
    axes[a].xaxis.set_major_locator(mdates.MonthLocator(bymonth=(3, 6, 9, 12)))
    axes[a].xaxis.set_minor_locator(mdates.MonthLocator())
    axes[a].xaxis.set_major_formatter(xfmt_years)




# # set the legend and labels
# axes['a)'].legend(loc='lower right', fontsize='medium')
axes['a)'].legend(loc='lower left', fontsize='medium')
axes['b)'].legend(loc='lower left', fontsize='medium')



axes['a)'].set_ylim(-410,410)
axes['b)'].set_ylim(-410,410)

# # Fix labels
axes['a)'].set_ylabel('Wind CREDI [FLH]')
# axes['b)'].set_ylabel('Solar Energy Balance index')



# # make it look better
plt.tight_layout()

# print subplot names
for label, ax in axes.items():
    # label physical distance in and down:
    trans = mtransforms.ScaledTranslation(10/72, -8/72, fig.dpi_scale_trans)
    ax.text(0.0, 1.0, label, transform=ax.transAxes + trans,
            fontsize='xx-large', verticalalignment='top')

plt.savefig(FOLDER_project+'results/publication/WindCREDI_annual.png')
plt.savefig(FOLDER_project+'results/publication/WindCREDI_annual.pdf')

plt.show()



#%% Solar
# =============================================================================
# Build pandas dataframe
# =============================================================================

# Initialize the dataframe
df_SEBi = pd.DataFrame()


# we want to see all years
for year in np.arange(start=1991,stop=2021):
    
    # Show the data for all the years
    if year == 1991:
        df_SEBi[str(year)] = ds_SPVanom.anom.sel(time=str(year)).cumsum().to_numpy()
    else:
        df_SEBi[str(year)] = ds_SPVanom.anom.sel(time=str(year)).cumsum().values

#%%
# =============================================================================
# Figure for interannual behaviour
# =============================================================================


# we start a new figure
# fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(13,5), sharey=True)
fig, axes = plt.subplot_mosaic([['a)', 'b)']], figsize=(13,5))


# fix date-format
fig.autofmt_xdate()

### First plot the initial yearly energy balance index and additional lines 

# show years
year_dates = pd.date_range('1990-01-01', periods=8760, freq='1h')

# we want to see all years
for year in np.arange(start=1991,stop=2021):
    
    # Show the data for all the years
    axes['a)'].plot(year_dates, df_SEBi[str(year)], color='orange', alpha=0.5, linewidth=1)
    
axes['a)'].plot(year_dates,df_SEBi['1996'], color='red', label='1996', alpha=0.9, linewidth=1)
axes['a)'].plot(year_dates,df_SEBi['1998'], color='green', label='1998', alpha=0.9, linewidth=1)
axes['a)'].plot(year_dates,df_SEBi['2003'], color='purple', label='2003', alpha=0.9, linewidth=1)
axes['a)'].plot(year_dates,df_SEBi['2016'], color='black', label='2016', alpha=0.9, linewidth=1)

axes['b)'].fill_between(
    year_dates, 
    df_SEBi.quantile(0,  axis=1),
    df_SEBi.quantile(1,  axis=1),
    color='orange', alpha=0.1, label='min-max'
    )

axes['b)'].fill_between(
    year_dates, 
    df_SEBi.quantile(0.1,  axis=1),
    df_SEBi.quantile(0.9,  axis=1),
    color='orange', alpha=0.2, label='10-90%'
    )

axes['b)'].fill_between(
    year_dates, 
    df_SEBi.quantile(0.25,  axis=1),
    df_SEBi.quantile(0.75,  axis=1),
    color='orange', alpha=0.4, label='25-75%'
    )

axes['b)'].plot(year_dates,df_SEBi.quantile(0.5,  axis=1), color='orange', label='50%')

# axes['b)'].plot(year_dates,df_SEBi['1996'], color='red', alpha=0.9, linewidth=1)
axes['b)'].plot(year_dates,df_SEBi['1998'], color='green', alpha=0.9, linewidth=1)
# axes['b)'].plot(year_dates,df_SEBi['2003'], color='purple', alpha=0.9, linewidth=1)
# axes['b)'].plot(year_dates,df_SEBi['2016'], color='black', label='2016', alpha=0.9, linewidth=1)


   
# # Add a line through zero
axes['a)'].axhline(y=0.0, color='gray', linestyle='--')
axes['b)'].axhline(y=0.0, color='gray', linestyle='--')

# # add window markers
# axes['a)'].vlines(x=['1991-01-01', '2020-12-31'], ymin=0, ymax=900, color='gray', alpha=0.6, linestyle='-.',  label='Climatology period')
# axes['b)'].vlines(x=['1991-01-01', '2020-12-31'], ymin=-250, ymax=0, color='gray', alpha=0.6, linestyle='-.', label='Climatology period')





# ## Now fix the nice stuff



# formate the date-axis 
xfmt_years = mdates.DateFormatter('%b')
for a in ['a)', 'b)']:
    axes[a].xaxis.set_major_locator(mdates.MonthLocator(bymonth=(3, 6, 9, 12)))
    axes[a].xaxis.set_minor_locator(mdates.MonthLocator())
    axes[a].xaxis.set_major_formatter(xfmt_years)




# # set the legend and labels
# axes['a)'].legend(loc='lower right', fontsize='medium')
axes['a)'].legend(loc='lower left', fontsize='medium')
axes['b)'].legend(loc='lower left', fontsize='medium')



axes['a)'].set_ylim(-110,110)
axes['b)'].set_ylim(-110,110)

# # Fix labels
axes['a)'].set_ylabel('Solar CREDI [FLH]')



# # make it look better
plt.tight_layout()

# print subplot names
for label, ax in axes.items():
    # label physical distance in and down:
    trans = mtransforms.ScaledTranslation(10/72, -8/72, fig.dpi_scale_trans)
    ax.text(0.0, 1.0, label, transform=ax.transAxes + trans,
            fontsize='xx-large', verticalalignment='top')

plt.savefig(FOLDER_project+'results/publication/SolarCREDI_annual.png')
plt.savefig(FOLDER_project+'results/publication/SolarCREDI_annual.pdf')

plt.show()

