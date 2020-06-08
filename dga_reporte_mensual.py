# -*- coding: utf-8 -*-
"""
Created on Wed May 27 22:26:17 2020

@author: fneir

idea general: extraer la información contenida en los reportes de DGA.
            ordenado y que de lo mismo la cantidad de datos del reporte.

que debe hacer este script:
- generar un listado de archivos
- generar un listado de estaciones contenidas en dichos archivos con metadata
    * supuestos criticos, se usar nombre de hoja como identificador.
- generar un dataframe vacío con el período (1980-2020) de información a extraer
- asignar los datos de las estaciones dentro de este dataframe acorde a la fecha
- escribir un archivo XLS con datos brutos y


supuestos claves:
    - datos vienen en libros de calculo con multiples hojasm, cada hoja posee nombre unico
    - al leerlo con pandas, este genera una serie de diccionarios con las hojas.
        (siendo una lista de listas de diccionarios de dataframes)
    - en caso de faltar un año, la cantidad de datos sera distinta (condicion)

https://www.pythonforbeginners.com/dictionary/how-to-use-dictionaries-in-python/


vecinos mas cercanos:
    - https://towardsdatascience.com/nearest-neighbour-analysis-with-geospatial-data-7bcd95f34c0e
    - https://www.timvink.nl/closest-coordinates/
    - https://medium.com/nam-r/10-essential-operations-for-spatial-data-in-python-4603d933bdda

relleno de datos de pp:
    - https://www.researchgate.net/post/Filling_of_Rainfall_data_gaps
    - http://gidahatari.com/ih-es/metodos-estimacion-completar-datos-precipitacion

IDF:
    - https://www.youtube.com/watch?v=A0aJZqWRqP0

"""

import os, pandas as pd, numpy as np
from glob import glob
# import seaborn as sb
# import os

# necesarios para transformar cada diccionario de hojas, en una lista de estaciones
# import operator
# from functools import reduce

os.chdir('E:/ESTACIONES_CORRECCION/DGA')


archivos_xls = None
archivos_xls = glob('*.xl*')

nombres = None
# nombres = list(set(reduce(operator.concat,[list(pd.read_excel(xls, sheet_name=None).keys()) for xls in archivos_xls])))
nombres = list(set([y for x in [list(pd.read_excel(xls, sheet_name=None).keys()) for xls in archivos_xls]  for y in x]))

data_variable = None
data_variable = pd.DataFrame(index=pd.date_range('1980/01','2020/01',freq='M',closed='left'),
                             columns=nombres)

libros_xls = None
libros_xls = [(pd.read_excel(xls, sheet_name=None, header=10, usecols=[1,2,5,7,9,11,13,15,17,19,21,23,25], skipfooter=1)) for xls in archivos_xls]

for libro in libros_xls[:]:
    for hoja in libro.keys():
        print(hoja)
        ini, fin = str(libro[hoja].iloc[0,0]), str(libro[hoja].iloc[-1,0]+1)
        periodo = pd.date_range(ini, fin, freq='M')
        rango_completo = np.unique(periodo.year) # np.array(range(np.int(ini), np.int(fin)))
        rango_reporte = libro[hoja].iloc[:,0].to_numpy()
        if len(rango_completo) != len(rango_reporte):
            rango = rango_completo[[not(jar in rango_reporte) for jar in rango_completo]]
            for jar in rango:
                niu_fila = {'AÑO':jar, 'ENE':np.float('nan'), 'FEB':np.float('nan'),
                            'MAR':np.float('nan'),'ABR':np.float('nan'),
                            'MAY':np.float('nan'),'JUN':np.float('nan'),
                            'JUL':np.float('nan'),'AGO':np.float('nan'),
                            'SEP':np.float('nan'),'OCT':np.float('nan'),
                            'NOV':np.float('nan'),'DIC':np.float('nan')}
                libro[hoja] = libro[hoja].append(niu_fila, ignore_index=True)
                libro[hoja] = libro[hoja].sort_values(by=['AÑO'], ignore_index=True)


        data = pd.DataFrame(libro[hoja].iloc[:,1:].values.reshape(len(periodo),1), index=periodo, columns=[str(hoja)])
        data_variable.loc[periodo, hoja] = data.loc[:,hoja]
        data, rango_completo, rango_reporte, rango, periodo, ini, fin, jar, niu_fila = None, None, None, None, None, None, None, None, None

