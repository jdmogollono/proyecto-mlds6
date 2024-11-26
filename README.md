# Predicción de Precipitaciones Utilizando Deep Learning

## Descripción del Proyecto

Este proyecto tiene como objetivo desarrollar un modelo de predicción de precipitaciones utilizando técnicas avanzadas de Deep Learning, específicamente redes neuronales de tipo LSTM (Long Short-Term Memory). La precisión en la predicción de precipitaciones es crucial para diversas industrias y sectores, incluyendo meteorología, agricultura, gestión de riesgos y energía.

```
proyecto/
├── scripts/
│   ├── data_load.py
│   ├── data_dictionaries.py
│   ├── 1_business_data_load.ipynb
│   └── main.py
├── requirements.txt
├── README.md
└── LICENSE
```



- **scripts/**: Carpeta que contiene los scripts del proyecto.
  - **data_load.py**: Módulo que contiene las funciones para la carga y procesamiento de datos desde el IDEAM.
  - **data_dictionaries.py**: Script que ejecuta el código de `data_load.py` y genera diccionarios de datos.
  - **main.py**: Script principal que ejecuta el pipeline completo del proyecto.
  - **1_business_data_load.ipynb**: Notebook de base sobre el que se desarrolló la etapa de carga.
 

## Instalación y Ejecución

### Clonar el Repositorio

```bash
git clone https://github.com/tuusuario/proyecto-prediccion-precipitaciones.git
cd proyecto-prediccion-precipitaciones
```

Este proyecto es parte del curso de Machine Learning y Deep Learning de la Universidad Nacional de Colombia.
