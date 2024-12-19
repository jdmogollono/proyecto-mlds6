
# Despliegue de Modelos

## Infraestructura

**Nombre del modelo:** Modelo DNN para predicción de precipitación

**Plataforma de despliegue:**  
- El modelo se expone como un servicio web a través de FastAPI.  
- Se puede desplegar en un entorno local, servidor virtual en la nube (ej. AWS, GCP, Azure) o dentro de un contenedor Docker.  
- Adicionalmente, se puede integrar con un frontend (ej. `visor.html`) para visualización.

**Requisitos técnicos:**  
- Python 3.9 o superior  
- Bibliotecas:
  - fastapi
  - uvicorn
  - pydantic
  - pandas
  - numpy
  - tensorflow (Versión 2.X)
  - scikit-learn
  - pickle (generalmente incluido en Python, si no usar `pickle5`)
  - nest_asyncio
  - requests
  - folium (para la generación de mapas en el visor)
- Hardware: CPU estándar es suficiente para la inferencia. Para cargas mayores, puede evaluarse el uso de GPU.

**Requisitos de seguridad:**  
- Opcional: Autenticación en los endpoints (no implementada actualmente).  
- Recomendado: Uso de HTTPS (configurar un proxy inverso o TLS si se despliega en producción).  
- Control de CORS: Actualmente se encuentra abierto (`allow_origins=["*"]`), modificar según las políticas de seguridad necesarias.

**Diagrama de arquitectura:**  

![image](https://github.com/user-attachments/assets/6465b461-4da4-43d1-a6eb-c49bdf4a1459)




El visor (`visor.html`) se apoya en la API (`/prediccion/{estacion_id}`) para obtener predicciones y mostrarlas en un mapa interactivo.


## Código de despliegue

**Archivo principal:** `api.ipynb` (recomendado convertirlo a `api.py` para ejecución directa con `uvicorn`).

**Rutas de acceso a los archivos:**  
- Modelo: `../../data/best_model_dnn.keras`  
- Diccionario de estaciones: `../../data/station_dict.pkl`  
- Datos: `../../data/data_modelo.csv`  
- Archivos auxiliares (ej. `CNE_IDEAM.xls`, `visor.html`): ubicados en `../../data/`

**Variables de entorno (opcional):**  
- `WORKSPACE`: Ruta absoluta a la carpeta raíz del proyecto (por defecto `os.path.join(os.getcwd(), '../../')`).  
- `DATA_FOLDER`: Ruta a la carpeta de datos (`WORKSPACE/data` por defecto).  
- `HOST`, `PORT`: Si se desea cambiar el host o puerto del servidor FastAPI/Uvicorn.


## Documentación del despliegue

**Instrucciones de instalación:**
1. Clonar el repositorio o ubicar los archivos en el servidor.
2. Crear y activar un entorno virtual (opcional, recomendado):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Instalar dependencias:
   ```bash
   pip install fastapi uvicorn pydantic pandas numpy tensorflow scikit-learn nest_asyncio requests folium
   ```
4. Confirmar que `best_model_dnn.keras`, `station_dict.pkl`, `data_modelo.csv` y otros datos estén en `../../data/`.

**Instrucciones de configuración:**
- Ajustar las rutas a archivos en `api.py` según la estructura real del proyecto.
- Cambiar el puerto en `uvicorn.run(app, host="0.0.0.0", port=1304)` si se desea usar otro.
- Configurar variables de entorno si es necesario.

**Instrucciones de uso:**
1. Ejecutar la API (asumiendo `api.py` como nombre final):
   ```bash
   uvicorn api:app --host 0.0.0.0 --port 1304
   ```
   Esto iniciará la API en `http://localhost:1304/`.
2. Verificar el endpoint principal:  
   `GET http://localhost:1304/`  
   Debería retornar `{"message": "API de predicciones activa"}`.
3. Obtener predicciones para una estación específica:  
   `POST http://localhost:1304/prediccion/{estacion_id}`  
   Reemplazar `{estacion_id}` con un código de estación válido. Retorna un JSON con valores `Real` y `Prediccion`.
4. Abrir `visor.html` (generado por `visor.ipynb`) para visualizar el mapa con estaciones. Al hacer clic en "Obtener Predicción" en una estación se mostrará la gráfica con datos reales y predicción.

**Instrucciones de mantenimiento:**
- Actualizar el modelo reemplazando `best_model_dnn.keras` con la nueva versión.
- Si cambian las estaciones o datos, actualizar `data_modelo.csv`, `station_dict.pkl` y reiniciar el servidor.
- Actualizar dependencias con `pip install --upgrade <paquete>` si es necesario.
- Monitorear logs del servidor para solucionar problemas.
