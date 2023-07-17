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
import matplotlib.transforms as mtransforms
from datetime import timedelta

import matplotlib.dates as mdates



# Set general definitions of figures 
import matplotlib.pylab as pylab
params = {'legend.fontsize': 'xx-large',
          'figure.figsize': (10, 7),
         'axes.labelsize': 'xx-large',
         'axes.titlesize':'xx-large',
         'xtick.labelsize':'xx-large',
         'ytick.labelsize':'xx-large'}
pylab.rcParams.update(params)

## Colour definitions
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

#%%
# =============================================================================
# Choices and parameter settings
# =============================================================================

## Length of the period to consider for CREDI assessment (in hours)
# add 1 to get indexes that make sense 
# PERIOD_length = 337 # 14 days
# PERIOD_length = 241 # 10 days
PERIOD_length = 193 # 8 days

# Sampling of the period (in hours)
PERIOD_stride = 24


# Events selected (max value for PECDv4.0 ~ 1948-1967)
EVENTS_topk = 1800

# Definition of season start (number of the month)
SEASON_start_WON = 5



#%%
# =============================================================================
# Data definition & loading
# =============================================================================

# Define some folders
FOLDER_project='/Users/3986209/Library/CloudStorage/OneDrive-UniversiteitUtrecht/Projects/ccmetrics/'


## Retrieve from disk
# Solar
ds_SPVanom = xr.open_dataset(FOLDER_project+'data/processed/ERA5_SPV_clim-anom_PECD_PEON_hrwCLIM40_additionalYear.nc')
# Wind
ds_WONanom = xr.open_dataset(FOLDER_project+'data/processed/ERA5_WON_clim-anom_PECD_PEON_hrwCLIM40_additionalYear.nc')




#%%
# =============================================================================
# Create a new subseason dataset with the period length (~10 seconds)
# =============================================================================

# main dataset
ds = xr.Dataset()

## Adding in the data
# Solar
ds['SPVanom_event'] = ds_SPVanom.rolling(time=PERIOD_length).construct(time = "event_hour", stride=PERIOD_stride).anom
ds['SPV_event'] = ds_SPVanom.rolling(time=PERIOD_length).construct(time = "event_hour", stride=PERIOD_stride).SPV
ds['CREDI_spv'] = ds.SPVanom_event.cumsum(dim='event_hour')

# Wind
ds['WONanom_event'] = ds_WONanom.rolling(time=PERIOD_length).construct(time = "event_hour", stride=PERIOD_stride).anom
ds['WON_event'] = ds_WONanom.rolling(time=PERIOD_length).construct(time = "event_hour", stride=PERIOD_stride).WON
ds['CREDI_won'] = ds.WONanom_event.cumsum(dim='event_hour')


# Assign coordinates to event_hour (in timedelta's)
# ds = ds.assign_coords(event_hour=pd.to_timedelta(range(PERIOD_length), unit='h'))


#%% 
# =============================================================================
# A few quick figures
# =============================================================================




#%% Lineplot for each timestep (slow: ~15 seconds total)


# Solar
ds.CREDI_spv.plot.line(x='event_hour', add_legend=False)
plt.show()
# Wind
ds.CREDI_won.plot.line(x='event_hour', add_legend=False)
plt.show()






#%% event filter ideas 
# =============================================================================
# Event filtering method
# =============================================================================


## return index of max value
# Not used, but can be handy
ds.cumsum(dim='event_hour').sel(event_hour=PERIOD_length-1).idxmax()



## Generate event list for highest/lowest events 

# Generate dataset of last event hours
df = pd.DataFrame()
# Solar
df['SPV_event_credi'] = ds.SPVanom_event.cumsum(dim='event_hour').sel(event_hour=PERIOD_length-1).to_pandas()
# Wind
df['WON_event_credi'] = ds.WONanom_event.cumsum(dim='event_hour').sel(event_hour=PERIOD_length-1).to_pandas()

# Select the smallest 100K events (technically all are listed as we do not drop data)
# Solar
df_sort_SPV = df.nsmallest(len(df), 'SPV_event_credi', keep='all')
# Wind
df_sort_WON = df.nsmallest(len(df), 'WON_event_credi', keep='all')
# df = df.nlargest(100000, 'anom_event', keep='all')


## Filter the full dataset to only get the top-k events
## dropp all less then 5 days away 
# not used, but shows example
df_sort_SPV.drop(df_sort_SPV.loc[(abs(df_sort_SPV.index - df_sort_SPV.index[0]) < timedelta(5))].index)

