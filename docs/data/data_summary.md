# Reporte de Datos

Este documento contiene los resultados del análisis exploratorio de datos.

## Resumen general de los datos

En esta sección se presenta un resumen general de los datos. Se describe el número total de observaciones, variables, el tipo de variables, la presencia de valores faltantes y la distribución de las variables.

Número de documentos en el dataset: 13'417.098

| Columna         | Tipo de Dato         |
|------------------|----------------------|
| CodigoEstacion  | int64                |
| Fecha           | datetime64[ns]       |
| HR_CAL_MN_D     | float64              |
| HR_CAL_MX_D     | float64              |
| NV_MEDIA_D      | float64              |
| NV_MN_D         | float64              |
| NV_MX_D         | float64              |
| PTPM_CON        | float64              |
| TMN_CON         | float64              |
| TMX_CON         | float64              |
| DOY             | int32                |
| WOY             | int64                |
| MOY             | int32                |

Tamaño del dataset: 594.41 MB

## Resumen de calidad de los datos

En esta sección se presenta un resumen de la calidad de los datos. Se describe la cantidad y porcentaje de valores faltantes, valores extremos, errores y duplicados. También se muestran las acciones tomadas para abordar estos problemas.

Las columnas CodigoEstacion, Fecha, PTPM_CON, DOY, WOY, MOY son las unicas columnas sin datos faltantes en el dataset

No existe ninguna mezcla de formatos en las respectivas columnas.

Datos faltantes en porcentaje:
| Columna         | Porcentaje de Datos Faltantes |
|------------------|-------------------------------|
| CodigoEstacion  | 0.000000%                     |
| Fecha           | 0.000000%                     |
| HR_CAL_MN_D     | 83.005543%                    |
| HR_CAL_MX_D     | 83.005528%                    |
| NV_MEDIA_D      | 97.789112%                    |
| NV_MN_D         | 99.364773%                    |
| NV_MX_D         | 99.364773%                    |
| PTPM_CON        | 0.000000%                     |
| TMN_CON         | 81.074753%                    |
| TMX_CON         | 82.036779%                    |
| DOY             | 0.000000%                     |
| WOY             | 0.000000%                     |
| MOY             | 0.000000%                     |

| Columna         | Cantidad de Datos Faltantes |
|------------------|-----------------------------|
| CodigoEstacion  | 0                           |
| Fecha           | 0                           |
| HR_CAL_MN_D     | 11,136,935                  |
| HR_CAL_MX_D     | 11,136,933                  |
| NV_MEDIA_D      | 13,120,461                  |
| NV_MN_D         | 13,331,869                  |
| NV_MX_D         | 13,331,869                  |
| PTPM_CON        | 0                           |
| TMN_CON         | 10,877,879                  |
| TMX_CON         | 11,006,955                  |
| DOY             | 0                           |
| WOY             | 0                           |
| MOY             | 0                           |


## Variable objetivo

En esta sección se describe la variable objetivo. Se muestra la distribución de la variable y se presentan gráficos que permiten entender mejor su comportamiento.

PTPM_CON= Precipitacion acumulada diaria

![Distribución de la variable PTPM_CON](/docs/data/images/PTPM_CON_Distribucion.png)

Esta distribución sería esperable en datos meteorológicos. La mayoría de los días tienen poca o ninguna precipitación, y solo unos pocos tienen precipitaciones muy altas (tormentas, etc.).

La distribución de la columna PTPM_CON parece estar sesgada hacia valores bajos o ceros, ya que la mediana y el percentil 25% son cero.
La desviación estándar indica que, aunque muchos valores son bajos, hay una dispersión considerable en los valores.
La presencia de un máximo bastante alto sugiere que puede haber algunos valores extremos o atípicos que podrían necesitar más investigación.


## Variables individuales

En esta sección se presenta un análisis detallado de cada variable individual. Se muestran estadísticas descriptivas, gráficos de distribución y de relación con la variable objetivo (si aplica). Además, se describen posibles transformaciones que se pueden aplicar a la variable.

| Variable       | Etiqueta                             |
|----------------|--------------------------------------|
| HR_CAL_MN_D    | Humedad relativa mínima diaria       |
| HR_CAL_MX_D    | Humedad relativa máxima diaria       |
| NV_MEDIA_D     | Nivel medio del agua diario          |
| NV_MN_D        | Nivel mínimo del agua diario         |
| NV_MX_D        | Nivel máximo del agua diario         |
| TMN_CON        | Temperatura mínima diaria            |
| TMX_CON        | Temperatura máxima diaria            |

Distribuciones variables:

