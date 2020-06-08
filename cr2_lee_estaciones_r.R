# -*- coding: utf-8 -*-
##
"
https://www.youtube.com/watch?v=A3gClkblXK8
"
###
## limpiar el espacio de trabajo
rm ( list = ls () )
cat( rep ( "\n", 64 ) )

## funciones

# racha <- function(x, negate = FALSE, na.rm = FALSE) {
#   # aqui agregue esto para que sea 0 y 1
#   # racha <- function(x, negate = FALSE, na.rm = TRUE) {
#   #racha(!is.nan(as.numeric(asdfVAR[13,rango])), negate=FALSE, na.rm = TRUE)
#   #https://stackoverflow.com/questions/4655848/calculating-a-consecutive-streak-in-data#4656018
#   x <- is.nan(as.numeric(x))
#   rles <- rle(x > 0)
#   if(negate) {
#     max(rles$lengths[!rles$values], na.rm = na.rm)
#   } else {
#     max(rles$lengths[rles$values], na.rm = na.rm)
#   }
# }
# wins <- lapply(split(subRes[,2],subRes[,1]), FUN)
# loses <- lapply(split(subRes[,2],subRes[,1]), FUN, negate = TRUE)


#### FUNCIONES USADAS #####
getmode <- function(v) {
  # https://www.tutorialspoint.com/r/r_mean_median_mode.htm
  uniqv <- unique(v)
  uniqv[which.max(tabulate(match(v, uniqv)))]
}


data_num <- function(x) {
  b <- sum(!is.na(x))
  return(b)
}


nodata_num <- function(x) {
  b <- sum(is.na(x))
  return(b)
}


zeros_num <- function(x) {
  x <- x * ifelse(x == 0, 1, NA)
  b <- sum(is.na(x))
  return(b)
}


promedio <- function(x) {
  b <- round(mean(x, na.rm = TRUE), 3)
  return(b)
}

minimo <- function(x) {
  b <- min(x, na.rm = TRUE)
  return(b)
}


maximo <- function(x) {
  b <- max(x, na.rm = TRUE)
  return(b)
}


desviacion <- function(x) {
  b <- round(sd(x, na.rm = TRUE), 3)
  return(b)
}


cuantil <- function(x) {
  # x <- x * ifelse(x == 0, NA, 1)
  b <- quantile(x, probs = (c(25, 50, 75, 90, 95, 99 )/100) , na.rm = TRUE)
  return(b)
}


rango_iqr <- function(x) {
   b <- IQR(x, na.rm = TRUE, type=7)
  return(b)
}


sumario <- function(x) {
  b <- summary(x)
  return(b)
}


mediana <- function(x) {
  b <- median(x, na.rm=TRUE)
  return(b)
}


median_absolute_deviation <- function(x) {
  mediana <- median(x, na.rm=TRUE)
  cum_sum <- 0
  for (i in seq(1:length(x))){
    if (is.na(x[i])){
      #print('F!')
    } else{
    cum_sum = sum(abs(x[i]-mediana)) + cum_sum
    }
  }
  b <- (cum_sum / length(x))
  return(b)
}


#### LIBRERIAS USADAS ####
library(dplyr)

#### LECTURA DE DATOS ####
archivo_zip <- unzip('D:/WORK/GIT/bases_datos/cr2_bases_datos/cr2_prAmon_2019.zip')
# "./cr2_prAmon_2019/cr2_prAmon_2019.txt"
df <- read.csv(archivo_zip[2], sep=',', header = FALSE, na.strings = '-9999',
                    stringsAsFactors = TRUE, encoding = 'utf-8')
rm(archivo_zip)

## limpieza dataframe ##
df <- t(df)
colnames(df) <- c(as.character(df[1,]))
df <- (df[-1,])
rownames(df) <- (c(1:length(df[,1])))
df <- as.data.frame(df)
df <- type.convert(df, na.strings = "NA", numerals = "no.loss")
# str(df) ## chequeo de estructura de los datos


## comienzo de filtros de informacion
# filtro 0, respecto a ubicación espacial, stgo = -33.4 && temuco = -38.8
df <- filter(df, df$latitud>=-40.0, df$latitud <= -32.0)
# df <- filter(df, df$latitud>=-36.64, df$latitud <= -34.1)

