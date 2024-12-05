import os
import pandas as pd
import numpy as np
import logging
import random
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Ajustar directorios de trabajo
WORKSPACE = '../../'
DATA_FOLDER = os.path.join(WORKSPACE, 'datos')
IMAGES_FOLDER = os.path.join('images')  # en scripts/eda/images

def add_time_features(df):
    """
    Agrega características temporales al DataFrame.
    """
    if not pd.api.types.is_datetime64_any_dtype(df['Fecha']):
        df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
    df['DOY'] = df['Fecha'].dt.dayofyear
    df['WOY'] = df['Fecha'].dt.isocalendar().week.astype(int)
    df['MOY'] = df['Fecha'].dt.month
    return df

def process_station_group(station, group, min_rows):
    """
    Procesa una estación individual y calcula la correlación entre PTPM_CON y el resto de variables numéricas.
    """
    exclude_cols = ['CodigoEstacion', 'Fecha']
    numeric_cols = group.select_dtypes(include=[np.number]).columns
    numeric_cols = numeric_cols[~numeric_cols.isin(exclude_cols)]

    if 'PTPM_CON' not in numeric_cols:
        return None, None

    correlations = {}
    for col in numeric_cols:
        if col != 'PTPM_CON':
            df_clean = group[['PTPM_CON', col]].dropna()
            if len(df_clean) >= min_rows:
                correlation_value = df_clean['PTPM_CON'].corr(df_clean[col])
                correlations[col] = correlation_value

    if len(correlations) == 0:
        return None, None

    return station, correlations

def process_all_stations(df, min_rows=1000):
    """
    Processes all stations sequentially (no multiprocessing).
    """
    grouped = df.groupby('CodigoEstacion')
    results = [
        process_station_group(station, group, min_rows) 
        for station, group in grouped
    ]
    return {station: corr for station, corr in results if station is not None}

def generate_summary_table(correlations):
    """
    Genera una tabla con max, min y promedio de correlación para cada variable.
    """
    summary_data = {
        'Variable': [],
        'Correlación Máxima': [],
        'Correlación Mínima': [],
        'Correlación Promedio': []
    }

    all_correlations = pd.DataFrame()
    for station, station_corrs in correlations.items():
        temp_df = pd.DataFrame(station_corrs, index=[station])
        all_correlations = pd.concat([all_correlations, temp_df])

    for col in all_correlations.columns:
        max_corr_value = all_correlations[col].max()
        min_corr_value = all_correlations[col].min()
        avg_corr_value = all_correlations[col].mean()
        summary_data['Variable'].append(col)
        summary_data['Correlación Máxima'].append(max_corr_value)
        summary_data['Correlación Mínima'].append(min_corr_value)
        summary_data['Correlación Promedio'].append(avg_corr_value)

    summary_df = pd.DataFrame(summary_data)
    return summary_df

def filtrar_outliers(df, columnas, limite_inferior=None, limite_superior=None):
    for col in columnas:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR if limite_inferior is None else max(limite_inferior, Q1 - 1.5 * IQR)
        upper_bound = Q3 + 1.5 * IQR if limite_superior is None else min(limite_superior, Q3 + 1.5 * IQR)
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound) | df[col].isna()]
    return df

