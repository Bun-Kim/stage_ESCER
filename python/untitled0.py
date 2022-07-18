#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 06:11:50 2022

@author: bun-kim
"""



import datetime
import os

import numpy as np

import xarray as xr
from netCDF4 import Dataset

import pandas as pd

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


from eofs.standard import Eof


import warnings
warnings.filterwarnings("ignore")

import data_processing
import ajustement

base = {'anneeDebut': 2018, 'anneeFin': 2019, 'anneeDebut_model': 2018,
        'anneeFin_model': 2019,
        'frequence': '1D', 'resolution': 1,
        'proxy': ['cape', 'cp'], 'model_proxy': 'Era5', 'model_obs': 'WWLLN',
        'latS': 40,
        'latN': 90, 'lonW': -150, 'lonE': -50, 'method_obs': 'max',
        'methode_temporelle_proxy': ['max', 'sum'],
        'methode_spatiale_proxy': ['mean', 'mean'], 'methode_proxy': 'mul', 'methode_spatiale': ['bilinear', 'bilinear']}


dir_data='./data/'
dir_res='./result/'
dir_figs='./figs/'
dir_anim='./anim/'

if not os.path.exists(dir_figs):
    os.makedirs(dir_figs)
if not os.path.exists(dir_anim):
    os.makedirs(dir_anim)
if not os.path.exists(dir_res):
    os.makedirs(dir_res)
    
infile = dir_data+'WWLLN_2010-2019.nc'
infile_model = dir_data+'cape_cp_era5_2018-2020.nc'
data0    = data_processing.ouvre_fichier('../data/observation/WWLLN_2010-2019.nc')
data0_model    = data_processing.ouvre_fichier('../data/model/cape_cp_era5_2018-2020.nc')
data0 = data0.rename({'Time': 'time'})
data0

data0_model = data_processing.changement_nom_coordonnees_model(base, data0_model)

data0_model = ajustement.resolution_temporelle_obs(base, data0_model)
data0_model = temp2 = ajustement.resolution_spatiale_model(base,data0,data0_model)


startday  = '2018-01-01'
endday  = '2019-12-31'

startyear = startday[0:4]

latS=40
latN=90
lonW=-150
lonE=50

# Date index from startday to endday
dates = pd.date_range(startday, endday, freq='D')

#Exclusion du 29 février
jours=np.any([dates.day!=29,dates.month!=2],axis=0)
dates2=dates[jours]

data = data0.assign_coords(lon=(((data0.lon + 180) % 360) - 180)).sortby('lon')
data_season = data0.sel(lat=slice(latS,latN)).sel(lon=slice(lonW,lonE)).sel(time=slice(startday,endday)).sel(time=dates2)

lat  = data_season.lat.values
lon  = data_season.lon.values
time  = data_season.time.values

bounds = [lonW, lonE, latS, latN]

#Les anomalies sont calculées par rapport à une moyenne glissante sur une fenêtre de 90jours
anomalies = data_season.groupby('time')-data_season.rolling(time=30,center=True).mean()
anomalies

#On se débarasse des nan en excluant les jours sur les bords du domaine (les 45 premiers et les 45 derniers)

delta = datetime.timedelta(days = 15)
startday2 = dates2[0] + delta
endday2 = dates2[-1]-delta

#dates3 servira pour le calcul des fréquences mensuelles
dates3 = pd.date_range(startday2, endday2, freq='D')
jours=np.any([dates3.day!=29,dates3.month!=2],axis=0)
dates3=dates3[jours]

anomalies=anomalies.sel(time=slice(startday2,endday2))


infile1 = dir_res+"F"
data_season.to_netcdf(infile1)

infile2=dir_res+"anoZ500"
anomalies.to_netcdf(infile2)

filename = infile1
ncin = Dataset(filename, 'r')
lons = ncin.variables['lon'][:]
lats = ncin.variables['lat'][:]
Z500 = ncin.variables['F'][:]
ncin.close()

filename = infile2
ncin = Dataset(filename, 'r')
lons = ncin.variables['lon'][:]
lats = ncin.variables['lat'][:]
AnoZ500 = ncin.variables['F'][:]
ncin.close()


AnoZ500 = data0.F.values

coslat = np.sqrt(np.cos(np.deg2rad(lat)))
wgts = np.reshape(coslat,(np.shape(coslat)[0],1))
solver = Eof(AnoZ500, weights=wgts, center=True)

varfrac = solver.varianceFraction()


n=15
eofs = solver.eofsAsCovariance(neofs=n)
#pcs = solver.pcs(npcs=n, pcscaling=1)
pcs = solver.pcs( pcscaling=1)

import eofs.tools.standard

correlation_maps = eofs.tools.standard.correlation_map(pcs, anomalies.F.values)

correlation_maps=xr.DataArray(correlation_maps)
correlation_maps=xr.DataArray.to_dataset(correlation_maps,name='F')
for k in range(700):
    correlation_maps.F.values[np.isnan(correlation_maps.F.values)]=0
    
correlation_maps=correlation_maps.assign_coords({"time" : time, "lat" : lat,"lon": lon})

import carte


carte.tracer(base, correlation_maps, "F")