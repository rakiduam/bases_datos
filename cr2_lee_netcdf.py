# -*- coding: utf-8 -*-
"""
Created on Mon May  4 21:16:34 2020

@author: fanr
"""


from netCDF4 import Dataset
from matplotlib import pyplot as plt
import numpy as np
# import pandas as pd

pp = Dataset('E:/ESTACIONES_CORRECCION/BBDD/CR2MET_pr_v2.0_mon/CR2MET_pr_v2.0_mon_1979_2018_005deg.nc',
             "r", format='NETCDF3_CLASSIC')

pp

print(pp["/pr"])

print(pp.__dict__)
print(pp.variables['pr'][2,])
pp.variables['time']

# extraer datos de grilla
lats = pp.variables['lat'][:]
lons = pp.variables['lon'][:]
time = pp.variables['time'][:]

# malla espacial de datos
lon2, lat2  = np.meshgrid(lons, lats)


plt.imshow(np.array(pp.variables['pr'][2,]), vmin=0, vmax=150)
plt.colorbar()

np.array(pp.variables['pr'][2,])