def preprocessing():
    logging.info("Etapa 1/14: Carga de datos diarios")
    df = pd.read_csv(os.path.join(DATA_FOLDER, 'data.csv'))
    df = df.dropna(subset=['PTPM_CON'])
    df = add_time_features(df)

    logging.info("Etapa 2/14: Carga de datos acumulados")
    df_acumulados = pd.read_csv(os.path.join(DATA_FOLDER, 'data_acumulados.csv'))
    df_acumulados = df_acumulados.dropna(subset=['PTPM_CON'])
    df_acumulados = add_time_features(df_acumulados)

    logging.info("Etapa 3/14: Cálculo de correlaciones - datos diarios")
    correlaciones = process_all_stations(df)
    tabla_resumen = generate_summary_table(correlaciones).sort_values('Correlación Promedio', ascending=False)

    logging.info("Etapa 4/14: Cálculo de correlaciones - datos acumulados")
    correlaciones_acumulados = process_all_stations(df_acumulados)
    tabla_resumen_acumulados = generate_summary_table(correlaciones_acumulados).sort_values('Correlación Promedio', ascending=False)

    # Filtrar estaciones con correlación mayor 0.15 y al promedio por variable
    logging.info("Etapa 5/14: Filtrado de estaciones según correlaciones - datos diarios")
    correlacion_promedio = tabla_resumen.set_index('Variable')['Correlación Promedio'].to_dict()

    estaciones_filtradas = []
    for estacion, valores_correlacion in correlaciones.items():
        for var, correlacion_val in valores_correlacion.items():
            if correlacion_val > correlacion_promedio.get(var, -np.inf) and correlacion_val > 0.15:
                estaciones_filtradas.append(estacion)
                break
    estaciones_filtradas = list(set(estaciones_filtradas))
    logging.info(f"Estaciones filtradas (diarios): {len(estaciones_filtradas)}")

    df_filtrado = df[df['CodigoEstacion'].isin(estaciones_filtradas)]
    df_filtrado = df_filtrado.drop(columns=['TMN_CON', 'TMX_CON', 'DOY', 'WOY', 'MOY'], errors='ignore')

    df_filtrado = df_filtrado[
        ((df_filtrado['HR_CAL_MN_D'].ge(0) & df_filtrado['HR_CAL_MN_D'].le(100)) | df_filtrado['HR_CAL_MN_D'].isna()) &
        ((df_filtrado['HR_CAL_MX_D'].ge(0) & df_filtrado['HR_CAL_MX_D'].le(100)) | df_filtrado['HR_CAL_MX_D'].isna()) &
        ((df_filtrado['NV_MEDIA_D'].ge(0)) | df_filtrado['NV_MEDIA_D'].isna()) &
        ((df_filtrado['NV_MN_D'].ge(0)) | df_filtrado['NV_MN_D'].isna()) &
        ((df_filtrado['NV_MX_D'].ge(0)) | df_filtrado['NV_MX_D'].isna())
    ]

    columnas_a_filtrar = ['HR_CAL_MN_D', 'HR_CAL_MX_D', 'NV_MEDIA_D', 'NV_MN_D', 'NV_MX_D']
    df_filtrado = filtrar_outliers(df_filtrado, columnas_a_filtrar)

    logging.info("Etapa 6/14: Filtrado por mínimo 1000 registros por estación - datos diarios")
    registros_por_estacion = df_filtrado.groupby('CodigoEstacion').size()
    estaciones_validas = registros_por_estacion[registros_por_estacion >= 1000].index
    df_filtrado_base = df_filtrado[df_filtrado['CodigoEstacion'].isin(estaciones_validas)]

    logging.info("Etapa 7/14: Generación de dataset filtrado con NV_MEDIA_D - datos diarios")
    df_filtrado_NV = df_filtrado_base.dropna(subset=['NV_MEDIA_D'])
    df_filtrado_NV = df_filtrado_NV.drop(columns=['HR_CAL_MN_D', 'HR_CAL_MX_D', 'NV_MN_D', 'NV_MX_D'], errors='ignore')
    df_filtrado_NV.to_csv(os.path.join(DATA_FOLDER, 'data_filtrado_NV_MEDIA_D.csv'), index=False)

    logging.info("Etapa 8/14: Generación de dataset filtrado con HR_CAL_MN_D y HR_CAL_MX_D - datos diarios")
    df_filtrado_HR = df_filtrado_base.dropna(subset=['HR_CAL_MN_D', 'HR_CAL_MX_D'])
    df_filtrado_HR = df_filtrado_HR.drop(columns=['NV_MN_D', 'NV_MX_D', 'NV_MEDIA_D'], errors='ignore')
    df_filtrado_HR.to_csv(os.path.join(DATA_FOLDER, 'data_filtrado_HR_CAL_D.csv'), index=False)

    # Filtrado acumulados
    logging.info("Etapa 9/14: Filtrado de estaciones según correlaciones - datos acumulados")
    correlacion_promedio_acum = tabla_resumen_acumulados.set_index('Variable')['Correlación Promedio'].to_dict()

    estaciones_filtradas_acum = []
    for estacion, valores_correlacion in correlaciones_acumulados.items():
        for var, correlacion_val in valores_correlacion.items():
            if correlacion_val > correlacion_promedio_acum.get(var, -np.inf) and correlacion_val > 0.15:
                estaciones_filtradas_acum.append(estacion)
                break
    estaciones_filtradas_acum = list(set(estaciones_filtradas_acum))
    logging.info(f"Estaciones filtradas (acumulados): {len(estaciones_filtradas_acum)}")

    df_acumulados_filtrado = df_acumulados[df_acumulados['CodigoEstacion'].isin(estaciones_filtradas_acum)]

    logging.info("Etapa 10/14: Filtrado de columnas en datos acumulados")
    patterns = ['TMN', 'TMX','NV_MN','NV_MX','_30D']
    regex_pattern = '|'.join(patterns)
    df_acumulados_filtrado = df_acumulados_filtrado.loc[:, ~df_acumulados_filtrado.columns.str.contains(regex_pattern)]

    logging.info("Etapa 11/14: Filtrado por mínimo 1000 registros por estación - datos acumulados")
    registros_por_estacion = df_acumulados_filtrado.groupby('CodigoEstacion').size()
    estaciones_validas_acum = registros_por_estacion[registros_por_estacion >= 1000].index
    df_acumulados_filtrado = df_acumulados_filtrado[df_acumulados_filtrado['CodigoEstacion'].isin(estaciones_validas_acum)]

    logging.info("Etapa 12/14: Filtro de outliers HR y NV en datos acumulados")
    columnas_hr = df_acumulados_filtrado.filter(like='HR').columns
    columnas_nv = df_acumulados_filtrado.filter(like='NV').columns
    df_acumulados_filtrado = filtrar_outliers(df_acumulados_filtrado, columnas_hr, limite_inferior=0, limite_superior=100)
    df_acumulados_base = filtrar_outliers(df_acumulados_filtrado, columnas_nv, limite_inferior=0)

    logging.info("Etapa 13/14: Generación dataset acumulados NV_MEDIA_D")
    columnas = df_acumulados_base.filter(regex='HR').columns
    df_acumulados_NV = df_acumulados_base.drop(columns=columnas, errors='ignore')
    columnas_na = df_acumulados_NV.filter(regex='NV|PTPM_CON_15D').columns
    df_acumulados_NV = df_acumulados_NV.dropna(subset=columnas_na)
    df_acumulados_NV.to_csv(os.path.join(DATA_FOLDER, 'data_filtrado_acumulados_NV_MEDIA_D.csv'), index=False)

    logging.info("Etapa 14/14: Generación dataset acumulados HR_CAL")
    columnas = df_acumulados_base.filter(regex='NV').columns
    df_acumulados_HR = df_acumulados_base.drop(columns=columnas, errors='ignore')
    columnas_na = df_acumulados_HR.filter(regex='HR|PTPM_CON_15D').columns
    df_acumulados_HR = df_acumulados_HR.dropna(subset=columnas_na)
    df_acumulados_HR.to_csv(os.path.join(DATA_FOLDER, 'data_filtrado_acumulados_HR_CAL_D.csv'), index=False)

    logging.info("Preprocesamiento finalizado correctamente.")