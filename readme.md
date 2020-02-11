
# Serie de scripts basicos para manejo de bases de datos de Chile

## Lectura de datos
son scripts básicos, de limpieza y busqueda rapida de datos o series dentro de
estas bases de datos, idealmente en python y R.<br/>


* cr2     : [Centro de Ciencia del Clima y la Resiliencia (CR)2](http://www.cr2.cl)
           + base de datos por variable  
           + base de datos grillada de clima, de CR2  

* sinca   : [Sistema de Información Nacional de Calidad del Aire](https://sinca.mma.gob.cl/)  
           + datos de estacion de medicion de contaminantes  

* ran     : [Red Agroclimatica Nacional (agromet)](http://www.agromet.cl)  
           + lectura y union de datos historicos por estacion  

* dmc     : [Dirección meteorologica de Chile]  

* dga     : [Banco Nacional Aguas, reportes](http://snia.dga.cl/BNAConsultas/reportes)  
           + lectura datos descargados

~~Graficos, si alcanza el tiempo~~  

## Listado de paquetes usados (para recordar) :  
* python  : scipy numpy gdal pandas geopandas matplotlib seaborn BeautifulSoup4 h5py netCDF4 rasterio statsmodels tqdm xarray  
```{python} pip list ```
* R       : tidyverse, lattice, rgdal, raster, maptools, gdalUtils, geoR, hydroGOF, hydroTSM, influenceR, maps, mapdata, ncdf4,  
```{r} installed.packages() ```