# filtro 1, por estaciones de interes, en este caso de la zona estudio, mediante id
interes <- c('340031', '360011', '6019003', '6019005', '6034003', '6036001',
             '6044001', '6055003', '6120001', '6130001', '6130002', '6130003',
             '6132002', '7106007', '7115001', '7116004', '7116005', '7118003',
             '7119007', '7121003', '7123001', '7200001', '7210001', '7317001',
             '7320002', '7321002', '7331002', '7332003', '7335004', '7336003',
             '7337002', '7340002', '7340003', '7341002', '7342002', '7345001',
             '7350001', '7350006', '7352002', '7352003', '7353001', '7355002',
             '7355006', '7355007', '7357003', '7358007', '7358008', '7359001',
             '7359005', '7370001', '7371002', '7373003', '7373004', '7374004',
             '7374005', '7376002', '7378002', '7378003', '7379002', '7381003',
             '7383001', '7384002', '8113001', '8117002', '8117009', '8118003',
             '8118004', '8141002', '8142001')
df <- filter(df, df$codigo_estacion %in% interes)

# filtro 1, continuacion, acotacion de estaciones al norte del maule
maule_norte <- c('340031', '6019003', '6019005', '6034003', '6036001', '6044001',
                 '6055003', '6120001', '6130001', '6130002', '6130003', '6132002',
                 '7106007', '7115001', '7116004', '7116005', '7118003', '7119007',
                 '7121003', '7123001', '7200001', '7210001', '7320002', '7321002',
                 '7370001', '7371002', '7373003', '7373004', '7374004', '7374005',
                 '7376002', '7378002', '7378003', '7379002', '7381003', '7383001')
df <- filter(df, df$codigo_estacion %in% maule_norte)



# filtro 2, por rango de años de datos, 30 años datos
rango_asdf <- c(1:11, (ncol(df)-(12*(30+1))+1):ncol(df))
asdfVAR <- type.convert(as.data.frame(df[, c(4, (ncol(df)-(12*(30+1))+1):ncol(df))]))


# filtro 3, eliminación de aquellas estaciones que no tengan datos para periodo
asdfVAR[, c(2:ncol(asdfVAR))] <- asdfVAR[, c(2:ncol(asdfVAR))] * ifelse(asdfVAR[, c(2:ncol(asdfVAR))] < 0, NA, 1)
dim(asdfVAR)

# if (exists("maule_norte")) {}

# estimacion de parametros descriptivos/estadisticos/informacion
margen = 1  ## eje horizontal
oldcol <- ncol(asdfVAR)  ## determinacion numero original de columnas
rango = c(2:ncol(asdfVAR))  ## rango donde se aplicaran las estimaciones

asdfVAR$n_data <- apply(asdfVAR[, rango], MARGIN = margen, FUN = data_num)  ## n datos
asdfVAR$n_nodata <- apply(asdfVAR[, rango], MARGIN = margen, FUN = nodata_num)  ## n no_datos
asdfVAR$n_zeros <- apply(asdfVAR[, rango], MARGIN = margen, FUN = zeros_num)  # # n de ceros


# asdfVAR$racha <- apply(asdfVAR[, rango], MARGIN = margen, FUN = racha, negate= TRUE, na.rm=TRUE)

# minimo
asdfVAR$min <- apply(asdfVAR[, rango], MARGIN = margen, FUN = minimo)
# maximo
asdfVAR$max <- apply(asdfVAR[, rango], MARGIN = margen, FUN = maximo)
# mediana
asdfVAR$mediana <- apply(asdfVAR[, rango], MARGIN = margen, FUN = mediana)
# median absolute deviation
asdfVAR$mad <- (apply(asdfVAR[, rango], MARGIN = margen, FUN = median_absolute_deviation))
# promedio
asdfVAR$promedio <- apply(asdfVAR[, rango], MARGIN = margen, FUN = promedio)
# desviacion estandar
asdfVAR$desviacion_estandar <- apply(asdfVAR[, rango], MARGIN = margen, FUN = desviacion)
# rango intercuartil
asdfVAR$rango_intercuantil <- (apply(asdfVAR[, rango], MARGIN = margen, FUN = rango_iqr))
# cuantiles
asdfVAR <- cbind(asdfVAR, t(apply(asdfVAR[, rango], MARGIN = margen, FUN = cuantil)))

