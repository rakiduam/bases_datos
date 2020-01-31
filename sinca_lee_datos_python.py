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

file_entrada = entrada_dir + carpeta_ent + archivo_txt

print(file_entrada)


def dateparse(x):

    if len(str(x))==6:
        x = ('-').join([('').join(['200', str(x)[:1]]), str(x)[2:4], str(x)[-2:]])
    else:
        x = ('-').join([('').join(['20', str(x)[:1]]), str(x)[2:4], str(x)[-2:]])
    return(pd.datetime.strptime(x, '%YY-%m-%d'))

dataVAR = pd.read_csv(file_entrada, sep=";",
                     parse_dates = ['FECHA (YYMMDD)'], date_parser = dateparse,
                     )

print(dataVAR)

#%%
dataVAR = None
fechas = None

