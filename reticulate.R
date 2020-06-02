# no he logrado hacer funcionar

# importar libreria
library(reticulate)

# py_versions_windows()
# py_config()
# conda_binary("auto")
# setear ambiente.
if (FALSE){
  
  use_python('C:/Users/fneir/miniconda3/python.exe')
  use_miniconda(condaenv = 'py37')
  # py27 C:/Users/fneir/miniconda3/envs/py27/python.exe
  # py37 C:/Users/fneir/miniconda3/envs/py37/python.exe
}

np <- import("numpy")
pd <- import("pandas")
sns <- import("seaborn")
zipfile <- import("zipfile")


entrada_dir <- ('D:/WORK/GIT/bases_datos')
carpeta_ent <- '/cr2_bases_datos'
archivo_zip <- '/cr2_prAmon_2019.zip'
archivo_txt <- 'cr2_prAmon_2019/cr2_prAmon_2019.txt'

file_entrada <- (paste0(entrada_dir, carpeta_ent, archivo_zip))

zip_file <- zipfile$ZipFile(file_entrada)
py_to_r(zipfile)
# datos_variable = pd.read_csv(zip_file.open(archivo_txt))

dateparse <- py_( lambda x: pd.datetime.strptime(x, '%Y-%m') )

# lee los datos y transpone, dejando columnas como filas.
# esto solo para evitar eliminar informacion de metadata de cada estacion
dataVAR <- py_eval((pd$read_csv(filepath_or_buffer=zip_file$open(archivo_txt), sep=',', na_values=-9999, encoding = 'utf-8',dtype='unicode')))
read.csv(zip_file$open(archivo_txt), sep=',')
## todo el proceso anterior lee los datos como si fueran texto,
## para otros analisis es necesario transformar a numerico, como pasa con R.


# cambiando los nombres de las columnas por la fila 0
dataVAR.columns = dataVAR.iloc[0]

# eliminando la fila 0
dataVAR = dataVAR[1:-1]

dataVAR.latitud = pd.to_numeric(dataVAR.latitud)
dataVAR.longitud = pd.to_numeric(dataVAR.longitud)

dataVAR.iloc[0, 15:] = pd.to_numeric(dataVAR.iloc[0, 15:])

dataVAR.iloc

# coordenadas = dataVAR.loc[(dataVAR.latitud<=-34.04) & (dataVAR.latitud>-36.6) &
#                           (dataVAR.longitud>-73) & (dataVAR.longitud<=-71.0)]
coordenadas = dataVAR.loc[(dataVAR.latitud<=-17.0) & (dataVAR.latitud>-58.1) &
                            (dataVAR.longitud>-73.0) & (dataVAR.longitud<=-69.0)]

print(coordenadas.latitud.values, coordenadas.longitud.values)

# seleccionar datos dentro de un periodo de tiempo, acorde a la base
ini = '2019-01'
fin = '2019-12'

# https://pandas.pydata.org/docs/user_guide/merging.html
periodo = pd.concat([coordenadas.iloc[:,0:14], coordenadas.loc[:, ini:fin]], axis=1, join='inner')

# contador de cuantos datos validos posee la estación en dicho periodo
# se basa en que datos ya han sido filtrados por nan.
periodo['cuenta'] = (periodo.T).iloc[14:-2,:].count()

periodo = periodo.loc[periodo.cuenta>1]
#periodo = periodo.loc[periodo.cuenta>238]

## ambas funciones realizan lo mismo, una mascara de los valores nulos.
# pd.notna(periodo.iloc[:,14:])
# periodo.iloc[:,14:-1].isnull()

# generar heatmap de datos estacion
calormap = periodo.iloc[:,14:-1].T
calormap.columns = periodo.nombre

# ADDED: Extract axes.
fig, ax = plt.subplots(1, 1,
                       # figsize = (15, 15),
                       #dpi=300
)

# la razon porque mostraba solo valores 0-1, era porque estaba como texto.
heat_map = sb.heatmap(periodo.iloc[:,14:-1].astype(float),
                      #vmin=0,
                      #vmax=300,
                      #square=True,
                      mask = periodo.iloc[:,14:-1].isnull(),
                      cbar=True,
                      #center=0.5,
                      #cmap="magma_r",
                      cmap="coolwarm_r",
                      #cmap="binary",
                      #cmap="viridis",
                      yticklabels=periodo.nombre,
                      #annot=True
                      #linewidths=.005
)


# ADDED: Remove labels.
ax.set_ylabel('')
ax.set_xlabel('')