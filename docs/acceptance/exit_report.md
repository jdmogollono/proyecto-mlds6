# Informe de salida

## Resumen Ejecutivo

Este informe describe los resultados del proyecto de machine learning y presenta los principales logros y lecciones aprendidas durante el proceso.

## Resultados del Proyecto

### Resumen de los entregables y logros alcanzados en cada etapa del proyecto

1. **Entendimiento del negocio y carga de datos**:
   - Se obtuvo y estructuró un conjunto de datos de precipitaciones y variables meteorológicas proporcionado por IDEAM (2000-2023).
   - Se elaboraron diccionarios de datos y un marco de proyecto claro, estableciendo la base para el análisis posterior.

2. **Preprocesamiento y análisis exploratorio**:
    - Se identificaron datos faltantes y las variables con mayor correlación con la precipitación, además de realizar un análisis descriptivo para explorar patrones en los datos.
   - Se realizó la limpieza y transformación de datos, eliminando valores atípicos, estaciones con persistencia de ceros y correlaciones bajas.

3. **Modelamiento y extracción de características**:
   - Se realizó la extracción de características utilizando herramientas de análisis de la biblioteca tsfresh, identificando aquellas con mayor correlación con la precipitación.
   - Se implementó un modelo de redes neuronales profundas (DNN), optimizado mediante técnicas avanzadas de ajuste de hiperparámetros de la biblioteca KerasTuner.

4. **Despliegue**:
   - Se probó un entorno de despliegue simulado, asegurando la replicabilidad de los resultados.
   - Se desplegó el modelo utilizando la biblioteca FastAPI, permitiendo obtener las predicciones de manera eficiente y accesible.
   - Se construyó un visor geográfico utilizando Folium, HTML y JavaScript para visualizar las predicciones de manera más interactiva y comprensible.

5. **Evaluación y entrega final**:
   - La comparación entre el modelo DNN desarrollado en el curso Deep Learning y el modelo final mostró mejoras significativas, con una reducción del MAE del 73.33%.
   - Se realizó un video explicativo y presentación final donde se destacaron la metodología empleada y resultados obtenidos.

### Evaluación del modelo final y comparación con el modelo anterior

El modelo final basado en redes neuronales DNN superó al modelo DNN anterior en la métrica evaluada:

| Métrica          | Modelo Anterior (DNN)| Modelo Final (DNN) |
|------------------|--------------------------|---------------------|
| MAE (mm)         | 0.18                  | 0.048                |

El modelo final logró eliminar el sesgo presente en el modelo anterior, siendo ahora capaz de predecir valores de tiempo seco, incluyendo valores cero o cercanos a cero. Sin embargo, se sigue evidenciando un desfase en las predicciones, lo que sugiere que el modelo podría estar sobreajustándose a los datos de las condiciones de precipitación del dia anterior.

### Descripción de los resultados y su relevancia para el negocio

- **Resultados obtenidos**:
  - Predicciones precisas de precipitaciones en puntos geográficos específicos dentro del rango temporal de prueba, respecto a los modelos evaluados anteriormente.
  - Herramienta para la visualización y generación interactiva de las predicciones por parte del usuario en un entorno de prueba.

- **Relevancia para el negocio**:
  - Se establece una base para la incorporación futura de datos adicionales, arquitecturas de modelos diferentes y técnicas de preprocesamiento más complejas.

## Lecciones aprendidas

- Identificación de los principales desafíos y obstáculos encontrados durante el proyecto.
- Lecciones aprendidas en relación al manejo de los datos, el modelamiento y la implementación del modelo.
- Recomendaciones para futuros proyectos de machine learning.

## Impacto del proyecto

- Descripción del impacto del modelo en el negocio o en la industria.
- Identificación de las áreas de mejora y oportunidades de desarrollo futuras.

## Conclusiones

- Resumen de los resultados y principales logros del proyecto.
- Conclusiones finales y recomendaciones para futuros proyectos.

## Agradecimientos

- Agradecimientos al equipo de trabajo y a los colaboradores que hicieron posible este proyecto.
- Agradecimientos especiales a los patrocinadores y financiadores del proyecto.
