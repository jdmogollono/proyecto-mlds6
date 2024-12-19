# Predicción de Precipitaciones Utilizando Deep Learning

## Descripción del Proyecto


Este proyecto tiene como objetivo desarrollar un modelo de predicción de precipitaciones utilizando técnicas avanzadas de Deep Learning, específicamente redes neuronales profundas (DNN - Deep Neural Networks). La precisión en la predicción de precipitaciones es crucial para diversas industrias y sectores, incluyendo meteorología, agricultura, gestión de riesgos y energía.

![Grabación de pantalla 2024-12-19 a la(s) 2 21 49 p m](https://github.com/user-attachments/assets/b54fee63-6ffd-4530-a51c-97f9aeadbae0)


El sistema incluye etapas de adquisición, procesamiento y análisis de datos climáticos, así como la construcción de modelos predictivos que se despliegan a través de una API interactiva y un visor gráfico.


```
├── scripts/
│   ├── data_acquisition/
│   │   ├── data_load.ipynb
│   ├── training/
│   │   ├── training.ipynb
│   ├── feature_extraction/
│   │   ├── feature_extraction.ipynb
│   ├── evaluation/
│   │   ├── api.ipynb
│   │   ├── visor.ipynb
│   ├── preprocessing/
│   │   ├── preprocessing.ipynb
│   ├── eda/
│   │   ├── eda.ipynb
├── requirements.txt
├── README.md
```


### Descripción de Carpetas y Archivos

- **scripts/data_acquisition:**  
  Contiene los scripts para la adquisición de datos desde el IDEAM.
  - `data_load.ipynb`: Notebook que incluye funciones para la carga y procesamiento inicial de datos.

- **scripts/training:**  
  Contiene los scripts para el entrenamiento de modelos predictivos.
  - `training.ipynb`: Notebook que define y entrena el modelo DNN para la predicción de precipitaciones.

- **scripts/feature_extraction:**  
  Scripts relacionados con la extracción de características.
  - `feature_extraction.ipynb`: Extracción de características avanzadas usando herramientas como `tsfresh`.

- **scripts/evaluation:**  
  Contiene los scripts para la evaluación del modelo y la implementación del sistema interactivo.
  - `api.ipynb`: Implementación de una API utilizando FastAPI para la predicción en tiempo real.
  - `visor.ipynb`: Creación de un visor interactivo con Folium y Chart.js.

- **scripts/preprocessing:**  
  Scripts para el preprocesamiento de los datos.
  - `preprocessing.ipynb`: Notebook que incluye técnicas de limpieza, transformación y escalamiento de datos.

- **scripts/eda:**  
  Scripts de análisis exploratorio de datos.
  - `eda.ipynb`: Notebook que analiza los datos para entender su distribución, identificar valores faltantes, entre otros.

- **requirements.txt:** Archivo que define todas las dependencias necesarias para ejecutar el proyecto.
- **README.md:** Documento que describe el proyecto, su instalación y uso.

## Instalación y Ejecución

### 1. Clonar el Repositorio

Clona el repositorio en tu entorno local para acceder a los scripts y archivos necesarios:

```bash
git clone https://github.com/jdmogollono/proyecto-mlds6.git
```

### 2. Crear un Entorno Virtual

Es recomendable utilizar un entorno virtual para gestionar las dependencias del proyecto:

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instalar Dependencias

Instala las bibliotecas necesarias listadas en `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configuración Inicial

Asegúrate de que los datos crudos estén en la carpeta `data/raw/` y que las rutas en los notebooks y scripts apunten a las carpetas correctas.  
Por ejemplo, revisa los paths en los archivos:
- `data_load.ipynb` (adquisición de datos)
- `preprocessing.ipynb` (preprocesamiento)
- `training.ipynb` (entrenamiento)

### 5. Ejecución de las Etapas

#### a) Adquisición de Datos
Ejecuta el notebook `data_load.ipynb` para cargar los datos desde las fuentes especificadas (ej. IDEAM).

#### b) Preprocesamiento
Corre el notebook `preprocessing.ipynb` para limpiar y transformar los datos en un formato adecuado para el modelo.

#### c) Análisis Exploratorio
Utiliza `eda.ipynb` para realizar un análisis preliminar de los datos y entender su distribución y características.

#### d) Extracción de Características
Ejecuta `feature_extraction.ipynb` para calcular características relevantes usando herramientas como `tsfresh`.

#### e) Entrenamiento del Modelo
Abre y corre `training.ipynb` para entrenar el modelo DNN utilizando los datos preprocesados y características extraídas.

#### f) Evaluación e Interactividad
1. Ejecuta la API interactiva definida en `api.ipynb`. Convierte el notebook en un script Python si lo deseas y corre:
   ```bash
   uvicorn api:app --host 0.0.0.0 --port 1304
   ```
2. Genera el visor interactivo corriendo `visor.ipynb`. Esto creará un archivo `visor.html` que puedes abrir en tu navegador para visualizar las predicciones.

### 6. Visualización y Uso del Modelo


- Accede a la API en `http://localhost:1304/` para verificar que está activa.  
- Usa `POST http://localhost:1304/prediccion/{estacion_id}` para obtener predicciones para una estación específica.
- Abre `visor.html` para explorar el mapa interactivo de estaciones y visualizar predicciones gráficas en tiempo real.

### 7. Actualización y Mantenimiento

- **Actualización de datos:** Si cambian los datos de entrada, vuelve a ejecutar las etapas desde el preprocesamiento.  
- **Entrenamiento:** Si deseas mejorar el modelo, ajusta los hiperparámetros en `training.ipynb` o utiliza herramientas como Keras Tuner.
- **Monitoreo:** Verifica los logs del servidor FastAPI para solucionar posibles errores.

