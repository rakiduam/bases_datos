# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 10:16:37 2020

@author: fanr
"""

import pandas as pd, numpy as np, os

os.chdir('E:/Factor_R/BBDD/')

jars = pd.read_excel('jars_filtrado.xlsx', sheet_name="Sheet1", usecols="B:JU",
                     skipfooter=5).T
jars = jars.reset_index()
jars.columns = jars.iloc[0,:]
jars = jars.iloc

fill = pd.read_excel('ALLrellenado1pixel.xlsx', sheet_name="Sheet1",skiprows=1, usecols="A:JU",
                     skipfooter=4).T
fill = fill.reset_index()
fill.columns = fill.iloc[0,:]


estaciones = estaciones.reset_index()
# estaciones.columns = estaciones.iloc[0,:]
estaciones.columns = estaciones.iloc[1,:]
estaciones = estaciones.iloc[2:,:]
estaciones = estaciones.sort_values(by='lat', ascending=False)
estaciones = estaciones.iloc[:, np.arange(0,17).tolist()+np.arange(125,497).tolist()]
estaciones.iloc[:,-372:] = estaciones.iloc[:,-372:].apply(pd.to_numeric)
estaciones = estaciones.reset_index()
estaciones = estaciones.iloc[:,1:]
