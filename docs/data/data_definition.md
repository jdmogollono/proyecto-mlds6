# Definición de los datos

## Origen de los datos

- **Fuente de los datos:** Los datos fueron recopilados del portal del IDEAM utilizando su servidor REST, específicamente de las estaciones meteorológicas incluidas en el CNE (Catálogo Nacional de Estaciones). La información incluye variables meteorológicas como precipitaciones, humedad relativa, nivel del agua y temperatura.
- **Forma de obtención:** Los datos se descargaron automáticamente utilizando el script `get_station_data`, que realiza solicitudes al servidor IDEAM para obtener archivos en formato CSV. Los archivos son procesados y almacenados localmente.

## Especificación de los scripts para la carga de datos

- **Script principal:** `1_business_data_load.ipynb`
  - Funciones destacadas:
    - `get_station_data`: Descarga y almacena los datos de las estaciones desde el servidor del IDEAM.
    - `procesar_estacion`: Procesa los datos de cada estación individualmente.
    - `procesar_estaciones_paralelo`: Ejecuta el procesamiento de múltiples estaciones en paralelo para optimizar tiempos.
    - `consolidar_csv`: Consolida múltiples archivos CSV en un único archivo de datos.
    - `download_cne`: Descarga el catálogo nacional de estaciones desde el portal del IDEAM.
  - Por otro lado, los scripts `*.py` se agregaron para poder importar y hacer uso de las funciones en forma modular. 

## Referencias a rutas o bases de datos origen y destino

### Rutas de origen de datos

- **Ubicación de los archivos de origen:**
  - Los datos descargados desde el servidor del IDEAM se almacenan en la carpeta: `<WORKSPACE>/data/variables/`.
  - Los metadatos del Catálogo Nacional de Estaciones se descargan en: `<WORKSPACE>/data/CNE_IDEAM.xls`.
  
- **Estructura de los archivos de origen:**
  - Los archivos de datos de las estaciones están en formato CSV y contienen columnas como:
    - `CodigoEstacion`: Identificador de la estación.
    - `Fecha`: Fecha de la medición.
    - Variables meteorológicas como `PTPM_CON`, `HR_CAL_MN_D`, `TMX_CON`, entre otras.
  
- **Procedimientos de transformación y limpieza de datos:**
  - Los datos de las estaciones se transforman para garantizar la coherencia temporal, creando series temporales completas para cada estación.
  - Se eliminan filas donde todas las variables son `NaN` para optimizar el procesamiento.
  - Los datos de múltiples estaciones se consolidan en un único archivo para su uso posterior.

### Base de datos de destino

- **Base de datos de destino:**
  - Los datos procesados y consolidados se almacenan como archivos CSV en la ruta de destino especificada por el usuario.
  - Ejemplo de ruta de salida: `<WORKSPACE>/data/procesados/`.

- **Estructura de la base de datos de destino:**
  - Cada archivo de salida es un CSV con las siguientes columnas principales:
    - `Fecha`: Fecha de las mediciones.
    - Variables meteorológicas consolidadas por estación.
    - Opcionalmente, una columna `CodigoEstacion` que identifica la estación en caso de consolidación.

- **Procedimientos de carga y transformación de datos en la base de datos de destino:**
  - Se realiza la consolidación de múltiples CSV individuales en un único archivo usando la función `consolidar_csv`.
  - Los datos consolidados se optimizan para ser utilizados directamente en el modelado predictivo utilizando técnicas de Deep Learning.
