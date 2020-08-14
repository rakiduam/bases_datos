# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 16:10:39 2019

@author: fanr

IDEA:
    - ordenar informacion desde una base tipo CR2, puede variar la cantidad de
    filas, pero que mantenga: CODIGO, NOMBRE, LAT, LON. al menos.
    - idea tomar puntos DGA estaciones,
    - estandarizar valor cercano
    - regresion (kfold?)
    - guardar parametros

FUENTES:
- https://www.statsmodels.org/stable/regression.html
- https://scikit-learn.org/stable/index.html

- https://datasciencebeginners.com/2018/11/26/your-holistic-guide-to-building-linear-regression-model/
- https://towardsdatascience.com/a-beginners-guide-to-linear-regression-in-python-with-scikit-learn-83a8f7ae2b4f
- https://www.listendata.com/2018/03/regression-analysis.html#Terminologies-related-to-regression-analysis
- https://www.youtube.com/watch?v=_OJRjwv1mxo
- https://www.dataquest.io/blog/k-nearest-neighbors-in-python/
- https://medium.com/@rrfd/standardize-or-normalize-examples-in-python-e3f174b65dfc
- https://medium.com/@xzz201920/stratifiedkfold-v-s-kfold-v-s-stratifiedshufflesplit-ffcae5bfdf

COSAS A TOMAR EN CUENTA PARA VERSIONES FUTURAS:
Heteroskedasticity, Non-Normality and Correlated Errors
Statisticians pay considerable attention to the distribution of the residuals. It turns
out that ordinary least squares (see “Least Squares”) are unbiased, and in some
cases the “optimal” estimator, under a wide range of distributional assumptions.
This means that in most problems, data scientists do not need to be too concerned
with the distribution of the residuals.


