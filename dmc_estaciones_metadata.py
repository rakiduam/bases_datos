# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 12:39:34 2020

@author: fneir
"""
import pandas as pd
import bs4


import pandas as pd
from calendar import monthrange
# import numpy as np
from bs4 import BeautifulSoup
import requests

# Informe Climatológico Mensual Con Datos Diarios (Agro)
url = 'https://climatologia.meteochile.gob.cl/application/informacion/catastroEstaciones/'
# datos de metadata estacion, periodo
# estacion, date_year, date_month = (url.split(sep='/'))[-3:]

# # estimacion de la cantidad de dias del mes.
# # se puede optimizar donde solo calcule feb que varia, y el resto como opciones
# date_days = str(monthrange(int(date_year), int(date_month))[-1])

# comienzo de la extraccion de datos
requ = requests.get(url)
soup = BeautifulSoup(requ.text, "html.parser")

requ = None # solo libera memoria de la peticion

# ubicacion de la tabla de interes, para estos datos las tablas varian
# es necesario ubicar que es lo que interesa
#reporte > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > table:nth-child(1)
# table table-bordered table-hover

div = soup.find_all('table', attrs={'class':"table table-bordered table-hover"})

div.find('td')
#div = soup.find_all('div', attrs={'class':"panel-body"})
#table_rows

l = []
for le_div in div:
    table_rows = le_div.find_all('tr')
    for tr in table_rows:
        td = tr.find('td')
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


https://climatologia.meteochile.gob.cl/application/informacion/catastroEstaciones/