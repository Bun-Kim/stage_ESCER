#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 11:03:28 2022

@author: san
"""
import xarray as xr
import numpy as np

def data_saison(dataset,champs,saison,dates,lon,lat):
    mois=[]
    for i in range(1,13):
            mois.append(np.any([dates.month==i],axis=0))
   
    data_mensuel=[dataset[champs].values[mois[i]] for i in range(12)]
    if saison == 'DJF':
        
        xarrayseason=xr.DataArray(data_mensuel[11].mean(axis=0) + data_mensuel[0].mean(axis=0) + 
                              data_mensuel[0].mean(axis=0))
        season_dataset=xr.DataArray.to_dataset(xarrayseason,name='DJF_' + champs)
        season_dataset=season_dataset.assign_coords({'lat' : lat, 'lon' : lon})
    if saison == 'MAM':
        xarrayseason=xr.DataArray(data_mensuel[11].mean(axis=0) + data_mensuel[0].mean(axis=0) + 
                              data_mensuel[0].mean(axis=0))
        season_dataset=xr.DataArray.to_dataset(xarrayseason,name='MAM_' + champs)
        season_dataset=season_dataset.assign_coords({'lat' : lat, 'lon' : lon})
    if saison == 'JJA':
        xarrayseason=xr.DataArray(data_mensuel[11].mean(axis=0) + data_mensuel[0].mean(axis=0) + 
                              data_mensuel[0].mean(axis=0))
        season_dataset=xr.DataArray.to_dataset(xarrayseason,name='JJA_' + champs)
        season_dataset=season_dataset.assign_coords({'lat' : lat, 'lon' : lon})
    if saison == 'SON':
        xarrayseason=xr.DataArray(data_mensuel[11].mean(axis=0) + data_mensuel[0].mean(axis=0) + 
                              data_mensuel[0].mean(axis=0))
        season_dataset=xr.DataArray.to_dataset(xarrayseason,name='SON_' + champs)
        season_dataset=season_dataset.assign_coords({'lat' : lat, 'lon' : lon})
    return season_dataset
    