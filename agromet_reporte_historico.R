# SCRIPT RAN AGROMETEOROLOGICA (http//www.agromet.cl) ####

# LIMPIA EL AREA DE TRABAJO ####
rm(list=ls())
library(tidyverse)

# MIDE EL TIEMPO QUE DEMORA EN EJECUTAR
#start.time <- Sys.time()

# FUNCIONES ####
fechas1 <- function (x, y) {
    x <- as.data.frame(x)
    z <- x
    x <- data.frame( do.call( rbind, strsplit( as.character( x[,1] ),
                                               split = '[[:space:]]') ) )
    x[, 1] <- as.Date( as.character( x[, 1] ), format = y )
    x <- cbind(x,z)
    colnames(x) <- c( 'fecha', 'hora', 'fecha-hora' )
    return(x)
}

fechas2 <- function (x, y) {
    x <- as.data.frame(x)
    x <- data.frame( do.call( rbind, strsplit( as.character( x[,1] ),
                                               split = '[[:space:]]') ) )
    x[, 1] <- as.Date( as.character( x[, 1] ), format = y )
    colnames(x) <- c( 'fecha', 'hora')
    return(x)
}

# read.url <- function(url, ...){
#     tmpFile <- tempfile()
#     download.file(url, destfile = tmpFile, method = "curl")
#     url.data <- fread(tmpFile, ...)
#     return(url.data)
# }

# DIRECTORIOS ####
dirOUT <- 'E:/AGROMET/descargas/'
dirENT <- 'D:/Downloads/agromet/'#'D:/WORK/GIT/bases_datos/agromet_base_datos/'
setwd(dirOUT)


aa <- list.files(path = dirENT, all.files = FALSE, pattern = '*.csv')
split(x=aa,sep = '-')


# ESTACIONES AGROMET FUENTE IDE ####
emas <- as.data.frame(read.csv2(paste0(dirENT,'listado_emas.csv'), sep = ';'))

# PERIODO DESCARGA DATOS ####
yearI <- 2009 ; yearF <- 2020

# PERIODO CADA 15 MIN EN BASE A FECHAS ####
fecha <- fechas1(substr(as.character(seq( ISOdate(yearI,1,1,0,0),
                                          ISOdate(yearF,12,31,23,0), "15 min")),
                        1, 16), '%Y-%m-%d')

# VECTOR DE FECHA, HORA, AÑO, MES, DIA ; TABLAS DINAMICAS ESTACIONES ####
fecha1 <- data.frame( do.call( rbind, strsplit( as.character( fecha[,1] ),
                                                split = '[[:punct:]]' )))

# union de fechas
fecha <- cbind(fecha,fecha1)
colnames(fecha) <- c( 'fecha', 'hora', 'fecha-hora', 'año', 'mes', 'dia')

# DATA.FRAME VACIO, RELLENA AÑOS O FALLAS DESCARGAS
vacio <- data.frame(matrix(ncol = 20, nrow = 0))

asdf <- data.frame(matrix(ncol = 1, nrow = 0))


for (estacion in (emas$estacion) ){
    # obtencion de datos anuales
    for ( year in c( yearI:yearF ) ) {
        url00 <- paste('https://www.agromet.cl/csv/agromet_', estacion, '-',
                       year, '0101000000-', year, '1231235900.csv', sep='')
        asdf <- data.frame(rbind(as.matrix(asdf), as.matrix(url00)))
        }
    }

write.csv2(asdf, 'urls_descarga-csv')



