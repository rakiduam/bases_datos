# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 16:45:31 2020

@author: fanr
"""

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

url = ('https://climatologia.meteochile.gob.cl/application/mensuales/viento18DireccionesMensual/180005/2019/1')

r  = requests.get(url)
data = r.text
soup = BeautifulSoup(data, "html.parser")


print(soup.div['style']="display:none")
soup.table['id']='freq'


for sub_heading in soup.find_all('table'):
    print(sub_heading.text)

table = soup.find('table', attrs={'border':"0", 'cellpadding':"0", 'cellspacing':"0", 'id':"freq"})
table_rows = table.find_all('tr')
