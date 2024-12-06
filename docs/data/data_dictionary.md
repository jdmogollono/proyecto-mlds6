# Diccionario de Datos

## Base de datos 1: data.csv
**Descripción:** Datos históricos recopilados de estaciones meteorológicas del IDEAM, incluyendo variables relacionadas con precipitaciones y condiciones meteorológicas entre 2000 y 2023.

| Variable         | Descripción                                   | Tipo de dato     | Rango/Valores posibles       | Fuente de datos       |
|-------------------|-----------------------------------------------|------------------|------------------------------|-----------------------|
| CodigoEstacion    | Código único de la estación meteorológica.   | int64           | Valores enteros únicos       | IDEAM                |
| Fecha             | Fecha de la medición.                       | datetime64[ns]  | 2000-01-01 a 2023-12-31      | IDEAM                |
| HR_CAL_MN_D       | Humedad relativa mínima diaria.             | float64         | 0 a 100 (%)                  | IDEAM                |
| HR_CAL_MX_D       | Humedad relativa máxima diaria.             | float64         | 0 a 100 (%)                  | IDEAM                |
| NV_MEDIA_D        | Nivel medio del agua.                       | float64         | Valores reales positivos     | IDEAM                |
| NV_MN_D           | Nivel mínimo del agua diario.               | float64         | Valores reales positivos     | IDEAM                |
| NV_MX_D           | Nivel máximo del agua diario.               | float64         | Valores reales positivos     | IDEAM                |
| PTPM_CON          | Precipitación acumulada diaria.             | float64         | 0 a valores reales positivos | IDEAM                |
| TMN_CON           | Temperatura mínima diaria.                  | float64         | Valores reales negativos y positivos | IDEAM       |
| TMX_CON           | Temperatura máxima diaria.                  | float64         | Valores reales negativos y positivos | IDEAM       |

## Base de datos 2 data_promedios.csv
**Descripción:** Datos preprocesados con promedios temporales de 1, 3, 7, 15 y 30 días previos de variables meteorológicas para modelado predictivo.

| Variable           | Descripción                                      | Tipo de dato     | Rango/Valores posibles       | Fuente de datos       |
|---------------------|--------------------------------------------------|------------------|------------------------------|-----------------------|
| CodigoEstacion      | Código único de la estación meteorológica.       | int64           | Valores enteros únicos       | IDEAM                |
| Fecha               | Fecha de la medición.                           | datetime64[ns]  | 2000-01-01 a 2023-12-31      | IDEAM                |
| PTPM_CON            | Precipitación acumulada diaria.                 | float64         | 0 a valores reales positivos | IDEAM                |
| PTPM_CON_1D         | Precipitación acumulada del día anterior.       | float64         | 0 a valores reales positivos | IDEAM                |
| HR_CAL_MN_D_1D      | Humedad relativa mínima del día anterior.       | float64         | 0 a 100 (%)                  | IDEAM                |
| HR_CAL_MX_D_1D      | Humedad relativa máxima del día anterior.       | float64         | 0 a 100 (%)                  | IDEAM                |
| NV_MEDIA_D_1D       | Nivel medio del agua del día anterior.          | float64         | Valores reales positivos     | IDEAM                |
| NV_MN_D_1D          | Nivel mínimo del agua del día anterior.         | float64         | Valores reales positivos     | IDEAM                |
| NV_MX_D_1D          | Nivel máximo del agua del día anterior.         | float64         | Valores reales positivos     | IDEAM                |
| TMN_CON_1D          | Temperatura mínima del día anterior.            | float64         | Valores reales negativos y positivos | IDEAM       |
| TMX_CON_1D          | Temperatura máxima del día anterior.            | float64         | Valores reales negativos y positivos | IDEAM       |
| PTPM_CON_3D         | Precipitación acumulada de los últimos 3 días.  | float64         | 0 a valores reales positivos | IDEAM                |
| HR_CAL_MN_D_3D      | Humedad relativa mínima en 3 días.              | float64         | 0 a 100 (%)                  | IDEAM                |
| HR_CAL_MX_D_3D      | Humedad relativa máxima en 3 días.              | float64         | 0 a 100 (%)                  | IDEAM                |
| ...                 | ...                                              | ...              | ...                          | ...                  |

**Nota:** Se incluyen otras variables acumuladas en ventanas de tiempo de 7, 15 y 30 días siguiendo una estructura similar, enfocadas en precipitaciones, humedad relativa, nivel del agua y temperatura mínima y máxima.
