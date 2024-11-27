# data_load.py

import requests
import json
import time
import base64
import zipfile
import io
import pandas as pd
import os
from tqdm import tqdm
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import numpy as np
from datetime import datetime
import multiprocessing as mp
from functools import partial

# Definir la ruta de la carpeta de datos
WORKSPACE = os.path.abspath(os.path.join(os.getcwd(), '../../'))
DATA_FOLDER = os.path.join(WORKSPACE, 'data')

print("Workspace:", WORKSPACE)
print("Data folder:", DATA_FOLDER)

def get_station_data(station_codes, start_date, end_date, id_parametro, etiqueta, group_size=20):
    """
    Obtiene datos de estaciones del servidor IDEAM.

    Entradas:
    - station_codes: Lista de códigos de estaciones
    - start_date: Fecha de inicio
    - end_date: Fecha de fin
    - id_parametro: ID del parámetro a obtener
    - etiqueta: Etiqueta del parámetro
    - group_size: Tamaño del grupo de estaciones para procesar

    Salida:
    - None (guarda los archivos en DATA_FOLDER)
    """
    url = "http://dhime.ideam.gov.co/server/rest/services/AtencionCiudadano/DescargarArchivo/GPServer/DescargarArchivo/submitJob"
    groups = [station_codes[i:i + group_size] for i in range(0, len(station_codes), group_size)]

    empty_groups = 0
    overtime_groups = 0
    total_groups = len(groups)

    with tqdm(total=total_groups, desc=f"PROCESANDO {etiqueta} ({id_parametro})", unit="grupo") as pbar:
        for group in groups:
            filter_stations = "~or~".join([f"(IdParametro~eq~'{id_parametro}'~and~Etiqueta~eq~'{etiqueta}'~and~IdEstacion~eq~'{code}')" for code in group])
            params = {
                "Filtro": f"sort=&filter=({filter_stations})&group=&fechaInicio={start_date}T05%3A00%3A00.000Z&fechaFin={end_date}T05%3A00%3A00.000Z&mostrarGrado=true&mostrarCalificador=true&mostrarNivelAprobacion=true",
                "Items": json.dumps([{"IdParametro": id_parametro, "Etiqueta": etiqueta, "EsEjeY1": False, "EsEjeY2": False, "EsTipoLinea": False, "EsTipoBarra": False, "TipoSerie": "Estandard", "Calculo": ""}] * len(group)),
                "f": "pjson"
            }

            response = requests.post(url, data=params)

            if response.status_code == 200:
                job_id = response.json()['jobId']
                zip_url = f"http://dhime.ideam.gov.co/server/rest/services/AtencionCiudadano/DescargarArchivo/GPServer/DescargarArchivo/jobs/{job_id}/results/Archivo?f=pjson"

                start_time = time.time()
                saved_data = False
                while True:
                    zip_response = requests.get(zip_url)
                    if zip_response.status_code == 200 and 'value' in zip_response.json():
                        base64_string = zip_response.json()['value']
                        padding = 4 - (len(base64_string) % 4)
                        if padding:
                            base64_string += '=' * padding

                        try:
                            decoded_bytes = base64.b64decode(base64_string)
                            with zipfile.ZipFile(io.BytesIO(decoded_bytes)) as zip_file:
                                for filename in zip_file.namelist():
                                    if filename.endswith('.csv'):
                                        with zip_file.open(filename) as f:
                                            csv_data = f.read()
                                        os.makedirs(f'{DATA_FOLDER}/variables/', exist_ok=True)
                                        with open(f'{DATA_FOLDER}/variables/{etiqueta}.csv', 'ab') as file:
                                            file.write(csv_data)
                                        saved_data = True
                            break
                        except Exception as e:
                            if not saved_data:
                                empty_groups += 1
                            break
                    elif time.time() - start_time > 120:
                        if not saved_data:
                            overtime_groups += 1
                            print(f"{etiqueta} : {group}")
                        break
                    else:
                        time.sleep(1)

            pbar.update(1)

    print(f"Número de grupos sin datos: {empty_groups}/{total_groups}")
    print(f"Número de grupos fuera del límite de espera: {overtime_groups}/{total_groups}")

