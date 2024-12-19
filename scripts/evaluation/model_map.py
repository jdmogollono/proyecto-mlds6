import pandas as pd
import folium
import requests
import matplotlib.pyplot as plt
from io import BytesIO

# 1. Cargar los datasets
data_modelo_path = 'data_modelo.csv'
cne_ideam_path = 'CNE_IDEAM.xls'

# Cargar los datasets
df_modelo = pd.read_csv(data_modelo_path)
df_ideam = pd.read_excel(cne_ideam_path)

# 2. Identificar los códigos de estación únicos
df_modelo_codes = df_modelo['CodigoEstacion'].unique()

# 3. Filtrar la información en `df_ideam` relacionada con los códigos
df_ideam_filtered = df_ideam[df_ideam['CODIGO'].isin(df_modelo_codes)]


df_ideam_filtered = df_ideam_filtered.rename(columns={
    'CODIGO': 'CodigoEstacion',
    'LATITUD': 'Latitud',
    'LONGITUD': 'Longitud',
    'NOMBRE': 'NombreEstacion',
    'DEPARTAMENTO': 'Departamento',
    'MUNICIPIO': 'Municipio'
})

# 4. Crear el mapa interactivo
mapa = folium.Map(location=[df_ideam_filtered['Latitud'].mean(), df_ideam_filtered['Longitud'].mean()], zoom_start=6)

# Función para manejar el evento de clic
def on_click(event, estacion_id):
    # Llamar a la API del modelo para obtener predicciones
    url = f"http://api.modelo.com/prediccion/{estacion_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        fechas = data['fechas']
        predicciones = data['predicciones']

        # Graficar las predicciones
        plt.figure(figsize=(8, 4))
        plt.plot(fechas, predicciones, label=f"Predicción para estación {estacion_id}")
        plt.xlabel("Fecha")
        plt.ylabel("Precipitación")
        plt.title("Predicción de precipitación")
        plt.legend()
        plt.grid()

        # Mostrar la gráfica
        plt.show()
    else:
        print(f"Error al obtener la predicción para la estación {estacion_id}: {response.status_code}")

# Añadir puntos de las estaciones al mapa
for _, row in df_ideam_filtered.iterrows():
    estacion_id = row['CodigoEstacion']
    nombre = row['NombreEstacion']
    lat = row['Latitud']
    lon = row['Longitud']
    departamento = row['Departamento']
    municipio = row['Municipio']

    # Información de la estación
    info = f"""
    <b>Estación:</b> {nombre}<br>
    <b>Departamento:</b> {departamento}<br>
    <b>Municipio:</b> {municipio}<br>
    <b>Codigo:</b> {estacion_id}<br>
    <button onclick="open_model({estacion_id})">Obtener Predicción</button>
    """

    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(info, max_width=300),
        tooltip=f"Estación: {nombre} ({estacion_id})"
    ).add_to(mapa)

# Guardar el mapa como un archivo HTML
mapa.save("mapa_estaciones.html")

print("Mapa generado: mapa_estaciones.html")