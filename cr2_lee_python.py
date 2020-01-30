# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 13:57:03 2020

@author: fanr
"""

import pandas as pd
# import numpy as np
from zipfile import ZipFile


entrada_dir = ('D:/GIT/Bases de Datos')
carpeta_ent = '/cr2_bases_datos'
archivo_zip = '/cr2_prAmon_2018.zip'
# archivo_csv = '/cr2_tasminDaily_2018_ghcn/cr2_tasminDaily_2018_ghcn.txt'
archivo_txt = 'cr2_prAmon_2018/cr2_prAmon_2018.txt'

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
                        )
            ).T

# cambiando los nombres de las columnas por la fila 0
dataVAR.columns = dataVAR.iloc[0]

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
dataVAR.altura = pd.to_numeric(dataVAR.altura)

dataVAR.inicio_observaciones = pd.to_datetime(dataVAR.inicio_observaciones)
dataVAR.fin_observaciones = pd.to_datetime(dataVAR.fin_observaciones)

# dataVAR.institucion = pd.to_string(dataVAR.institucion)
# @todo
#%% estacion por ubicacion particular dentro de la serie (slice)

estacion = dataVAR[0:1]
print(estacion)
#%% buscar estaciones por rango de coordenadas.

#%% buscar estacion por nombre aproximado de estacion y/o cuenca
estacion = dataVAR.loc[dataVAR.nombre=='Visviri']  ## nombre especifico estacion
estacion = dataVAR.loc[dataVAR.nombre_cuenca=='Rio Maipo']

print(estacion)
#%% heatmap de informacion comprendida con los datos




#%%
#%%
#%%
print(dataVAR.iloc[0:1, 0:10])

#latitud
print(dataVAR.iloc[0,4])

#longitud
print(dataVAR.iloc[0,5])

print(dataVAR.where(dataVAR.iloc[4,:]=='-19.*'))

dataVAR[(dataVAR[4]=='-19.*' and dataVAR[5]=='-54.*')]
#df[(df['col1'] >= 1) & (df['col1'] <=1 )]

dataVAR.any(dataVAR[4]=='-19.*')


# %%
############## %%
#df = pd.DataFrame(np.arange(12).reshape(3, 4), columns=['A', 'B', 'C', 'D'])