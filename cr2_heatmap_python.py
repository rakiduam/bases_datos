# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 14:23:07 2020

@author: fanr
"""

import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
import os
import pandas as pd

os.chdir('D:/HEATMAP_CR2/')

path_data_sd = 'cr2_tasDaily_2018/'

# datosCR2 = np.genfromtxt('cr2_tasDaily_2018/puntos_full_TS_original.csv',
#                                skip_header=1, dtype='int16', delimiter=';',
#                                usecols=np.arange(1, 391), autostrip=True)

# 1900-01-01
dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')

datosCR2 = pd.read_csv(filepath_or_buffer = 'cr2_tasDaily_2018/cr2_tasDaily_2018.txt', 
                       #sep = ',',
                       #na_values = -9999, 
                       #skiprows = range(1,15), 
                       skiprows = range(1,30500), 
                       nrows = 1000,
                       parse_dates = ['codigo_estacion'], date_parser = dateparse,
                       )

# datosCR2 = np.genfromtxt('cr2_tasDaily_2018/cr2_tasDaily_2018.txt', 
#                          skiprows =20,  skipcols=2,pdtype='float', delimiter=',')

# np.genfromtxt(fname='cr2_tasDaily_2018/cr2_tasDaily_2018.txt', delimiter=',', 
#               skip_header=3000,
#               skip_footer=7366,
#               usecols=np.arange(1,2))


data = np.random.rand(4, 6)
heat_map = sb.heatmap(data)

# Replace values where the condition is False.
data2 = datosCR2.where(datosCR2 != -9999, 0)

data2 = data2.where(datosCR2 == -9999, 1)


heat_map = sb.heatmap(data2.iloc[0:-1,1:-1], vmin=0, vmax=1, cbar=False, yticklabels = False )

datosCR2.slice_shift(datosCR2.iloc[0,:], periods=1, axis=0)


sns.heatmap(df, vmin=0, vmax=0.5)
plt.show()
