# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 16:10:39 2020

@author: fanr

idea tomar puntos DGA estaciones,
estandarizar valor
cercano
regresion (kfold?)
guardar parametros

https://datasciencebeginners.com/2018/11/26/your-holistic-guide-to-building-linear-regression-model/
https://towardsdatascience.com/a-beginners-guide-to-linear-regression-in-python-with-scikit-learn-83a8f7ae2b4f


INFORMACION:
Heteroskedasticity, Non-Normality and Correlated Errors
Statisticians pay considerable attention to the distribution of the residuals. It turns
out that ordinary least squares (see “Least Squares”) are unbiased, and in some
cases the “optimal” estimator, under a wide range of distributional assumptions.
This means that in most problems, data scientists do not need to be too concerned
with the distribution of the residuals.


"""
#%clear

from scipy import spatial
from sklearn import metrics
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import os
import pandas as pd, numpy as np, geopandas as gpd

import seaborn as seabornInstance
import statsmodels.api as sm

#% funciones
def anomalia_estandarizada(vector):
    """  """
    vector = vector.astype(np.float)
    media = np.mean(vector)
    desviacion = np.std(vector)
    salida = (vector-media)/desviacion
    return(salida)


os.chdir('E:/Factor_R/')
jars = -372
# reordenar
#estaciones = pd.read_csv('cr2_prAmon_2019.txt', na_values=-9999, names=None, skiprows=np.arange(14,975), index_col=0)
# estaciones = pd.read_excel('BBDD/DGA_CR2_Erosion2010_1980-2019.xlsx', index=1, columns=None).T
estaciones = pd.read_excel('BBDD/LIMPIO_DGA_CR2_Erosion2010_1980-2019.xlsx', index=1, columns=None, na_values=-9999).T

estaciones = estaciones.reset_index()
# estaciones.columns = estaciones.iloc[0,:]
estaciones.columns = estaciones.iloc[1,:]
estaciones = estaciones.iloc[2:,:]
estaciones = estaciones.sort_values(by='lat', ascending=False)
estaciones = estaciones.iloc[:, np.arange(0,17).tolist()+np.arange(125,497).tolist()]
estaciones.iloc[:,-372:] = estaciones.iloc[:,-372:].apply(pd.to_numeric)
estaciones = estaciones.reset_index()
estaciones = estaciones.iloc[:,1:]

for row in np.arange(0, estaciones.shape[0]):
    estaciones.iloc[row, 16] = np.int(estaciones.iloc[row, jars:].count())

# CHIRPS
puntos_chirp = gpd.read_file('CAPAS/satelites_modelos/puntos_CHIRP.shp')
puntos_chirp.iloc[:,3:-1] = puntos_chirp.iloc[:,3:-1].apply(pd.to_numeric)
## ene1990-dic2019
#puntos_chirp = puntos_chirp.iloc[:,-365:-5]
## ene1981-dic2019
#puntos_chirp = puntos_chirp.iloc[:,np.arange(0,471)].apply(pd.to_numeric)

puntos_chirp.columns = (
    puntos_chirp.columns.to_list()[0:3] +
    (pd.date_range('1981/01','2020/01',freq='M',closed='left')).to_list() +
    ['geometry'])

puntos_chirp = puntos_chirp.iloc[:, np.arange(0,3).tolist()+np.arange(99,472).tolist()]

puntos_chirp = puntos_chirp.iloc[:,:-1]

# puntos_chirp.LAT = anomalia_estandarizada(puntos_chirp.LAT)
# puntos_chirp.LON = anomalia_estandarizada(puntos_chirp.LON)

# estaciones.lat = anomalia_estandarizada(estaciones.lat)
# estaciones.lon = anomalia_estandarizada(estaciones.lon)


#puntos_imerg =
# puntos_chirp.to_crs(epsg=32719)

#%% analisis de regresion y rellenado de chirps

k = 3
kdtree = spatial.KDTree(puntos_chirp.loc[:,['LAT', 'LON']])

#jars = -468#-372

# ndatos = estaciones.iloc[:, 16]

modelos_ols = {}
model = None
formato3='n:{:03.0f},\t {:40.40}, {:40.40}, \tR2: {:02.3f}, \t\tSSR: {:10.3f}'
for n, nombre_est in enumerate(estaciones.nombre):
    vecinos = kdtree.query(estaciones.loc[n, ['lat','lon']], p=2, k=k)
    index = vecinos[1][:]
    if estaciones.iloc[n, 16] == 372:
        print('n:{:03.0f},\t{:40.40},{}, \tdatos completos en periodo'.format(n, nombre_est, (puntos_chirp.ID.iloc[index[0]])))
    elif estaciones.iloc[n, 16] <= 119:
        print('n:{:03.0f},\t {:40.40},{}, \tsin datos'.format(n, nombre_est, (puntos_chirp.ID.iloc[index[0]])))
    else:
        # determinación de veciones cercanas
        #vecinos = kdtree.query(estaciones.loc[n, ['lat','lon']], p=2, k=k)
        #index = vecinos[1][:]
        # # estaciones de datos
        est  = anomalia_estandarizada((estaciones.iloc[n, jars:]).apply(pd.to_numeric))
        x_p1 = anomalia_estandarizada((puntos_chirp.iloc[index[0], jars:]).apply(pd.to_numeric))
        x_p2 = anomalia_estandarizada((puntos_chirp.iloc[index[1], jars:]).apply(pd.to_numeric))
        x_p3 = anomalia_estandarizada((puntos_chirp.iloc[index[2], jars:]).apply(pd.to_numeric))
        # est  = ((estaciones.iloc[n, jars:]).apply(pd.to_numeric))
        # x_p1 = ((puntos_chirp.iloc[index[0], jars:]).apply(pd.to_numeric))
        # x_p2 = ((puntos_chirp.iloc[index[1], jars:]).apply(pd.to_numeric))
        # x_p3 = ((puntos_chirp.iloc[index[2], jars:]).apply(pd.to_numeric))
        # data
        data = pd.DataFrame({'est': est,'X_P1': x_p1, 'X_P2': x_p2, 'X_P3': x_p3})
        # borrar nodata
        data = (data).dropna()
        if data.empty:
            print('n:{:03.0f},\t estacion: {:40.40}, \tsin datos'.format(n, nombre_est))
        else:
            #X = data[['X_P1','X_P2','X_P3']]
            X = data[['X_P1']]
            y = data['est']
            model = sm.OLS(y, X).fit()
            #model2= sm.OLS(y, X).fit().resid
            print(formato3.format(n, nombre_est, (puntos_chirp.ID.iloc[index[0]]), (model.rsquared), model.ssr))
    modelos_ols[nombre_est]= model
    data, est, x_p1, x_p2, x_p3, x, y, model = None, None, None, None, None, None, None, None


#%%
# del model, data, est, x_p1, x_p2, x_p3, x, y, n, nombre_est

## log de las regresiones estaciones.
f = open('BBDD/estaciones_vs_chirps.txt', 'w')
f.write('LISTADO ESTACIONES ANALISIS DE REGRESION OLS CON PIXELES DE CHIRPS CERCANOS'+
        '\n'+'DISTANCIA ESTIMADA MEDIANTES DISTANCIA EUCLIDIANA\n\n')
for n, nombre_est in enumerate(estaciones.nombre):#print(n,estaciones.loc[n, ['lat','lon']])
    vecinos = kdtree.query(estaciones.loc[n, ['lat','lon']], p=2, k=k)
    index = vecinos[1][:]
    #print(index)
    #print((puntos_chirp.ID.iloc[index[0:1]]).to_list())
    if modelos_ols[nombre_est]!=None and (modelos_ols[nombre_est].rsquared)>=0.7:
        f.write('col: {:03.0f} \t{} \tnombre: {} \t \npuntos: {}, en ese orden\n\n'.format((n),
                   str(estaciones.codigo_FUENTE[n]),
                   ', '.join([nombre_est,str(estaciones.lat[n]), str(estaciones.lon[n])]),
                       (puntos_chirp.ID.iloc[index[0:1]]).to_list()) + str((modelos_ols[nombre_est]).summary())+'\n'*5)
f.close()

for n, nombre_est in enumerate(estaciones.nombre):
    if modelos_ols[nombre_est]!=None and (modelos_ols[nombre_est].rsquared)>=0.7:
        est  = estaciones.iloc[n, jars:]
        vecinos = kdtree.query(estaciones.iloc[n, 11:13], p=2, k=k)
        index = vecinos[1][:]
        # valores de X
        # x_p1 = anomalia_estandarizada(puntos_chirp.iloc[index[0], jars:]).apply(pd.to_numeric)
        # x_p2 = anomalia_estandarizada(puntos_chirp.iloc[index[1], jars:]).apply(pd.to_numeric)
        # x_p3 = anomalia_estandarizada(puntos_chirp.iloc[index[2], jars:]).apply(pd.to_numeric)
        x_p1 = (puntos_chirp.iloc[index[0], jars:]).apply(pd.to_numeric)
        x_p2 = (puntos_chirp.iloc[index[1], jars:]).apply(pd.to_numeric)
        x_p3 = (puntos_chirp.iloc[index[2], jars:]).apply(pd.to_numeric)
        # calculo
        parametros = (modelos_ols[estaciones.nombre[n]]).params
        #relleno = (x_p1*parametros[0] + x_p2*parametros[1] + x_p3*parametros[2])
        relleno = (x_p1*parametros[0])
        ix = np.where(estaciones.iloc[n, jars:].isnull())
        #relleno[relleno < 0.0] = np.nan
        est_mean  = np.mean((estaciones.iloc[n, jars:]).apply(pd.to_numeric))
        est_std  = np.std((estaciones.iloc[n, jars:]).apply(pd.to_numeric))
        #if [relleno < 0.0]: print(nombre_est)
        #(estaciones.iloc[n, jars:]).iloc[ix] = ((relleno.iloc[ix])*est_std+est_mean)
        (estaciones.iloc[n, jars:]).iloc[ix] = (relleno.iloc[ix])
    relleno = None

# prstd, iv_l, iv_u = wls_prediction_std(res)
# fig, ax = plt.subplots(figsize=(8,6))
# ax.plot(x, y, 'o', label="data")
# ax.plot(x, y_true, 'b-', label="True")
# ax.plot(x, res.fittedvalues, 'r--.', label="OLS")
# ax.plot(x, iv_u, 'r--')
# ax.plot(x, iv_l, 'r--')
# ax.legend(loc='best');


for row in np.arange(0, estaciones.shape[0]):
    estaciones.iloc[row, 16] = np.int(estaciones.iloc[row, jars:].count())

#(estaciones.T).to_excel('BBDD/rellenado1pixel.xlsx')

estaciones_llenas = estaciones.loc[estaciones.iloc[:,16]==jars*-1, :]

#%% RELLENO DE ESTACIONES

k = 4
# kdtree_est = spatial.KDTree(estaciones_llenas.loc[:,['lat', 'lon']])
kdtree_est = spatial.KDTree(estaciones_llenas.loc[:,['utmN', 'utmE']])
#jars = -468

modest_ols = {}
model = None

for n, nombre_est in enumerate(estaciones.nombre):
    if estaciones.iloc[n, 16] == 372:
        print('n:{:03.0f},\t estacion: {:40.40}, \tdatos completos en periodo'.format(n, nombre_est))
    elif estaciones.iloc[n, 16] <= 119:
        print('n:{:03.0f},\t estacion: {:40.40}, \tsin datos'.format(n, nombre_est))
    else:
        # determinación de veciones cercanas
        #vecinos = kdtree_est.query(estaciones.loc[n, ['lat','lon']], p=2, k=k)
        vecinos = kdtree_est.query(estaciones.loc[n, ['utmN','utmE']], p=2, k=k)
        index = vecinos[1][:]
        # # estaciones de datos
        est  = ((estaciones.iloc[n, jars:]).apply(pd.to_numeric))
        x_p1 = ((estaciones_llenas.iloc[index[1], jars:]).apply(pd.to_numeric))
        x_p2 = ((estaciones_llenas.iloc[index[2], jars:]).apply(pd.to_numeric))
        x_p3 = ((estaciones_llenas.iloc[index[3], jars:]).apply(pd.to_numeric))
        # data
        data = pd.DataFrame({'est': est,'X_P1': x_p1, 'X_P2': x_p2, 'X_P3': x_p3})
        # borrar nodata
        data = (data).dropna()
        if data.empty:
            print('n:{:03.0f},\t estacion: {:40.40}, \tsin datos'.format(n, nombre_est))
        else:
            X = data[['X_P1','X_P2','X_P3']]
            #X = data[['X_P1']]
            y = data['est']
            model = sm.OLS(y, X).fit()
            print('n:{:03.0f},\t estacion: {:40.40}, \tR2: {:02.3f}, \t\terror: {:10.3f}\t{}'.format(n, nombre_est, (model.rsquared), model.ssr, (estaciones_llenas.nombre.iloc[index[1:2]]).to_list() ))
    modest_ols[nombre_est]= model
    data, est, x_p1, x_p2, x_p3, x, y, model = None, None, None, None, None, None, None, None


## log de las regresiones estaciones.
f = open('BBDD/estaciones_vs_estaciones_regresion.txt', 'w')
f.write('listado de analisis de regresion de estaciones meteorologicas'+
        '\n'+'respecto a estaciones cercanas, mediante distancia euclidiana\n\n')
for n, nombre_est in enumerate(estaciones.nombre):
    vecinos = kdtree_est.query(estaciones.loc[n, ['lat','lon']], p=2, k=k)
    index = vecinos[1][:]
    if modest_ols[nombre_est]!=None and (modest_ols[nombre_est].rsquared)>=0.7:
        f.write('fila: {:03.0f} \t{} \tnombre: {} \t \n rellenada con: {}, en ese orden\n'.format((n),
                str(estaciones.codigo_FUENTE[n]),
                nombre_est,
                (estaciones_llenas.nombre.iloc[index[1:2]]).to_list()) + str((modest_ols[nombre_est]).summary())+'\n'*5)
f.close()


for n, nombre_est in enumerate(estaciones.nombre):
    #if modelos_ols[nombre_est]!=None and modest_ols[nombre_est]!=None and (modelos_ols[nombre_est].rsquared)<0.7 and (modest_ols[nombre_est].rsquared)>=0.7:
    if modest_ols[nombre_est]!=None and (modest_ols[nombre_est].rsquared)>=0.7:
        print('n{:03.0f} \t {:50.50} \t R2: {}'.format(n, nombre_est, modest_ols[nombre_est].rsquared))
        #est  = estaciones.iloc[n, jars:]
        #vecinos = kdtree_est.query(estaciones.iloc[n, 11:13], p=2, k=k)
        vecinos = kdtree_est.query(estaciones.loc[n, ['utmN','utmN']], p=2, k=k)
        index = vecinos[1][:]
        # estaciones.iloc[index[1], jars:].count()
        # estaciones.iloc[index[2], jars:].count()
        # estaciones.iloc[index[3], jars:].count()
        # valores de X
        x_p1 = (estaciones_llenas.iloc[index[1], jars:]).apply(pd.to_numeric)
        x_p2 = (estaciones_llenas.iloc[index[2], jars:]).apply(pd.to_numeric)
        x_p3 = (estaciones_llenas.iloc[index[3], jars:]).apply(pd.to_numeric)
        # calculo
        parametros = (modest_ols[estaciones.nombre[n]]).params
        #relleno = (x_p1*parametros[0] + x_p2*parametros[1] + x_p3*parametros[2])
        relleno = (x_p1*parametros[0])
        ix = np.where(estaciones.iloc[n, jars:].isnull())
        (estaciones.iloc[n, jars:]).iloc[ix] = (relleno.iloc[ix])
    relleno = None


##  (estaciones.T).to_excel('BBDD/rellenado1estacionespatron.xlsx')

#%%
est  = estaciones.iloc[n, jars:]
vecinos = kdtree.query(estaciones.iloc[n, 11:13], p=2, k=k)
index = vecinos[1][:]

# valores de X
x_p1 = (puntos_chirp.iloc[index[0], jars:]).apply(pd.to_numeric)
x_p2 = (puntos_chirp.iloc[index[1], jars:]).apply(pd.to_numeric)
x_p3 = (puntos_chirp.iloc[index[2], jars:]).apply(pd.to_numeric)
# calculo
parametros = (modelos_ols[estaciones.nombre[n]]).params
relleno = (x_p1*parametros[0] + x_p2*parametros[1] + x_p3*parametros[2])
ix = np.where(estaciones.iloc[n, jars:].isnull())
(estaciones.iloc[n, jars:]).iloc[ix] = relleno.iloc[ix]

#(estaciones.T).to_excel('BBDD/ALLrellenado1pixel.xlsx')

#%#%
# # para consultar modelos especificos, hay que saber el N y la estacion.
# (modelos_ols['ARMERILLO']).summary()
# parametros = (modelos_ols['ARMERILLO']).params

# estaciones.iloc[, -360:]
# estaciones.nombre.iloc[48]
# vecinos = kdtree.query(estaciones.iloc[48, 11:13], p=2, k=k)
# index = vecinos[1][:]
# puntos_chirp.loc[index,['LAT', 'LON']]
# x_p1 = (puntos_chirp.iloc[index[0], -360:]).apply(pd.to_numeric)
# x_p2 = (puntos_chirp.iloc[index[1], -360:]).apply(pd.to_numeric)
# x_p3 = (puntos_chirp.iloc[index[2], -360:]).apply(pd.to_numeric)

# plt.plot(estaciones.columns[-360:], estaciones.iloc[48, -360:], label='original')
# plt.xlabel('precipitacion (mm)')
# plt.ylabel('fecha')
# plt.plot(estaciones.columns[-360:], (x_p1*parametros[0] + x_p2*parametros[1] + x_p3*parametros[2]-12), alpha=0.8, label='simulado')
# plt.legend()
# plt.show()

# (modelos_ols[334]['TALCA']).summary()

#     plt.plot(data.est, predictions, 'bo')

# %#% asfg
# k = 3
# kdtree = spatial.KDTree(puntos_chirp.loc[:,['LAT', 'LON']])

# modelos_ols = []
# prediccion_ols = []
# #rsquared = []
# for n, nombre_est in enumerate(estaciones.nombre):
#     # n = 300
#     # determinación de veciones cercanas
#     vecinos = kdtree.query(estaciones.iloc[n, 11:13], p=2, k=k)
#     index = vecinos[1][:]
#     # # estaciones de datos
#     # est  = anomalia_estandarizada((estaciones.iloc[n, -360:]).apply(pd.to_numeric))
#     # x_p1 = anomalia_estandarizada((puntos_chirp.iloc[index[0], -360:]).apply(pd.to_numeric))
#     # x_p2 = anomalia_estandarizada((puntos_chirp.iloc[index[1], -360:]).apply(pd.to_numeric))
#     # x_p3 = anomalia_estandarizada((puntos_chirp.iloc[index[2], -360:]).apply(pd.to_numeric))
#     est  = (estaciones.iloc[n, -360:]).apply(pd.to_numeric)
#     x_p1 = (puntos_chirp.iloc[index[0], -360:]).apply(pd.to_numeric)
#     x_p2 = (puntos_chirp.iloc[index[1], -360:]).apply(pd.to_numeric)
#     x_p3 = (puntos_chirp.iloc[index[2], -360:]).apply(pd.to_numeric)
#     # data
#     data = pd.DataFrame({'est': est,'X_P1': x_p1, 'X_P2': x_p2, 'X_P3': x_p3})
#     # borrar nodata
#     data = (data).dropna()
#     if data.empty:
#         print('n:{:03.0f},\t estacion: {:30.30}, \tsin datos'.format(n, nombre_est))
#     else:
#         X = data[['X_P1','X_P2','X_P3']]
#         # X = data[['X_P1']]
#         y = data['est']
#         model = sm.OLS(y, X).fit()
#         prediccion_ols.extend([{nombre_est: model.predict(X)}])
#         print('n:{:03.0f},\t estacion: {:30.30}, \t\tR2: {:02.3f}, \t\terror: {:10.3f}'.format(n, nombre_est, (model.rsquared), model.ssr))
#     modelos_ols.extend([{nombre_est: model}])
#     modelrecursiveLS =None
#     est, x_p1, x_p2, x_p3, data, x, y, model = None, None, None, None, None, None, None, None

# data = pd.DataFrame({
#     'estacion': (estaciones.iloc[n, -468:]).apply(pd.to_numeric),
#     'X_P1': (puntos_chirp.iloc[index[0], -468:].to_numpy()),
#     'X_P2': (puntos_chirp.iloc[index[1], -468:].to_numpy()),
#     'X_P3': (puntos_chirp.iloc[index[2], -468:].to_numpy())
#     })



## %% reemplazo de no data, por valores generados

# #%% generar anomalias?. grupos.
# estaciones=estaciones.iloc[-480:,-10:].dropna()
# pd.to_numeric(estaciones.iloc[-480:, -3]).plot()
# a = ((estaciones.iloc[-480:, -3]).apply(pd.to_numeric)).to_numpy().reshape(-1,1)
# b = ((estaciones.iloc[-480:, -4]).apply(pd.to_numeric)).to_numpy().reshape(-1,1)

# seabornInstance.distplot((estaciones.iloc[-480:, -104]).apply(pd.to_numeric))

# seabornInstance.distplot(anomalia_estandarizada(estaciones.iloc[-480:, -104]).apply(pd.to_numeric))

# preprocessing.scale(a)
# #anomalia
# """n = (a-np.nanmean(a))/np.nanstd(a)
# (n*np.nanstd(a)+np.nanmean(a))-a"""
# ##




