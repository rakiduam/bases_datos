# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 14:13:04 2020

@author: fanr
"""

import pandas as pd
# import seaborn as sb
# import numpy as np
# import datetime

entrada_dir = ('D:/GIT/Bases de Datos')
carpeta_ent = '/sinca_base_datos'
archivo_txt = '/datos_090125_200130.csv'
#archivo_txt = '/datos_150509_200131.txt'

file_entrada = entrada_dir + carpeta_ent + archivo_txt

print(file_entrada)


def obtener_fechas(x):
    """
    mejora formato del dato de fecha a uno que pueda ser leido en python
    los años estan de forma que 2010 se representa como 10 en archivo original.
    """
    x = ('-').join([('').join(['20', str(x)[:2]]), str(x)[2:4], str(x)[-2:]])
#    if len(str(x)) == 6:
#        x = ('-').join([('').join(['20', str(x)[:2]]), str(x)[2:4], str(x)[-2:]])
#    else:
#        x = ('-').join([('').join(['200', str(x)[:2]]), str(x)[2:4], str(x)[-2:]])
    return(pd.datetime.strptime(x, '%Y-%m-%d'))

columnas = ['fecha', 'hora', 'variable', 'nans']

if archivo_txt[-3:]=='csv':
    dataVAR = pd.read_csv(file_entrada, sep=";",
                          parse_dates=['FECHA (YYMMDD)'],
                          date_parser=obtener_fechas,
                          memory_map=True,
                          #encoding='utf-8',
                          #dtype='unicode',
                          decimal=','
                          )
else:
    dataVAR = pd.read_csv(file_entrada,
                          header=None,
                          sep=",",
                          skiprows=range(0, 32),
                          parse_dates=[0],
                          date_parser=obtener_fechas,
                          #memory_map=True,
#                          #encoding='utf-8',
#                          #dtype='unicode',
#                          decimal=','
                          engine='python',
                          skipfooter=5,
                          )
    dataVAR.columns = columnas
    #obtener_fechas(dataVAR.iloc[:,0])

print(dataVAR)
#print(dataVAR.columns)
#print(dataVAR.iloc[0])
#print(dataVAR.loc['Registros validados'])
#%%
dataVAR = None
fechas = None

