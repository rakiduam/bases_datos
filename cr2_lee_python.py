# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 13:57:03 2020

@author: fanr
"""

import pandas as pd
import seaborn as sb
# import numpy as np
from zipfile import ZipFile


entrada_dir = ('D:/GIT/Bases de Datos')
carpeta_ent = '/cr2_bases_datos'
archivo_zip = '/cr2_tasmaxDaily_2018_ghcn.zip'
archivo_txt = 'cr2_tasmaxDaily_2018_ghcn/cr2_tasmaxDaily_2018_ghcn.txt'

file_entrada = entrada_dir + carpeta_ent + archivo_zip

zip_file = ZipFile(file_entrada)

# datos_variable = pd.read_csv(zip_file.open(archivo_txt))

dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')

# lee los datos y transpone, dejando columnas como filas.
# esto solo para evitar eliminar informacion de metadata de cada estacion
dataVAR = (pd.read_csv(filepath_or_buffer=zip_file.open(archivo_txt),
                        sep=',',
                        #header=np.arange(0,15).tolist(),
                        na_values=-9999,
                        #dtype=np.float32,
                        encoding = 'utf-8',
                        dtype='unicode'
                        )
            ).T

# cambiando los nombres de las columnas por la fila 0
dataVAR.columns = dataVAR.iloc[0]
# for count, i in enumerate(dataVAR.columns[:20]): print(count, i)

# eliminando la fila 0
dataVAR = dataVAR[1:-1]

#dataVAR.dtypes
#dataVAR.head
#dataVAR.shape
#dataVAR.keys
#dataVAR.head

dataVAR.columns

dataVAR.latitud = pd.to_numeric(dataVAR.latitud)
dataVAR.longitud = pd.to_numeric(dataVAR.longitud)

# @todo
#%% estacion por ubicacion particular dentro de la serie (slice)

estacion = dataVAR.iloc[0:1]
print(estacion)

# buscar estacion por nombre aproximado de estacion y/o cuenca
estacion = dataVAR.loc[dataVAR.nombre=='Visviri']  ## nombre especifico estacion
print(estacion)

#%% busqueda por cuenca, solo valido datos de Chile
cuenca = dataVAR.loc[dataVAR.nombre_cuenca=='Rio Maipo']
print(cuenca)

# heatmap de periodos con datos dentro de la cuenca
heat_map = sb.heatmap(pd.notna(cuenca.iloc[:,14:]), vmin=0, vmax=1, cbar=True,
                      #center=0.5,
                      cmap="binary",
                      yticklabels=cuenca.nombre,
                      )


#%% seleccionar datos dentro de un periodo de tiempo, acorde a la base
ini = '1980-01-01'
fin = '2018-01-01'

# https://pandas.pydata.org/docs/user_guide/merging.html
periodo = pd.concat([cuenca.iloc[:,0:14], cuenca.loc[:, ini:fin]], axis=1, join='inner')

heat_map = sb.heatmap(pd.notna(periodo.iloc[:,14:]), vmin=0, vmax=1, cbar=True,
                      #center=0.5,
                      cmap="binary",
                      yticklabels=cuenca.nombre,
                      )



#%% seleccionar datos comprendidos entre ciertas coordenadas espaciales

# con respecto a una coordenada
coordenadas = dataVAR[dataVAR.latitud<=-19.0]

# entre dos coordenadas
# https://stackoverflow.com/questions/42082385/pandas-slicing-selecting-with-multiple-conditions-with-or-statement
coordenadas = dataVAR.loc[(dataVAR.latitud<-19.0) & (dataVAR.latitud>-32.0)]
print(coordenadas.latitud)

# un poligono definido entre coordenadas geograficas de informacion.
# https://stackoverflow.com/questions/42082385/pandas-slicing-selecting-with-multiple-conditions-with-or-statement
coordenadas = dataVAR.loc[(dataVAR.latitud<=-19.0) & (dataVAR.latitud>-32.0) &
                          (dataVAR.longitud>-72.0) & (dataVAR.longitud<=-68.0)]
print(coordenadas.latitud.values, coordenadas.longitud.values)

