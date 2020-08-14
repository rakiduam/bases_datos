# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 16:31:29 2020

@author: fanr
"""

import pandas as pd, numpy as np
import wget
import os

os.chdir('E:/AGROMET/descargas/')

estaciones = pd.read_csv('D:/WORK/GIT/bases_datos/agromet_base_datos/listado_emas.csv',
                        sep=';',
                        header=None,
                        encoding='utf-8'
                        )

estaciones = open('D:/WORK/GIT/bases_datos/agromet_base_datos/listado_emas.txt', 'r')

le = pd.read_csv(estaciones)
estaciones.close()
estaciones = estaciones[estaciones.region.isin(['V', 'VI', 'VII', 'VIII','XIII'])]

estaciones.estacion




url = "https://www.agromet.cl/csv/agromet_Aresti-20190101000000-20191231235900.csv"

wget.download(url, url.split('/')[-1])

for estacion in estaciones.estacion:
    for jar in range(2000, 2020):
        url = ('').join(['https://www.agromet.cl/csv/agromet_', estacion, '-', str(jar),'0101000000-', str(jar), '1231235900.csv'])
        print(url)


https://www.agromet.cl/csv/agromet_Aresti-20100101000000-20101231235900.csv
https://www.agromet.cl/csv/agromet_Lontue-20100101000000-20101231235900.csv
