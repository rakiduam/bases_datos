# -*- coding: utf-8 -*-
"""
Created on Mon May  4 21:16:34 2020


# %coorrecion de latitud en z # codigo matlab.
# for y=1:nlat
#  z(:,y,:)=z(:,y,:)*(cos(pi*lat1(y)/180))^0.5;
# end
np.array([y*(math.cos((math.pi)*y/180))**0.5 for y in lats]) ## [::-1]


@author: fanr
"""


from netCDF4 import Dataset
from matplotlib import pyplot as plt
import numpy as np
import math
# import pandas as pd





pp = Dataset('E:/ESTACIONES_CORRECCION/BBDD/CR2MET_pr_v2.0_mon/CR2MET_pr_v2.0_mon_1979_2018_005deg.nc',
             "r", format='NETCDF3_CLASSIC')

pp

print(pp["/pr"])

print(pp.__dict__)
print(pp.variables['pr'][2,])
pp.variables['time']



# extraer datos de grilla
#latitud invertida
lats = np.array(pp.variables['lat'][:])
lons = pp.variables['lon'][:]
time = pp.variables['time'][:]

# malla espacial de datos
lon2, lat2  = np.meshgrid(lons, lats)

# debido a que estan invertidas deben ser ploteadas asi.
plt.imshow(np.array(pp.variables['pr'][2,])[::-1], vmin=0)
plt.colorbar()



np.array(pp.variables['pr'][2,])