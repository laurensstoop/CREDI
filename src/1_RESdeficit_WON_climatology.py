# -*- coding: utf-8 -*-
"""
Spyder Editor

Created on 2023-02-01

@author: Laurens P. Stoop
"""


# load the dependencies
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import sys
from datetime import datetime

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
fileName= 'WON/PEON/H_ERA5_ECMW_T639_WON_NA---_Pecd_PEON_S198001010000_E202112312300_CFR_TIM_01h_NA-_noc_org_30_NA---_NA---_PhM01.csv'


#%%
# =============================================================================
# Get the data to open
# =============================================================================

# Open the file and set the index as the date
df = pd.read_csv(FOLDER_hist+fileName, header=52, parse_dates=True, index_col='Date')
df.index = df.index.rename('time')
ds = df.to_xarray()

#%%
# =============================================================================
# Functional definition call of climatology
# =============================================================================

# Make the Climatology dataset
ds_Clim = xr.Dataset()

# determine climatology
ds_Clim['Daily'], MOD = creb.Climatology_MOD(ds, 'NL01')
ds_Clim['RolClim10'], MOD = creb.Climatology_MOD_Rolling(ds, 'NL01', RollingWindow=240)
ds_Clim['RolClim20'], MOD = creb.Climatology_MOD_Rolling(ds, 'NL01', RollingWindow=480)
ds_Clim['RolClim30'], MOD = creb.Climatology_MOD_Rolling(ds, 'NL01', RollingWindow=960)
ds_Clim['RolClim42'], MOD = creb.Climatology_MOD_Rolling(ds, 'NL01', RollingWindow=1008)
ds_Clim['RolClim60'], MOD = creb.Climatology_MOD_Rolling(ds, 'NL01', RollingWindow=1920)
ds_Clim['RolClim90'], MOD = creb.Climatology_MOD_Rolling(ds, 'NL01', RollingWindow=2880)


ds_Clim['Hourly'], MOH = creb.Climatology_Hourly(ds, 'NL01')

ds_Clim['RolHour20'], OH = creb.Climatology_Hourly_Rolling(ds, 'NL01', RollingWindow=20)
ds_Clim['RolHour60'], OH = creb.Climatology_Hourly_Rolling(ds, 'NL01', RollingWindow=60)
ds_Clim['RolHour42'], OH = creb.Climatology_Hourly_Rolling(ds, 'NL01', RollingWindow=42)



# # determine the anomaly
# ds_Anom = ds.NL01.groupby(MOD) - ds_Clim
# ds_RolAnom = ds.NL01.groupby(MOD) - ds_RolClim30




#%%
# =============================================================================
# Harmonic mean
# =============================================================================

# Determin Fourier T
fft_D, freq_D = creb.fourier_transform(ds_Clim.Daily.values, 1/366.)
# fft_H, freq_H = creb.fourier_transform(ds_Clim.Hourly.values, 1/8764.)

# Get the frequency spectrum information
spd_D, pos_freqs_D = creb.spectrum(fft_D, freq_D) #, scaling='power')
# spd_H, pos_freqs_H = creb.spectrum(fft_H, freq_H) #, scaling='power')

# quickly plot the frequency spectrum for the Daily version
f, ax = plt.subplots(1,1)
ax.plot(pos_freqs_D, spd_D)
ax.set_xlabel('Frequency(units: cycles per length of domain)', fontsize=14)
ax.set_title('Spectral density', fontsize=16)


# # quickly plot the frequency spectrum for the hourly version
# f, ax = plt.subplots(1,1)
# ax.plot(pos_freqs_H, spd_H)
# ax.set_xlabel('Frequency(units: cycles per length of domain)', fontsize=14)
# ax.set_title('Spectral density', fontsize=16)
# ax.set_xlim(0,1200)

