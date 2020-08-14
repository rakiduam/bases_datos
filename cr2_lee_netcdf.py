# -*- coding: utf-8 -*-
"""
Created on Mon May  4 21:16:34 2020


# %coorrecion de latitud en z # codigo matlab.
# for y=1:nlat
#  z(:,y,:)=z(:,y,:)*(cos(pi*lat1(y)/180))^0.5;
# end
np.array([y*(math.cos((math.pi)*y/180))**0.5 for y in lats]) ## [::-1]

float64 time(time)
    long_name: time
    units: months since 1978-12-15

@author: fanr

- http://www.cr2.cl/datos-productos-grillados/
METADATA:
El conjunto de datos CR2MET contiene información meteorológica (precipitación,
temperaturas medias y extremas ) en un grilla rectangular de 0.05º
latitud-longitud (aproximadamente 5km) para el territorio de Chile continental
y el periodo 1979-2016. El desarrollo de este producto responde a la necesidad
de contar con datos distribuidos espacialmente coherentes con la información
observacional disponible para, entre otras aplicaciones, el estudio del clima
e hidrología a escala regional y la evaluación de modelos atmosféricos.

La técnica utilizada para la construcción del producto de precipitación se basa
en una regionalización estadística de datos del reanálisis atmosférico ERA-Interim
(datos disponibles en grillas de ~70 km). El método utiliza modelos estadísticos
como funciones de transferencia para traducir precipitación, flujos de humedad y
otras variables de gran escala de ERA-Interim, en precipitación regional. Los
modelos estadísticos consideran la topografía local y se definen mediante un
conjunto de parámetros calibrados con observaciones locales de precipitación.

Los productos de temperatura y temperaturas extremas (máximas y mínimas diurnas)
se construyeron con un enfoque relativamente distinto. En este caso, además de
la información local (topografía y observaciones de temperatura) y de variables
de gran escala (ERA-Interim), se consideraron datos de temperatura superficial
estimada mediante imágenes satelitales (MODIS LST).

"""

from netCDF4 import Dataset
from matplotlib import pyplot as plt
import numpy as np
# import math
# import pandas as pd

entDIR ='E:/ESTACIONES_CORRECCION/BBDD/'
inFILE = 'CR2MET_pr_v2.0_mon/CR2MET_pr_v2.0_mon_1979_2018_005deg.nc'
pp = Dataset(entDIR + inFILE, "r") #format='NETCDF3_CLASSIC')

pp.get_variables_by_attributes()
# pp.getattrs()
# pp.ncattrs()

print(pp["/pr"])

print(pp.__dict__)
print(pp.variables['pr'][2,])
pp.variables['time']

# pp.getValue(pr)

# extraer datos de grilla
#latitud invertida
lats = np.array(pp.variables['lat'][:])
lons = pp.variables['lon'][:]
time = pp.variables['time'][:]
print(time)

aa = lats[np.where(lats>-45)]
aa = aa[np.where(aa<-32)]


# malla espacial de datos
lon2, lat2  = np.meshgrid(lons, lats)

# debido a que estan invertidas deben ser ploteadas asi.
plt.imshow(np.array(pp.variables['pr'][2,])[::-1], vmin=0)
plt.colorbar()

np.array(pp.variables['pr'][2,])