# fechas donde se produce el maximo
for (i in c(1:nrow(asdfVAR))){
  asdfVAR$fecha_max[i] <- names(asdfVAR)[which(asdfVAR[i, rango]==asdfVAR$max[i])+1]
  asdfVAR$`fecha_max75%`[i] <- names(asdfVAR)[which(asdfVAR[i, rango]==asdfVAR$`75%`[i])+1]
  # asdfVAR$fecha_max99[i] <- names(asdfVAR)[which(asdfVAR[i, rango]==asdfVAR$`99%`[i])+1]
}

# filtro 4
asdfVAR<-filter(asdfVAR, data_num>120)

# asdfVAR$revisa <- '-'
# getmode(asdfVAR$colmax)

fecha_max_registro <- unique(asdfVAR$fecha_max)

# for (i in c(1:nrow(asdfVAR))){
#   print(i)
#   if ((asdfVAR$data_num[i] <= 336 & asdfVAR$max[i] >= (3*asdfVAR$mad[i]+asdfVAR$med[i]) & asdfVAR$zeros_num[i]>248 & asdfVAR$nodata_num[i] > 120 & asdfVAR$nodata_num[i] < 252)){
#     asdfVAR$revisa[i] <- 'revisar'
#   } else{
#     asdfVAR$revisa[i] <- '-'
#   }
# }

#asdfVAR$iqrmax <- asdfVAR$std*3+asdfVAR$pro
#asdfVAR$MAD <- asdfVAR$med

#aa <- asdfVAR$std*3+asdfVAR$pro


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
# View(asdf1)
# View(asdf1[,14])
asdf.max = max(asdf, na.rm = TRUE)

par (mar=c(18, 4, 2, 2)+0.1)
boxplot(asdf[,c(1:ncol(asdf))], las = 2, ylim=c(0, asdf.max))

write.table(asdf1, 'E:/ESTACIONES_CORRECCION/DGA/asdf3.csv', sep=';')

##### . #####
# df1 <- filter(df[c(seq(1:15), (ncol(df)-(12*(30+1))+1):ncol(df))], df$nombre %in% asdfVAR$nombre)
# View(df1)
# df1[, c(16:ncol(df1))] <- (df1[, c(16:ncol(df1))] * ifelse(df1[, c(16:ncol(df1))] < 0, NA, 1))
# 
# df1 <- t(df1)
# 
# write.table(df1, 'E:/cr2_ppMonth_1989-2019.csv',sep = ';')


#ncol(asdf)/3
#grid

#abline(h=seq(650, asdf.max+100, 100), lty = 3, col='red')
#boxplot(asdf[,c(36:69)], las = 2, ylim=c(0, asdf.max))
#abline(h=seq(650, asdf.max+100, 100), lty = 3, col='red')
#abline(h=1000)

# par (mar=(c(18, 4, 2, 2)+0.1))
# gplots::boxplot2(asdf[,c(1:35)], las = 2, ylim=c(0, asdf.max), shrink=0.8, top=FALSE, font="Times New Roman")
# gplots::boxplot2(asdf[,c(36:69)], las = 2, ylim=c(0, asdf.max), shrink=0.8, top=FALSE)
#
# par(mar=c(5, 5, 5, 5)+0.1)
#
# for (i in c(1:ncol(asdf))){
#   hist(asdf[,i], main = as.character(asdfVAR$nombre[i]), xlab = 'Precipitación (mm)')
# }
#
# for (i in c(1:ncol(asdf))){
#   hist(asdf[,i], main = as.character(asdfVAR$nombre[i]), xlab = 'Precipitación (mm)')
#   qqnorm(asdf[,i], ylab = "Precipitación (mm)", main = as.character(asdfVAR$nombre[i]))
# }
#
#
# #qqPlot(asdf[,1], dist="chisq", df=2)
# # gplots::boxplot2(asdf[,c(17:32)], las = 2)
# # gplots::boxplot2(asdf[,c(33:48)], las = 2)
# # gplots::boxplot2(asdf[,c(49:64)], las = 2)
# # gplots::boxplot2(asdf[,c(65:ncol(asdf))], las = 2)