# #%% regresion

# X_train, X_test, y_train, y_test = train_test_split(a, b, test_size=0.2, random_state=0)

# regressor = LinearRegression()
# regressor.fit(X_train, y_train) #training the algorithm
# print(regressor.intercept_)
# print(regressor.coef_)

# y_pred = regressor.predict(X_test)
# pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': y_pred.flatten()})

# plt.scatter(X_test, y_test,  color='gray')
# plt.plot(X_test, y_pred, color='red', linewidth=2)
# plt.show()
# #%%


# # IMERG
# puntos_imerg = gpd.read_file('BBDD/puntos_IMERG.shp')
# puntos_imerg = puntos_imerg.iloc[:,:-1]
# puntos_imerg.columns = puntos_imerg.columns.to_list()[0:3] + pd.date_range('2015/01','2020/01',freq='M',closed='left').to_list()
# puntos_imerg = puntos_imerg.apply(pd.to_numeric)

# # CR2
# puntos_nccr2 = pd.read_csv('BBDD/CR2MET_pr_v2.0_mon/ncdf_todo.csv')

# puntos_nccr2.columns = ['ID_TXT','LON','LAT'] + pd.date_range('1979/01','2019/01',freq='M',closed='left').to_list()

# puntos_nccr2 = puntos_nccr2.loc[(puntos_nccr2.LAT >= -40.075) & (puntos_nccr2.LAT <= -31.725) &
#                           (puntos_nccr2.LON >= -75.125) & (puntos_nccr2.LON <= -68.675)]
# -68.675 -75.125
# puntos_nccr2 = gpd.read_file('BBDD/puntos_CR2v2.shp')
# puntos_nccr2.columns = pd.date_range('1980/01','2019/01',freq='M',closed='left')
# old_cols = puntos_nccr2.columns.to_list()
# puntos_nccr2['LAT'], puntos_nccr2['LON'], puntos_nccr2['ID_TXT'] = puntos_imerg.iloc[:,0], puntos_imerg.iloc[:,1], puntos_imerg.iloc[:,2]
# puntos_nccr2 = puntos_nccr2.reindex(columns = ['LAT', 'LON', 'ID_TXT']+old_cols)
# del old_cols
# puntos_nccr2.iloc[:,3:-1] = puntos_nccr2.iloc[:,3:-1].apply(pd.to_numeric)
## ene1990-dic2019
#
## ene1981 - dic2019
#puntos_nccr2.iloc[:,-457:-1]