# Harmonics based on daily data
ds_Clim['Harmonic1']  = xr.DataArray(np.real(creb.inverse_fourier_transform(fft_D, freq_D, max_freq=1)), coords={'ModifiedOrdinalDay': ds_Clim.ModifiedOrdinalDay}, dims=['ModifiedOrdinalDay'])
ds_Clim['Harmonic3']  = xr.DataArray(np.real(creb.inverse_fourier_transform(fft_D, freq_D, max_freq=3)), coords={'ModifiedOrdinalDay': ds_Clim.ModifiedOrdinalDay}, dims=['ModifiedOrdinalDay'])
ds_Clim['Harmonic5']  = xr.DataArray(np.real(creb.inverse_fourier_transform(fft_D, freq_D, max_freq=5)), coords={'ModifiedOrdinalDay': ds_Clim.ModifiedOrdinalDay}, dims=['ModifiedOrdinalDay'])
ds_Clim['Harmonic10']  = xr.DataArray(np.real(creb.inverse_fourier_transform(fft_D, freq_D, max_freq=10)), coords={'ModifiedOrdinalDay': ds_Clim.ModifiedOrdinalDay}, dims=['ModifiedOrdinalDay'])

# # Harmonics based on Houlry data
# ds_Clim['HourHarm1']  = xr.DataArray(np.real(creb.inverse_fourier_transform(fft_H, freq_H, max_freq=1)), coords={'ModifiedOrdinalHour': ds_Clim.ModifiedOrdinalHour}, dims=['ModifiedOrdinalHour'])
# ds_Clim['HourHarm3']  = xr.DataArray(np.real(creb.inverse_fourier_transform(fft_H, freq_H, max_freq=3)), coords={'ModifiedOrdinalHour': ds_Clim.ModifiedOrdinalHour}, dims=['ModifiedOrdinalHour'])
# ds_Clim['HourHarm5']  = xr.DataArray(np.real(creb.inverse_fourier_transform(fft_H, freq_H, max_freq=5)), coords={'ModifiedOrdinalHour': ds_Clim.ModifiedOrdinalHour}, dims=['ModifiedOrdinalHour'])
# ds_Clim['HourHarm200']  = xr.DataArray(np.real(creb.inverse_fourier_transform(fft_H, freq_H, max_freq=200)), coords={'ModifiedOrdinalHour': ds_Clim.ModifiedOrdinalHour}, dims=['ModifiedOrdinalHour'])




#%%
# =============================================================================
# Now we do a slow moving climatology calculation
# =============================================================================



# we start a new figure
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14,12), sharey=True)

# first subplot is the climatology comparison
ds_Clim.Daily.plot(ax=axes[0,0], label='Daily', alpha=0.5, color='dodgerblue')
ds_Clim.RolClim30.plot(ax=axes[0,0],label='Rolling [30 d]', color='red')
ds_Clim.RolClim60.plot(ax=axes[0,0],label='Rolling [60 d]', color='green')
ds_Clim.Harmonic3.plot(ax=axes[0,0],label='3rd Harmonic', color='black')

# Comparison of rolling climatology
ds_Clim.Daily.plot(ax=axes[1,0], label='Daily climatology', alpha=0.2, color='dodgerblue')
ds_Clim.RolClim10.plot(ax=axes[1,0],label='Rolling climatology [10 d]', alpha=0.6)
ds_Clim.RolClim20.plot(ax=axes[1,0],label='Rolling climatology [20 d]', alpha=0.6)
ds_Clim.RolClim30.plot(ax=axes[1,0],label='Rolling climatology [30 d]', color='red')
ds_Clim.RolClim42.plot(ax=axes[1,0],label='Rolling climatology [42 d]', color='black')
ds_Clim.RolClim60.plot(ax=axes[1,0],label='Rolling climatology [60 d]', color='green')
ds_Clim.RolClim90.plot(ax=axes[1,0],label='Rolling climatology [90 d]', alpha=0.6)

