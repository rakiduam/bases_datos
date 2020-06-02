# -*- coding: utf-8 -*-
"""
Created on Wed May 27 22:26:17 2020

@author: fneir

idea general, leer de manera rapida una serie de estaciones extraidas desde
dga. para esto da lo mismo la cantidad de daots solo que exista el archivo.

que debe hacer este script...
- generar un listado de las estaciones que se estan agregando. para esto
lo que se me ocurre es leer todos los archivos guardar y obtener los nombres
y otros datos

- de ahi generar una suerte de dataframe vacio, donde las columnas sean las estaciones
y posterior ir asignando los datos en las fechas correspondientes



conceptos claves:
    - los datos vienen dentro de una libros de calculo con multiples hojas
    - al leerlo con pandas, este genera una serie de diccionarios.
        (como los entiendo por ahora, seria una suerte de lista, pero con nombre
         que permite desplegar la informacion)
    -

https://www.pythonforbeginners.com/dictionary/how-to-use-dictionaries-in-python/

relleno de datos de pp:
- https://www.researchgate.net/post/Filling_of_Rainfall_data_gaps
- http://gidahatari.com/ih-es/metodos-estimacion-completar-datos-precipitacion


"""

import os, pandas as pd, numpy as np
from glob import glob
# import seaborn as sb
# import os

# necesarios para transformar cada diccionario de hojas, en una lista de estaciones
import operator
from functools import reduce

os.chdir('E:/ESTACIONES_CORRECCION/DGA')

# listado de archivos
lista_xls = glob('*.xl*')
# lista_xls.sort()

# listado estaciones
nombres = None
nombres = list(set(reduce(operator.concat,[list(pd.read_excel(xls, sheet_name=None).keys()) for xls in lista_xls])))


[pd.read_excel(xls, sheet_name=None).keys() for xls in lista_xls]

metadata = []
# nombres.sort()
# nombres = nombres[:1]
# rango de fechas
fechas = pd.date_range('1980-01', '2020-01', freq='M')

# dataframe vacío con estaciones y el periodo. predefinidos. 1980-2019, 12 meses
data_variable = None
data_variable = pd.DataFrame(index=fechas, columns=nombres)

libros_xls = None
libros_xls = [(pd.read_excel(xls, sheet_name=None, header=10, usecols=[1,2,5,7,9,11,13,15,17,19,21,23,25], skipfooter=1)) for xls in lista_xls]


for libro in libros_xls[:]:
    #print(libro.keys())
    for hoja in libro.keys():
        # print(libro[hoja])
        print(hoja)
        inicio, fin = str(libro[hoja].iloc[0,0]), str(libro[hoja].iloc[-1,0]+1)
        periodo = pd.date_range(inicio, fin, freq='M')
        data = pd.DataFrame(libro[hoja].iloc[:,1:].values.reshape(len(periodo),1), index=periodo, columns=[str(hoja)])
        data_variable.loc[periodo, hoja] = data.loc[:,hoja]
        data = None


a = (periodo.year).unique().to_list()
b = libro[hoja].iloc[:,0].to_list()
if a != b:
    periodo = None
    periodo = pd.DataFrame(index=np.arange(0,len(b)*12), columns=['fechas'])
    periodo = pd.DataFrame([(pd.date_range(str(jar)+'-01',str(jar+1)+'-01', freq='M')) for jar in b]).values.reshape(len(b*12),1)

    for jar in b:
        periodo =


set(a).intersection(b)

if np.arange(np.int(inicio), np.int(fin)) IN np.array([1980, 1981, 1982, 1983, 1984, 1985,1986, 1987, 1988, 1989, 1990]):
    usar in inverso. para generar los años que no estan
    en una lista... y luego itera

    periodo faltante = comparar unico años existentes / guardar añps que existen
    periodo = periodo [ periodo faltante y dejar lo que esta bien]
else:
    periodo = periodo



data_variable.to_excel('D:/Desktop/asdfghj.xlsx')





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