del data, rango_completo, rango_reporte, rango, periodo, ini, fin, jar, niu_fila, hoja, libro

data_variable.to_excel('D:/Desktop/DGA_estaciones_1980-2020.xlsx')


# data_variable = pd.DataFrame([pd.to_numeric(data_variable[str(y)]) for y in data_variable.columns]).T
data_variable.head()
data_variable.info()
data_variable.describe()

#%%#############################################################################

# metadata
libros_xls = [pd.read_excel(xls, sheet_name=None, header=4, usecols=[1,3,14,17,21,25], index_col=None, nrows=4) for xls in archivos_xls]

rows = ['Estación','CodigoBNA','Altitud(msnm)','UTMNorte(m)','Cuenca',
        'LatitudS','UTMEste(m)','SubCuenca','LongitudW','ÁreaDrenaje(km2)']

metadata = pd.DataFrame(index=rows, columns=nombres)

for libro in libros_xls:
    for hoja in libro.keys():
        data = pd.DataFrame(libro[hoja].values.reshape(12,2), columns=['0', str(hoja)]).dropna(inplace=False)
        data.index = rows
        metadata.loc[rows, hoja] = data.loc[rows, hoja]
        data = None

metadata = metadata.reindex(['CodigoBNA','Estación','UTMNorte(m)','UTMEste(m)',
                             'LatitudS','LongitudW','Altitud(msnm)','Cuenca',
                             'SubCuenca','ÁreaDrenaje(km2)'])
del libro, hoja, rows, data

metadata = metadata.T

metadata.to_excel('D:/Desktop/DGA_estaciones_1980-2020_metadata.xlsx')

#%% ##########################################################################

## DISTANCIAS
coord = np.transpose(metadata)





#%% ##########################################################################

#     metadata
# libros_xls = [(pd.read_excel(xls, sheet_name=None, header=10, usecols=[1,2,5,7,9,11,13,15,17,19,21,23,25], skipfooter=1)) for xls in archivos_xls]
# xls = archivos_xls[0]
# nombres = list(set(reduce(operator.concat,[list(pd.read_excel(xls, sheet_name=None).keys()) for xls in archivos_xls])))
# [y for x in list for y in x]
# [(pd.read_excel(xls, sheet_name=None, header=4, usecols=cols, index_col=None, nrows=4))
# aa = [pd.read_excel(x, sheet_name=None, header=4, usecols=cols,index_col=None, nrows=4) for x in archivos_xls for y in x]
# [pd.DataFrame(x[y].values.reshape(12,2)).dropna(inplace=False) for x in

# cols = [1,3,14,17,21,25]

# cc = [pd.DataFrame(x[y].values.reshape(12,2)).dropna(inplace=False) for x in aa for y in x]

# cc = metadata.append([y for y in cc])

# [y for x in [list(pd.read_excel(xls, sheet_name=None).keys()) for xls in archivos_xls]  for y in x]

# metadata.loc[rows,:] = cc =pd.DataFrame(aa, columns=nombres)


# aa[0].keys()

# ;print(aa)

# pd.DataFrame(aa[0]['DIGUA EMBALSE'][:5].values.reshape(12,2)).dropna()

# # [pd.read_excel(xls, sheet_name=None).keys() for xls in archivos_xls]

# metadata = []
# # nombres.sort()
# # nombres = nombres[:1]
# # rango de fechas



# #rango_reporte = np.array([2010, 2011, 2015, 2016, 2017, 2019])


