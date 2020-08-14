## https://opensourceoptions.com/blog/open-netcdf-and-view-metadata/

## install.package("ncdf4")

library(ncdf4)

# abrir netcdf
nc <- nc_open(file.choose())

# metadata del archivo
print(nc)

# atributos
attributes(nc$var)

# nombres de los atributos
attributes(nc$var)$names

#
attributes(nc$var)$names[1]

# obtener datos
dat <- ncvar_get(nc, attributes(nc$var)$names[1])

dim(dat)

print(dat)

# leer las dimensiones del dato
dat[1:220,1:800,2]

library(raster)

nc.brick <- brick(file.choose())

dim(nc.brick)

nc.df <-as.data.frame(nc.brick[[1:480]], xy=T)

head(nc.df)

write.csv(nc.df, file.choose())
