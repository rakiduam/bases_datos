# -*- coding: utf-8 -*-
#### IDEA #####

"

idea:
  - crear una bateria de analisis para datos de precipitacion que permitan identificar
  datos anomalos dentro de la serie

contexto:
  Precipitación es una variable climatica dificil de caracterizar, ya que no
  posee valores continuos. Y en lugares como Chile, donde gran parte del territorio
  tiene peridos secos y humedos marcados, este tipo de analisis es complicado.

pasos:
  - se define una bateria de estadisticos, sesgados e insesgados
  - algunos criterios de informacion, tales como n_datos, fechas valor máximo
  - criterios estadisticos como, como percentiles, rango intercuantil y mediana

fuentes:
  - https://www.stat.purdue.edu/~huang251/1018.html
  - https://www.youtube.com/watch?v=A3gClkblXK8
  - https://www.youtube.com/watch?v=12Xq9OLdQwQ // https://github.com/Zelazny7/isofor
  - https://algobeans.com/2016/09/14/k-nearest-neighbors-anomaly-detection-tutorial/
  - https://machinelearningstories.blogspot.com/2018/07/anomaly-detection-anomaly-detection-by.html?m=1
  - https://towardsdatascience.com/time-series-of-price-anomaly-detection-13586cd5ff46

  USO DE IQR Y DESVIACION ESTANDAR
  - https://www.youtube.com/watch?v=rzR_cKnkD18

  MAHALANOBIS DETECCION OUTLIERS
  - http://eurekastatistics.com/using-mahalanobis-distance-to-find-outliers/

"
###
# LIMPIAR ESPACIO TRABAJO ####
rm ( list = ls () )
cat( rep ( "\n", 64 ) )

#### LIBRERIAS USADAS ####
library(dplyr)
library(readxl)
library(stringr)
#library(lubridate)

#### DIRECTORIO ####
setwd('E:/Factor_R/BBDD/')
print(getwd())

# LECTURA DE DATOS ####
df <- as.data.frame(read_excel("DGA_CR2_Erosion2010_1980-2019.xlsx", col_names=FALSE, na="-9999"))

# LIMPIEZA DATAFRAME ####
df <- as.data.frame((df[c(2,2:nrow(df)), c(3:ncol(df)) ]))

colnames(df) <- df[1,]
df <- df[c(2:nrow(df)), ]

#### AGREGAR FECHAS y CAMPOS DE FECHA  ####
fecha <- (as.data.frame(str_split(c(as.character(seq.Date(from=as.Date('1980-01-31'),
                                              to=as.Date('2020-01-01'), by='months'))), '-')))

fecha = as.data.frame(t(fecha))
rownames(fecha) = NULL
colnames(fecha) = c('year', 'month', 'dia')

df <- cbind(fecha[, 1:2], df)

# FACTORES A  NUMERICO ####
df <- as.data.frame(apply(df, MARGIN=2, FUN = function(x){as.numeric(as.character(x))}))
rownames(df) <- c(as.character(seq.Date(from = as.Date('1980-01-31'), to = as.Date('2020-01-01'), by = 'months')))

# filtro por periodo ####
df <- df[df$year>1988,]

# elimina años sin datos ####
df <- as.data.frame(t(df))

# ESTADISTICA DESCRIPTIVA #####
# funciones #####
zeros_num <- function(x) {
  x <- x * ifelse(x == 0, 1, NA)
  b <- sum(is.na(x))
  return(b)
}

median_absolute_deviation <- function(x) {
  mediana <- median(x, na.rm=TRUE)
  cum_sum <- 0
  for (i in seq(1:length(x))){
    if (is.na(x[i])){
      # print('F!')
    } else{
      cum_sum = sum(abs(x[i]-mediana)) + cum_sum
    }
  }
  b <- (cum_sum / length(x))
  return(b)
}

# df[c("1989-01-31","2019-12-31")]
rango = c(as.character(seq.Date( from=as.Date('1900-01-31'), to=as.Date('2020-01-01'), by='months')))
# estimación #####
margen = 1