# CODIGO DESCARGA ####
for (estacion in (emas$estacion) ){
    # obtencion de datos anuales
    for ( year in c( yearI:yearF ) ) {
        url00 <- paste('https://www.agromet.cl/csv/agromet_', estacion, '-',
                       year, '0101000000-', year, '1231235900.csv', sep='')
        # lectura de url
        tryCatch(
            expr = {
                # Your code...
                # goes here...
                # ...
                d00 <- as.data.frame( read.csv2( (url00),
                                                 header=FALSE,
                                                 sep=',',
                                                 quote='""',
                                                 dec=',',
                                                 skip=0))
            },
            error = function(e){
                # (Optional)
                # Do this if an error is caught...
                print('error')
                d00 <- vacio
            },
            warning = function(w){
                # (Optional)
                # Do this if an warning is caught...
                print('warning')
                d00 <- as.data.frame( read.csv2( (url00),
                                                 header=FALSE,
                                                 sep=',',
                                                 quote='""',
                                                 dec=',',
                                                 skip=0))
            },
            finally = {
                # (Optional)
                # Do this at the end before quitting the tryCatch structure...
                d00 <- vacio
            }
        )
        # en caso de que sea el primer año y no tenga datos, est = vacio
        if (year==yearI){
            est <- vacio
        } else{
            est <- do.call( rbind, list(est, d00) )
            }
    }
    # cambiar el nombre de las columnas acorde a los datos
    colnames(est) <- c( 'Fecha Hora', 'Temp. promedio aire(°C)',
                        'Precipitación horaria (mm)', 'Humed. rel. promedio (%)',
                        'Presión atmosférica', 'Radiación solar máx.',
                        'Veloc. máx. viento', 'Temp. Mínima (°C)',
                        'Temp. Máxima (°C)', 'Dirección del viento',
                        'Temp. superficial (°C)', 'Grados día (base 10)',
                        'Horas frío (base 7)')
    # write.csv( est, file = paste0(dirOUT, estacion, '_ID', ".csv", sep="" ) )
    # if ( nrow(est) == 0 ) {
    # } else {
    #     # REEMPLAZA CARACTERES PARA DEJAR FORMATO DE FECHA SEPARADO POR "-"
    #     est[,1] <- gsub( '/', '-', as.character( estacion[, 1] ) )
    #     # DA FORMATO DE FECHA A DATOS DESCARGADOS  #Y GENERA COLUMNAS DE dia mes a?o
    #     hora1 <- fechas2( est[,1], '%d-%m-%Y')
    #     est <- cbind( hora1, est )
    #     est <- merge( est, fecha, by = c(1,2), all.y = TRUE )
    #     # REORDENA COLUMNAS PARA AUMENTAR LEGIBILIDAD DEL ARCHIVO DE SALIDA
    #     est <- est[, c(14:ncol(estacion),1:2,4:13)]
    #     est <- est[ do.call(order, as.list(estacion)), ]
    # }
    # # GUARDA ESTACIONES EN CSV ####
    # write.csv( estacion[, c(1,2,3,4:ncol(estacion)) ],
    #            file = paste(dirOUT, "/2015_", i, '_ID', noms$ID[i], "_",
    #                         noms$noms[i], ".csv", sep="" ) )
}