![Distribución de la variable HR_CAL_MN_D](/docs/data/images/Dis_HR_CAL_MN_D.png)
![Distribución de la variable HR_CAL_MX_D](/docs/data/images/Dis_HR_CAL_MX_D.png)
![Distribución de la variable NV_MEDIA_D](/docs/data/images/Dis_NV_MEDIA_D.png)
![Distribución de la variable NV_MN_D](/docs/data/images/Dis_NV_MN_D.png)
![Distribución de la variable NV_MX_D](/docs/data/images/Dis_NV_MX_D.png)
![Distribución de la variable TMN_CON](/docs/data/images/Dis_TMX_CON.png)
![Distribución de la variable TMX_CON](/docs/data/images/Dis_TMN_CON.png)

Estadistica descriptiva
| Variable       | Count         | Mean        | Std         | Min        | 25%        | 50%        | 75%        | Max        |
|----------------|---------------|-------------|-------------|------------|------------|------------|------------|------------|
| HR_CAL_MN_D    | 2,280,163     | 66.57       | 14.21       | -39.00     | 57.00      | 67.00      | 77.00      | 113.00     |
| HR_CAL_MX_D    | 2,280,165     | 91.49       | 7.33        | 23.00      | 89.00      | 93.00      | 97.00      | 239.00     |
| NV_MEDIA_D     | 296,637       | 479.38      | 315.65      | 0.00       | 203.00     | 438.00     | 697.00     | 2797.00    |
| NV_MN_D        | 85,229        | 495.07      | 337.90      | 0.00       | 200.00     | 449.50     | 725.50     | 1864.00    |
| NV_MX_D        | 85,229        | 512.07      | 336.27      | 0.00       | 226.50     | 474.00     | 737.00     | 1866.00    |
| TMN_CON        | 2,539,219     | 17.34       | 6.05        | -9.80      | 13.00      | 18.60      | 22.40      | 30.00      |
| TMX_CON        | 2,410,143     | 27.35       | 6.06        | 0.00       | 22.80      | 28.60      | 32.20      | 44.00      |



## Relación entre variables explicativas y variable objetivo

En esta sección se presenta un ranking de las variables más importantes para predecir la variable objetivo. Se utilizan técnicas como la correlación,  o la importancia de las variables en un modelo de aprendizaje automático.

Correlaciones: 
| Variable       | Correlación Máxima | Correlación Mínima | Correlación Promedio |
|----------------|--------------------|--------------------|-----------------------|
| HR_CAL_MN_D    | 0.404781           | -0.023732          | 0.172999             |
| NV_MX_D        | 0.394250           | -0.000688          | 0.148298             |
| HR_CAL_MX_D    | 0.396269           | -0.018289          | 0.140107             |
| NV_MN_D        | 0.278228           | -0.002044          | 0.132138             |
| NV_MEDIA_D     | 0.307581           | -0.000404          | 0.119564             |
| TMN_CON        | 0.263418           | -0.200379          | 0.054178             |
| MOY            | 0.223845           | -0.153680          | 0.053268             |
| WOY            | 0.226407           | -0.152244          | 0.053194             |
| DOY            | 0.225094           | -0.153102          | 0.052857             |
| TMX_CON        | 0.083413           | -0.412070          | -0.147917            |

El análisis de correlación entre la precipitación acumulada diaria (PTPM_CON) y las demás variables meteorológicas se llevó a cabo mediante una función que procesa los datos de cada estación de forma individual y calcula el promedio de la correlación para cada una de las variables meteorológicas, tomando en cuenta todas las estaciones. Para garantizar la calidad de los datos, se eliminaron las filas con valores nulos y se exigió un número mínimo de 1000 registros para calcular las correlaciones. Los resultados muestran que la humedad relativa mínima (HR_CAL_MN_D) tiene la correlación promedio más alta (0.173), seguida por el nivel del agua máximo (NV_MX_D) con 0.148 y la humedad relativa máxima (HR_CAL_MX_D) con 0.140. Por otro lado, la temperatura mostró una correlación negativa (-0.148), y las variables temporales (día, semana y mes del año) presentaron correlaciones muy bajas, alrededor de 0.05, lo que indica que su influencia sobre la precipitación es mínima. Se aplico la misma metodologia para el dataset de promedios y se obtuvieros resultados similares, sin embargo, este dataset nos permite tomar como variable de entrada el comportamiento de la precipitacion de los dias anteriores, lo cual puede influir en mejor rendimiento de los modelos que se prueben. Por ende, se decide tomar los datos promedios de dias anteriores de la variable precipitacion. A continuacion se muestran su matriz de correlación:

![Matriz correlacion](/docs/data/images/correlation_matrix.png)