# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 13:59:48 2021

@author: eliza
"""
from _01Load_fluxpol_data import cass_df
import numpy as np
from numpy import save
def latandLT(df,val,LT_range,lowlat=False,highlats=False, poslat=False, neglat=False):
    if highlats == True:
        df =df[(df['Latitude'] < -5) | (df['Latitude']>5)]
    if lowlat == True:
        df =df[(df['Latitude'] > -5) & (df['Latitude']<5)]
    elif poslat == True:
        df =df[(df['Latitude'] > 5)]
    elif neglat == True:
        df =df[(df['Latitude'] < -5)]
    df =df[(df['LT'] >= LT_range[0]) & (df['LT'] < LT_range[1])]
    return df[val]

def getpercentile(df):
    percentile = [[np.percentile(i,10),np.percentile(i,75)] for i in df]
    return percentile
    
    
'''Separate Flux Data according to Latitude Range and Local Time Range'''
#Latitude is separated by <|5| degrees and >|5| degrees.
#LT separated into 4 sections.
#8 lists of flux generated in total.
LT_Ranges=[[0,6], [6,12], [12,18],[18,24.1]]
flux_df = cass_df[(cass_df['flux'] >= 1e-24) & (cass_df['flux'] <= 1e-19)].reset_index(drop=True)
flux_highlat = [latandLT(flux_df,val='flux', highlats=True, LT_range=i) for i in LT_Ranges]
flux_lowlat = [latandLT(flux_df,val='flux', lowlat=True, LT_range=i) for i in LT_Ranges]
#Log of fluxes to be used for histograms
flux_highlat_lists = [np.log10(i) for i in flux_highlat]
flux_lowlat_lists = [np.log10(i) for i in flux_lowlat]

#make list of the 10th and 75th percentiles
highlat_percentile = save('output_data/fluxhighlatpercentiles.npy', getpercentile(flux_highlat))
lowlat_percentile = save('output_data/fluxlowlatpercentiles.npy',getpercentile(flux_lowlat))


'''Separate Pol Data according to Latitude Range and Local Time Range'''
#Latitude is separated by <|5| degrees, >5 degrees and <5 degrees.
#LT separated into 4 sections.
#12 lists of polarization generated in total.


#Remove values of zero polarization.
pol_df = cass_df
pol_df = pol_df[pol_df['polarization'] !=0].reset_index(drop=True)
pol_lowlat_lists = [latandLT(pol_df,val='polarization', lowlat=True, LT_range=i) for i in LT_Ranges]
pol_poslat_lists = [latandLT(pol_df,val='polarization', poslat=True, LT_range=i) for i in LT_Ranges]
pol_neglat_lists = [latandLT(pol_df,val='polarization', neglat=True, LT_range=i) for i in LT_Ranges]