#
#
#
#
#
#
#
#
#
#
# # CODIGO DESCARGA ####
# for (estacion in (emas$estacion) ){
#     # ITERACION ANUAL
#     #
#     for ( year in c( yearI:yearF ) ) {
#         url00 <- paste('https://www.agromet.cl/csv/agromet_', estacion, '-',
#                        year, '0101000000-', year, '1231235900.csv', sep='')
#         if (nrow(read.csv2(url00, header=FALSE)) <= 2){
#             d00  <- vacio
#             print(paste0(as.character(year), ', no existe ', url00))
#         } else {
#                 d00 <- as.data.frame( read.csv2((url00),
#                                                  header=FALSE,
#                                                  sep=',', quote='""',
#                                                  dec=',', skip=0))
#         }
#         est <- do.call( rbind, list(est, d00) )
#     }
#     colnames(est) <- c( 'Fecha Hora', 'Temp. promedio aire(°C)',
#                         'Precipitación horaria (mm)', 'Humed. rel. promedio (%)',
#                         'Presión atmosférica', 'Radiación solar máx.',
#                         'Veloc. máx. viento', 'Temp. Mínima (°C)',
#                         'Temp. Máxima (°C)', 'Dirección del viento',
#                         'Temp. superficial (°C)', 'Grados día (base 10)',
#                         'Horas frío (base 7)')
#     if ( nrow(est) == 0 ) {
#     } else {
#         # REEMPLAZA CARACTERES PARA DEJAR FORMATO DE FECHA SEPARADO POR "-"
#         est[,1] <- gsub( '/', '-', as.character( estacion[, 1] ) )
#         # DA FORMATO DE FECHA A DATOS DESCARGADOS  #Y GENERA COLUMNAS DE dia mes a?o
#         hora1 <- fechas2( est[,1], '%d-%m-%Y')
#         est <- cbind( hora1, est )
#         est <- merge( est, fecha, by = c(1,2), all.y = TRUE )
#         # REORDENA COLUMNAS PARA AUMENTAR LEGIBILIDAD DEL ARCHIVO DE SALIDA
#         est <- est[, c(14:ncol(estacion),1:2,4:13)]
#         est <- est[ do.call(order, as.list(estacion)), ]
#     }
#     # GUARDA ESTACIONES EN CSV ####
#     write.csv( estacion[, c(1,2,3,4:ncol(estacion)) ],
#                file = paste(dirOUT, "/2015_", i, '_ID', noms$ID[i], "_",
#                             noms$noms[i], ".csv", sep="" ) )
# }
#
#
#
#
#
#         # LEE URLs COMO DATAFRAMES
#
#
#     # UNE DATOS DESCARGADOS
#     # d00, d01, d02, d03, d04, d05, d06, d07, d08, d09,
#     est <- do.call( rbind, list(d10, d11, d12, d13, d14, d15, d16, d17, d18, d19) )
#     rm(d00, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15, d16, d17, d18, d19, d20)
#     ###UNE A?OS DE DATOS DESCARGADOS A NIVEL DE ESTACION, RESPETANDO A?O DE INICIO
#     # if ( year == yearI ) { estacion <- est } else { estacion <- rbind( estacion, est ) } }
#
#     ##NOMBRES POR DEFECTO COLUMNAS SEGUN SITIO (CHEQUEAR, SI SE MANTIENE EN EL TIEMPO)
#     colnames(estacion) <- c( 'Fecha Hora', 'Temp. promedio aire(?C)',
#                              'Precipitacion horaria(mm)',
#                              'Humed. rel. promedio(%)',
#                              'Presi?n atmosferica(mbar)',
#                              'Radiacion solar max.(W/m?)',
#                              'Veloc. m?x. viento(m/s)', 'Temp. Minima(°C)',
#                              'Temp. Maxima(°C)', 'Direccion del viento(°)',
#                              'Temp. superficial(°C)' )
#     #aa <- estacion
#     #estacion <- aaaa
#
#     if ( nrow(estacion) == 0 ) {
#
#     } else {
#         #REEMPLAZA CARACTERES PARA DEJAR FORMATO DE FECHA SEPARADO POR "-"
#         estacion[,1] <- gsub( '/', '-', as.character( estacion[, 1] ) )
#
#         ###DA FORMATO DE FECHA A DATOS DESCARGADOS  #Y GENERA COLUMNAS DE dia mes a?o
#         hora1 <- fechas2( estacion[,1], '%d-%m-%Y')
#         #hora2 <- data.frame( do.call( rbind, strsplit( as.character( hora1[,1] ), split = '[[:punct:]]' )))
#         #hora <- cbind( hora1, hora2 ) ; colnames(hora) <- c( 'fecha', 'hora', 'dia', 'mes', 'a?o' )
#         estacion <- cbind( hora1, estacion )
#
#         estacion <- merge( estacion, fecha, by = c(1,2), all.y = TRUE )
#
#         ##REORDENA COLUMNAS PARA AUMENTAR LEGIBILIDAD DEL ARCHIVO DE SALIDA
#         estacion <- estacion[, c(14:ncol(estacion),1:2,4:13)]
#         #bestacion <- estacion[, c(14:ncol(estacion),1:2,4:13)]
#
#         #df<-df[ do.call(order, as.list(df)), ]
#         estacion<-estacion[ do.call(order, as.list(estacion)), ]
#     }
#
#     ##GENERA CARPETA POR REGION CON ESTACIONES SEGUN SE ESTIME NECESARIO / FUNCIONA EN WIN Y LINUX
#     ##DE MOMENTO PREFERIR LA OPCION YA ACTIVADA POR DEFECTO
#     #dir.create(paste(dirOUT,'/',noms$REGION[i],sep=""), showWarnings = F, recursive = FALSE, mode = "0777")
#
#
#
#     ##INDICADOR AVANCE DESCARGA n DE ESTACION
#     print (i)
# }
# ###CODIGO DESCARGA/ORDEN FIN
#
# ###MIDE EL TIEMPO QUE DEMORA EN EJECUTAR
# #end.time <- Sys.time()
# #time.taken <- end.time - start.time
# #time.taken
#
#
#
# for (estacion in (emas$estacion[1:10]) ){
#     for ( year in c( yearI:yearF ) ) {
#         url00 <- paste('https://www.agromet.cl/csv/agromet_', estacion, '-',
#                        year, '0101000000-', year, '1231235900.csv', sep='')
#         # download.file(url00, paste0(estacion, year,'.csv'),
#         #               method = 'libcurl', quiet=FALSE)
#
#         #if (RCurl::getURIAsynchronous(url00)==""){
#         if(RCurl::getURL(url00)){
#             print(paste0(estacion, ', ', year, ''))
#         } else{
#             print(paste0(estacion, ', ', year, ', existe'))
#         }
#     }
# }
#
# if (RCurl::url.exists(url00)==FALSE){
#     # nrow(read.csv2( url(url00), header=FALSE)) <= 2) {
#     d00  <- vacio
#     print(paste0(as.character(year), ', no existe ', url00))
# } else {
#     d00 <- as.data.frame( read.csv2( (url00),
#                                      header=FALSE,
#                                      sep=',', quote='""',
#                                      dec=',', skip=0))
# }
#
#
#
# readUrl <- function(url) {
#     out <- tryCatch(
#
#         ########################################################
#         # Try part: define the expression(s) you want to "try" #
#         ########################################################
#
#         {
#             # Just to highlight:
#             # If you want to use more than one R expression in the "try part"
#             # then you'll have to use curly brackets.
#             # Otherwise, just write the single expression you want to try and
#
#             message("This is the 'try' part")
#             readLines(con = url, warn = FALSE)
#         },
#
#         ########################################################################
#         # Condition handler part: define how you want conditions to be handled #
#         ########################################################################
#
#         # Handler when a warning occurs:
#         warning = function(cond) {
#             message(paste("Reading the URL caused a warning:", url))
#             message("Here's the original warning message:")
#             message(cond)
#
#             # Choose a return value when such a type of condition occurs
#             return(NULL)
#         },
#
#         # Handler when an error occurs:
#         error = function(cond) {
#             message(paste("This seems to be an invalid URL:", url))
#             message("Here's the original error message:")
#             message(cond)
#
#             # Choose a return value when such a type of condition occurs
#             return(NA)
#         },
#
#         ###############################################
#         # Final part: define what should happen AFTER #
#         # everything has been tried and/or handled    #
#         ###############################################
#
#         finally = {
#             message(paste("Processed URL:", url))
#             message("Some message at the end\n")
#         }
#     )
#     return(out)
# }
#
#
#
# tryCatch(
#     expr = {
#         # Your code...
#         # goes here...
#         # ...
#         d00 <- as.data.frame( read.csv2( url(url00),
#                                          header=FALSE,
#                                          sep=',',
#                                          quote='""',
#                                          dec=',',
#                                          skip=0))
#     },
#     error = function(e){
#         # (Optional)
#         # Do this if an error is caught...
#         d00 <- vacio
#     },
#     warning = function(w){
#         # (Optional)
#         # Do this if an warning is caught...
#         d00 <- vacio
#     },
#     finally = {
#         # (Optional)
#         # Do this at the end before quitting the tryCatch structure...
#     }
# )
#
#
#
#
# # CODIGO DESCARGA ####
# for (estacion in (emas$estacion) ){
#     # ITERACION ANUAL
#     #
#     for ( year in c( yearI:yearF ) ) {
#         url00 <- paste('https://www.agromet.cl/csv/agromet_', estacion, '-',
#                        year, '0101000000-', year, '1231235900.csv', sep='')
#         tryCatch(
#             expr = {
#                 # Your code...
#                 # goes here...
#                 # ...
#                 d00 <- as.data.frame( read.csv2( url(url00),
#                                                  header=FALSE,
#                                                  sep=',',
#                                                  quote='""',
#                                                  dec=',',
#                                                  skip=0))
#             },
#             error = function(e){
#                 # (Optional)
#                 # Do this if an error is caught...
#                 d00 <- vacio
#             },
#             warning = function(w){
#                 # (Optional)
#                 # Do this if an warning is caught...
#                 d00 <- vacio
#             },
#             finally = {
#                 # (Optional)
#                 # Do this at the end before quitting the tryCatch structure...
#             }
#         )
#         est <- do.call( rbind, list(est, d00) )
#     }
#     colnames(est) <- c( 'Fecha Hora', 'Temp. promedio aire(°C)',
#                         'Precipitación horaria (mm)', 'Humed. rel. promedio (%)',
#                         'Presión atmosférica', 'Radiación solar máx.',
#                         'Veloc. máx. viento', 'Temp. Mínima (°C)',
#                         'Temp. Máxima (°C)', 'Dirección del viento',
#                         'Temp. superficial (°C)', 'Grados día (base 10)',
#                         'Horas frío (base 7)')
#     if ( nrow(est) == 0 ) {
#     } else {
#         # REEMPLAZA CARACTERES PARA DEJAR FORMATO DE FECHA SEPARADO POR "-"
#         est[,1] <- gsub( '/', '-', as.character( estacion[, 1] ) )
#         # DA FORMATO DE FECHA A DATOS DESCARGADOS  #Y GENERA COLUMNAS DE dia mes a?o
#         hora1 <- fechas2( est[,1], '%d-%m-%Y')
#         est <- cbind( hora1, est )
#         est <- merge( est, fecha, by = c(1,2), all.y = TRUE )
#         # REORDENA COLUMNAS PARA AUMENTAR LEGIBILIDAD DEL ARCHIVO DE SALIDA
#         est <- est[, c(14:ncol(estacion),1:2,4:13)]
#         est <- est[ do.call(order, as.list(estacion)), ]
#     }
#     # GUARDA ESTACIONES EN CSV ####
#     write.csv( estacion[, c(1,2,3,4:ncol(estacion)) ],
#                file = paste(dirOUT, "/2015_", i, '_ID', noms$ID[i], "_",
#                             noms$noms[i], ".csv", sep="" ) )
# }
#
#
#