# Make event list
# Solar
SPV_event_date = []
SPV_event_value = []
# Wind
WON_event_date = []
WON_event_value = []

for i in np.arange(EVENTS_topk):
    
    ## add the top-k event to the list
    # Solar
    SPV_event_date.append(df_sort_SPV.iloc[0].name)
    SPV_event_value.append(df_sort_SPV.iloc[0,0])
    # Wind
    WON_event_date.append(df_sort_WON.iloc[0].name)
    WON_event_value.append(df_sort_WON.iloc[0,1])
    
    ## now filter this event and all others
    # Solar
    df_sort_SPV = df_sort_SPV.drop(df_sort_SPV.loc[(abs(df_sort_SPV.index - df_sort_SPV.index[0]) < timedelta(5))].index)
    # Wind
    df_sort_WON = df_sort_WON.drop(df_sort_WON.loc[(abs(df_sort_WON.index - df_sort_WON.index[0]) < timedelta(5))].index)
    



#%%
# =============================================================================
# Save events to disk
# =============================================================================

# create a common file
df_save = pd.DataFrame()

## Add data
df_save['SPV_event_date']= pd.DataFrame(SPV_event_date)
df_save['SPV_event_value']= pd.DataFrame(SPV_event_value)
# Wind
df_save['WON_event_date']= pd.DataFrame(WON_event_date)
df_save['WON_event_value']= pd.DataFrame(WON_event_value)

# Store to disk
df_save.to_csv(FOLDER_project+'data/processed/ERA5_CREDI_'+str(int((PERIOD_length-1)/24))+'days_PECDv4.0_PEON_hrwCLIM40_additionalYear.csv', sep=';', decimal=',', header='true', date_format='%Y-%m-%d')




#%%
# =============================================================================
# Figures
# =============================================================================

# Coincidence of CREDI extremes
df.plot.scatter(x='WON_event_credi', y='SPV_event_credi')
plt.show()

# Coincidence
for i in range(10):
    ds.sel(time=WON_event_date[i]).SPVanom_event.cumsum().plot(label=str(WON_event_date[i].year)+' Rank:'+str(i))
ds.sel(time=WON_event_date[8]).SPVanom_event.cumsum().plot(c='black', label=str(WON_event_date[8].year)+' Rank:'+str(8))
plt.legend(loc='upper left', fontsize='small')
plt.show()





#%%

# time-series van anom tijdens event
ds.sel(time=WON_event_date[0]).WONanom_event.plot()
plt.show()


# CREDI tijdens event
ds.sel(time=WON_event_date[0]).WONanom_event.cumsum().plot()
plt.show()


# WON tijdens event
ds.sel(time=WON_event_date[0]).WON_event.plot()
plt.show()

# for a histogram of the dates
# https://stackoverflow.com/questions/27365467/can-pandas-plot-a-histogram-of-dates





#%%
# =============================================================================
# Figure for short term behaviour
# =============================================================================


# we start a new figure
# fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(13,5), sharey=True)
fig, axes = plt.subplot_mosaic([['a)', 'b)']], figsize=(13,5))


# fix date-format
fig.autofmt_xdate()

### First plot the initial yearly energy balance index and additional lines 

# Get usable x-axis
year_dates = pd.date_range('1990-04-30', periods=PERIOD_length, freq='1h')
# year_dates = pd.to_timedelta(range(PERIOD_length), unit='h')
    
# Show the data for all the years
for event_dates in WON_event_date:
    
    axes['a)'].plot(
        year_dates,
        ds.CREDI_won.sel(time=event_dates),
        color='dodgerblue', 
        alpha=0.5, 
        linewidth=0.3)
   
# Show selected years 
for year_selected, year_colour in zip([1996,1998,2003,2016], ['red', 'green','purple','black']):

    # look at sub-top years
    for date_of_events in WON_event_date[0:50]:
        
        # If the date of the event is after may in the year selected plot it
        if date_of_events.year == year_selected and date_of_events.month > SEASON_start_WON:
            axes['a)'].plot(
                year_dates,
                ds.sel(time=date_of_events).CREDI_won.values, 
                color=year_colour, 
                label=str(year_selected), 
                alpha=0.9, 
                linewidth=1
                )
        
        # if the date of the events is before may in the year+1 selected (second half of season) plot it 
        elif date_of_events.year == year_selected+1 and date_of_events.month <= SEASON_start_WON:
            axes['a)'].plot(
                year_dates,
                ds.sel(time=date_of_events).CREDI_won.values,
                color=year_colour, 
                label=str(year_selected),
                alpha=0.9, 
                linewidth=1)




