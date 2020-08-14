# -*- coding: utf-8 -*-
"""
Created on Wed May 20 21:42:40 2020

@author: fneir
"""


import shutil
from glob import glob
import os

os.chdir('E:/')

sentinel = ['18HYE', '18HYF', '18HYG', '19HBA', '19HBB', '19HBV', '19HCA', '19HCB', '18HXF']
# sentinel = ['18HYF', '18HYG', '19HBA', '19HBB', '19HBV', '19HCA', '19HCB']


for i in sentinel:
    print('\t', i)
    # ./CIREN_guardar_aqui/11 SENTINEL 2A/Sentinel-2 Segunda entrega/Agos_Sept_2019/Region_Biobio/
    szip = glob('./CIREN_guardar_aqui/11 SENTINEL 2A/Sentinel-2 Segunda entrega/**/**/*' + i + '*.zip')
    #szip = glob('./**/???SENTINEL?2*/**/*Agos*/**/**' + i + '*.zip')
    print('\n', szip)
    # shutil.move('C:\\bacon.txt', 'C:\\eggs\\new_bacon.txt')
    # 'print()
    [shutil.move(x, ('').join(['E:/SENTINEL/', x.split('\\')[-1]])) for x in szip]
    #szip = None

# %%
##############################################################################

import shutil
from glob import glob
import os

os.chdir('D:/Downloads/ALOS/')

dem = glob('**/**.dem.tif')
len(dem)

[shutil.move(x, ('').join(['DEM/', x.split('\\')[-1]])) for x in dem]
