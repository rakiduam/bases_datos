# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 13:57:03 2020

@author: fanr
"""

import pandas as pd
import seaborn as sb
import numpy as np
from zipfile import ZipFile


entrada_dir = ('D:/WORK/GIT/bases_datos')
carpeta_ent = '/cr2_bases_datos'
archivo_zip = '/cr2_prDaily_2018_ghcn.zip'
archivo_txt = 'cr2_prDaily_2018_ghcn/cr2_prDaily_2018_ghcn.txt'

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
del zip_file, file_entrada, archivo_txt, archivo_zip, carpeta_ent
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

# dataVAR.columns

dataVAR.latitud = pd.to_numeric(dataVAR.latitud)
dataVAR.longitud = pd.to_numeric(dataVAR.longitud)

# # coordenadas
dataVAR = dataVAR.loc[(dataVAR.latitud<=-32.00) & (dataVAR.latitud>-40.0) &
                          (dataVAR.longitud>-73) & (dataVAR.longitud<=-69.0)]

# temporal
# bisiestos [1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020]
dataVAR = dataVAR.iloc[:,(-365+10960+66):-68]


#dataVAR = dataVAR.iloc[(-(365+10960+66):-68),,]


df = np.array(dataVAR.iloc[:, 14:], dtype=np.float)
