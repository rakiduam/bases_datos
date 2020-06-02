# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 13:57:03 2020

@author: fanr
"""

import pandas as pd
import seaborn as sb
# import numpy as np
from zipfile import ZipFile


entrada_dir = ('D:/WORK/GIT/bases_datos')
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

## todo el proceso anterior lee los datos como si fueran texto,
## para otros analisis es necesario transformar a numerico, como pasa con R.


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

#%% mensual
""" documentacion:
    - https://stackoverflow.com/questions/34275140/hide-axis-titles-in-seaborn
    - https://stackoverflow.com/questions/15891038/change-data-type-of-columns-in-pandas

"""

import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
# import numpy as np
from zipfile import ZipFile
import numpy as np
import seaborn as sns
import scipy

entrada_dir = ('D:/WORK/GIT/bases_datos')
carpeta_ent = '/cr2_bases_datos'
archivo_zip = '/cr2_prAmon_2019.zip'
archivo_txt = 'cr2_prAmon_2019/cr2_prAmon_2019.txt'

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

## todo el proceso anterior lee los datos como si fueran texto,
## para otros analisis es necesario transformar a numerico, como pasa con R.

# cambiando los nombres de las columnas por la fila 0
dataVAR.columns = dataVAR.iloc[0]

# eliminando la fila 0
dataVAR = dataVAR[1:-1]

dataVAR.latitud = pd.to_numeric(dataVAR.latitud)
dataVAR.longitud = pd.to_numeric(dataVAR.longitud)

# cambiar datos a numerico
## todo el proceso anterior lee los datos como si fueran texto,
 ## para otros analisis es necesario transformar a numerico, como pasa con R.
# for i in range(0, len(dataVAR.iloc[:])):
#     print(i)
#     (dataVAR.iloc[i,14:]) = pd.to_numeric(dataVAR.iloc[i,14:])

# for j in range(14, dataVAR.shape[-1]):
#     print(j)
#     dataVAR.loc[dataVAR.iloc[:, j]<0] = np.nan

df = np.array(dataVAR.iloc[:, 14:], dtype=np.float)

df[np.where(df<0)] = np.nan

dataVAR.iloc[:, 14:] = df

dataVAR.to_excel('D:/dataVAR.xlsx')

# stats.mstats.mquantiles(df)

coordenadas = dataVAR.loc[(dataVAR.latitud<=-34.04) & (dataVAR.latitud>-36.6) &
                          (dataVAR.longitud>-73) & (dataVAR.longitud<=-71.0)]

# coordenadas = dataVAR.loc[(dataVAR.latitud<=-17.0) & (dataVAR.latitud>-58.1) &
#                            (dataVAR.longitud>-73.0) & (dataVAR.longitud<=-69.0)]

# print(coordenadas.latitud.values, coordenadas.longitud.values)

# seleccionar datos dentro de un periodo de tiempo, acorde a la base
ini = '1900-01'
fin = '2019-12'

# https://pandas.pydata.org/docs/user_guide/merging.html
periodo = pd.concat([coordenadas.iloc[:,0:14], coordenadas.loc[:, ini:fin]], axis=1, join='inner')

# contador de cuantos datos validos posee la estación en dicho periodo
# se basa en que datos ya han sido filtrados por nan.
periodo['cuenta'] = (periodo.T).iloc[14:-2,:].count()

periodo = periodo.loc[periodo.cuenta>1]
#periodo = periodo.loc[periodo.cuenta>238]

## ambas funciones realizan lo mismo, una mascara de los valores nulos.
# pd.notna(periodo.iloc[:,14:])
# periodo.iloc[:,14:-1].isnull()

# generar heatmap de datos estacion
calormap = periodo.iloc[:,14:-1].T
calormap.columns = periodo.nombre

# ADDED: Extract axes.
fig, ax = plt.subplots(1, 1,
                       # figsize = (15, 15),
                       #dpi=300
                       )

#la razon porque mostraba solo valores 0-1, era porque estaba como texto.
heat_map = sns.heatmap(periodo.iloc[:,14:-1].astype(float),
                      #vmin=0,
                      #vmax=300,
                      #square=True,
                      mask = periodo.iloc[:,14:-1].isnull(),
                      cbar=True,
                      #center=0.5,
                      #cmap="magma_r",
                      cmap="coolwarm_r",
                      #cmap="binary",
                      #cmap="viridis",
                      yticklabels=periodo.nombre,
                      #annot=True
                      #linewidths=.005
                      )


# ADDED: Remove labels.
ax.set_ylabel('')
ax.set_xlabel('')


#periodo.to_csv('E:/CR2_pp_periodo.csv', sep=';' )

#periodo.to_excel('E:/CR2_pp_periodo.xlsx')

# dataVAR.to_excel('D:/dataVAR.xlsx')

aa = scipy.stats.mstats.idealfourths(df,1)