# puntos_nccr2.insert(loc=[0,1,2], column=list(puntos_imerg.iloc[:,:3].columns), value=puntos_imerg.iloc[:,:3])

# [str(i).replace('POINT (','').replace(')','').split(' ')  for i in (puntos_nccr2['geometry'])]
# aa = puntos_nccr2['geometry'] == puntos_imerg['geometry']

# puntos_chirp.columns
# puntos_nccr2.columns
#%% CURICO
# (estaciones.iloc[63, -480:]).plot()

# puntos_imerg.iloc[5401,-61:-1].plot()
# puntos_chirp.iloc[5401,-467:-1].plot()
# puntos_nccr2.iloc[5401,-467:-1].plot()

# curico = pd.DataFrame({'DGA':(estaciones.iloc[63, -60:]).values, 'IMERG': (puntos_imerg.iloc[5401,-61:-1].values),
#  'CHIRP':puntos_chirp.iloc[5401,-61:-1].values, 'CR2':puntos_nccr2.iloc[5401,-62:-2].values})

# curico.plot()

#%% evaluar cercanos generar KDTree

# # paso 1: generar tree
# kdtree = spatial.KDTree(puntos_chirp.loc[:,['LAT', 'LON']])

# kdtree_cr2 = spatial.KDTree(puntos_nccr2.loc[:,['LAT', 'LON']])

