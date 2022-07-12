#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 13:56:14 2022

@author: san
"""

import data_processing
import ajustement
import proxy_calculation as pc

base = {'anneeDebut':2018, 'anneeFin':2019,'anneeDebut_model':2018,
        'anneeFin_model':2020,
        'frequence':'1D', 'resolution':1, 
        'proxy':['cape','cp'], 'model_proxy':'Era5', 'model_obs':'WWLLN',
        'latS':40,
        'latN':90,'lonW':-150,'lonE':-50,'method_obs':'max',
        'methode_temporelle_proxy':['max','sum'],
        'methode_spatiale_proxy':['mean','mean'],'methode_proxy':'mul','methode_spatiale':['bilinear','bilinear']}

#etape 1 : initialisation
infile0_obs=[]
infile0_model=[]
varname_obs=[]
varname_model=[]
debut=[]
fin=[]
time=[]
lat=[]
lon=[]
data_season=[]
saison=[]
dates=[]
nom_fichier=[]


a,b,c,d= data_processing.initialise_variables(base)
infile0_obs.append(a)
infile0_model.append(b)
varname_obs.append(c)
varname_model.append(d)

print('ouverture des fichiers')

temp = data_processing.ouvre_fichier(a)
temp1 = data_processing.ouvre_fichier(b)
temp = data_processing.changement_nom_coordonnees_obs(base, temp)
temp1 = data_processing.changement_nom_coordonnees_model(base, temp1)

print('ajustement des obs')
temp=ajustement.resolution_temporelle_obs(base, temp)
#temp=ajustement.resolution_spatiale_obs(base,temp,temp1)


[t_obs,la_obs,lo_obs,da_obs,date2_obs]=data_processing.selectionDonnees(base,temp)

print('ajustement des donnees pour le proxy')
temp1=ajustement.resolution_temporelle_model(base, temp1)

temp1 = ajustement.resolution_spatiale_model(base,temp,temp1)


[t_model,la_model,lo_model,da_model,date2_model]=data_processing.selectionDonnees(base,temp1)

proxy= pc.proxy_calculus(base, da_model)

#attention si on ajuste sur les donnees modeles, faire une fonction pour trier les lat

import cartopy.feature as cfeature
import matplotlib as mpl
from matplotlib.colors import BoundaryNorm
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

import numpy as np

dico = base
bounds = [base['lonW'], base['lonE'], base['latS'], base['latN']]



#colbar=mpl.colors.ListedColormap(proxy)
fig=plt.figure(figsize=(10,6), frameon=True)   
ax = plt.subplot(111, projection=ccrs.Orthographic(central_longitude=(dico['lonW']+dico['lonE'])/2, central_latitude=(dico['latS']+dico['latN'])/2))

ax.set_extent(bounds, crs=ccrs.PlateCarree())

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

mm = ax.pcolormesh(lo_model,\
                   la_model,\
                   np.mean(proxy.values,axis=0),\
                   vmin=0,\
                   vmax=4, \
                   transform=ccrs.PlateCarree(),\
                   cmap='jet' )
ax.coastlines(resolution='110m');

plt.show()

############

#colbar=mpl.colors.ListedColormap(proxy)
fig=plt.figure(figsize=(10,6), frameon=True)   
ax = plt.subplot(111, projection=ccrs.Orthographic(central_longitude=(dico['lonW']+dico['lonE'])/2, central_latitude=(dico['latS']+dico['latN'])/2))

ax.set_extent(bounds, crs=ccrs.PlateCarree())

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

mm = ax.pcolormesh(lo_model,\
                   la_model,\
                   np.mean(da_obs.F.values,axis=0),\
                   vmin=0,\
                   vmax=60, \
                   transform=ccrs.PlateCarree(),\
                   cmap='jet' )
ax.coastlines(resolution='110m');

plt.show()

#####