def procesar_estacion(codigo_estacion, variables_dataframes, fecha_inicio, fecha_fin, output_folder):
    """
    Procesa una estación individual y crea su archivo CSV con todas las variables.
    
    Args:
        codigo_estacion (str): Código de la estación a procesar
        variables_dataframes (dict): Diccionario con los DataFrames de variables
        fecha_inicio (str): Fecha de inicio del período a procesar
        fecha_fin (str): Fecha fin del período a procesar
        output_folder (str): Carpeta donde se guardarán los archivos CSV
    """
    try:
        # Crear un DataFrame vacío con el rango de fechas completo
        fecha_idx = pd.date_range(start=fecha_inicio, end=fecha_fin, freq='D')
        df_estacion = pd.DataFrame(index=fecha_idx)
        df_estacion.index.name = 'Fecha'
        
        # Para cada variable, obtener los valores correspondientes a la estación
        for nombre_var, df_var in variables_dataframes.items():
            # Filtrar datos para esta estación
            datos_var = df_var[df_var['CodigoEstacion'] == codigo_estacion].copy()
            
            # Convertir los datos a serie temporal con la fecha como índice
            if not datos_var.empty:
                serie_temporal = pd.Series(
                    datos_var[nombre_var].values,
                    index=datos_var['Fecha'],
                    name=nombre_var
                )
            else:
                # Si no hay datos para esta variable, crear una serie vacía con NaN
                serie_temporal = pd.Series(
                    np.nan,
                    index=fecha_idx,
                    name=nombre_var
                )
            
            # Unir con el DataFrame principal
            df_estacion = df_estacion.join(serie_temporal)
        
        # Eliminar las filas donde todas las variables son NaN
        df_estacion = df_estacion.dropna(how='all')

        # Verificar si tenemos al menos una variable con datos
        if len(df_estacion) > 0:
            # Guardar el DataFrame como CSV
            output_path = os.path.join(output_folder, f'{codigo_estacion}.csv')
            df_estacion.to_csv(output_path, date_format='%Y-%m-%d')
            return f"Procesada estación {codigo_estacion}"
        else:
            return f"Estación {codigo_estacion} no tiene datos para ninguna variable"
    
    except Exception as e:
        return f"Error procesando estación {codigo_estacion}: {str(e)}"

def procesar_estaciones_paralelo(catalogo_estaciones_activas, variables_dataframes, 
                                 fecha_inicio, fecha_fin,
                                 output_folder, chunk_size=500):
    """
    Procesa todas las estaciones en paralelo usando todos los núcleos disponibles,
    procesando en lotes de 100 estaciones y mostrando el progreso con una barra de progreso.
    
    Args:
        catalogo_estaciones_activas (pd.DataFrame): DataFrame con las estaciones activas.
        variables_dataframes (dict): Diccionario con los DataFrames de variables.
        fecha_inicio (str): Fecha de inicio del período a procesar.
        fecha_fin (str): Fecha fin del período a procesar.
        output_folder (str): Carpeta donde se guardarán los archivos CSV.
    """
    # Crear la carpeta de salida si no existe
    os.makedirs(output_folder, exist_ok=True)
    
    # Obtener lista de códigos de estaciones
    codigos_estaciones = catalogo_estaciones_activas['CODIGO'].unique()
    
    # Dividir las estaciones en lotes
    lotes_estaciones = [codigos_estaciones[i:i + chunk_size] for i in range(0, len(codigos_estaciones), chunk_size)]
    
    # Configurar el procesamiento en paralelo
    num_cores = mp.cpu_count()
    print(f"Utilizando {num_cores} núcleos para el procesamiento")
    print(f"Procesando {len(codigos_estaciones)} estaciones en {len(lotes_estaciones)} lotes de {chunk_size} estaciones")
    print(f"Variables disponibles: {list(variables_dataframes.keys())}")
    
    # Crear función parcial con los argumentos comunes
    func = partial(procesar_estacion, 
                   variables_dataframes=variables_dataframes,
                   fecha_inicio=fecha_inicio,
                   fecha_fin=fecha_fin,
                   output_folder=output_folder)
    
    # Inicializar los contadores globales para el resumen final
    estaciones_con_datos_global = 0
    estaciones_sin_datos_global = 0
    estaciones_con_error_global = 0
    
    # Inicializar barra de progreso
    with tqdm(total=len(codigos_estaciones)) as pbar:
        # Procesar los lotes en paralelo
        for lote in lotes_estaciones:
            # Crear pool de procesos
            with mp.Pool(num_cores) as pool:
                resultados = pool.map(func, lote)
            
            # Actualizar la barra de progreso
            pbar.update(len(lote))
            
            # Contadores parciales
            estaciones_con_datos = 0
            estaciones_sin_datos = 0
            estaciones_con_error = 0
            
            # Mostrar resultados parciales y actualizar contadores globales
            for resultado in resultados:
                if "no tiene datos" in resultado:
                    estaciones_sin_datos += 1
                    estaciones_sin_datos_global += 1
                elif "Error" in resultado:
                    estaciones_con_error += 1
                    estaciones_con_error_global += 1
                else:
                    estaciones_con_datos += 1
                    estaciones_con_datos_global += 1

    # Mostrar resumen final
    print("\nResumen final del procesamiento de todas las estaciones:")
    print(f"- Estaciones procesadas con éxito: {estaciones_con_datos_global}")
    print(f"- Estaciones sin datos: {estaciones_sin_datos_global}")
    print(f"- Estaciones con errores: {estaciones_con_error_global}")
    print(f"\nLos archivos CSV se encuentran en: {output_folder}")