axes['b)'].fill_between(
    year_dates, 
    ds.CREDI_won.sel(time=WON_event_date).quantile(0, dim='time'),
    ds.CREDI_won.sel(time=WON_event_date).quantile(1, dim='time'),
    color='dodgerblue', alpha=0.05, label='min-max'
    )

axes['b)'].fill_between(
    year_dates, 
    ds.CREDI_won.sel(time=WON_event_date).quantile(0.1, dim='time'),
    ds.CREDI_won.sel(time=WON_event_date).quantile(0.9, dim='time'),
    color='dodgerblue', alpha=0.1, label='10-90%'
    )

axes['b)'].fill_between(
    year_dates,
    ds.CREDI_won.sel(time=WON_event_date).quantile(0.25, dim='time'),
    ds.CREDI_won.sel(time=WON_event_date).quantile(0.75, dim='time'),
    color='dodgerblue', alpha=0.2, label='25-75%'
    )

axes['b)'].plot(year_dates,ds.CREDI_won.sel(time=WON_event_date).quantile(0.5, dim='time'), color='dodgerblue', label='50%')

# Show selected years 
for year_selected, year_colour in zip([1996,2016], ['red','black']):

    # look at sub-top years
    for date_of_events in WON_event_date[0:50]:
        
        # If the date of the event is after may in the year selected plot it
        if date_of_events.year == year_selected and date_of_events.month > SEASON_start_WON:
            axes['b)'].plot(year_dates,ds.sel(time=date_of_events).WONanom_event.cumsum(dim='event_hour').values, color=year_colour, label=str(year_selected), alpha=0.9, linewidth=1)
        
        # if the date of the events is before may in the year+1 selected (second half of season) plot it 
        elif date_of_events.year == year_selected+1 and date_of_events.month <= SEASON_start_WON:
            axes['b)'].plot(year_dates,ds.sel(time=date_of_events).WONanom_event.cumsum(dim='event_hour').values, color=year_colour, label=str(year_selected), alpha=0.9, linewidth=1)


## Now fix the nice stuff




# formate the date-axis 
xfmt_years = mdates.DateFormatter('%d')
for a in ['a)', 'b)']:
    axes[a].xaxis.set_major_locator(mdates.DayLocator(bymonthday=(1,3,5,7)))
    axes[a].xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    axes[a].xaxis.set_major_formatter(xfmt_years)



## Legends
# get legend handles and their corresponding labels
handles_a, labels_a = axes['a)'].get_legend_handles_labels()
handles_b, labels_b = axes['b)'].get_legend_handles_labels()

# zip labels as keys and handles as values into a dictionary, ...
# so only unique labels would be stored 
dict_of_labels_a = dict(zip(labels_a, handles_a))
dict_of_labels_b = dict(zip(labels_b, handles_b))


# set the legend and labels
axes['a)'].legend(dict_of_labels_a.values(), dict_of_labels_a.keys(),loc='upper right', fontsize='medium')
axes['b)'].legend(dict_of_labels_b.values(), dict_of_labels_b.keys(),loc='upper right', fontsize='medium')


#  Set limits
axes['a)'].set_ylim(-75,50)
axes['b)'].set_ylim(-75,50)

# Fix labels
axes['a)'].set_ylabel('Wind CREDI [FLH]')
axes['b)'].set_ylabel('')




# make it look better
plt.tight_layout()

# print subplot names
for label, ax in axes.items():
    # label physical distance in and down:
    trans = mtransforms.ScaledTranslation(10/72, -8/72, fig.dpi_scale_trans)
    ax.text(0.0, 1.0, label, transform=ax.transAxes + trans,
            fontsize='xx-large', verticalalignment='top')

plt.savefig(FOLDER_project+'results/publication/WindCREDI_shortterm.png')
plt.savefig(FOLDER_project+'results/publication/WindCREDI_shortterm.pdf')

plt.show()


#%%
# =============================================================================
# Figure for short term behaviour
# =============================================================================


# we start a new figure
# fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(13,5), sharey=True)
fig, axes = plt.subplot_mosaic([['a)', 'b)']], figsize=(13,5))


# fix date-format
fig.autofmt_xdate()

### First plot the initial yearly energy balance index and additional lines 

# Get usable x-axis
year_dates = pd.date_range('1990-04-30', periods=PERIOD_length, freq='1h')
# year_dates = pd.to_timedelta(range(PERIOD_length), unit='h')
    
# Show the data for all the years
for event_dates in WON_event_date:
    
    axes['a)'].plot(
        year_dates,
        ds.CREDI_won.sel(time=event_dates),
        color='dodgerblue', 
        alpha=0.5, 
        linewidth=0.3)
   
