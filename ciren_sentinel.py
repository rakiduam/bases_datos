# -*- coding: utf-8 -*-
"""
Created on Thu May 21 14:21:33 2020

@author: fneir
"""

import os, glob, rasterio, pandas as pd, numpy as np
os.chdir('E:/SENTINEL')

# E:\SENTINEL\UNZIP\S2A_MSIL2A_20190129T143751_N0211_R096_T18HYE_20190225T140527\S2A_MSIL2A_20190129T143751_N0211_R096_T18HYE_20190225T140527.SAFE\GRANULE\L2A_T18HYE_A018826_20190129T144524


for root, dirs, files in os.walk(".*/GRANULE", topdown=False):
   for name in dirs:
      print(os.path.join(dirs, name))

print(dirs)
type(dirs)

aa = [ x.split('_')[-5][:8] for x in dirs]
type(aa)
pd.DataFrame(set(aa))