# ####
#
# library(ggplot2)
#
#
#
# # prepare a special xlab with the number of obs for each group
# my_xlab <- paste(levels(data$names),"\n(N=",table(data$names),")",sep="")
#
# # plot
# ggplot(as.data.frame(asdf) ) +
#   geom_boxplot(varwidth = TRUE, alpha=0.2) +
#   theme(legend.position="none") #+
  #scale_x_discrete(labels=my_xlab)# asdfVAR$revisa <- asdfVAR[]
#
# asdfVAR[1, (which(asdfVAR[1, c(2:oldcol)] %in% asdfVAR$max[1]))]
#
# if(asdfVAR$max>asdfVAR$iqrmax){
#   asdfVAR$revisa <- which(x %in% c(2,4))
# }
#
# # asdfVAR <- cbind(asdfVAR, t(apply(asdfVAR[, rango], MARGIN = margen, FUN = cuantil0)))
#
# niucol <- ncol(asdfVAR)
# difcol <- niucol-oldcol
#
# asdfVAR<-filter(asdfVAR, nodata_num<240)
#
# aa<-filter(asdfVAR, data_num>350); View(aa[, c(1,374:ncol(aa))])
#
# View(asdfVAR[, c(1,374:ncol(asdfVAR))])
# View(asdfVAR)
# dim(asdfVAR)
#
# nombre = asdfVAR$nombre
#
#
# # asdf <- t(filter(asdfVAR, asdfVAR$nombre %in% nombre))
#
# asdf <- t(asdfVAR[2:(ncol(asdfVAR)-difcol)])
# View(asdf)
#
# # asdf <- (type.convert(as.data.frame((asdf[c(2:(nrow(asdfVAR))), ]))))
# colnames(asdf) <- asdfVAR$nombre
#
# # dim(asdfVAR)
# # dim(asdf)
# # View(asdf)
#
# # for (i in c(1:ncol(asdf))){
# #   hist(asdf[,i], main = as.character(asdfVAR$nombre[i]), xlab = 'Precipitación (mm)')
# # }
# #
# asdf <- asdf*ifelse(asdf == 0, NA, 1)
# asdf.max = max(asdf, na.rm = TRUE)+100
# #
# # for (i in c(1:ncol(asdf))){
# #   hist(asdf1[,i], main = as.character(asdfVAR2[1,i]), xlab = 'Precipitación (mm)')
# # }
# #
#
# par (mar=c(22, 4, 2, 2)+0.1)
# grid
# boxplot(asdf[,c(1:(ncol(asdf)/2))], las = 2, ylim=c(0, asdf.max))
# abline(h=seq(1000, asdf.max+100, 100), lty = 3)
# boxplot(asdf[,c((ncol(asdf)/2):ncol(asdf))], las = 2, ylim=c(0, asdf.max))
# abline(h=1000)
# # boxplot(asdf[,c(17:32)], xlas = 2)
# # boxplot(asdf[,c(33:48)], las = 2)
# # boxplot(asdf[,c(49:64)], las = 2)
# # boxplot(asdf[,c(65:ncol(asdf))], las = 2)
#
#
# # apply(asdfVAR$`25%`, margin, ...)
# #
# # apply(asdfVAR, MARGIN=1, FUN = if (asdfVAR$`75%` < asdfVAR$max) {asdfVAR$revisa='maximo'})
#
#
# # if ((asdfVAR$`25%`- 1.5*asdfVAR$iqr)<=asdfVAR$min){
# #   asdfVAR$revisa = 'minimo'
# # }
#
#
#
# # nombre <- type.convert(as.data.frame(c('Litueche', 'Cocalan',
# #                                        'Rio Cachapoal En Puente Arqueado (Ca)', 'Pichidegua', 'Pichilemu',
# #                                        'Nilahue Barahona', 'Paniahue', 'Laguna De Torca', 'Convento Viejo',
# #                                        'La Candelaria', 'El Membrillo', 'Ranguili', 'Santa Susana', 'La Palma',
# #                                        'Curico', 'Rio Mataquito En Licanten', 'Lontue', 'Villa Prat',
# #                                        'Potrero Grande', 'Putu', 'Gualleco', 'El Guindo',
# #                                        'Rio Palos En Junta Con Colorado', 'San Rafael', 'Agua Fria', 'Constitucion',
# #                                        'Pencahue', 'Rio Maule En Forel', 'Fundo El Radal', 'Talca U.C.',
# #                                        'Rio Claro En Rauquen', 'Huapi', 'El Durazno', 'Nirivilo', 'Vilches Alto',
# #                                        'San Javier', 'Rio Loncomilla En Las Brisas', 'Colbun (Maule Sur)',
# #                                        'Colorado', 'Huerta Del Maule', 'Rio Claro En San Carlos', 'Armerillo',
# #                                        'Rio Maule En Armerillo', 'La Estrella', 'Melozal', 'Linares', 'Rio Melado En La Lancha Dga',
# #                                        'Hornillo', 'Tutuven Embalse', 'Rio Ancoa En El Morro', 'Ancoa Embalse',
# #                                        'Liguay', 'Los Huinganes En Curipeumo', 'Quella', 'Juan Amigo', 'La Sexta De Longavi',
# #                                        'El Alamo', 'Parral', 'Rio Longavi En La Quiriquina', 'Mangarral', 'Digua Embalse',
# #                                        'Bullileo Embalse', 'Embalse Bullileo (Lago)', 'Millauquen', 'San Manuel En Perquilauquen',
# #                                        'Rio Perquilauquen En San Manuel', 'San Agustin De Puual', 'Rio Itata En Coelemu',
# #                                        'Coelemu', 'Portezuelo', 'Canal De La Luz En Chillan', 'General Freire Curico Ad.',
# #                                        "Bernardo O'Higgins Chillan Ad.")))
# #
#
#
# #
# #
# # View(asdf)
# #
# #
# #
# # gplots::boxplot2(asdf[,c(1:27)], las = 2)
# #
# #
# # gplots::boxplot2(asdf[,c(1:16)], las = 2)
# # gplots::boxplot2(asdf[,c(17:32)], las = 2)
# # gplots::boxplot2(asdf[,c(33:48)], las = 2)
# # gplots::boxplot2(asdf[,c(49:64)], las = 2)
# # gplots::boxplot2(asdf[,c(65:ncol(asdf))], las = 2)
# #
# #
# #
# #
# # hist(asdf[,1], xlab = as.character(asdfVAR$nombre[1]), main =  as.character(asdfVAR$nombre[1]))
# # hist(asdf[,2])
# #
# #
# #
# # ##### pruebas en general #####
# #
# # # if (asdfVAR$max >= (asdfVAR$`75%`+ asdfVAR$iqr*1.5) ){
# # #   asdfVAR$revisa = 'revisar'
# # # }
# # #
# # #
# # # Si max = 99% cuantil <- Revisar
# #
# #
# # # aa <- filter(asdfVAR, !nodata_num >239)
# #
# # # View(asdfVAR[, c(1,373:ncol(asdfVAR))])
# # # View(aa[, c(1,374:ncol(aa))])
# #
# #
# #
# #
# #
# #
# # asdfVAR2 <- (filter(asdfVAR, asdfVAR$nombre %in% nombre))
# # View(asdfVAR2)
# # dim(asdfVAR2)
# # length(nombre)
# #
# # asdf <- as.data.frame(t(asdfVAR[, c(2:373)]))
# # colnames(asdf) <- asdfVAR$nombre
# # View(asdf)
# #
# #
# # #### escritura de datos ####
# # write.table(asdfVAR, 'D:/asdf2.csv', sep=';')
# #
# #
# #
# # #subset(D1, V1 %in% c('B','N',T'))
# #
# #
# #
# #
# #
# #
# # # View(asdfVAR)
# # #
# # # bb <- apply(t(aa[, rango]), MARGIN = margen, FUN = racha)
# # # View(bb)
# # # na.contiguous(aa[, rango])
# #
# #
# #
# #
# #
# # #aa <- t(apply(df[, c(16:ncol(df))], MARGIN = margen, FUN = cuantil))
# #
# #
# # #outliers::outlier(asdfVAR, opposite = FALSE)
# # #View(aa)
# # # for (i in c(1:nrow(asdfVAR))){
# # #   print(asdfVAR[i,])
# # # }
# # #
# # # asdfVAR <- asdfVAR[!complete.cases(asdfVAR), ]
# # #
# # # View(asdfVAR)
# # # View(df)
# # #
# # #
# # # aa <- asdfVAR[is.na(asdfVAR)==TRUE]
# # #
# # # fullrecords <-  collecteddata[!complete.cases(collecteddata)]
# # # droprecords <-  collecteddata[complete.cases(collecteddata)]
# # #
# # #
# # # # asdfVAR %>% drop_na()
# # # #
# # # # View(asdfVAR)
# # # #
# # # # df[, c(16:ncol(df)) < 0.0] <- NA
# # # #
# # # #
# # # #
# # # # str(df[, c((-100 + ncol(df)):ncol(df))])
# # # #
# # # #
# # # # df[, c(16:ncol(df))] <- sapply(df[, c(16:ncol(df))], as.numeric)
# # # #
# # # #
# # #
# #
# #
# #
# #
# # df[, c(16:ncol(df))] <- sapply(df[, c(16:ncol(df))], as.numeric)
# #
# # df[, c(16:ncol(df)) < 0.0] <- NA
# #
# #
# #
# # min(df[, c(16:ncol(df))], na.rm = NA)
# #
# #
# #
# #
# # str(df)
# # # df <- type.convert(df)
# # # df[, c(16:ncol(df))] %>%  mutate_if(is.factor,as.numeric)
# #
# # data60 <- df[,c(1:15,780:ncol(df))]
# # data80 <- df[,c(1:15,(ncol(df)-100):ncol(df))]
# #
# # str(data80)
# #
# #
# # View(df)
# #
# # dim(df)
# #
# # df[, c(16:ncol(df)) < 0] <- NA
# # data80[, c(16:ncol(data80)) < 0] <- NA
# #
# # # primero
# # # df[df==""]<-NA
# #
# # bb <- summary(df)
# # View(bb)
# #
# # write.table(x = df, file = 'D:/asdf03.csv', sep = ';')
# # write.table(x = data80, file = 'D:/asdf80.csv', sep = ';')
# #
# # # dim(df)
# # # View(df)
# #
# # margen = 1
# # aa <- apply(df[, c(16:ncol(df))], MARGIN = margen, FUN = promedio)
# # bb <- apply(df[, c(16:ncol(df))], MARGIN = margen, FUN = maximo)
# # cc <- apply(df[, c(16:ncol(df))], MARGIN = margen, FUN = minimo)
# # dd <- apply(df[, c(16:ncol(df))], MARGIN = margen, FUN = desviacion)
# # ee <- apply(df[, c(16:1455)], MARGIN = margen, FUN = cuantil)
# # ff <- apply(df[, c(780:1455)], MARGIN = margen, FUN = sumario)
# #
# # View(ff)
# #
# # aa <-unlist(lapply(df[, c(16:1455)], maximo))
# #
# # rbind(df, ff)
# #
# # margen = 2
# # apply(df[, c(16:1455)], MARGIN = margen, FUN = cuantil)
# #
# # View(bb)
# # View(cc[,c((1355-16):(1455-16))])
# #
# #
# #
# # df[, c(16:1455)] > maximo
# # df[, c(16:1455)] %>% minimo
# #
# #
#
# # bb <- sapply(df[, c(16:1455)], min)
# # View(bb)
# # mean(df[,c(1455:1455)],na.rm = TRUE)
# #
# # # View(df)
# # df$latitud<-as.numeric(df$latitud)
# # # mean(df)
# # # View(df[,1])
# #
# # sapply(df[, as.numeric(c(5, 6, 7, 8, 16:1455))], as.numeric)
# #
# # df[, (c(5, 6, 7, 8, 16:1455))] <- df[, as.numeric(c(5, 6, 7, 8, 16:1455))]
# #
# # as.numeric(df[, 5])
# #
# #
# #
# #
# #
# # # length(df[c(1:99),])
# # # df$V1[1:1000]
# # #
# # # View(df)
# # #
# # #
# # #
# # #
# # # View(df)
# # #
# #
# # length(df$nombre[,])


# FUN <- function(x, negate = FALSE, na.rm = FALSE) {
#   rles <- rle(x > 0)
#   if(negate) {
#     max(rles$lengths[!rles$values], na.rm = na.rm)
#   } else {
#     max(rles$lengths[rles$values], na.rm = na.rm)
#   }
# }
