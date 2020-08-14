# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 21:39:05 2020

@author: fanr
"""

import glob
import os
from os import path
import pandas as pd
os.chdir('E:/ESTACIONES_CORRECCION/BBDD/IMERG/')
# os.chdir('E:/ESTACIONES_CORRECCION/BBDD/downthemall/')
os.getcwd()

def limpieza(x):
    salida = str(x)
    salida = salida.strip()
    salida = salida.replace('GIOVANNI-g4.timeAvg.GPM_3IMERGM_06_precipitation.','')
    return(salida)


geotif_list = glob.glob('*.*')

# excepcion a los nombres de datos.
geotif_list = [(str(i).replace('Estero_Nilahue_Parcial', 'Rio_Reloca_xxxx'))[:-4] for i in geotif_list]
# geotif_list = [(str(i).replace('.', ''))[:-3] for i in geotif_list]

geotif_list.sort()

# se genera un dataframe, para agregar columnas que permitan el comparar
# nombre original y renombreado.
df = pd.DataFrame(set(geotif_list))
df.columns = ['archivos']
df['limpio'] = [limpieza(i) for i in df.archivos]

tipos = glob.glob('*.*')
tipos = set([str(i)[-4:] for i in tipos])

# extensions = ['.ovr', '.prj', '.tab', '.tfw', '.tif', '.txg', '.xml', '.kml']

os.getcwd()


# print(glob.glob(df.iloc[count, 0]+'*.*'))
for ext in tipos:
    print(ext)
    for count, dem in enumerate(df.archivos):
        #print('1')
        archivo0 = ('').join(glob.glob(df.iloc[count, 0] + '*' + ext))
        largo = len(df.iloc[count, 0])
        archivo1 = (df.iloc[count, 1] + archivo0[largo:])
        if path.exists(archivo0):
            #print(archivo0, archivo1)
            os.rename(archivo0, archivo1)

    # print(df.iloc[count, 0], df.iloc[count, 1])