# # rango_completo[not(jar in rango_reporte) for jar in rango_completo]

# # if a[[not(d in b) for d in a]]


# # a = list(range(libro[hoja].iloc[0,0], libro[hoja].iloc[-1,0]+1))
# # b = ([2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2019])

# np.


# a[[not(d in b) for d in a]]
# a


# if b in a

# a = np.array((periodo.year).unique().to_list())
# b = np.array(libro[hoja].iloc[:,0].to_list())
# c = list(set(a).intersection(b))
# c.sort()
# c

# df.loc[df.index.month = 3]
# [periodo.index.year in list(set(a).intersection(b))]


# if a != b:
#     periodo = None
#     periodo = pd.DataFrame(index=np.arange(0,len(b)*12), columns=['fechas'])
#     periodo = [(pd.date_range(str(jar)+'-01',str(jar+1)+'-01', freq='M')) for jar in b]


#     data = pd.DataFrame(libro[hoja].iloc[:,1:].values.reshape(len(periodo),1), index=periodo, columns=[str(hoja)])
# #     for jar in b:
# #         periodo =


# set(a).intersection(b)

# if np.arange(np.int(inicio), np.int(fin)) IN np.array([1980, 1981, 1982, 1983, 1984, 1985,1986, 1987, 1988, 1989, 1990]):
#     usar in inverso. para generar los años que no estan
#     en una lista... y luego itera

#     periodo faltante = comparar unico años existentes / guardar añps que existen
#     periodo = periodo [ periodo faltante y dejar lo que esta bien]
# else:
#     periodo = periodo



# data_variable.to_excel('D:/Desktop/asdfghj.xlsx')





#         print(hoja)
#         libro[hoja]
#         [print( (libro[hoja].iloc[:,1:]).values.reshape(1) ) for hoja in libro]

# # lista[libro][hoja]
# libros_xls[0]['AGUA FRIA'].iloc[0,0]
# libros_xls[0]['AGUA FRIA'].iloc[-1,0]


#%% OLD
#         #
#         # data_variable = data_variable.join(data, lsuffix=fechas, rsuffix=periodo, sort = True)
#         # aa = data_variable.merge(data, how='left', on=hoja)        # aa = data_variable.merge(data, how='left', left_index=True, right_index=True)
#         # aa= data_variable.merge(data, on=hoja)
#         #
#         #
#         #
# # dictionary
# df0 = pd.read_excel(archivo, sheet_name=None, header=10, usecols=[2,5,7,9,11,13,15,17,19,21,23,25], skipfooter=1)
# # df1 = pd.read_excel(archivo, header=10, usecols=[1,2,5,7,9,11,13,15,17,19,21,23,25], skipfooter=1)

# # imprime todas los diccionatios y sus datos
# # for key in df0.items(): print (key)

# # genera la lista de los diccionarios "nombre"
# # type(df0['LONTUE'])
# hojas = list(df0.keys())

# # acceder a un dato especifico dentro de un diccionario especifico y reshapear
# aa = pd.DataFrame(index=np.arange(0,120), columns=hojas)

# for i in (hojas):
#     print(i)
#     #df0[i].to_csv(entrada_dir + 'hidrobas/data_'+ str(i) +'.txt', sep=',', header=False, index=False, line_terminator='\t')
#     aa[i] = pd.DataFrame(df0[i].values.reshape(120,1))
#     # if count==0:
#     #     aa[i] = pd.DataFrame(df0[i].values.reshape(120,1))
#     # else:
#     #     aa.append(pd.DataFrame(df0[i].values.reshape(120,1)))



# aa.to_excel(entrada_dir + 'estaciones.xlsx')


# # aa = [(df0[i].values.reshape(120,1)) for i in hojas]


# # pd.DataFrame((df0['RIO MATAQUITO EN LICANTEN']).to_numpy().reshape(120,1))
# # (df0['RIO MATAQUITO EN LICANTEN'])
