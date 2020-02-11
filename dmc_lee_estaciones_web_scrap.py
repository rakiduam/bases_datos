# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 16:45:31 2020

@author: fanr

# referencias:
- https://pandas.pydata.org/
- https://www.youtube.com/watch?v=E5cSNSeBhjw
"""

import pandas as pd
from calendar import monthrange
# import numpy as np
from bs4 import BeautifulSoup
import requests

# Informe Climatológico Mensual Con Datos Diarios (Agro)
url = 'https://climatologia.meteochile.gob.cl/application/mensuales/climatMensualDatosDiarios/180005/2019/2'
# datos de metadata estacion, periodo
estacion, date_year, date_month = (url.split(sep='/'))[-3:]

# estimacion de la cantidad de dias del mes.
# se puede optimizar donde solo calcule feb que varia, y el resto como opciones
date_days = str(monthrange(int(date_year), int(date_month))[-1])

# comienzo de la extraccion de datos
requ = requests.get(url)
soup = BeautifulSoup(requ.text, "html.parser")

requ = None # solo libera memoria de la peticion

# ubicacion de la tabla de interes, para estos datos las tablas varian
# es necesario ubicar que es lo que interesa
div = soup.find('div', attrs={'class':"panel-body text-left"})
table_rows = div.find_all('tr')

# comienzo de la depuracion de informacion y transformacion a un dataframe
# primero almacena en una lista
l = []
for tr in table_rows:
    td = tr.find_all('td')
    row = [tr.text for tr in td]
    l.append(row)

# transforma la lista y le asigna nombres a las columnas, modificadas desde
# columnas de origen
data = pd.DataFrame(l, columns=['tmin_c','tmax_c','tmed_c',
                                'humedad_media_porcentaje','agua_caida_mm',
                                'evapotranspiracion_mm-dia',
                                'rad_glob_total_dia_watt-m2',
                                'rad_glob_max_watt-m2',
                                'rad_glob_hora_local'], dtype='unicode')

# se eliminan aquellos filas sin informacion, 2 primeras, 3 ultimas
data = data.drop(axis=0, index=(data.index[:2].tolist()+data.index[-3:].tolist()))

# se calcula e inserta la fecha correspondiente, como primera columna
data.insert(loc=0, column='fecha',
            value=pd.date_range(start=('-').join([date_year, str(date_month).zfill(2),'01']),
                                end=('-').join([date_year, str(date_month).zfill(2), date_days])))

# en teoria, este codigo debería ser iterable, para extraer informacion desde dmc

# periodo = (('-').join([date_year, str(date_month).zfill(2),'01']) + '_'+ ('-').join([date_year, str(date_month).zfill(2), date_days]))
# nombre = ('/').join(['D:', ('_').join([estacion, periodo])])

# data.to_csv(path_or_buf=(nombre+'.csv'), sep=',', na_rep='NaN')

# %% listado estaciones

url = 'https://climatologia.meteochile.gob.cl/application/informacion/buscadorDeEstaciones/'
req = requests.get(url)
soup = BeautifulSoup(req.text, 'html_parser')







# %% de aqui en adelante es solo relleno y pruebas, falta para codigo final

#print(soup.div['style']="display:none")
soup.table['id']='freq'


for sub_heading in soup.find_all('table'):
    print(sub_heading.text)

table = soup.find('table', attrs={'border':"0", 'cellpadding':"0", 'cellspacing':"0", 'id':"freq"})
table_rows = table.find_all('tr')


div = soup.find('div', attrs={'id':"excel"})
table_rows = div.find_all('tr')