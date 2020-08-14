# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 21:19:48 2020

@author: fneir

idea: compararar dos bases de datos
    identificadores, codigos de estaciones.

"""
#%% COMPARAR CON CR2

import pandas as pd, numpy as np

file_cr2 = 'E:/ESTACIONES_CORRECCION/BBDD/cr2_prAmon_2019/cr2_prAmon_2019.txt'
file_dga = 'E:/ESTACIONES_CORRECCION/DGA/DGA_1980-2020_reporte_web.xlsx'

cr2 = pd.read_csv(file_cr2, sep=',', na_values=-9999, header = None,
                  skiprows=( np.concatenate(([2, 8], np.arange(10,975)), axis=0) ),
                  encoding='latin_1')

dga = pd.read_excel(file_dga, sheet_name=0, index_col=None)

cr2.info()
cr2.head()
dga.info()
dga.head()
# dga.columns = None

cod_dga = list([str(np.int(cod.split('-')[0])) for cod in dga.iloc[0,1:]])
cod_cr2 = list(cr2.iloc[0])

filtro = set(cod_cr2).intersection(cod_dga)

len(filtro)-len(cod_dga)

dga.columns = list([dga.iloc[0,0]]) + ([str(np.int(cod.split('-')[0])) for cod in dga.iloc[0,1:]])
cr2.columns = list(cr2.iloc[0])

cr2v2 = cr2[filtro]
dgav2 = dga[filtro]

dgav2 = dgav2.T; dgav2.columns = (dga.iloc[:,0])
cr2v2 = cr2v2.T; cr2v2.columns = cr2.iloc[:,0]

dgav2.nombre = [nom.strip().upper() for nom in dgav2.nombre]
cr2v2.nombre = [nom.upper() for nom in cr2v2.nombre]

# este no funciono, porque los nombres no estan iguales
# dgav2 = dgav2.sort_values(by=['nombre'])
# cr2v2 = cr2v2.sort_values(by=['nombre'])

dgav2 = dgav2.sort_values(by=['codigo_estacion'])
cr2v2 = cr2v2.sort_values(by=['codigo_estacion'])

for count, i in enumerate(dgav2.nombre): print(dgav2.nombre[count]==cr2v2.nombre[count], dgav2.nombre[count], cr2v2.nombre[count])


##%%
array_dga = np.array(dgav2[dgav2.columns[-480:]].apply(pd.to_numeric))
array_cr2 = np.array(cr2v2[cr2v2.columns[-480:]].apply(pd.to_numeric))

guardar = np.copy(array_dga)

array_cr2.dtype
array_dga.dtype

array_dga = np.nan_to_num(array_dga, copy=True, nan=-9999, posinf=None, neginf=None)
array_cr2 = np.nan_to_num(array_cr2, copy=True, nan=-9999, posinf=None, neginf=None)

compara = np.where((array_cr2-array_dga)==0, True, False)
compara1 = np.array(compara, dtype=np.float)
#compara1 = np.where((array_cr2-array_dga)==0, True, False)
# compara = np.where(compara==0, True, False)
# compara = np.where(array_dga == array_cr2, True, False)
# compara2 = array_dga == array_cr2
# bb = compara1==compara2

# [print(i) for i in compara[::,::]]
cuenta=0
for count_row, row in enumerate(compara[:]):
    for count_item, item in enumerate(row):
        if compara[count_row, count_item] == True:
            compara1[count_row, count_item] = array_dga[count_row, count_item]
        elif compara[count_row, count_item] == False:
            if array_dga[count_row, count_item] > array_cr2[count_row, count_item]:
                compara1[count_row, count_item] = array_dga[count_row, count_item]
            elif array_dga[count_row, count_item] < array_cr2[count_row, count_item]:
                compara1[count_row, count_item] = array_cr2[count_row, count_item]
                cuenta=cuenta+1

compara1[compara1<0] = np.nan


relleno = (dga.iloc[:,(dga.columns).isin(filtro)]).T

relleno.columns = dga.iloc[:,0]

relleno = relleno.sort_values(['codigo_estacion'])

relleno[relleno.columns[-480:]] = np.array(relleno[relleno.columns[-480:]].apply(pd.to_numeric))

relleno.fuente = 'dga_web+cr2'

relleno[relleno.columns[-480:]] = compara1

relleno = relleno.sort_values(['Estación'])

relleno = relleno.T

fechas = [(i) for i in (relleno.index[-480:])]

#fechas
relleno = relleno.reindex(['CodigoBNA', 'codigo_estacion', 'fuente', 'institucion',
                            'nombre', 'Estación', 'UTMNorte(m)', 'UTMEste(m)',
                            'LatitudS', 'LongitudW', 'lat', 'lon', 'Altitud(msnm)',
                            'Cuenca', 'SubCuenca', 'ÁreaDrenaje(km2)']+
                            fechas)
# relleno.info()
# sumario = [relleno.iloc[16:,].describe(), relleno.iloc[16:,].min(),
#            relleno.iloc[16:,].max(),relleno.iloc[16:,].std()]

# relleno.summary()


relleno.to_excel('D:/Desktop/DGA_CR2_1980-2019.xlsx', header=False, encoding='utf-8')

#%% COMPARAR CON EROSION 2010
import pandas as pd, numpy as np, os

os.chdir('E:/Factor_R/')

er2010 = pd.read_excel('BBDD/erosion2010/pp_erosion_2010_ordenado.xlsx')
dgacr2 = pd.read_excel('BBDD/DGA_reporte_web_1980-2019/DGA_CR2_1980-2019.xlsx')

er2010[pd.isnull(er2010)] = -9999
dgacr2[pd.isnull(dgacr2)] = -9999

# filtrado de datos.
cod_er2010 = [str(i).strip() for i in pd.to_numeric(er2010.iloc[2,1:])]
cod_dgacr2 = [str(i).strip() for i in pd.to_numeric(dgacr2.iloc[1,1:])]

filtro = set(cod_er2010).intersection(cod_dgacr2)

# columnas y filtrado
er2010.columns = ['CODIGO']+cod_er2010 # er2010.iloc[2,:]
dgacr2.columns = ['CODIGO']+cod_dgacr2 # [i.strip() for i in dgacr2.iloc[1,:]]

er2010.head()
dgacr2.head()

er2010v2 = (er2010[filtro]).T
dgacr2v2 = (dgacr2[filtro]).T

er2010v2.columns = er2010.iloc[:,0]
dgacr2v2.columns = dgacr2.iloc[:,0]

er2010v2 = er2010v2.sort_values(by=['CODIGO'])
dgacr2v2 = dgacr2v2.sort_values(by=['CODIGO'])

comparar_nombres = (pd.DataFrame([list(er2010v2.NOMBRE==dgacr2v2.nombre), list(er2010v2.NOMBRE), list(dgacr2v2.nombre)])).T

# aqui hay que hacer match de los periodos de tiempo.
# erosion2010 va desde 1900 a 2010, debi poner 2019
# dgacr2 va desde 1980 a 2019
array_er2010v2 = np.array(er2010v2.iloc[:,-(364+8):-24].apply(pd.to_numeric))
array_dgacr2v2 = np.array(dgacr2v2.iloc[:,16:364].apply(pd.to_numeric))

# aa = er2010v2.iloc[:,-(364+8):-24]
# bb = dgacr2v2.iloc[:,16:364]

compara = np.where((array_er2010v2 - array_dgacr2v2)==0, True, False)
compara1 = np.array(compara, dtype=np.float)

# analizar caso a caso que valores cambiar
# si son iguales se mantiene el valor
# si difieren, se mantiene el valor de erosion2010
#       si difieren y erosion2010 es -9999, y dgacr2 existe, queda dgacr2
#       si difieren y erosion2010 no es -9999, queda erosion2010
cuenta=0
for count_row, row in enumerate(compara[:]):
    for count_item, item in enumerate(row):
        # son iguales
        if compara[count_row, count_item] == True:
            compara1[count_row, count_item] = array_dgacr2v2[count_row, count_item]
        # difiere
        elif compara[count_row, count_item] == False:
            # si difiere y ero2010=-9999
            if array_dgacr2v2[count_row, count_item] == -9999:
                compara1[count_row, count_item] = array_er2010v2[count_row, count_item]
                cuenta=cuenta+1
            # si difiere y ero2010>-9999
        else: #array_dgacr2v2[count_row, count_item] < array_er2010v2[count_row, count_item]:
                compara1[count_row, count_item] = array_dgacr2v2[count_row, count_item]


# reemplazar los nan definidos como -9999, a NAN
# compara1[compara1<0] = np.nan

dgacr2v2.iloc[:,16:364] = compara1
dgacr2v2.fuente = 'dga_web+cr2+erosion2010'

# datos no comprendidos dentro de la comparacion anterior, son los que deberian
# agregarse como la base completa de datos.
no_compara = dgacr2[dgacr2.columns.difference(filtro, sort=False)]
# no_compara[no_compara<0] = np.nan

#dejar index (rows) iguales
no_compara.index = dgacr2v2.T.index

bb = (pd.merge(left=no_compara, right=dgacr2v2.T, how='outer', left_index=True, right_index=True)).reset_index(drop=True)

bb.head(20)
dgacr2.head(20)

len(set(bb.columns.to_list()).intersection(set(dgacr2.columns.to_list())))

cc = bb[(['CODIGO']+sorted((bb.columns.to_list()))[:-1])] == dgacr2[(['CODIGO']+sorted(dgacr2.columns.to_list())[:-1])]

bb.to_excel('BBDD/DGA_CR2_Erosion2010_1980-2019.xlsx', header=False, encoding='utf-8')
cc.to_excel('BBDD/DGA_CR2_Erosion2010_comparacion.xlsx', header=False, encoding='utf-8')
# bb[bb<0] = np.nan




# en este paso se busca reemplazar el dato dentro de la serie original.


# bb = dgacr2 == no_compara
# aa = dgacr2v2.iloc[:,16:364] == compara1
# er2010v2.iloc[:,-(364+8):-24].to_excel('BORRAR/er2010v2.xlsx')
# dgacr2v2.iloc[:,16:364].to_excel('BORRAR/dgacr2v2.xlsx')
# pd.DataFrame(compara1).to_excel('BORRAR/compara1.xlsx')
# pd.DataFrame(no_compara).to_excel('BORRAR/no_compara.xlsx')




# #%%
# aa = cr2.iloc[:,cr2.where(cr2.iloc[2,1:], dga.iloc[2,1:], axis=0)]

# f = list(set(cod_dga) & set(cod_cr2))



# [i for i, j in zip(cod_dga, cod_cr2) if i == j]


# # cr2 = (cr2.T)
# #cr2.iloc[:,2] = [nomme.upper() for nomme in cr2.iloc[:,2]]

# # cr2.columns = ([nomme.upper() for nomme in cr2.iloc[2]])
# cr2.columns = list(cr2.iloc[0])

# cr2.loc[cr2.where(f) f]
# cr2.iloc[cr2.where(cr2.columns, cod_dga, axis=0)]

# list(x for x in lst_df if x["origin"] == 'JFK' and x["carrier"] == 'B6')

# type(cod_dga)


# df.iloc[[index for index,row in df.iterrows() if row['origin'] == 'JFK' and row['carrier'] == 'B6']]

# cr2.iloc[[index for index,row in cr2.iterrows() if cr2['NOMBRE'] == 'VISVIRI']]

# [cr2.NOMBRE in ['VISVIRI', 'HUMALPACA']]
# pd.

# cr2.head()
# dga.head()