"""
from scipy import spatial
# import matplotlib.pyplot as plt
import os, pandas as pd, numpy as np, statsmodels.api as sm

# from sklearn.model_selection import KFold

# x = [1,2,3,4,5,6,7,8,9,10,11,12]
# X = ["a", "b", "c", "d"]
# kf = KFold(n_splits=2)
# for train, test in kf.split(X):
#     print("%s %s" % (train, test))


#% funciones
def estandarizar(vector):
    """  """
    #vector = vector.to_numpy()
    salida = (vector-vector.mean())/vector.std()
    # media = vector.mean()
    # desviacion = vector.std()
    # salida = (vector-media)/desviacion
    return(salida)

dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')

# DIRECTORIO ####
os.chdir('E:/FIA_MAGALLANES/cr2_prAmon_2019/')
#os.chdir('D:/')

# ESTACIONES ####
#estaciones = pd.read_csv(filepath_or_buffer='DGA-DMC_1980-2020.csv',
estaciones = pd.read_csv(filepath_or_buffer='cr2_prAmon_2019.txt',
                        sep=',',
                        #sep=';',
                        header=None,
                        #dtype='unicode',
                        #na_values=-9999,
                        encoding='utf-8',
                        #memory_map=True,
                        ).T

#estaciones = pd.read_excel('DGA-DMC_1980-2020.xlsx')


print(estaciones.head())

print(estaciones.shape)

estaciones.columns = estaciones.iloc[0,:]
estaciones = estaciones.iloc[1:,]

# print(estaciones.columns.to_list())


# las primeras 15 columnas son puro relleno
estaciones.columns = estaciones.iloc[:, :15].columns.tolist() + pd.date_range('1980/01','2020/01',freq='M',closed='left').tolist()
estaciones.iloc[:, 15:] = estaciones.iloc[:, 15:].apply(pd.to_numeric)

rango = np.arange(4, 7).tolist() + np.arange(15, len(estaciones.columns)).tolist()

estaciones.iloc[:, rango] = estaciones.iloc[:, rango].apply(pd.to_numeric)
del rango


estaciones.columns


estaciones.latitud = estaciones.latitud.apply(pd.to_numeric)
estaciones.longitud = estaciones.longitud.apply(pd.to_numeric)
estaciones.altura = estaciones.altura.apply(pd.to_numeric)
#estaciones.utmE = estaciones.utmE.apply(pd.to_numeric)
#estaciones.utmN = estaciones.utmN.apply(pd.to_numeric)

#% FILTRAR ESTACIONES por ubicación.
# estandarización de los valores para estimar distancia entre estaciones.
# hasta donde entiendo, lo que hace es basicamente formar cluster de informacion
# con caracteristicas similares, en atributos como lat, lon y alt.
estaciones.insert(15,'norm_lat', estandarizar(estaciones.latitud))
estaciones.insert(16,'norm_lon', estandarizar(estaciones.longitud))
estaciones.insert(17,'norm_alt', estandarizar(estaciones.altura))

#% FILTROS UBICACION / AÑOS
# filtro obtener solo los ultimos 30 años de datos de la serie.
jars = (31 * 12 ) * -1
estaciones = estaciones.iloc[:, np.arange(0,18).tolist()+np.arange(jars,0).tolist()]

# filtro dentro de determinada ubicación
estaciones = estaciones.loc[(estaciones.latitud  <= -47.0) &
                            (estaciones.latitud  >= -58.0) &
                            (estaciones.longitud >= -74.0) &
                            (estaciones.longitud <= -68.0)]


# filtro de datos menos a 0 dentro de CR2
#estaciones.loc[estaciones.iloc[:,18:]<0] = np.nan
df = np.array(estaciones.iloc[:, 18:], dtype=np.float)
df[np.where(df<0)] = np.nan
estaciones.iloc[:, 18:] = df

# establecer la cantidad datos disponibles en el periodo
estaciones.insert(18,'contador', estaciones.iloc[:, jars:].T.apply(pd.to_numeric).count())

estaciones.iloc[:, jars:] = estaciones.iloc[:, jars:].apply(pd.to_numeric)


contar = estaciones.T.iloc[19:,:].groupby([index.year for index in estaciones.T.index[19:]]).count()

contar = estaciones.T.iloc[:19,:].append(contar)

#%
est10menos = estaciones[(estaciones.contador < 120) & (estaciones.contador >= 12)]
# eliminar estaciones con una cantidad de datos menor a 10 años.
estaciones = estaciones[estaciones.contador >= 120]

# limpiar indices y reordenar dataframe
estaciones = estaciones.reset_index()
estaciones = estaciones.iloc[:, 1:]
estaciones.iloc[:, jars:] = estaciones.iloc[:, jars:].apply(pd.to_numeric)


estaciones_llenas = estaciones.loc[estaciones.contador >= (jars * -1), :]
estaciones_llenas = estaciones_llenas.reset_index()
estaciones_llenas = estaciones_llenas.iloc[:, 1:]


#% MODELOS DE RELLENO
k = 4
kdtree_est = spatial.KDTree(estaciones_llenas.loc[:,['norm_lat', 'norm_lon', 'norm_alt']])

modest_ols = {}
model = None

formato1 = 'n:{:03.0f}, estacion: {:40.40}, \tDATOS COMPLETOS PARA PERIODO'
formato2 = 'n:{:03.0f}, estacion: {:40.40}, \tSIN DATOS'
formato4 = 'n:{:03.0f}, estacion: {:40.40}, \tR2: {:02.3f}, \tSSR: {:10.3f}\t{},\t{:02.3f}'

for n, nombre_est in enumerate(estaciones.nombre):
    if estaciones.contador.iloc[n] == (jars*-1):
        print(formato1.format(n, nombre_est))
    elif estaciones.contador.iloc[n] <= 119:
        print(formato2.format(n, nombre_est))
    else:
        # determinación de veciones cercanas
        vecinos = kdtree_est.query(estaciones[['norm_lat', 'norm_lon', 'norm_alt']].iloc[n], p=2, k=k)
        index = vecinos[1][:]
        # # estaciones de datos
        est  = ((estaciones.iloc[n, jars:]).apply(pd.to_numeric))
        x_p1 = ((estaciones_llenas.iloc[index[1], jars:]).apply(pd.to_numeric))
        x_p2 = ((estaciones_llenas.iloc[index[2], jars:]).apply(pd.to_numeric))
        x_p3 = ((estaciones_llenas.iloc[index[3], jars:]).apply(pd.to_numeric))
        # data
        data = pd.DataFrame({'est': est,'x_p1': x_p1, 'x_p2': x_p2, 'x_p3': x_p3})
        # borrar nodata
        data = (data).dropna()
        data.est = (data.est)
        data.x_p1 = (data.x_p1)
        data.x_p2 = (data.x_p2)
        data.x_p3 = (data.x_p3)
        if data.empty:
            print(formato2.format(n, nombre_est))
        else:
            X = data[['x_p1','x_p2','x_p3']]
            # X = data[['X_P1']]
            y = data['est']
            model = sm.OLS(y, X).fit()
            print(formato4.format(n, nombre_est,
                                  (model.rsquared), model.ssr,
                                  (estaciones_llenas.nombre.iloc[index[1:5]]).to_list(),
                                  vecinos[0][1]))
    modest_ols[nombre_est]= model
    data, est, x_p1, x_p2, x_p3, x, y, model = None, None, None, None, None, None, None, None

f = open('MODELOS_RELLENO_ESTACIONES_REGRESION.txt', 'w')
f.write('RELLENO DE ESTACIONES METEOROLOGICAS USANDO OLS'+
        'listado de analisis de regresion de estaciones meteorologicas'+
        '\n'+'respecto a estaciones cercanas, mediante distancia euclidiana\n\n')
for n, nombre_est in enumerate(estaciones.nombre):
    vecinos = kdtree_est.query(estaciones[['norm_lat', 'norm_lon', 'norm_alt']].iloc[n], p=2, k=k)
    index = vecinos[1][1:4]
    if modest_ols[nombre_est]!=None and (modest_ols[nombre_est].rsquared)>=0.7:
        f.write('fila: {:03.0f} \t{} \tnombre: {} \n rellenada x_p1,x_p2,x_p3: {}, en ese orden\n'.format((n),
                str(estaciones.codigo_estacion[n]),
                nombre_est,
                (estaciones_llenas.nombre.iloc[index]).to_list()) +
                str((modest_ols[nombre_est]).summary())+'\n'*5)
f.close()



#% PROCESO DE RELLENO

for n, nombre_est in enumerate(estaciones.nombre):
    #if modelos_ols[nombre_est]!=None and modest_ols[nombre_est]!=None and (modelos_ols[nombre_est].rsquared)<0.7 and (modest_ols[nombre_est].rsquared)>=0.7:
    if modest_ols[nombre_est]!=None and (modest_ols[nombre_est].rsquared)>=0.7:
        print('n{:03.0f} \t {:50.50} \t R2: {}'.format(n,
                                                       nombre_est,
                                                       modest_ols[nombre_est].rsquared))
        #est  = estaciones.iloc[n, jars:]
        #vecinos = kdtree_est.query(estaciones.iloc[n, 11:13], p=2, k=k)
        vecinos = kdtree_est.query(estaciones[['norm_lat', 'norm_lon', 'norm_alt']].iloc[n], p=2, k=k)
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
        relleno = round((x_p1*parametros[0] + x_p2*parametros[1] + x_p3*parametros[2]),2)
        relleno[relleno<=0] = 0
        #relleno = (x_p1*parametros[0])
        ix = np.where(estaciones.iloc[n, jars:].isnull())
        #estaciones.iloc[n, jars:] = pd.to_numeric(estaciones.iloc[n, jars:])
        #estaciones.iloc[n, jars:].iloc[ix[0]] = relleno.iloc[ix][0]
        estaciones.iloc[n, (ix[0]+19)] = relleno.iloc[ix]
    # relleno = None


estaciones.contador = estaciones.iloc[:, jars:].T.apply(pd.to_numeric).count()
estaciones_llenas = estaciones.loc[estaciones.contador >= (jars * -1), :]
estaciones_llenas = estaciones_llenas.reset_index()
estaciones_llenas = estaciones_llenas.iloc[:, 1:]

estaciones_llenas.to_excel('BBDD_magallanes_estaciones_actualizada1.xlsx', freeze_panes=(1,20), float_format="%.8f")
contar.to_excel('BBDD_magallanes_datosXmes.xlsx', freeze_panes=(20,1), float_format="%.8f")

#%% limpiar
del (data, X, df, est, f, formato1, formato2, formato4, ix, index, n, 
     nombre_est, parametros, vecinos, relleno, model, modest_ols, x, x_p1, x_p2,
     x_p3, y, kdtree_est, k, jars)

#%% todas
#est10menos.iloc[:, 19:] = np.array(est10menos.iloc[:, 19:], dtype=np.float64)
#est10menos.contador = est10menos.iloc[:, -372:].T.apply(pd.to_numeric).count()

aa = estaciones.append(est10menos)
aa = aa.T
aa = aa.reset_index()
aa.columns = aa.iloc[0,:]
aa.index = aa.iloc[:, 0]
aa = aa.iloc[:, 1:]
aa.index = aa.iloc[:19, :].index.tolist() + pd.date_range('1989/01','2020/01',freq='M',closed='left').tolist()
aa.iloc[19:, :] = aa.iloc[19:, :].apply(pd.to_numeric)
aa.iloc[19:, :] = aa.iloc[19:, :]*1
aa.iloc[19:, :] = np.array(aa.iloc[19:,:])

# aa = aa.reset_index()
# a = aa.iloc[:, 1:]
# pp = estaciones.T

# pp = aa.T
# pp = pp.iloc[:, 1:]

pp = aa

#%% fournier y pp anuales.
from datetime import datetime
import math
# import math

# dateparse = lambda x: datetime.strptime(x, '%d-%m-%Y')
dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d')

fournier1 = lambda x: (sum([y**2 for y in x])/(sum(x)))

fournier2 = lambda x: (sum([y**2 for y in x]))/(sum(x)/12)

r1 = lambda x: (sum([y**2 for y in x]))


pp_ndatos = None
#pp_ndatos = pp.iloc[19:,:].groupby([dateparse(index[:-5]).year for index in pp.index[19:]]).count()
pp_ndatos = pp.iloc[19:,:].groupby([index.year for index in pp.index[19:]]).count()
# pp_ndatos.iloc[np.where(pp_ndatos == 0)] = np.nan
pp_ndatos.index = [('').join(['NMes_', str(i)]) for i in pp_ndatos.index]

pp_anual = None
# pp_anual = pp.iloc[19:,:].groupby([dateparse(index[:-5]).year for index in pp.index[19:]]).sum()
pp_anual = pp.iloc[19:,:].groupby([index.year for index in pp.index[19:]]).sum()
pp_anual.iloc[(pp_ndatos < 12.0)] = np.nan
pp_anual.index = [('').join(['PpAcu_', str(i)]) for i in pp_anual.index]

#pp_if = pp.iloc[19:,:].groupby([dateparse(index[:-5]).year for index in pp.index[19:]]).agg(fournier1)
pp_if1 = None
pp_if1 = pp.iloc[19:,:].groupby([index.year for index in pp.index[19:]]).agg(fournier1)
pp_if1.iloc[(pp_ndatos < 12.0)]  = np.nan
pp_if1.index = [('').join(['IMF_', str(i)]) for i in pp_if1.index]

pp_r = None
pp_r = pp_if1.copy()

for x in range(0, 353):
    for y in range(0, 31):
        if pd.isnull(pp_r.iloc[y,x]):
            pp_r.iloc[y,x] = pp_r.iloc[y,x]
        else:
            pp_r.iloc[y,x] = (1.735*10**(1.5*math.log10(pp_r.iloc[y,x])-0.08188))

pp_r.iloc[(pp_ndatos < 12.0)]  = np.nan
pp_r.index = [('').join(['R_', str(i)[-4:]]) for i in pp_r.index]

# pp_if2 = None
# pp_if2 = pp.iloc[19:,:].groupby([index.year for index in pp.index[19:]]).agg(fournier2)
# pp_if2.iloc[(pp_ndatos < 12.0)]  = np.nan
# pp_if2.index = [('').join(['IFM2_', str(i)]) for i in pp_if2.index]

# pp_r1 = None
# pp_r1 = pp.iloc[19:,:].groupby([index.year for index in pp.index[19:]]).agg(r1)
# pp_r1.iloc[(pp_ndatos < 12.0)]  = np.nan
# pp_r1.index = [('').join(['R1', str(i)]) for i in pp_if3.index]

#pp = pp.append(vacio)
bb = pp.append(pp_ndatos)
#pp = pp.append(vacio)
bb = bb.append(pp_anual)
#pp = pp.append(vacio)
bb = bb.append(pp_if1)
bb = bb.append(pp_r)
#pp = pp.append(vacio.T)
#pp.append(vacio.T)

#estaciones_llenas.to_excel('BBDD_erosion2019_estaciones_actualizada1.xlsx', freeze_panes=(1,20), float_format="%.8f")
bb.to_excel('BBDD_erosion2019_estaciones_actualizada.xlsx', freeze_panes=(20,1), float_format="%.8f")

#%% relleno 10menos

est10menos 


#% MODELOS DE RELLENO
k = 4
kdtree_est = spatial.KDTree(estaciones_llenas.loc[:,['norm_lat', 'norm_lon', 'norm_alt']])

modest_ols = {}
model = None

formato1 = 'n:{:03.0f}, estacion: {:40.40}, \tDATOS COMPLETOS PARA PERIODO'
formato2 = 'n:{:03.0f}, estacion: {:40.40}, \tSIN DATOS'
formato4 = 'n:{:03.0f}, estacion: {:40.40}, \tR2: {:02.3f}, \tSSR: {:10.3f}\t{},\t{:02.3f}'

for n, nombre_est in enumerate(est10menos.nombre):
    if est10menos.contador.iloc[n] == (jars*-1):
        print(formato1.format(n, nombre_est))
    elif est10menos.contador.iloc[n] <= 119:
        print(formato2.format(n, nombre_est))
    else:
        # determinación de veciones cercanas
        vecinos = kdtree_est.query(est10menos[['norm_lat', 'norm_lon', 'norm_alt']].iloc[n], p=2, k=k)
        index = vecinos[1][:]
        # # estaciones de datos
        est  = ((est10menos.iloc[n, jars:]).apply(pd.to_numeric))
        x_p1 = ((estaciones_llenas.iloc[index[1], jars:]).apply(pd.to_numeric))
        x_p2 = ((estaciones_llenas.iloc[index[2], jars:]).apply(pd.to_numeric))
        x_p3 = ((estaciones_llenas.iloc[index[3], jars:]).apply(pd.to_numeric))
        # data
        data = pd.DataFrame({'est': est,'x_p1': x_p1, 'x_p2': x_p2, 'x_p3': x_p3})
        # borrar nodata
        data = (data).dropna()
        data.est = (data.est)
        data.x_p1 = (data.x_p1)
        data.x_p2 = (data.x_p2)
        data.x_p3 = (data.x_p3)
        if data.empty:
            print(formato2.format(n, nombre_est))
        else:
            X = data[['x_p1','x_p2','x_p3']]
            # X = data[['X_P1']]
            y = data['est']
            model = sm.OLS(y, X).fit()
            print(formato4.format(n, nombre_est,
                                  (model.rsquared), model.ssr,
                                  (estaciones_llenas.nombre.iloc[index[1:5]]).to_list(),
                                  vecinos[0][1]))
    modest_ols[nombre_est]= model
    data, est, x_p1, x_p2, x_p3, x, y, model = None, None, None, None, None, None, None, None

f = open('MODELOS_RELLENO_ESTACIONES_REGRESION.txt', 'w')
f.write('RELLENO DE ESTACIONES METEOROLOGICAS USANDO OLS'+
        'listado de analisis de regresion de estaciones meteorologicas'+
        '\n'+'respecto a estaciones cercanas, mediante distancia euclidiana\n\n')
for n, nombre_est in enumerate(est10menos.nombre):
    vecinos = kdtree_est.query(est10menos[['norm_lat', 'norm_lon', 'norm_alt']].iloc[n], p=2, k=k)
    index = vecinos[1][1:4]
    if modest_ols[nombre_est]!=None and (modest_ols[nombre_est].rsquared)>=0.7:
        f.write('fila: {:03.0f} \t{} \tnombre: {} \n rellenada x_p1,x_p2,x_p3: {}, en ese orden\n'.format((n),
                str(est10menos.codigo_estacion[n]),
                nombre_est,
                (estaciones_llenas.nombre.iloc[index]).to_list()) +
                str((modest_ols[nombre_est]).summary())+'\n'*5)
f.close()



#% PROCESO DE RELLENO

for n, nombre_est in enumerate(est10menos.nombre):
    #if modelos_ols[nombre_est]!=None and modest_ols[nombre_est]!=None and (modelos_ols[nombre_est].rsquared)<0.7 and (modest_ols[nombre_est].rsquared)>=0.7:
    if modest_ols[nombre_est]!=None and (modest_ols[nombre_est].rsquared)>=0.7:
        print('n{:03.0f} \t {:50.50} \t R2: {}'.format(n,
                                                       nombre_est,
                                                       modest_ols[nombre_est].rsquared))
        #est  = estaciones.iloc[n, jars:]
        #vecinos = kdtree_est.query(estaciones.iloc[n, 11:13], p=2, k=k)
        vecinos = kdtree_est.query(est10menos[['norm_lat', 'norm_lon', 'norm_alt']].iloc[n], p=2, k=k)
        index = vecinos[1][:]
        # estaciones.iloc[index[1], jars:].count()
        # estaciones.iloc[index[2], jars:].count()
        # estaciones.iloc[index[3], jars:].count()
        # valores de X
        x_p1 = (estaciones_llenas.iloc[index[1], jars:]).apply(pd.to_numeric)
        x_p2 = (estaciones_llenas.iloc[index[2], jars:]).apply(pd.to_numeric)
        x_p3 = (estaciones_llenas.iloc[index[3], jars:]).apply(pd.to_numeric)
        # calculo
        parametros = (modest_ols[est10menos.nombre[n]]).params
        relleno = (x_p1*parametros[0] + x_p2*parametros[1] + x_p3*parametros[2])
        relleno[relleno<=0] = 0
        #relleno = (x_p1*parametros[0])
        ix = np.where(est10menos.iloc[n, jars:].isnull())
        #estaciones.iloc[n, jars:] = pd.to_numeric(estaciones.iloc[n, jars:])
        #estaciones.iloc[n, jars:].iloc[ix[0]] = relleno.iloc[ix][0]
        est10menos.iloc[n, (ix[0]+19)] = relleno.iloc[ix]
    # relleno = None


# estaciones.contador = estaciones.iloc[:, jars:].T.apply(pd.to_numeric).count()
# estaciones_llenas = estaciones.loc[estaciones.contador >= (jars * -1), :]
# estaciones_llenas = estaciones_llenas.reset_index()
# estaciones_llenas = estaciones_llenas.iloc[:, 1:]

est10menos.to_excel('est10menos_rellenada.xlsx')

# #%% ITERACION 2
# #% MODELOS DE RELLENO
# k = 4
# kdtree_est = spatial.KDTree(estaciones_llenas.loc[:,['norm_lat', 'norm_lon', 'norm_alt']])

# modest_ols = {}
# model = None

# formato1 = 'n:{:03.0f}, estacion: {:40.40}, \tDATOS COMPLETOS PARA PERIODO'
# formato2 = 'n:{:03.0f}, estacion: {:40.40}, \tSIN DATOS'
# formato4 = 'n:{:03.0f}, estacion: {:40.40}, \tR2: {:02.3f}, \tSSR: {:10.3f}\t{},\t{:02.3f}'

# for n, nombre_est in enumerate(estaciones.nombre):
#     if estaciones.contador.iloc[n] == (jars*-1):
#         print(formato1.format(n, nombre_est))
#     elif estaciones.contador.iloc[n] <= 119:
#         print(formato2.format(n, nombre_est))
#     else:
#         # determinación de veciones cercanas
#         vecinos = kdtree_est.query(estaciones[['norm_lat', 'norm_lon', 'norm_alt']].iloc[n], p=2, k=k)
#         index = vecinos[1][:]
#         # # estaciones de datos
#         est  = ((estaciones.iloc[n, jars:]).apply(pd.to_numeric))
#         x_p1 = ((estaciones_llenas.iloc[index[1], jars:]).apply(pd.to_numeric))
#         x_p2 = ((estaciones_llenas.iloc[index[2], jars:]).apply(pd.to_numeric))
#         x_p3 = ((estaciones_llenas.iloc[index[3], jars:]).apply(pd.to_numeric))
#         # data
#         data = pd.DataFrame({'est': est,'X_P1': x_p1, 'X_P2': x_p2, 'X_P3': x_p3})
#         # borrar nodata
#         data = (data).dropna()
#         if data.empty:
#             print(formato2.format(n, nombre_est))
#         else:
#             X = data[['X_P1','X_P2','X_P3']]
#             # X = data[['X_P1']]
#             y = data['est']
#             model = sm.OLS(y, X).fit()
#             print(formato4.format(n, nombre_est,
#                                   (model.rsquared), model.ssr,
#                                   (estaciones_llenas.nombre.iloc[index[1:5]]).to_list(),
#                                   vecinos[0][1]))
#     modest_ols[nombre_est]= model
#     data, est, x_p1, x_p2, x_p3, x, y, model = None, None, None, None, None, None, None, None

# f = open('MODELOS_RELLENO_ESTACIONES_REGRESION_ITERACION_02.txt', 'w')
# f.write('RELLENO DE ESTACIONES METEOROLOGICAS USANDO OLS'+
#         'listado de analisis de regresion de estaciones meteorologicas'+
#         '\n'+'respecto a estaciones cercanas, mediante distancia euclidiana\n\n')
# for n, nombre_est in enumerate(estaciones.nombre):
#     vecinos = kdtree_est.query(estaciones[['norm_lat', 'norm_lon', 'norm_alt']].iloc[n], p=2, k=k)
#     index = vecinos[1][1:4]
#     if modest_ols[nombre_est]!=None and (modest_ols[nombre_est].rsquared)>=0.7:
#         f.write('fila: {:03.0f} \t{} \tnombre: {} \n rellenada X_P1,X_P2,X_P3: {}, en ese orden\n'.format((n),
#                 str(estaciones.codigo_estacion[n]),
#                 nombre_est,
#                 (estaciones_llenas.nombre.iloc[index]).to_list()) +
#                 str((modest_ols[nombre_est]).summary())+'\n'*5)
# f.close()

# #% PROCESO DE RELLENO

# for n, nombre_est in enumerate(estaciones.nombre):
#     #if modelos_ols[nombre_est]!=None and modest_ols[nombre_est]!=None and (modelos_ols[nombre_est].rsquared)<0.7 and (modest_ols[nombre_est].rsquared)>=0.7:
#     if modest_ols[nombre_est]!=None and (modest_ols[nombre_est].rsquared)>=0.7:
#         print('n{:03.0f} \t {:50.50} \t R2: {}'.format(n,
#                                                        nombre_est,
#                                                        modest_ols[nombre_est].rsquared))
#         #est  = estaciones.iloc[n, jars:]
#         #vecinos = kdtree_est.query(estaciones.iloc[n, 11:13], p=2, k=k)
#         vecinos = kdtree_est.query(estaciones[['norm_lat', 'norm_lon', 'norm_alt']].iloc[n], p=2, k=k)
#         index = vecinos[1][:]
#         # estaciones.iloc[index[1], jars:].count()
#         # estaciones.iloc[index[2], jars:].count()
#         # estaciones.iloc[index[3], jars:].count()
#         # valores de X
#         x_p1 = (estaciones_llenas.iloc[index[1], jars:]).apply(pd.to_numeric)
#         x_p2 = (estaciones_llenas.iloc[index[2], jars:]).apply(pd.to_numeric)
#         x_p3 = (estaciones_llenas.iloc[index[3], jars:]).apply(pd.to_numeric)
#         # calculo
#         parametros = (modest_ols[estaciones.nombre[n]]).params
#         relleno = (x_p1*parametros[0] + x_p2*parametros[1] + x_p3*parametros[2])
#         #relleno = (x_p1*parametros[0])
#         ix = np.where(estaciones.iloc[n, jars:].isnull())
#         #estaciones.iloc[n, jars:] = pd.to_numeric(estaciones.iloc[n, jars:])
#         #estaciones.iloc[n, jars:].iloc[ix[0]] = relleno.iloc[ix][0]
#         estaciones.iloc[n, (ix[0]+19)] = relleno.iloc[ix]
#     # relleno = None


# estaciones.contador = estaciones.iloc[:, jars:].T.apply(pd.to_numeric).count()
# estaciones_llenas = estaciones.loc[estaciones.contador >= (jars * -1), :]
# estaciones_llenas = estaciones_llenas.reset_index()
# estaciones_llenas = estaciones_llenas.iloc[:, 1:]

