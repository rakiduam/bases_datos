# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 12:16:22 2020

@author: fneir
"""
import fiona
import rasterio
import rasterio.mask

with fiona.open('E:/Factor_R/CAPAS/divisiones/extension_chile_epsg4326.shp', "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]


with rasterio.open('E:/Factor_R/BBDD/CHIRPSv2_005deg_1980-2019_month/CH198901.tif') as src:
    out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
    out_meta = src.meta


out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})


with rasterio.open("'E:/Factor_R/BBDD/CHIRPSv2_005deg_1980-2019_month/CH198901new.tif')", "w", **out_meta) as dest:
    dest.write(out_image)





'CH' + str(jar) + str(mes).zfill(2) + '*.tif'
entDIR = ('E:/Factor_R/BBDD/CHIRPSv2_005deg_1980-2019_month/CH198901.tif')

for jar in range(1989, 2020):
    for mes in range(1, 13):
        print(jar)
        inRaster = glob.glob('CH' + str(jar) + str(mes).zfill(2) + '*.tif')
        chirp = ExtractByMask(inRaster, inMaskData)
        chirp.save('D:/SPATIAL_TEST/CHIRPS/chile_chirp_' + str(jar) + str(mes).zfill(2) + '.tif')
        chirp = None