
# Serie de scripts para bases de datos climaticas de Chile

## Lectura de datos
scripts básicos, de limpieza y subset de datos o series<br/>


* cr2     : [Centro de Ciencia del Clima y la Resiliencia (CR)2](http://www.cr2.cl)
           + base de datos por variable
           + base de datos grillada de clima, de CR2

* sinca   : [Sistema de Información Nacional de Calidad del Aire](https://sinca.mma.gob.cl/)
           ~~+ datos de estacion de medicion de contaminantes  ~~

* ran     : [Red Agroclimatica Nacional (agromet)](http://www.agromet.cl)
           + lectura y union de datos historicos por estacion

* dmc     : [Dirección meteorologica de Chile]
           ~~+ script consulta web  ~~

* dga     : [Banco Nacional Aguas, reportes](http://snia.dga.cl/BNAConsultas/reportes)
           + lectura datos descargados
           + creación de base de datos a partir de reportes mensuales

~~Graficos, si alcanza el tiempo~~

## Listado de paquetes usados (para recordar) :
* python  : scipy numpy gdal pandas geopandas matplotlib seaborn BeautifulSoup4 h5py netCDF4 rasterio statsmodels tqdm xarray scikit-learn
```{python}
pip list
```
* R       : tidyverse, lattice, rgdal, raster, maptools, gdalUtils, geoR, hydroGOF, hydroTSM, influenceR, maps, mapdata, ncdf4,
```{r}
installed.packages()
```
