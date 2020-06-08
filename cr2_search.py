# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 12:36:37 2020

@author: fanr

filter(df, df$latitud>=-40.0, df$latitud <= -32.0)
"""
import pandas as pd, numpy as np
from scipy import spatial
# import seaborn as sb
from zipfile import ZipFile

entrada_dir = ('D:/WORK/GIT/bases_datos')
carpeta_ent = '/cr2_bases_datos'
archivo_zip = '/cr2_prDaily_2018_ghcn.zip'
archivo_txt = 'cr2_prDaily_2018_ghcn/cr2_prDaily_2018_stations_ghcn.txt'

file_entrada = entrada_dir + carpeta_ent + archivo_zip

zip_file = ZipFile(file_entrada)

dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')

est = None
est = (pd.read_csv(filepath_or_buffer=zip_file.open(archivo_txt),sep=',',
                   na_values=-9999, encoding = 'utf-8', dtype='unicode'))

est.nombre
est = pd.DataFrame([est.nombre, est.latitud, est.longitud, est.altura]).T
est.latitud = pd.to_numeric(est.latitud)*-1
est.longitud = pd.to_numeric(est.longitud)*-1
est.altura = pd.to_numeric(est.altura)
est.info()

est2 = None
est2 = pd.read_excel('D:/Desktop/DGA_estaciones_1980-2020_metadata.xlsx', header=0, index_col=0)
#est2.columns = est2.iloc[0,:]
#est2 = est2.iloc[1:-1,:-3]
est2 = est2.iloc[:,:-3]

#[(np.int(lat.strip()[:2]) + np.int(lat.strip()[4:6])/60 + np.int(lat.strip()[8:10])/3600
# 35° 42' 14''"
# 36° 03' 25''
# [lat.strip() for lat in est2.LatitudS]
est2['LAT'] = np.array([(np.int(lat.strip()[:2]) + np.int(lat.strip()[4:6])/60 + np.int(lat.strip()[8:10])/3600) for lat in est2.LatitudS])
est2['LON'] = np.array([(np.int(lat.strip()[:2]) + np.int(lat.strip()[4:6])/60 + np.int(lat.strip()[8:10])/3600) for lat in est2.LongitudW])

est2.iloc[:,2] = pd.to_numeric(est2.iloc[:,2])
est2.iloc[:,3] = pd.to_numeric(est2.iloc[:,3])
est2.iloc[:,-1] = pd.to_numeric(est2.iloc[:,-1])
est2.info()

n = np.arange(0, len(est.altura))

kdtree = spatial.KDTree(est.loc[:,['latitud', 'longitud']])

#estaciones.latitud[0],estaciones.longitud[0],estaciones.altura[0]
k=6
neigh = kdtree.query(est.loc[:,['latitud', 'longitud']], k=k)
closest = kdtree.query([est.latitud[375],est.longitud[375]], p = 2, k=k)
# 3 estaciones mas cercanas acorde a las coordenadas
index = closest[1][:]
est.iloc[index,:] , closest[0]
est.latitud[375],est.longitud[375], est.altura[375]
est.latitud[closest[1]], est.longitud[closest[1]], est.altura[closest[1]]



kdtree2 = spatial.KDTree(est2.iloc[:,[2, 3, 6]])
# neigh2 = kdtree2.query(est2.iloc[:,[2, 3, 6]], k=k)
closest2 = kdtree2.query([est2.iloc[15,2], est2.iloc[15,3], est2.iloc[15,6]], p = 2, k=k)
index2 = closest2[1][:]
utm_e_n_alt = (est2.iloc[index2,:])

kdtree2 = spatial.KDTree(est2.iloc[:,[2, 3]])
# neigh2 = kdtree2.query(est2.iloc[:,[2, 3]], k=k)
closest2 = kdtree2.query([est2.iloc[15,2], est2.iloc[15,3]], p = 2, k=k)
index2 = closest2[1][:]
utm_e_n = (est2.iloc[index2,:])

kdtree2 = spatial.KDTree(est2.iloc[:,[2, 6]])
# neigh2 = kdtree2.query(est2.iloc[:,[2, 6]], k=k)
closest2 = kdtree2.query([est2.iloc[15,2], est2.iloc[15,6]], p = 2, k=k)
index2 = closest2[1][:]
utm_n_alt = (est2.iloc[index2,:])


kdtree2 = spatial.KDTree(est2.iloc[:,[-2, -1]])
# neigh2 = kdtree2.query(est2.iloc[:,[2, 6]], k=k)
closest2 = kdtree2.query([est2.iloc[15,-2], est2.iloc[15,-1]], p = 2, k=k)
index2 = closest2[1][:]
utm_lat_lon = (est2.iloc[index2,:])


# est = (pd.DataFrame(data = [estaciones.nombre, estaciones.latitud,
#                             estaciones.longitud, estaciones.altura])).T

#%%

# from sklearn.neighbors import KDTree

# points = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]

# tree = KDTree(points, leaf_size=2)
# all_nn_indices = tree.query_radius(points, r=1.5)  # NNs within distance of 1.5 of point
# all_nns = [[points[idx] for idx in nn_indices] for nn_indices in all_nn_indices]
# for nns in all_nns:
#     print(nns)

# tree = spatial.KDTree(estaciones.loc[:,['latitud', 'longitud']])
# #estaciones.latitud[0],estaciones.longitud[0],estaciones.altura[0]
# tree.query([estaciones.latitud[0],estaciones.longitud[0],estaciones.altura[0]], p = 2)

# from scipy import spatial

# for index, row in geonames.iterrows():
#     coordinates = [row['latitude'], row['longitude']]
#     cartesian_coord = cartesian(*coordinates)
#     places.append(cartesian_coord)

# tree = spatial.KDTree(places)

# def find_population(lat, lon):
#     cartesian_coord = cartesian(lat, lon)
#     closest = tree.query([cartesian_coord], p = 2)
#     index = closest[1][0]
#     return {
#         'name' : geonames.name[index],
#         'latitude' : geonames.latitude[index],
#         'longitude' : geonames.longitude[index],
#         'population' : geonames.population[index],
#         'distance' : closest[0][0]
#     }