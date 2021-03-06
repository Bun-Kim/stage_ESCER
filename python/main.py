#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 13:56:14 2022

@author: san
"""

import data_processing
import ajustement
import proxy_calculation as pc
import carte
import statistiques

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
#b='../data/model/cape_cp_era5_2018-2020_1.nc'
infile0_obs.append(a)
infile0_model.append(b)
varname_obs.append(c)
varname_model.append(d)

print('ouverture des fichiers')

temp = data_processing.ouvre_fichier(a)
temp1 = data_processing.ouvre_fichier(b)

#print('ajustement mask')
#temp1 = data_processing.mask_canada(temp1)

temp = data_processing.changement_nom_coordonnees_obs(base, temp)
temp1 = data_processing.changement_nom_coordonnees_model(base, temp1)




print('ajustement des obs')
print('ajustement temporel')
temp=ajustement.resolution_temporelle_obs(base, temp)
print('ajustement spatial')
#temp3=ajustement.resolution_spatiale_obs(base,temp,0.1)


[t_obs,la_obs,lo_obs,da_obs,date2_obs]=data_processing.selectionDonnees(base,temp  )



print('ajustement des donnees pour le proxy')
print('ajustement temporel')
temp1=ajustement.resolution_temporelle_model(base, temp1)
print('ajustement spatial')
temp2 = ajustement.resolution_spatiale_model(base,temp,temp1)

#Dataset_controle_methode=ajustement.controle_resolution_spatiale_model_cape(base,temp,temp1)

[t_model,la_model,lo_model,da_model,date2_model]=data_processing.selectionDonnees(base,temp2)

proxy= pc.proxy_calculus(base, da_model) *20

#attention si on ajuste sur les donnees modeles, faire une fonction pour trier les lat

###############
#carte.trace_controle_methode_regrid(base, Dataset_controle_methode, 'cape')

#proxy = proxy.where(proxy.proxy<10)

carte.tracer(base, proxy/10000, 'proxy')
carte.tracer(base, da_obs/(100*100),'F')


####################3

from netCDF4 import Dataset
infile1 = '../data/observation/F.nc'
da_obs.to_netcdf(infile1)

infile2='../data/model/proxy.nc'
proxy.to_netcdf(infile2)

filename = infile1
ncin = Dataset(filename, 'r')
lo_obs = ncin.variables['lon'][:]
la_obs = ncin.variables['lat'][:]
t_obs = ncin.variables['time'][:]
da_obs.F.values = ncin.variables['F'][:]
ncin.close()

filename = infile2
ncin = Dataset(filename, 'r')
lo_model = ncin.variables['lon'][:]
la_model = ncin.variables['lat'][:]
t_model = ncin.variables['time'][:]
proxy.proxy.values = ncin.variables['proxy'][:]
ncin.close()
##############

A= data_processing.ouvre_fichier(infile2
                                 )
















import numpy as np

F_values= da_obs.F.values/(100*100)
proxy_values = proxy.proxy.values/10000

F_mean_annuel= np.mean(da_obs.F.values,axis=0)/(100*100)
proxy_mean_annuel = np.mean(proxy.proxy.values,axis = 0)/10000


##############
#attention application du mask tres couteuse
#carte.tracer(base, data_processing.domaine_canada(proxy/10000), 'proxy')
#carte.tracer(base, data_processing.domaine_canada(da_obs/(100*100)),'F')

####
#saison = {'DJF','MAM','JJA','SON'}
DJF_dataset_obs = statistiques.data_saison(da_obs/(100*100), 'F', 'DJF', date2_obs, lo_obs, la_obs)
DJF_dataset_proxy = statistiques.data_saison(0.39*proxy/10000, 'proxy', 'DJF', date2_obs, lo_obs, la_obs)

MAM_dataset_obs = statistiques.data_saison(da_obs/(100*100), 'F', 'MAM', date2_obs, lo_obs, la_obs)
MAM_dataset_proxy = statistiques.data_saison(0.39*proxy/10000, 'proxy', 'MAM', date2_obs, lo_obs, la_obs)

JJA_dataset_obs = statistiques.data_saison(da_obs/(100*100), 'F', 'JJA', date2_obs, lo_obs, la_obs)
JJA_dataset_proxy = statistiques.data_saison(0.39*proxy/10000, 'proxy', 'JJA', date2_obs, lo_obs, la_obs)

SON_dataset_obs = statistiques.data_saison(da_obs/(100*100), 'F', 'SON', date2_obs, lo_obs, la_obs)
SON_dataset_proxy = statistiques.data_saison(0.39*proxy/10000, 'proxy', 'SON', date2_obs, lo_obs, la_obs)

#saison_dataset_obs names = {'DJF_F','MAM_F','JJA_F','SON_F'}
#saison_dataset_proxy names = {'DJF_proxy','MAM_proxy','JJA_proxy','SON_proxy'}
carte.tracer_saison(base, DJF_dataset_obs, "DJF_F")
carte.tracer_saison(base, DJF_dataset_proxy, "DJF_proxy")

carte.tracer_saison(base, MAM_dataset_obs, "MAM_F")
carte.tracer_saison(base, MAM_dataset_proxy, "MAM_proxy")

carte.tracer_saison(base, JJA_dataset_obs, "JJA_F")
carte.tracer_saison(base, JJA_dataset_proxy, "JJA_proxy")

carte.tracer_saison(base, SON_dataset_obs, "SON_F")
carte.tracer_saison(base, SON_dataset_proxy, "SON_proxy")
'''
import xarray as xr
import numpy as np
mask = xr.open_mfdataset('ERA5_mask_Canadian_timezone_ESRI_v4.nc')
#mask = mask.rename({'longitude': 'lon','latitude': 'lat'})


DJF_dataset_obs=DJF_dataset_obs.where(mask.region > 0 )
carte.tracer_saison(base, DJF_dataset_obs, "DJF_F")
'''
#mask_array=np.asarray(mask.region.values)
#mask_dataaray=xr.DataArray(mask_array)
#mask_dataset=xr.DataArray.to_dataset(mask_dataaray,name='region')
#mask_dataset=mask_dataset.assign_coords({'lat' : mask.latitude.values, 'lon' : mask.longitude.values})
#mask_regridded = ajustement.resolution_spatiale_obs(base, mask_dataset,'region', 1)