def consolidar_csv(data_path, output_file):
    """
    Lee todos los archivos CSV en una carpeta, los une y agrega una nueva columna con el nombre del archivo.
    
    Args:
        data_path (str): Ruta de la carpeta que contiene los archivos CSV.
        output_file (str): Nombre del archivo CSV de salida con los datos consolidados.
    """
    # Obtener la lista de archivos CSV en la carpeta
    archivos_csv = [f for f in os.listdir(data_path) if f.endswith('.csv')]
    
    # Lista para almacenar los DataFrames
    dataframes = []
    
    # Iterar sobre cada archivo CSV
    for archivo in archivos_csv:
        archivo_path = os.path.join(data_path, archivo)
        
        # Leer el archivo CSV en un DataFrame
        df = pd.read_csv(archivo_path)
        
        # Agregar una nueva columna con el nombre del archivo 
        df.insert(0, 'CodigoEstacion', os.path.splitext(archivo)[0])
        
        # Agregar el DataFrame a la lista
        dataframes.append(df)
    
    # Concatenar todos los DataFrames en uno solo
    df_consolidado = pd.concat(dataframes, ignore_index=True)
    
    # Guardar el DataFrame consolidado en un nuevo archivo CSV
    df_consolidado.to_csv(output_file, index=False)
    
    print(f"Archivo CSV consolidado guardado en: {output_file}")

def download_cne():
    url = "https://bart.ideam.gov.co/cneideam/CNE_IDEAM.xls"
    os.makedirs(DATA_FOLDER, exist_ok=True)
    file_name = os.path.basename(url)
    file_path = os.path.join(DATA_FOLDER, file_name)
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
    else:
        pass
 
def calcular_promedios(df):
    # Asegurar que la columna Fecha está en formato de fecha
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    
    # Ordenar por CodigoEstacion y Fecha para asegurar el cálculo adecuado
    df = df.sort_values(by=['CodigoEstacion', 'Fecha'])
    
    # Definir los días para los que se calcularán promedios
    dias_promedios = [1, 3, 7, 15, 30]
    
    # Listas de columnas
    columnas_promedio = ['PTPM_CON','HR_CAL_MN_D', 'HR_CAL_MX_D', 'NV_MEDIA_D', 'NV_MN_D', 'NV_MX_D', 'TMN_CON', 'TMX_CON']
    
    # Crear un nuevo DataFrame para almacenar los resultados
    df_resultado = df.copy()
    
    # Calcular promedios móviles para cada estacion
    for dias in dias_promedios:
        for col in columnas_promedio:
            # Crear la columna nueva para el promedio
            col_nueva = f'{col}_{dias}D'
            # Calcular el promedio
            df_resultado[col_nueva] = df.groupby('CodigoEstacion')[col].transform(lambda x: x.shift(1).rolling(window=dias, min_periods=dias).mean())

    # Redondear a dos decimales
    df_resultado = df_resultado.round(2)

    # Eliminar filas donde todas las columnas son NaN
    df_resultado = df_resultado.dropna(how='all', subset=[f'{col}_{dias}D' for dias in dias_promedios for col in columnas_promedio])

    return df_resultado