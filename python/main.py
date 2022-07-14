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

#####
carte.tracer(base, proxy/10000, 'proxy')
carte.tracer(base,da_obs/(100*100),'F')

####
import numpy as np
mois=[]
for i in range(1,13):
        mois.append(np.any([date2_model.month==i],axis=0))