# data_dictionaries.py

from data_load import (
    download_cne,
    get_station_data,
    procesar_estaciones_paralelo,
    consolidar_csv,
    calcular_acumulados,
    DATA_FOLDER
)
import os
import pandas as pd

def create_data_dictionaries():
    # Leer el catálogo nacional de estaciones del IDEAM
    download_cne()
    catalogo_estaciones = pd.read_excel(os.path.join(DATA_FOLDER, 'CNE_IDEAM.xls'))

    # Filtrar estaciones activas
    catalogo_estaciones_activas = catalogo_estaciones[catalogo_estaciones["ESTADO"] != "Suspendida"]
    print(f'Número de estaciones activas: {len(catalogo_estaciones_activas)}')

    # Uso de la función get_station_data
    parametros_etiquetas = {
        "Nivel Máximo": {"IdParametro": "NIVEL", "Etiqueta": "NV_MX_D"},
        "Nivel Mínimo": {"IdParametro": "NIVEL", "Etiqueta": "NV_MN_D"},
        "Nivel Medio": {"IdParametro": "NIVEL", "Etiqueta": "NV_MEDIA_D"},
        "Temperatura Máxima": {"IdParametro": "TEMPERATURA", "Etiqueta": "TMX_CON"},
        "Temperatura Mínima": {"IdParametro": "TEMPERATURA", "Etiqueta": "TMN_CON"},
        "Humedad Relativa Máxima": {"IdParametro": "HUM RELATIVA", "Etiqueta": "HR_CAL_MX_D"},
        "Humedad Relativa Mínima": {"IdParametro": "HUM RELATIVA", "Etiqueta": "HR_CAL_MN_D"},
        "Precipitación Acumulada": {"IdParametro": "PRECIPITACION", "Etiqueta": "PTPM_CON"}
    }

    for nombre_parametro, valores in parametros_etiquetas.items():
        try:
            get_station_data(
                catalogo_estaciones_activas['CODIGO'].tolist(),
                '2000-01-01',
                '2023-12-31',
                valores['IdParametro'],
                valores['Etiqueta']
            )
        except Exception as e:
            pass

    # Lista de DataFrames
    variables_dataframes = {}

    # Leer cada archivo en la carpeta de datos
    for archivo in os.listdir(os.path.join(DATA_FOLDER, 'variables')):
        if archivo.endswith('.csv'):
            # Extraer el nombre del archivo sin extensión
            nombre_variable = os.path.splitext(archivo)[0]
            
            # Leer el archivo CSV y solo cargar las columnas necesarias, especificando los tipos de datos
            archivo_path = os.path.join(DATA_FOLDER, 'variables', archivo)

            df = pd.read_csv(archivo_path, 
                                usecols=['CodigoEstacion', 'Fecha', 'Valor'],
                                dtype={'CodigoEstacion': 'int', 'Fecha': 'str', 'Valor': 'str'})  
             
            # Convertir la columna Fecha al tipo datetime forzando errores a NaN
            df['Fecha'] =  pd.to_datetime(df['Fecha'], errors='coerce').dt.normalize()  

            # Convertir la columna 'Valor' a float32, forzando errores a NaN
            df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').astype('float32')
            
            # Redondear la columna 'Valor' a 1 decimal
            df['Valor'] = df['Valor'].round(1)
            
            # Renombrar la columna 'Valor' con el nombre de la variable (archivo)
            df.rename(columns={'Valor': nombre_variable}, inplace=True)

            # Guardar el DataFrame en el diccionario usando el nombre de la variable
            variables_dataframes[nombre_variable] = df

    # Crear y ejecutar el procesamiento en paralelo
    procesar_estaciones_paralelo(
        catalogo_estaciones_activas=catalogo_estaciones_activas,
        variables_dataframes=variables_dataframes,
        fecha_inicio='2000-01-01',
        fecha_fin='2023-12-31',
        output_folder= os.path.join(DATA_FOLDER, 'estaciones')
    )

    # Consolidar los archivos CSV
    consolidar_csv(os.path.join(DATA_FOLDER, 'estaciones'), os.path.join(DATA_FOLDER, 'data.csv'))

    # Cargar el dataset
    df = pd.read_csv(os.path.join(DATA_FOLDER, 'data.csv'))

    # Calcular los acumulados
    df_acumulados = calcular_acumulados(df)
    df_acumulados = df_acumulados.drop(columns=['HR_CAL_MN_D', 'HR_CAL_MX_D', 'NV_MEDIA_D', 'NV_MN_D', 'NV_MX_D', 'TMN_CON', 'TMX_CON'])

    # Guardar el resultado en un archivo CSV
    output_path = os.path.join(DATA_FOLDER, 'data_acumulados.csv')
    df_acumulados.to_csv(output_path, index=False)

    # Crear diccionarios de datos
    data_dictionaries = df_acumulados.to_dict(orient='records')

    return data_dictionaries
