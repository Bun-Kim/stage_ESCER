#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 14:34:47 2022

@author: san
"""
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import matplotlib as mpl
from matplotlib.colors import BoundaryNorm

method_list = [
    "bilinear",
    "nearest_s2d",
    "nearest_d2s",
    "patch",
]


def bounds(dico):
    return [dico['lonW'], dico['lonE'], dico['latS'], dico['latN']]

def tracer(dico,data,champs):
    resolution= abs(data.lat.values[0]-data.lat.values[1])
    clevs = np.linspace(0, np.mean(data[champs].values)*10, 11)
    #cmap = mpl.cm.jet
    #norm = BoundaryNorm(clevs, cmap.N, extend='both')
    
    fig=plt.figure(figsize=(10,6), frameon=True)   
    ax = plt.subplot(111, projection=ccrs.Orthographic(central_longitude=(dico['lonW']+dico['lonE'])/2, central_latitude=(dico['latS']+dico['latN'])/2))
    
    ax.set_extent(bounds(dico), crs=ccrs.PlateCarree())
    ax.set_title(champs+ '  resolution ' + str(resolution) +'°' +dico['methode_spatiale'][0],loc='center')
   
    ax.add_feature(cfeature.OCEAN.with_scale('50m'))
    ax.add_feature(cfeature.LAKES.with_scale('50m'))
    ax.add_feature(cfeature.LAND.with_scale('50m'))
    ax.add_feature(cfeature.BORDERS.with_scale('50m'))
    states_provinces = cfeature.NaturalEarthFeature(
            category='cultural',
            name='admin_1_states_provinces_lines',
            scale='50m',
            facecolor='none')
    
    ax.add_feature(states_provinces, edgecolor='gray')
    
    mm = ax.pcolormesh(data.lon.values,\
                       data.lat.values,\
                       np.mean(data[champs].values,axis=0),\
                       vmin=0,\
                       vmax=np.mean(data[champs].values)*10, \
                       transform=ccrs.PlateCarree(),\
                       cmap='jet' )
    #ax.contour(data.lon.values, data.lat.values, np.mean(data[champs].values,axis=0), levels=clevs, colors='black', linewidths=1, transform=ccrs.PlateCarree())
    
    
   
    cb_ax = fig.add_axes([0.95, 0.1, 0.02, 0.8])
    cbar = plt.colorbar(mm, cax=cb_ax,extend='both')
    cbar.set_label("par km**2 par jour",horizontalalignment='center',rotation=90)
    ax.coastlines(resolution='110m');
    plt.savefig(champs+ '_resolution_' + str(resolution) +'.png' )
    plt.show()

def tracer_saison(dico,data,champs):
     resolution= abs(data.lat.values[0]-data.lat.values[1])
     clevs = np.linspace(0, np.mean(data[champs].values)*10, 11)
     #cmap = mpl.cm.jet
     #norm = BoundaryNorm(clevs, cmap.N, extend='both')
     
     fig=plt.figure(figsize=(10,6), frameon=True)   
     ax = plt.subplot(111, projection=ccrs.Orthographic(central_longitude=(dico['lonW']+dico['lonE'])/2, central_latitude=(dico['latS']+dico['latN'])/2))
     
     ax.set_extent(bounds(dico), crs=ccrs.PlateCarree())
     ax.set_title(champs+ '  resolution ' + str(resolution) +'°' +dico['methode_spatiale'][0],loc='center')
    
     ax.add_feature(cfeature.OCEAN.with_scale('50m'))
     ax.add_feature(cfeature.LAKES.with_scale('50m'))
     ax.add_feature(cfeature.LAND.with_scale('50m'))
     ax.add_feature(cfeature.BORDERS.with_scale('50m'))
     states_provinces = cfeature.NaturalEarthFeature(
             category='cultural',
             name='admin_1_states_provinces_lines',
             scale='50m',
             facecolor='none')
     
     ax.add_feature(states_provinces, edgecolor='gray')
        
     mm = ax.pcolormesh(data.lon.values,\
                       data.lat.values,\
                       np.mean(data[champs].values,axis=0),\
                       vmin=0,\
                       vmax=np.nanmean(data[champs].values)*10, \
                       transform=ccrs.PlateCarree(),\
                       cmap='jet' )
     #ax.contour(data.lon.values, data.lat.values, np.mean(data[champs].values,axis=0), levels=clevs, colors='black', linewidths=1, transform=ccrs.PlateCarree())
     
    
     
     cb_ax = fig.add_axes([0.95, 0.1, 0.02, 0.8])
     cbar = plt.colorbar(mm, cax=cb_ax,extend='both')
     cbar.set_label("par km**2 par jour",horizontalalignment='center',rotation=90)
     ax.coastlines(resolution='110m');
     plt.savefig(champs+ '_resolution_' + str(resolution) +'.png' )
     plt.show()   

'''   
def trace_controle_methode_regrid(dico,dataset,champs):
    clevs = np.linspace(-1, 1, 11)
    #cmap = mpl.cm.seismic
    #norm = BoundaryNorm(clevs, cmap.N, extend='both')
    fig=plt.figure(figsize=(20,6))
    fig.suptitle('cape', fontsize=16)
    
    for k in range (len(method_list)):
        ax=fig.add_subplot(2,3,k+1,projection=ccrs.Orthographic(central_longitude=(dico['lonW']+dico['lonE'])/2, central_latitude=(dico['latS']+dico['latN'])/2))
        
        ax.add_feature(cfeature.OCEAN.with_scale('50m'))
        ax.add_feature(cfeature.LAKES.with_scale('50m'))
        ax.add_feature(cfeature.LAND.with_scale('50m'))
        ax.add_feature(cfeature.BORDERS.with_scale('50m'))
        states_provinces = cfeature.NaturalEarthFeature(
                category='cultural',
                name='admin_1_states_provinces_lines',
                scale='50m',
                facecolor='none')
        
        ax.add_feature(states_provinces, edgecolor='gray')
        
        mm = ax.pcolormesh(dataset[0].lon.values,\
                   dataset[1].lon.values,\
                   np.mean(dataset[k][champs].values,axis=0),\
                   vmin=0,\
                   vmax=500, \
                   transform=ccrs.PlateCarree(),\
                   cmap="jet")
        ax.coastlines(resolution='110m');
    plt.show()
 '''