# Comparison of Harmonics
ds_Clim.Daily.plot(ax=axes[0,1], label='Daily climatology', alpha=0.2, color='dodgerblue')
ds_Clim.Harmonic1.plot(ax=axes[0,1],label='1st Harmonic', color='red')
ds_Clim.Harmonic3.plot(ax=axes[0,1],label='3rd Harmonic', color='black')
ds_Clim.Harmonic5.plot(ax=axes[0,1],label='5th Harmonic', color='blue')
ds_Clim.Harmonic10.plot(ax=axes[0,1],label='10th Harmonic ', color='purple')

# Comparison of Hourly version
ds_Clim.Hourly[8:8760:24].plot(ax=axes[1,1], label='Hourly climatology', alpha=0.2, color='dodgerblue')
ds_Clim.RolHour20[8:8760:24].plot(ax=axes[1,1],label='Rolling 20', color='red')
ds_Clim.RolHour42[8:8760:24].plot(ax=axes[1,1],label='Rolling 42', color='black')
ds_Clim.RolHour60[8:8760:24].plot(ax=axes[1,1],label='Rolling 60', color='blue')


# set the legend and labels
axes[0,0].legend(loc='upper right', fontsize='medium')
axes[0,1].legend(loc='upper right', fontsize='medium')
axes[1,0].legend(loc='upper right', fontsize='medium')
axes[1,1].legend(loc='upper right', fontsize='medium')

axes[0,0].set_title('Climatology methods')
axes[1,0].set_title('Rolling window comparison')
axes[0,1].set_title('Harmonic comparison')
axes[1,1].set_title('Hourly comparison [only 08:00]')


axes[0,0].set_ylabel('Climatology of RES-potential')
axes[0,1].set_ylabel('')
axes[1,0].set_ylabel('Climatology of RES-potential')
axes[1,1].set_ylabel('')

# make it look better
plt.tight_layout()

plt.savefig(FOLDER_project+'results/figures/Fig_ClimatologyComparison_WON.png')

plt.show()




#%%
# =============================================================================
# Final choice
# =============================================================================

# we start a new figure
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(14,6), sharey=True)

# selected hours
ds_Clim.Hourly[8:8760:24].plot(ax=axes[0], alpha=0.5, color='dodgerblue',linestyle='dashed')
ds_Clim.Hourly[12:8760:24].plot(ax=axes[0], label='Hourly climatology', alpha=0.5, color='dodgerblue')
ds_Clim.RolHour42[8:8760:24].plot(ax=axes[0],  color='black',linestyle='dashed')
ds_Clim.RolHour42[12:8760:24].plot(ax=axes[0], label='Rolling  Hourly 42', color='black')

# All hours
ds_Clim.Hourly[0:8760:24].plot(ax=axes[1], alpha=0.5, color='dodgerblue')
ds_Clim.Hourly[2:8760:24].plot(ax=axes[1], alpha=0.5, color='dodgerblue')
ds_Clim.Hourly[4:8760:24].plot(ax=axes[1], alpha=0.5, color='dodgerblue')
ds_Clim.Hourly[6:8760:24].plot(ax=axes[1], alpha=0.5, color='dodgerblue')
ds_Clim.Hourly[8:8760:24].plot(ax=axes[1], alpha=0.5, color='dodgerblue')
ds_Clim.Hourly[10:8760:24].plot(ax=axes[1], alpha=0.5, color='dodgerblue')
ds_Clim.Hourly[12:8760:24].plot(ax=axes[1], label='Hourly climatology', alpha=0.5, color='dodgerblue')
ds_Clim.RolHour42[0:8760:24].plot(ax=axes[1],  color='black')
ds_Clim.RolHour42[2:8760:24].plot(ax=axes[1],  color='black')
ds_Clim.RolHour42[4:8760:24].plot(ax=axes[1],  color='black')
ds_Clim.RolHour42[6:8760:24].plot(ax=axes[1],  color='black')
ds_Clim.RolHour42[8:8760:24].plot(ax=axes[1],  color='black')
ds_Clim.RolHour42[10:8760:24].plot(ax=axes[1],  color='black')
ds_Clim.RolHour42[12:8760:24].plot(ax=axes[1], label='Rolling  Hourly 42', color='black')


