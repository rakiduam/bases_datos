# -*- coding: utf-8 -*-
"""
Created on Fri May  8 11:14:05 2020

generar una serie de tablas de los datos de excel correspondientes a las
tablas de los datos de ciren, suelos agrologicos.

la idea es leer cada tabla, limpiar y generar una lista de las tablas,
posteriormente guardar en excel.

camelot es el que presenta mejores resultados
- https://www.youtube.com/watch?v=99A9Fz6uHAA
- https://camelot-py.readthedocs.io/en/master/
- https://www.youtube.com/watch?v=iYie42M1ZyU
@author: fneir
"""
# importacion de modulos a usar
# import tabula
import camelot, os, pandas as pd

# directorio trabajo
os.chdir('D:/series/')

# estudio = 'ESTUDIO_VI_2010'
estudio = 'ESTUDIO_VII_2012'

# listado series suelos, tabla de datos llenada a mano
lista_series = pd.read_excel(estudio + '.xlsx')

# count = 0
# # paginas = '29, 33, 37, 41, 46, 51, 55, 59, 63, 67, 71, 76, 82, 88, 93, 97, 101, 105, 110, 112, 120, 125, 125, 134, 139, 143, 149, 153, 158, 162, 167, 171, 175, 179, 183, 188, 195, 199, 203, 207, 210, 215, 221, 225, 229, 234, 239, 243, 249, 253, 257, 262, 268, 274, 279, 285, 290, 296, 302, 308, 314, 319, 324, 329, 333, 338, 343, 347, 353, 357, 361, 365, 369, 374, 380, 386, 392, 396, 402, 407, 411, 415, 420, 425, 429, 434, 440, 445, 449, 452, 460, 465, 470, 474, 480, 485, 490, 496, 501, 506, 512, 518, 524, 530, 536, 541, 545, 549, 554, 559, 564, 569, 573, 578, 583, 587, 592, 597'
# # pdf = camelot.read_pdf('ESTUDIO_VII_2012.pdf', pages=paginas)
# nombre_salida = ('_').join([str(lista_series.iloc[count,0]).zfill(3), str(lista_series.iloc[count,2])])
colnames = ['PROFUNDIDAD cm', 'MATERIA ORGÁNICA %', 'CARBONO ORGÁNICO %']
for i in (lista_series.N.iloc[:]):
    count = i-1
    #print(count, i)
    pdf = camelot.read_pdf(estudio + '/' + estudio + '-' + str(lista_series.PP_EN_PDF[count]) +'.pdf')
    suelos = (pdf[0].df.loc[pdf[0].df.iloc[:,0] == 'PROFUNDIDAD cm'])

    suelos = suelos.append(pdf[0].df.loc[pdf[0].df.iloc[:,0] == '< 2'])
    suelos = suelos.append(pdf[0].df.loc[pdf[0].df.iloc[:,0] == '2-1'])
    suelos = suelos.append(pdf[0].df.loc[pdf[0].df.iloc[:,0] == '1-0,5'])
    suelos = suelos.append(pdf[0].df.loc[pdf[0].df.iloc[:,0] == '0,5-0,25'])
    suelos = suelos.append(pdf[0].df.loc[pdf[0].df.iloc[:,0] == '0,25-0,10'])
    suelos = suelos.append(pdf[0].df.loc[pdf[0].df.iloc[:,0] == '0,10-0,05'])
    suelos = suelos.append(pdf[0].df.loc[pdf[0].df.iloc[:,0] == '0,05-0,002'])
    suelos = suelos.append(pdf[0].df.loc[pdf[0].df.iloc[:,0] == '< 0,002'])

    suelos = suelos.append(pdf[0].df.loc[pdf[0].df.iloc[:,0] == 'TEXTURA'])
    suelos = suelos.append(pdf[0].df.loc[pdf[0].df.iloc[:,0] == 'MATERIA ORGÁNICA %'])
    suelos = suelos.append(pdf[0].df.loc[pdf[0].df.iloc[:,0] == 'CARBONO ORGÁNICO %'])
    #suelos2 = suelos.where(suelos!='').dropna(axis=1, how='all')
    suelos = suelos.T
    suelos = suelos.rename(columns=(suelos.iloc[0,:]))
    suelos = suelos.iloc[1:,:]
    suelos.insert(loc=0, column='N', value=lista_series.N[count])
    suelos.insert(loc=1, column='N_ASOC_SUELOS', value=lista_series.N_ASOC_SUELOS[count])
    suelos.insert(loc=2, column='PP_EN_PDF', value=lista_series.PP_EN_PDF[count])
    suelos.insert(loc=3, column='SERIE', value=lista_series.SERIE_SUELO[count])
    suelos.insert(loc=4, column='SIMBOLO', value=lista_series.ACRONIMO[count])


    # suelos = (suelos.where(suelos!='')).dropna()

    # union de dataframes
    if not 'series_suelos' in locals():
        series_suelos = suelos
    else:
        series_suelos = series_suelos.append(suelos)
    pdf, suelos = None, None
    print(count)

series_suelos.to_excel(estudio + '_series_suelos' + '.xlsx')
del series_suelos


#series_suelos = None
# nombre_salida = ('_').join([str(lista_series.iloc[count,0]).zfill(3), str(lista_series.iloc[count,2])])
# pdf.export(nombre_salida + '.csv', sep=';')
# pdf[0].to_csv(nombre_salida + '.csv', sep=';', encoding='utf-8')
# print(pdf[0].df)
# print(pdf[1].df)
# print(pdf[2].df)
# # tables = camelot.read_pdf('ESTUDIO_VII_2012/ESTUDIO_VII_2012-' + str(lista_series.iloc[count,-1])+'.pdf')
# # nombre_salida = ('_').join([str(lista_series.iloc[count,0]).zfill(3), str(lista_series.iloc[count,2])])
# # tables.export(nombre_salida + '.csv')
# # # tables[0]
# # # tables[0].parsing_report
# # tables[0].df
# # print(tables[0].df)
# # camelot.plot(tables[0], kind='grid')
# nomme = pd.DataFrame(pdf.columns)
# # for count, i in enumerate(series.N.iloc[:1]):
# #     pdf = tabula.read_pdf('ESTUDIO_VII_2012/ESTUDIO_VII_2012-' +
# #                                  str(series.PP_PDF.iloc[count])+'.pdf')
# #     print(count, i, str(series.PP_PDF.iloc[count]))
# df1 =  tabula.read_pdf('tes1.pdf', page = 'all')#, multiple_tables = True)
# df2 =  camelot.read_pdf('tes1.pdf', page = 'all')#, multiple_tables = True)
# df1.iloc[0,:]
# df =  camelot.read_pdf('tes1.pdf', page = 34)
# if not 'series_suelos' in locals(): print('si')
# else: print('ano')