# # vecinos a considerar
# k = 3

# n = 100 # 63 curico

# vecinos = kdtree.query(estaciones.iloc[n, 11:13], p=2, k=k)
# index = vecinos[1][:]

# #############################################################################
# # puntos_chirp.iloc[index[0],:], vecinos[0]

# curico = pd.DataFrame({
#     'estacion': anomalia_estandarizada((estaciones.iloc[n, -360:]).apply(pd.to_numeric)),
#     'CHIRP_P1': (puntos_chirp.iloc[index[0], -360:].values - np.mean(puntos_chirp.iloc[index[0], -468:].values))/np.std(puntos_chirp.iloc[index[0], -468:].values),
#     'CHIRP_P2': (puntos_chirp.iloc[index[1], -360:].values - np.mean(puntos_chirp.iloc[index[1], -468:].values))/np.std(puntos_chirp.iloc[index[1], -468:].values),
#     'CHIRP_P3': (puntos_chirp.iloc[index[2], -360:].values- np.mean(puntos_chirp.iloc[index[2], -468:].values))/np.std(puntos_chirp.iloc[index[2], -468:].values)
#     }).apply(pd.to_numeric)

# curico.plot()


# curico = pd.DataFrame({
#     'estacion': (estaciones.iloc[n, -60:].values),
#     'CHIRP_P1': (puntos_chirp.iloc[index[0], -60:].values),
#     'CHIRP_P2': (puntos_chirp.iloc[index[1], -60:].values),
#     'CHIRP_P3': (puntos_chirp.iloc[index[2], -60:].values)
#     }).apply(pd.to_numeric)

# curico.plot()


# curico = pd.DataFrame({
#     'estacion': (estaciones.iloc[n, -60:].values),
#     'CHIRP_P1': (puntos_imerg.iloc[index[0], -60:].values),
#     'CHIRP_P2': (puntos_imerg.iloc[index[1], -60:].values),
#     'CHIRP_P3': (puntos_imerg.iloc[index[2], -60:].values)
#     }).apply(pd.to_numeric)

# curico.plot()



# vecinos_cr2 = kdtree.query(estaciones.iloc[63, 11:13], p=2, k=k)
# index_cr2 = vecinos_cr2[1][:]

# curico_cr2 = pd.DataFrame({
#     'estacion': estaciones.iloc[63, -468:].values,
#     'CR2_P1': puntos_nccr2.iloc[index[0], -468:].values,
#     'CR2_P2': puntos_nccr2.iloc[index[1], -468:].values,
#     'CR2_P3': puntos_nccr2.iloc[index[2], -468:].values
#     }).apply(pd.to_numeric)

# puntos_nccr2.iloc[index[2], -468:].values
# anomalia_estandarizada(puntos_nccr2.iloc[index[2], -468:].values)
# curico_cr2.plot()