# limited period
for year in np.arange(start=1980,stop=2021):
    axes[2].plot(ds.NL01.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31')), color='yellow', alpha=0.1)    
ds_Clim.Hourly.plot(ax=axes[2], label='Hourly climatology', alpha=0.5, color='dodgerblue')
ds_Clim.RolHour42.plot(ax=axes[2], label='Rolling  Hourly 42', color='black')
    
axes[2].set_xlim(4200,4400)

# set the legend and labels
axes[0].legend(loc='upper right', fontsize='medium')


axes[0].set_ylabel('Climatology of RES-potential')
axes[1].set_ylabel('')
axes[2].set_ylabel('')

# make it look better
plt.tight_layout()

plt.savefig(FOLDER_project+'results/figures/Fig_ClimatologyChoice_WON.png')

plt.show()

# #%%
# # =============================================================================
# # Now we do a yearly running sum of cumsum of capacity factor
# # =============================================================================

# # to quickly move from rolling to non-rolling
# ROLLING =False

# if ROLLING is True: 
#     dsr_nl01_anom = dsr_nl01_anom
# elif ROLLING is False:
#     print('NOTIFY: We have subset the data to non-rolling! FILE NAMING IS NOT NICE')
#     dsr_nl01_anom = ds_nl01_anom

# fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(17,12), sharey=True)

# # make a colorrange
# color = plt.cm.RdBu_r(np.linspace(0, 1, 41))

# for year, c in zip(np.arange(start=1980,stop=2021), color):
    
#     axes[0,0].plot(dsr_nl01_anom.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31')).cumsum(), c=c, linewidth=1)
#     axes[0,1].plot(dsr_nl01_anom.sel(time=slice(str(year)+'-02-01', str(year+1)+'-01-31')).cumsum(), c=c, linewidth=1)
#     axes[0,2].plot(dsr_nl01_anom.sel(time=slice(str(year)+'-03-01', str(year+1)+'-02-28')).cumsum(), c=c, linewidth=1)
#     axes[1,0].plot(dsr_nl01_anom.sel(time=slice(str(year)+'-04-01', str(year+1)+'-03-31')).cumsum(), c=c, linewidth=1)
#     axes[1,1].plot(dsr_nl01_anom.sel(time=slice(str(year)+'-05-01', str(year+1)+'-04-30')).cumsum(), c=c, linewidth=1)
#     axes[1,2].plot(dsr_nl01_anom.sel(time=slice(str(year)+'-06-01', str(year+1)+'-05-31')).cumsum(), c=c, linewidth=1)

# # set the legend, labels & titles of the subplots
# axes[0,0].set_title('January Start')
# axes[0,1].set_title('February Start')
# axes[0,2].set_title('March Start')
# axes[1,0].set_title('April Start')
# axes[1,1].set_title('May Start')
# axes[1,2].set_title('June Start')

# axes[0,0].set_ylabel('Cummalative sum of RES-potential deficit')
# axes[1,0].set_ylabel('Cummalative sum of RES-potential deficit')

# sm = plt.cm.ScalarMappable(cmap=plt.cm.RdBu_r, norm=plt.Normalize(vmin=1980, vmax=2021))
# fig.colorbar(sm, ax=axes.ravel().tolist())
# # make it loog better
# # plt.tight_layout()



# if ROLLING is True: 
#     plt.savefig(FOLDER_project+'results/figures/fig_yearlyCumsum_startdate.png')
# elif ROLLING is False:
#     plt.savefig(FOLDER_project+'results/figures/fig_yearlyCumsum_startdate_rolling.png')

# #%%
# # =============================================================================
# # Now we do a yearly running sum of cumsum of capacity factor
# # =============================================================================


# # now for a different approach
# fig = plt.figure(constrained_layout=True, figsize=(16,12))#, sharey=True)


# # make a colorrange
# color = plt.cm.RdBu_r(np.linspace(0, 1, 41))

# # Rearrange the subplots so we have 1 big and 1 small graph
# gs = plt.GridSpec(nrows=2,ncols=3, figure=fig)
# ax1 = fig.add_subplot(gs[0,0])
# ax2 = fig.add_subplot(gs[0,1:3])
# ax3 = fig.add_subplot(gs[1,0:3])

# for year, c in zip(np.arange(start=1980,stop=2021), color):
    
#     ax1.plot(dsr_nl01_anom.sel(time=slice(str(year)+'-05-01', str(year+1)+'-04-30')).cumsum(), c=c, linewidth=1)
#     ax2.plot(dsr_nl01_anom.sel(time=slice(str(year)+'-05-01', str(year+2)+'-04-30')).cumsum(), c=c, linewidth=1)
#     ax3.plot(dsr_nl01_anom.sel(time=slice(str(year)+'-05-01', str(year+3)+'-04-30')).cumsum(), c=c, linewidth=1)

# # set the legend, labels & titles of the subplots
# ax1.set_title('One year')
# ax2.set_title('Two year')
# ax3.set_title('Three years')

# ax1.set_ylim([-600,600])
# ax2.set_ylim([-600,600])
# ax3.set_ylim([-600,600])

# ax1.set_ylabel('Cumsum of RES deficit')
# ax3.set_ylabel('Cumsum of RES deficit')

# sm = plt.cm.ScalarMappable(cmap=plt.cm.RdBu_r, norm=plt.Normalize(vmin=1980, vmax=2021))
# fig.colorbar(sm, ax=ax3, location='bottom')

# # # make it loog better
# # plt.tight_layout()


# if ROLLING is True: 
#     plt.savefig(FOLDER_project+'results/figures/fig_multiyear_Cumsum.png')
# elif ROLLING is False:
#     plt.savefig(FOLDER_project+'results/figures/fig_multiyear_Cumsum_rolling.png')


# #%%

# fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(17,12), sharey=True)

# # make a colorrange
# color = plt.cm.RdBu_r(np.linspace(0, 1, 41))

# for year, c in zip(np.arange(start=1980,stop=2021), color):
    
#     axes[0,0].plot(dsr_nl01_anom.sel(time=slice(str(year)+'-01-01', str(year)+'-12-31')).cumsum(), c=c, linewidth=1)
#     axes[0,1].plot(dsr_nl01_anom.sel(time=slice(str(year)+'-05-01', str(year+1)+'-04-30')).cumsum(), c=c, linewidth=1)
#     axes[1,0].plot(dsr_nl01_anom.sel(time=slice(str(year)+'-09-01', str(year+1)+'-04-30')).cumsum(), c=c, linewidth=1)
#     axes[1,1].plot(dsr_nl01_anom.sel(time=slice(str(year)+'-10-01', str(year+1)+'-04-30')).cumsum(), c=c, linewidth=1)

# # set the legend, labels & titles of the subplots
# axes[0,0].set_title('January Start')
# axes[0,1].set_title('May Start')
# # axes[0,2].set_title('March Start')
# axes[1,0].set_title('Sept Start')
# axes[1,1].set_title('Okt Start')
# # axes[1,2].set_title('June Start')

# axes[0,0].set_ylabel('Cummalative sum of RES-potential deficit')
# axes[1,0].set_ylabel('Cummalative sum of RES-potential deficit')

# sm = plt.cm.ScalarMappable(cmap=plt.cm.RdBu_r, norm=plt.Normalize(vmin=1980, vmax=2021))
# fig.colorbar(sm, ax=axes.ravel().tolist())
# # make it loog better
# # plt.tight_layout()



# if ROLLING is True: 
#     plt.savefig(FOLDER_project+'results/figures/fig_yearlyCumsum_startdatev2.png')
# elif ROLLING is False:
#     plt.savefig(FOLDER_project+'results/figures/fig_yearlyCumsum_startdatev2_rolling.png')
# #%%
# # df_clim = df.groupby(cum_data.index.dayofyear).mean()