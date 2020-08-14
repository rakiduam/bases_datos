# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 19:56:07 2020

@author: fanr

reordenar archivos, descargados desde agromet-RAN.
por variable.

"""

import os, glob, numpy as np, pandas as pd
from datetime import datetime

dateparse = lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M')

os.chdir('D:/')

carpeta_reportes = 'D:/Downloads/agromet/'

reportes_historicos = set(glob.glob(carpeta_reportes + '*2019*.csv')) - set(glob.glob(carpeta_reportes + '*(?).csv'))

# dataframe/orden de lectura por estaciones.
estaciones = pd.DataFrame(([archivo.split('\\')[1][8:][:-34] for archivo in reportes_historicos],
                  reportes_historicos)).T

estaciones.columns = ['estacion', 'archivo']
estaciones = estaciones.reindex()
estaciones = estaciones.sort_values(by=['estacion'])

listado_estaciones = set([archivo.split('\\')[1][8:][:-34] for archivo in reportes_historicos])

#crear dataframe con columnas y datos cada 15min.

agromet = pd.DataFrame(index = pd.date_range( start = "2019/01/01 0:00",
                                            end = "2019/12/31 23:59",
                                            freq='1h'),
                      columns = ['jar', 'mes', 'dia', 'hora'])

agromet.jar = agromet.index.year
agromet.mes = agromet.index.month
agromet.dia = agromet.index.day
agromet.hora = agromet.index.hour

counter=0
listado_final=[]
for count, est in enumerate(estaciones.iloc[:,1]):
    bb = pd.read_csv(est, sep = ',', header=0)
    # si tiene menos de 6 meses de datos ni siquiera se considera.
    if bb.shape[0] > 4470:
        #counter += 1
        #print( counter, bb.shape, count , estaciones.iloc[count,0])
        listado_final = listado_final + [estaciones.iloc[count,0]]
        bb.columns = ['FechaHora', 'TempPromedioAire', estaciones.iloc[count,0], 
              'HumedRelPromedio', 'PresionAtmosferica', 'RadiacionSolarMax.',
              'VelocMaxViento', 'TempMinima', 'TempMaxima', 'DireccionDelViento',
              'TempSuperficial', 'GradosDiaBase10', 'HorasFrioBase7']
        bb.iloc[:,0] = (bb.iloc[:,0]).apply(dateparse)
        bb.index = bb.FechaHora
        bb[bb.iloc[:,2] < 0] = np.nan
        bb[bb.iloc[:,2] >= 30] = np.nan
        if bb.iloc[:,2].count() >= 8322:
            # se filtra que tenga aprox el 95% de datos del año
            agromet=agromet.join(bb.iloc[:,2], how='left')
    bb = None

agromet[agromet.iloc[:,4:] < 0] = np.nan
agromet[agromet.iloc[:,4:] >= 30] = np.nan


# identificar 12,7

# agromet.info()

aa=agromet.describe().T
bb=aa[aa.iloc[:,0] >= 8000]
agromet.to_excel("D:/agromet_v4.xlsx")


datos = (agromet.groupby('mes').count()).T
datos.to_excel("D:/datos_agromet.xlsx")



# aa = agromet.groupby([agromet.mes, agromet.dia]).agg(max)
# aa = agromet.groupby(agromet.año).agg(sum)

# max(aa)

# bb = pd.read_csv(estaciones.iloc[27, 1], sep = ',', header=0)

# agromet=agromet.join(bb.iloc[:,2], how='left')

# metadata.loc[rows, hoja] = data.loc[rows, hoja]

# bb.columns[:13] = ['FechaHora', 'TempPromedioAire', 'PrecipitacionHoraria', 
#               'HumedRelPromedio', 'PresionAtmosferica', 'RadiacionSolarMax.',
#               'VelocMaxViento', 'TempMinima', 'TempMaxima', 'DireccionDelViento',
#               'TempSuperficial', 'GradosDiaBase10', 'HorasFrioBase7']

# agromet=agromet.append(bb.iloc[:,2])