# Show selected years 
for year_selected, year_colour in zip([1996,1998,2003,2016], ['red', 'green','purple','black']):

    # look at sub-top years
    for date_of_events in WON_event_date[0:50]:
        
        # If the date of the event is after may in the year selected plot it
        if date_of_events.year == year_selected and date_of_events.month > SEASON_start_WON:
            axes['a)'].plot(
                year_dates,
                ds.sel(time=date_of_events).CREDI_won.values, 
                color=year_colour, 
                label=str(year_selected), 
                alpha=0.9, 
                linewidth=1
                )
        
        # if the date of the events is before may in the year+1 selected (second half of season) plot it 
        elif date_of_events.year == year_selected+1 and date_of_events.month <= SEASON_start_WON:
            axes['a)'].plot(
                year_dates,
                ds.sel(time=date_of_events).CREDI_won.values,
                color=year_colour, 
                label=str(year_selected),
                alpha=0.9, 
                linewidth=1)




axes['b)'].fill_between(
    year_dates, 
    ds.WON_event.sel(time=WON_event_date).quantile(0, dim='time'),
    ds.WON_event.sel(time=WON_event_date).quantile(1, dim='time'),
    color='dodgerblue', alpha=0.05, label='min-max'
    )

axes['b)'].fill_between(
    year_dates, 
    ds.WON_event.sel(time=WON_event_date).quantile(0.1, dim='time'),
    ds.WON_event.sel(time=WON_event_date).quantile(0.9, dim='time'),
    color='dodgerblue', alpha=0.1, label='10-90%'
    )

axes['b)'].fill_between(
    year_dates,
    ds.WON_event.sel(time=WON_event_date).quantile(0.25, dim='time'),
    ds.WON_event.sel(time=WON_event_date).quantile(0.75, dim='time'),
    color='dodgerblue', alpha=0.2, label='25-75%'
    )

axes['b)'].plot(year_dates,ds.WON_event.sel(time=WON_event_date).quantile(0.5, dim='time'), color='dodgerblue', label='50%')

# Show selected years 
for year_selected, year_colour in zip([1996,2016], ['red','black']):

    # look at sub-top years
    for date_of_events in WON_event_date[0:50]:
        
        # If the date of the event is after may in the year selected plot it
        if date_of_events.year == year_selected and date_of_events.month > SEASON_start_WON:
            axes['b)'].plot(
                year_dates,
                ds.sel(time=date_of_events).WON_event.values, 
                color=year_colour, label=str(year_selected), alpha=0.9, linewidth=1)
        
        
        
        # if the date of the events is before may in the year+1 selected (second half of season) plot it 
        elif date_of_events.year == year_selected+1 and date_of_events.month <= SEASON_start_WON:
            axes['b)'].plot(
                year_dates,
                ds.sel(time=date_of_events).WON_event.values, 
                color=year_colour, label=str(year_selected), alpha=0.9, linewidth=1)


## Now fix the nice stuff




# formate the date-axis 
xfmt_years = mdates.DateFormatter('%d')
for a in ['a)', 'b)']:
    axes[a].xaxis.set_major_locator(mdates.DayLocator(bymonthday=(1,3,5,7)))
    axes[a].xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    axes[a].xaxis.set_major_formatter(xfmt_years)



## Legends
# get legend handles and their corresponding labels
handles_a, labels_a = axes['a)'].get_legend_handles_labels()
handles_b, labels_b = axes['b)'].get_legend_handles_labels()

# zip labels as keys and handles as values into a dictionary, ...
# so only unique labels would be stored 
dict_of_labels_a = dict(zip(labels_a, handles_a))
dict_of_labels_b = dict(zip(labels_b, handles_b))


# set the legend and labels
axes['a)'].legend(dict_of_labels_a.values(), dict_of_labels_a.keys(),loc='upper right', fontsize='medium')
axes['b)'].legend(dict_of_labels_b.values(), dict_of_labels_b.keys(),loc='upper right', fontsize='medium')


#  Set limits
axes['a)'].set_ylim(-75,50)
# axes['b)'].set_ylim(-75,50)

# Fix labels
axes['a)'].set_ylabel('Wind CREDI [FLH]')
axes['b)'].set_ylabel('')




# make it look better
plt.tight_layout()

# print subplot names
for label, ax in axes.items():
    # label physical distance in and down:
    trans = mtransforms.ScaledTranslation(10/72, -8/72, fig.dpi_scale_trans)
    ax.text(0.0, 1.0, label, transform=ax.transAxes + trans,
            fontsize='xx-large', verticalalignment='top')

