# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 13:23:19 2021

@author: eliza
"""
from matplotlib.gridspec import SubplotSpec
import numpy as np
import pandas as pd
from scipy.io.idl import readsav
from datetime import timedelta
from datetime import datetime
import math
import matplotlib.pyplot as plt
from scipy import signal
from bisect import bisect_left



def take_closest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return 0
    if pos == len(myList):
        return -1
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
        return pos
    else:
        return pos-1
    


    

'''FLUX AND POLARIZATION DATA----------------------------------------------------------------'''
data = readsav('input_data/SKR_2006_CJ.sav', python_dict=True)

'''Trajectory Data----------------------------------------------------------------------------'''
df_traj = pd.read_csv('input_data/Full_Trajectory_file.csv',parse_dates=['datetime_ut'])
df_traj= df_traj.loc[df_traj['datetime_ut'].between(
        pd.Timestamp('20060101'), pd.Timestamp('20070101')), :].reset_index(drop=True)


'''-------------Make DataFrame with flux,pol,time,frequency,latitude,localtime,range------------------------------------'''
t_doy = data['t']
n_freqs = len(data['f'])
freqs = np.array(np.tile(data['f'], t_doy.shape[0]), dtype=np.float64)
doy_one = pd.Timestamp(str(1997)) - pd.Timedelta(1, 'D')
t_timestamp = np.array([doy_one + pd.Timedelta(t * 1440, 'm') for t in t_doy],
    dtype=pd.Timestamp)
datetime_ut = np.repeat(t_timestamp, n_freqs)
#array_conv is a function, uses lambda function method with arr as the variable.
#Inputs an array and flattens it to type 'F'
array_conv = lambda arr: np.array(arr, dtype=np.float64).flatten('F')
#Flux density in W/m^2Hz
flux = array_conv(data['s'])
flux = np.where(np.isclose(flux, 0., atol=1e-31) | (flux < 0.), np.nan, flux)
#Normalised degree of circular polarization
pol = array_conv(data['v'])
#Power in W/sr
pwr = array_conv(data['p'])



#Assign Trajectory values to flux pol dataframe
ind = [take_closest(df_traj['datetime_ut'], i) for i in t_timestamp]
lat = np.repeat(df_traj['Latitude'].iloc[ind],n_freqs).reset_index(drop=True)
lt = np.repeat(df_traj['LT'].iloc[ind],n_freqs).reset_index(drop=True)
rg = np.repeat(df_traj['Range'].iloc[ind],n_freqs).reset_index(drop=True)
cass_df = pd.DataFrame({'datetime_ut': datetime_ut, 'freq':freqs, 'flux': flux,
                        'power': pwr,'polarization':pol,'Latitude':lat, 'LT':lt,
                        'Range':rg})
n_sweeps = cass_df.shape[0] / n_freqs
#the sweep parameter of the cass_df data consists of an array of size n_freqs 
#with values of n_sweeps only 
cass_df['sweep'] = np.repeat(np.arange(n_sweeps), n_freqs)

cass_df.to_csv('output_data/pol_flux_withtrajectory06.csv', index=False)



