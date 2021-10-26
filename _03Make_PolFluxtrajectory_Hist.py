# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 15:17:39 2021

@author: eliza
"""
#Values of Polarization=0 have been removed and Flux is restricted to between
#1e-24-1e-19.
#flux_highlat_lists conists of flux recorded where spacecraft lat is >|5|, subdivided into 4 lists corresponding to each LT range.
#flux_lowlat_lists conists of flux recorded where spacecraft lat is <|5|, subdivided into 4 lists corresponding to each LT range.
#pol_lowlat_lists conists of polarization recorded where spacecraft lat is <|5|, subdivided into 4 lists corresponding to each LT range.                            
#pol_poslat_lists conists of polarization recorded where spacecraft lat is >5, subdivided into 4 lists corresponding to each LT range.                            
#pol_neglat_lists conists of polarization recorded where spacecraft lat is <5, subdivided into 4 lists corresponding to each LT range.                            


from _02Lat_LT_analysis import (flux_highlat_lists, 
flux_lowlat_lists, pol_lowlat_lists, pol_poslat_lists, pol_neglat_lists)
from matplotlib.gridspec import SubplotSpec
import numpy as np
import matplotlib.pyplot as plt

'''-------------------FLUX HIST--------------------------'''
#Make figure with 8 subplots. Each subplot displays a histogram showing of flux data recorded in 
#given location i.e latitudes <|5| degrees/latitudes >|5| degrees for each local time range (4 in total).
#Localtimeranges = [0,6][6,12][12,18][18,24]


def percentiles(ax,df,p,c,F=False,P=False):
    if F == True and len(df) >0:     
        val = np.percentile(df,p)
        label_string = str(p) +'th Percentile'
        ax.axvline(x=val,linestyle='--',color=c, label= label_string) 
    elif P==True and len(df) >0:
        val = np.percentile(abs(df),p)
        label_string = str(p) +'th Percentile'
        if np.sum(df)>0:
            ax.axvline(x=val,linestyle='--',color=c,label= label_string)  
        elif np.sum(df) <0:
            ax.axvline(x=-val,linestyle='--',color=c,label= label_string)  
            
    return None
    
def create_subtitle(fig: plt.Figure, grid: SubplotSpec, title: str):
    "Sign sets of subplots with title"
    row = fig.add_subplot(grid)
    # the '\n' is important
    row.set_title(f'{title}\n', fontweight='semibold')
    # hide subplot
    row.set_frame_on(False)
    row.axis('off')   

def make_figure(Flux=False, Pol=False):
    if Flux ==  True:
        xstring=f'Log of Flux Density (W/m\N{SUPERSCRIPT TWO}Hz Normalized to 1AU)'
        fig, axes = plt.subplots(2, 4, sharex=True, figsize=(22, 12))
        fig.text(0.5, 0.07, xstring, ha='center',size='xx-large')
        fig.text(0.07, 0.5, 'Frequency', va='center', rotation='vertical',size='xx-large')
        grid = plt.GridSpec(2, 4)
        create_subtitle(fig, grid[0, ::], 'Equatorial Region (<|5| degrees Latitude)')
        create_subtitle(fig, grid[1, ::], 'Higher Latitude Region (>|5| degrees Latitude)')
    elif Pol == True:
        fig, axes = plt.subplots(3, 4, sharex=True, figsize=(22, 14))
        #fig.suptitle("Histogram ", fontsize=14)
        fig.text(0.5, 0.07, 'Degree of Normalized Circular Polarization', ha='center',size='xx-large')
        fig.text(0.09, 0.5, 'Frequency', va='center', rotation='vertical',size='xx-large')
        grid = plt.GridSpec(3, 4)
        create_subtitle(fig, grid[0, ::], 'Equatorial Region (<|5| degrees Latitude)')
        create_subtitle(fig, grid[1, ::], 'Latitudes > 5 degrees')
        create_subtitle(fig, grid[2, ::], 'Latitudes <5 degrees')
    return fig, axes

def make_hist(axes,axnum,dfs,xtick,bins,ticklabels,F=False,P=False):
    LT_ranges = [[0,6], [6,12], [12,18],[18,24]]   
    legend_labels = ['{} - {} Hrs LT'.format(f1, f2) for f1, f2 in LT_ranges]
    colours = ['cornflowerblue','royalblue','blue','darkblue','midnightblue'] 
    for i,df in enumerate(dfs):
        ax = axes[axnum,i]
        ax.set_title(legend_labels[i])
        percentiles(ax,df,p=10, c='darkgrey',F=F,P=P)
        percentiles(ax,df,p=50,c = 'slategrey',F=F,P=P)
        percentiles(ax,df,p=80,c = 'darkslategrey',F=F,P=P)
        ax.set_xticks(xtick)
        ax.set_xticklabels(ticklabels)
        ax.hist(df,density=True, stacked=True,bins=bins,color=colours[i])
        ax.legend(fontsize=8)
        ax.set_title('N='+str(len(df)))
    return None
    
def plot(dfs,Flux=False, Pol=False):
    if Flux == True:
        fig, axes = make_figure(Flux=True)
        bins = np.log10([1e-24,1e-23,1e-22,1e-21,1e-20,1e-19])
        xtick = bins
        ticklabels = [str(i) for i in xtick]
    elif Pol==True:
        fig, axes = make_figure(Pol=True)
        xtick=[-1,-0.75,-0.5,-0.25,0,0.25,0.5,0.75,1]
        ticklabels = ['RH','-0.75','-0.5','-0.25','0','0.25','0.5','0.75','LH']
        bins=8 
    for i in range(len(axes)): 
        make_hist(axes,i,dfs[i],xtick,bins,ticklabels,F=Flux,P=Pol)
    return fig

f_fig = plot([flux_lowlat_lists,flux_highlat_lists], Flux=True)
p_fig = plot([pol_lowlat_lists, pol_poslat_lists, pol_neglat_lists], Pol=True)
f_fig.savefig('figs/hist_flux_separatedby_LatLT.png')
p_fig.savefig('figs/pol_flux_separatedby_LatLT.png')