plt.savefig(FOLDER_project+'results/publication/supplementary/WindCREDI_shortterm_behaviour.png')
plt.savefig(FOLDER_project+'results/publication/supplementary/WindCREDI_shortterm_behaviour.pdf')

plt.show()

#%%
# =============================================================================
# Figure for short term scatter CREDI spv won
# =============================================================================


# we start a new figure
# fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(13,5), sharey=True)
fig, axes = plt.subplot_mosaic([['a)']], figsize=(10,7))


### First plot the initial yearly energy balance index and additional lines 


# Coincidence of CREDI extremes
# Show the data for all the years
df.plot.scatter(
    x='WON_event_credi', 
    y='SPV_event_credi', 
    ax=axes['a)'],
    color='dodgerblue', 
    alpha=1)

    

   
# Show selected years 
for year_selected, year_colour in zip([1996,1998,2003,2016], ['red', 'green','purple','black']):

    # look at sub-top years
    for date_of_events in WON_event_date[0:50]:
        
        # If the date of the event is after may in the year selected plot it
        if date_of_events.year == year_selected and date_of_events.month > SEASON_start_WON:
            axes['a)'].scatter(
                x=ds.sel(time=date_of_events, event_hour=PERIOD_length-1).CREDI_won.values,
                y=ds.sel(time=date_of_events, event_hour=PERIOD_length-1).CREDI_spv.values, 
                color=year_colour, 
                label=str(year_selected), 
                alpha=0.9, 
                linewidth=1
                )
        
        # if the date of the events is before may in the year+1 selected (second half of season) plot it 
        elif date_of_events.year == year_selected+1 and date_of_events.month <= SEASON_start_WON:
            axes['a)'].scatter(
                x=ds.sel(time=date_of_events, event_hour=PERIOD_length-1).CREDI_won.values,
                y=ds.sel(time=date_of_events, event_hour=PERIOD_length-1).CREDI_spv.values, 
                color=year_colour, 
                label=str(year_selected),
                alpha=0.9, 
                linewidth=1)




# Now fix the nice stuff

## Legends
# get legend handles and their corresponding labels
handles_a, labels_a = axes['a)'].get_legend_handles_labels()

# zip labels as keys and handles as values into a dictionary, ...
# so only unique labels would be stored 
dict_of_labels_a = dict(zip(labels_a, handles_a))


# set the legend and labels
axes['a)'].legend(dict_of_labels_a.values(), dict_of_labels_a.keys(),loc='upper right', fontsize='medium')


# #  Set limits
# axes['a)'].set_ylim(-75,50)
# # axes['b)'].set_ylim(-75,50)

# Fix labels
axes['a)'].set_xlabel('Wind CREDI [FLH]')
axes['a)'].set_ylabel('Solar CREDI [FLH]')




# make it look better
plt.tight_layout()


plt.savefig(FOLDER_project+'results/publication/supplementary/WindCREDI_shortterm_scatter.png')
plt.savefig(FOLDER_project+'results/publication/supplementary/WindCREDI_shortterm_scatter.pdf')

plt.show()


#%%

#%% Historgram of probability
# Solar

# we start a new figure
# fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(13,5), sharey=True)
fig, axes = plt.subplot_mosaic([['a)']], figsize=(10,7))

ds.CREDI_spv.sel(event_hour=PERIOD_length-1).plot.hist(range=(-25,30), bins=54, ax=axes['a)'])

# Fix labels
axes['a)'].set_xlabel('Solar CREDI [FLH]')
axes['a)'].set_ylabel('Count')


# make it look better
plt.tight_layout()


plt.savefig(FOLDER_project+'results/publication/supplementary/SolarCREDI_shortterm_histogram.png')
plt.savefig(FOLDER_project+'results/publication/supplementary/SolarCREDI_shortterm_histogram.pdf')
plt.show()

# Wind
fig, axes = plt.subplot_mosaic([['a)']], figsize=(10,7))

ds.CREDI_won.sel(event_hour=PERIOD_length-1).plot.hist(range=(-110,160), bins=54)
axes['a)'].set_xlabel('Wind CREDI [FLH]')
axes['a)'].set_ylabel('Count')
plt.tight_layout()

plt.savefig(FOLDER_project+'results/publication/supplementary/WindREDI_shortterm_histogram.png')
plt.savefig(FOLDER_project+'results/publication/supplementary/WindCREDI_shortterm_histogram.pdf')
plt.show()