df$n_data <- apply(df[, rango], MARGIN = margen, FUN = function(x){sum(!is.na(x))} )       ## n datos
df$no_data<- apply(df[, rango], MARGIN = margen, FUN = function(x){sum(is.na(x))} )   ## n no_datos
df$n_zero <- apply(df[, rango], MARGIN = margen, FUN = zeros_num)      ## n de ceros
df$min    <- apply(df[, rango], MARGIN = margen, FUN = function(x) {min(x, na.rm = TRUE)} )            ## mínimo
df$max    <- apply(df[, rango], MARGIN = margen, FUN = function(x) {max(x, na.rm = TRUE)})            ## máximo
df$mediana<- apply(df[, rango], MARGIN = margen, FUN = function(x) { median(x, na.rm=TRUE) })       ## mediana
df$mad    <- apply(df[, rango], MARGIN = margen, FUN = median_absolute_deviation)  ## median absolute deviation
df$mean   <- apply(df[, rango], MARGIN = margen, FUN = function(x) {mean(x, na.rm = TRUE)} )     ## promedio
df$std    <- apply(df[, rango], MARGIN = margen, FUN =  function(x) {sd(x, na.rm = TRUE)} )  ## desviacion estandar
df$iqr    <- apply(df[, rango], MARGIN = margen, FUN = function(x) {IQR(x, na.rm = TRUE, type=7)} )  ## rango intercuartil

df <- cbind(df[,], t(apply(df[, rango], MARGIN = margen, FUN = function(x) {quantile(x, probs = (c(25, 50, 75 )/100) , na.rm = TRUE)} )))           ## cuantil

df$completa[ df$n_data == 372] = 'serie completa'
df$completa[ df$n_data <= 371] = 'serie incompleta'

df$fecha_max = ''
# fechas donde se produce el máximo ####
for (i in c(1:nrow(df))){
  if (df$n_data[i] >= 1){
    df$fecha_max[i] <- as.character( colnames(df)[ which( df[i, c(1:372)] == df$max[i])] )
  } else{
  }
}

View((df[, c(373:ncol(df))]))
#

# filtrar no data ####
# df <- filter(df, n_data>120)


################################################################################
View(t(df))

aa <- (t(df))

standarized_anomalies <- function(x, media_muestral, desviacion_estandar) {
  # formula extraída desde el wilks
  b <- ((x-media_muestral)/desviacion_estandar)
  return(b)
}

df$completa <- df$n_data

# fechas donde se produce el máximo
for (i in c(1:nrow(asdfVAR))){
  asdfVAR$fecha_max[i] <- names(asdfVAR)[which(asdfVAR[i, rango]==asdfVAR$max[i])+1]
  #  asdfVAR$`fecha_max75%`[i] <- names(asdfVAR)[which(asdfVAR[i, rango]==asdfVAR$`75%`[i])+1]
  # asdfVAR$fecha_max99[i] <- names(asdfVAR)[which(asdfVAR[i, rango]==asdfVAR$`99%`[i])+1]
}

# filtro 4
asdfVAR<-filter(asdfVAR, n_data>120)

fecha_max_registro <- unique(asdfVAR$fecha_max)

# View(asdfVAR)

#### ESCRITURA OUTPUT ####
niucol <- ncol(asdfVAR)
difcol <- niucol-oldcol
View(asdfVAR[, c(1,374:niucol)])
write.table(asdfVAR, 'D:/asdf2.csv', sep=';')

##### . #####
# ############################## TEST ###################

#asdfVAR <- ifelse(asdfVAR[13, c(2:ncol(asdfVAR))] < 0, NA, 1)


nombre = asdfVAR$nombre

asdf <- t(asdfVAR[2:(ncol(asdfVAR)-difcol)])


# aa = t(filter(asdfVAR, data_num==127))

colnames(asdf) <- asdfVAR$nombre
# View(asdf)
# View(asdf1[,14])
asdf.max = max(asdf, na.rm = TRUE)

#par (mar=c(18, 4, 2, 2)+0.1)
boxplot(asdf[,c(1:ncol(asdf))], las = 2, ylim=c(0, asdf.max),
        ylab = "Precipitaciones (mm)",
        # xlab = "Estaciones"
)

# boxplot(asdf[,c(1:(ncol(asdf)/50))], las = 2, ylim=c(0, asdf.max), ylab = "Precipitaciones (mm)",)
##### ASDSFSDFSDF #######
# me habria ahorrado la paja mental de calcular ccon summary
summary(asdf)
head(asdf)
dim(asdf)

standarized_anomalies(asdf[,1], 53.822, 87.997)

(apply(asdf[,c(1:36)], MARGIN = 0, FUN = standarized_anomalies))
asdf[,1]
