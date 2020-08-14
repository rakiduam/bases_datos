# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 18:09:08 2020

@author: fneir
"""
#%% ARCHIVO LLAMADO IF
import pandas as pd, numpy as np, os

os.chdir('E:/ESTACIONES_CORRECCION/datospp')

# xls_archivos = glob('*.xls')
# ['estaciones con el IF.xls',
#  'IX_REGION_A.xls',
#  'VIII-REGIO-B.xls',
#  'VIII_REGIÓN_A.xls',
#  'VII_REGIÓN_A.xls',
#  'VII_REGIÓN_B.xls',
#  'VI_REGION_B.xls',
#  'VI_REGIÓN_A.xls',
#  'V_REGION_A.xls']

df = pd.read_excel('estaciones con el IF.xls', sheet_name=None)


le_df = df['i reg']
lista = []
for cuenta_fila, fila in enumerate(le_df.iloc[:,1]):
    if type(fila)==str and fila[:7].strip() == 'Código':
        print(cuenta_fila, fila, le_df.iloc[cuenta_fila, 2], le_df.iloc[cuenta_fila-1, 2])
        lista.append(cuenta_fila)

lista = np.array(lista)

data0 = []
for x,fila in enumerate(lista):
    if x>=0:
        if x == len(lista)-1:
            bb = pd.DataFrame((le_df.iloc[lista[x]-1:,:]).iloc[0:-3,0:-6])
            data0 = data0 + list([bb])
            print(bb.iloc[-1,-13], bb.iloc[0,2])
        else:
            bb = pd.DataFrame((le_df.iloc[lista[x]-1:lista[x+1],:]).iloc[0:-3,0:-6])
            data0 = data0 + list([bb])
            print(bb.iloc[-1,-13], bb.iloc[0,2], 'else')
            #print()


data = []


le_df = df['iv reg']
lista = []
for cuenta_fila, fila in enumerate(le_df.iloc[:,1]):
    if fila == 'Código BNA:':
        print(cuenta_fila, fila, le_df.iloc[cuenta_fila, 2], le_df.iloc[cuenta_fila-1, 2])
        lista.append(cuenta_fila)

lista = np.array(lista)

data1 = []
for x,fila in enumerate(lista):
    if x>=0:
        if x == len(lista)-1:
            bb = pd.DataFrame((le_df.iloc[lista[x]-1:,:]).iloc[0:-3,0:-6])
            data1 = data1 + list([bb])
            print(bb.iloc[-1,-13], bb.iloc[0,2])
        else:
            bb = pd.DataFrame((le_df.iloc[lista[x]-1:lista[x+1],:]).iloc[0:-3,0:-6])
            data1 = data1 + list([bb])
            print(bb.iloc[-1,-13], bb.iloc[0,2], 'else')
            #print()




le_df = df['v reg']
lista = []
for cuenta_fila, fila in enumerate(le_df.iloc[:,1]):
    if fila == 'Código BNA:':
        print(cuenta_fila, fila, le_df.iloc[cuenta_fila, 2], le_df.iloc[cuenta_fila-1, 2])
        lista.append(cuenta_fila)

lista = np.array(lista)
data2 = []

for x,fila in enumerate(lista):
    if x>=0:
        if x == len(lista)-1:
            bb = pd.DataFrame((le_df.iloc[lista[x]-1:,:]).iloc[0:-3,0:-6])
            data2 = data2 + list([bb])
            print(bb.iloc[-1,-13], bb.iloc[0,2])
        else:
            bb = pd.DataFrame((le_df.iloc[lista[x]-1:lista[x+1],:]).iloc[0:-3,0:-6])
            data2 = data2 + list([bb])
            print(bb.iloc[-1,-13], bb.iloc[0,2], 'else')
            #print()


le_df = df['rm']
lista = []
for cuenta_fila, fila in enumerate(le_df.iloc[:,1]):
    if type(fila)==str and fila[:7].strip() == 'Código':
        print(cuenta_fila, fila, le_df.iloc[cuenta_fila, 2], le_df.iloc[cuenta_fila-1, 2])
        lista.append(cuenta_fila)

lista = np.array(lista)

data3 = []
for x,fila in enumerate(lista):
    if x>=0:
        if x == len(lista)-1:
            bb = pd.DataFrame((le_df.iloc[lista[x]-1:,:]).iloc[0:-3,0:-6])
            data3 = data3 + list([bb])
            print(bb.iloc[-1,-13], bb.iloc[0,2])
        else:
            bb = pd.DataFrame((le_df.iloc[lista[x]-1:lista[x+1],:]).iloc[0:-3,0:-6])
            data3 = data3 + list([bb])
            print(bb.iloc[-1,-13], bb.iloc[0,2], 'else')
            #print()


le_df = df['ix reg']
lista = []
for cuenta_fila, fila in enumerate(le_df.iloc[:,1]):
    if type(fila)==str and fila[:7].strip() == 'Código':
        print(cuenta_fila, fila, le_df.iloc[cuenta_fila, 2], le_df.iloc[cuenta_fila-1, 2])
        lista.append(cuenta_fila)

lista = np.array(lista)

data4 = []
for x,fila in enumerate(lista):
    if x>=0:
        if x == len(lista)-1:
            bb = pd.DataFrame((le_df.iloc[lista[x]-1:,:]).iloc[0:-3,0:-6])
            data4 = data4 + list([bb])
            print(bb.iloc[-1,-13], bb.iloc[0,2])
        else:
            bb = pd.DataFrame((le_df.iloc[lista[x]-1:lista[x+1],:]).iloc[0:-3,0:-6])
            data4 = data4 + list([bb])
            print(bb.iloc[-1,-13], bb.iloc[0,2], 'else')
            #print()


le_df = df['xii reg']
lista = []
for cuenta_fila, fila in enumerate(le_df.iloc[:,1]):
    if type(fila)==str and fila[:7].strip() == 'Código':
        print(cuenta_fila, fila, le_df.iloc[cuenta_fila, 2], le_df.iloc[cuenta_fila-1, 2])
        lista.append(cuenta_fila)

lista = np.array(lista)

data5 = []
for x,fila in enumerate(lista):
    if x>=0:
        if x == len(lista)-1:
            bb = pd.DataFrame((le_df.iloc[lista[x]-1:,:]).iloc[0:-3,0:-6])
            data5 = data5 + list([bb])
            print(bb.iloc[-1,-13], bb.iloc[0,2])
        else:
            bb = pd.DataFrame((le_df.iloc[lista[x]-1:lista[x+1],:]).iloc[0:-3,0:-6])
            data5 = data5 + list([bb])
            print(bb.iloc[-1,-13], bb.iloc[0,2], 'else')
            #print()


dataALL = data0+data1+data2+data3+data4+data5

print(len(dataALL))

estaciones = pd.DataFrame([ [str(df.iloc[0,2]).strip(), df.iloc[1,2], (df.iloc[5,0]), (df.iloc[-1,0])] for df in dataALL])

estaciones.min()
estaciones.max()

data_variable = pd.DataFrame(index=pd.date_range('1900/01','2011/01',freq='M',closed='left'))
                             #, columns=estaciones.iloc[:,0])


data = None
for cuenta, hoja in enumerate(dataALL[:]):
    est = pd.DataFrame(hoja).iloc[0,2]
    if type(est)==np.float: est = pd.DataFrame(hoja).iloc[0,3]
    print(cuenta, est)
    hoja = pd.DataFrame(hoja).iloc[6:,:13]
    if hoja.iloc[-1,-1]=='Media serie': hoja.iloc[-1,-1] = np.nan
    hoja = hoja.dropna(how='all')
    hoja.columns = ['AÑO', 'ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC']
    #print(hoja)
    ini, fin = str(np.int(hoja.iloc[0,0])), str(np.int(hoja.iloc[-1,0]+1))

    periodo = pd.date_range(ini, fin, freq='M')
    rango_completo = np.unique(periodo.year) # np.array(range(np.int(ini), np.int(fin)))
    rango_reporte = hoja.iloc[0:, 0].to_numpy()
    if len(rango_completo) != len(rango_reporte):
            rango = rango_completo[[not(jar in rango_reporte) for jar in rango_completo]]
            for jar in rango:
                niu_fila = {'AÑO':jar, 'ENE':np.float('nan'), 'FEB':np.float('nan'),
                            'MAR':np.float('nan'),'ABR':np.float('nan'),
                            'MAY':np.float('nan'),'JUN':np.float('nan'),
                            'JUL':np.float('nan'),'AGO':np.float('nan'),
                            'SEP':np.float('nan'),'OCT':np.float('nan'),
                            'NOV':np.float('nan'),'DIC':np.float('nan')}
                hoja = hoja.append(niu_fila, ignore_index=True)
                hoja = hoja.sort_values(by=['AÑO'], ignore_index=True)
    #
    data = pd.DataFrame(hoja.iloc[:,1:].values.reshape(len(periodo),1), index=periodo, columns=[str(est)])
    data_variable.loc[periodo, est] = data.loc[:,est]
    #         # data_variable.loc[periodo, hoja] = data.loc[:,hoja]
    # data = pd.DataFrame(libro[hoja].iloc[:,1:].values.reshape(len(periodo),1), index=periodo, columns=[str(hoja)])
    hoja, data, est = None, None, None

#del data, rango_completo, rango_reporte, rango, periodo, ini, fin, jar, niu_fila, hoja, libro

# jars = [str(df.iloc[-1,0]).strip() for df in data]

#data_variable['CodigoEstacion'] = estaciones.iloc[:,1]

data_variable.to_excel('D:/Desktop/datos_erosion2010_if_v_rm_ix.xlsx')
estaciones.to_excel('D:/Desktop/datos_erosion2010_meta_if_v_rm_ix.xlsx')
#aa = (le_df.iloc[lista[x]-1:,:])

#%%  SEXTA

# xls_archivos = glob('*.xls')
# ['estaciones con el IF.xls',
#  'IX_REGION_A.xls',
#  'VIII-REGIO-B.xls',
#  'VIII_REGIÓN_A.xls',
#  'VII_REGIÓN_A.xls',
#  'VII_REGIÓN_B.xls',
#  'VI_REGION_B.xls',
#  'VI_REGIÓN_A.xls',
#  'V_REGION_A.xls']

import pandas as pd, numpy as np
from os import chdir as chdir

chdir('E:/ESTACIONES_CORRECCION/datospp')

df = pd.read_excel('VI_REGION_B.xls', sheet_name='Hoja1')

lista = []
cuenta = 0
for cuenta_fila, fila in enumerate(df.iloc[:,1]):
    if type(fila) == str:
        #print(fila,fila[:7])
        if fila[:7].strip()=='Código':
            cuenta = cuenta+1
            print(cuenta, cuenta_fila, fila, df.iloc[cuenta_fila, 2], df.iloc[cuenta_fila-1, 2])
            lista.append(cuenta_fila)

lista = np.array(lista)

data0 = []
for x,fila in enumerate(lista[:]):
    if x>=0:
        if x == len(lista)-1:
            bb = pd.DataFrame((df.iloc[lista[x]-1:,:]).iloc[0:-2,0:-6])
            data0 = data0 + list([bb])
            print(bb.iloc[-1,-13], bb.iloc[0,2])
        else:
            bb = pd.DataFrame((df.iloc[lista[x]-1:lista[x+1],:]).iloc[0:-2,0:-6])
            data0 = data0 + list([bb])
            print(bb.iloc[-1,-13], bb.iloc[0,2], 'else')




estaciones = pd.DataFrame([ [str(df.iloc[0,2]).strip(), df.iloc[1,2], (df.iloc[8,0]), (df.iloc[-1,0])] for df in data0])
print(estaciones)

estaciones.min()
estaciones.max()

data_variable = pd.DataFrame(index=pd.date_range('1900/01','2011/01',freq='M',closed='left'))
                             #, columns=estaciones.iloc[:,0])


data = None
for cuenta, hoja in enumerate(data0[:]):
    est = pd.DataFrame(hoja).iloc[0,2]
    if type(est)==np.float: est = pd.DataFrame(hoja).iloc[0,3]
    print(cuenta, est)
    hoja = pd.DataFrame(hoja).iloc[7:,:13]
    if hoja.iloc[-1,-1]=='Media serie': hoja.iloc[-1,-1] = np.nan
    hoja = hoja.dropna(how='all')
    hoja.columns = ['AÑO', 'ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC']
    #print(hoja)
    ini, fin = str(np.int(hoja.iloc[0,0])), str(np.int(hoja.iloc[-1,0]+1))

    periodo = pd.date_range(ini, fin, freq='M')
    rango_completo = np.unique(periodo.year) # np.array(range(np.int(ini), np.int(fin)))
    rango_reporte = hoja.iloc[0:, 0].to_numpy()
    if len(rango_completo) != len(rango_reporte):
            rango = rango_completo[[not(jar in rango_reporte) for jar in rango_completo]]
            for jar in rango:
                niu_fila = {'AÑO':jar, 'ENE':np.float('nan'), 'FEB':np.float('nan'),
                            'MAR':np.float('nan'),'ABR':np.float('nan'),
                            'MAY':np.float('nan'),'JUN':np.float('nan'),
                            'JUL':np.float('nan'),'AGO':np.float('nan'),
                            'SEP':np.float('nan'),'OCT':np.float('nan'),
                            'NOV':np.float('nan'),'DIC':np.float('nan')}
                hoja = hoja.append(niu_fila, ignore_index=True)
                hoja = hoja.sort_values(by=['AÑO'], ignore_index=True)
    #
    data = pd.DataFrame(hoja.iloc[:,1:].values.reshape(len(periodo),1), index=periodo, columns=[str(est)])
    data_variable.loc[periodo, est] = data.loc[:,est]
    #         # data_variable.loc[periodo, hoja] = data.loc[:,hoja]
    # data = pd.DataFrame(libro[hoja].iloc[:,1:].values.reshape(len(periodo),1), index=periodo, columns=[str(hoja)])
    hoja, data, est = None, None, None

#del data, rango_completo, rango_reporte, rango, periodo, ini, fin, jar, niu_fila, hoja, libro

# jars = [str(df.iloc[-1,0]).strip() for df in data]

#data_variable['CodigoEstacion'] = estaciones.iloc[:,1]

data_variable.to_excel('D:/Desktop/datos_erosion2010_sexta.xlsx')
estaciones.to_excel('D:/Desktop/datos_erosion2010_meta_sexta.xlsx')
#aa = (df.iloc[lista[x]-1:,:])

#%%  SEPTIMA

# xls_archivos = glob('*.xls')
# ['estaciones con el IF.xls',
#  'IX_REGION_A.xls',
#  'VIII-REGIO-B.xls',
#  'VIII_REGIÓN_A.xls',
#  'VII_REGIÓN_A.xls',
#  'VII_REGIÓN_B.xls',
#  'VI_REGION_B.xls',
#  'VI_REGIÓN_A.xls',
#  'V_REGION_A.xls']

import pandas as pd, numpy as np
from os import chdir as chdir

chdir('E:/ESTACIONES_CORRECCION/datospp')

df = pd.read_excel('VII_REGIÓN_B.xls', sheet_name='PP')

lista = []
cuenta = 0
for cuenta_fila, fila in enumerate(df.iloc[:,1]):
    if type(fila) == str:
        #print(fila,fila[:7])
        if fila[:7].strip()=='Código':
            cuenta = cuenta+1
            print(cuenta, cuenta_fila, fila, df.iloc[cuenta_fila, 2], df.iloc[cuenta_fila-1, 2])
            lista.append(cuenta_fila)

lista = np.array(lista)

data0 = []
for x,fila in enumerate(lista[:]):
    if x>=0:
        if x == len(lista)-1:
            bb = pd.DataFrame((df.iloc[lista[x]-1:,:]).iloc[0:-2,0:-6])
            data0 = data0 + list([bb])
            print(bb.iloc[-1,-13], bb.iloc[0,2])
        else:
            bb = pd.DataFrame((df.iloc[lista[x]-1:lista[x+1],:]).iloc[0:-2,0:-6])
            data0 = data0 + list([bb])
            print(bb.iloc[-1,-13], bb.iloc[0,2], 'else')




estaciones = pd.DataFrame([ [str(df.iloc[0,2]).strip(), df.iloc[1,2], (df.iloc[8,0]), (df.iloc[-2,0])] for df in data0])
print(estaciones)

estaciones.min()
estaciones.max()

data_variable = pd.DataFrame(index=pd.date_range('1900/01','2011/01',freq='M',closed='left'))
                             #, columns=estaciones.iloc[:,0])


data = None
for cuenta, hoja in enumerate(data0[:]):
    est = pd.DataFrame(hoja).iloc[0,2]
    if type(est)==np.float: est = pd.DataFrame(hoja).iloc[0,3]
    print(cuenta, est)
    hoja = pd.DataFrame(hoja).iloc[7:,:13]
    if hoja.iloc[-1,-1]=='Media serie': hoja.iloc[-1,-1] = np.nan
    hoja = hoja.dropna(how='all')
    hoja.columns = ['AÑO', 'ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC']
    #print(hoja)
    ini, fin = str(np.int(hoja.iloc[0,0])), str(np.int(hoja.iloc[-1,0]+1))

    periodo = pd.date_range(ini, fin, freq='M')
    rango_completo = np.unique(periodo.year) # np.array(range(np.int(ini), np.int(fin)))
    rango_reporte = hoja.iloc[0:, 0].to_numpy()
    if len(rango_completo) != len(rango_reporte):
            rango = rango_completo[[not(jar in rango_reporte) for jar in rango_completo]]
            for jar in rango:
                niu_fila = {'AÑO':jar, 'ENE':np.float('nan'), 'FEB':np.float('nan'),
                            'MAR':np.float('nan'),'ABR':np.float('nan'),
                            'MAY':np.float('nan'),'JUN':np.float('nan'),
                            'JUL':np.float('nan'),'AGO':np.float('nan'),
                            'SEP':np.float('nan'),'OCT':np.float('nan'),
                            'NOV':np.float('nan'),'DIC':np.float('nan')}
                hoja = hoja.append(niu_fila, ignore_index=True)
                hoja = hoja.sort_values(by=['AÑO'], ignore_index=True)
    #
    data = pd.DataFrame(hoja.iloc[:,1:].values.reshape(len(periodo),1), index=periodo, columns=[str(est)])
    data_variable.loc[periodo, est] = data.loc[:,est]
    #         # data_variable.loc[periodo, hoja] = data.loc[:,hoja]
    # data = pd.DataFrame(libro[hoja].iloc[:,1:].values.reshape(len(periodo),1), index=periodo, columns=[str(hoja)])
    hoja, data, est = None, None, None

#del data, rango_completo, rango_reporte, rango, periodo, ini, fin, jar, niu_fila, hoja, libro

# jars = [str(df.iloc[-1,0]).strip() for df in data]

#data_variable['CodigoEstacion'] = estaciones.iloc[:,1]

data_variable.to_excel('D:/Desktop/datos_erosion2010_septima.xlsx')
estaciones.to_excel('D:/Desktop/datos_erosion2010_meta_septima.xlsx')

#%%  OCTAVA

# xls_archivos = glob('*.xls')
# ['estaciones con el IF.xls',
#  'IX_REGION_A.xls',
#  'VIII-REGIO-B.xls',
#  'VIII_REGIÓN_A.xls',
#  'VII_REGIÓN_A.xls',
#  'VII_REGIÓN_B.xls',
#  'VI_REGION_B.xls',
#  'VI_REGIÓN_A.xls',
#  'V_REGION_A.xls']

import pandas as pd, numpy as np
from os import chdir as chdir

chdir('E:/ESTACIONES_CORRECCION/datospp')

df = pd.read_excel('VIII-REGIO-B.xls', sheet_name='PP')

lista = []
cuenta = 0
for cuenta_fila, fila in enumerate(df.iloc[:,1]):
    if type(fila) == str:
        #print(fila,fila[:7])
        if fila[:7].strip()=='Código':
            print(cuenta, cuenta_fila, fila, df.iloc[cuenta_fila, 2], df.iloc[cuenta_fila-1, 2])
            lista.append(cuenta_fila)
            cuenta = cuenta+1

lista = np.array(lista)

data0 = []
for x,fila in enumerate(lista[:]):
    if x>=0:
        if x == len(lista)-1:
            bb = pd.DataFrame((df.iloc[lista[x]-1:,:]).iloc[0:-2,0:-6])
            data0 = data0 + list([bb])
            print(bb.iloc[-1,-13], bb.iloc[0,2])
        else:
            bb = pd.DataFrame((df.iloc[lista[x]-1:lista[x+1],:]).iloc[0:-2,0:-6])
            data0 = data0 + list([bb])
            print(bb.iloc[-1,-13], bb.iloc[0,2], 'else')


estaciones = pd.DataFrame([ [str(df.iloc[0,2]).strip(), df.iloc[1,2], (df.iloc[8,0]), (df.iloc[-2,0])] for df in data0])
print(estaciones)

estaciones.min()
estaciones.max()

data_variable = pd.DataFrame(index=pd.date_range('1900/01','2011/01',freq='M',closed='left'))
                             #, columns=estaciones.iloc[:,0])


data = None
for cuenta, hoja in enumerate(data0[:]):
    est = pd.DataFrame(hoja).iloc[0,2]
    if type(est)==np.float: est = pd.DataFrame(hoja).iloc[0,3]
    print(cuenta, est)
    hoja = pd.DataFrame(hoja).iloc[7:,:13]
    if hoja.iloc[-1,-1]=='Media serie': hoja.iloc[-1,-1] = np.nan
    hoja = hoja.dropna(how='all')
    hoja.columns = ['AÑO', 'ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC']
    #print(hoja)
    ini, fin = str(np.int(hoja.iloc[0,0])), str(np.int(hoja.iloc[-1,0]+1))

    periodo = pd.date_range(ini, fin, freq='M')
    rango_completo = np.unique(periodo.year) # np.array(range(np.int(ini), np.int(fin)))
    rango_reporte = hoja.iloc[0:, 0].to_numpy()
    if len(rango_completo) != len(rango_reporte):
            rango = rango_completo[[not(jar in rango_reporte) for jar in rango_completo]]
            for jar in rango:
                niu_fila = {'AÑO':jar, 'ENE':np.float('nan'), 'FEB':np.float('nan'),
                            'MAR':np.float('nan'),'ABR':np.float('nan'),
                            'MAY':np.float('nan'),'JUN':np.float('nan'),
                            'JUL':np.float('nan'),'AGO':np.float('nan'),
                            'SEP':np.float('nan'),'OCT':np.float('nan'),
                            'NOV':np.float('nan'),'DIC':np.float('nan')}
                hoja = hoja.append(niu_fila, ignore_index=True)
                hoja = hoja.sort_values(by=['AÑO'], ignore_index=True)
    #
    data = pd.DataFrame(hoja.iloc[:,1:].values.reshape(len(periodo),1), index=periodo, columns=[str(est)])
    data_variable.loc[periodo, est] = data.loc[:,est]
    #         # data_variable.loc[periodo, hoja] = data.loc[:,hoja]
    # data = pd.DataFrame(libro[hoja].iloc[:,1:].values.reshape(len(periodo),1), index=periodo, columns=[str(hoja)])
    hoja, data, est = None, None, None

#del data, rango_completo, rango_reporte, rango, periodo, ini, fin, jar, niu_fila, hoja, libro

# jars = [str(df.iloc[-1,0]).strip() for df in data]

#data_variable['CodigoEstacion'] = estaciones.iloc[:,1]

data_variable.to_excel('D:/Desktop/datos_erosion2010_octava.xlsx')
estaciones.to_excel('D:/Desktop/datos_erosion2010_meta_octava.xlsx')
