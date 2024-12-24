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

### **Manejo de los Datos**

#### **Desafíos encontrados**
1. **Acceso y descarga de datos:**
   - La extracción de datos desde el servidor del IDEAM implicó retos técnicos, como manejar respuestas vacías, tiempos de espera prolongados y posibles errores de codificación al procesar los archivos descargados.
   - El volumen de datos requería dividir las estaciones en grupos y procesarlas secuencialmente para evitar sobrecargar el servidor.

2. **Calidad y consistencia:**
   - Los datos presentaban inconsistencias como valores faltantes, formatos incorrectos (ejemplo: fechas mal codificadas) y columnas con registros nulos. 
   - Los datos contenían múltiples variables meteorológicas (`PTPM_CON`, `NV_MEDIA_D`, etc.) que debían ser consolidadas en un único formato estandarizado.

3. **Optimización del procesamiento:**
   - El tamaño del dataset resultante (aproximadamente 17.9 millones de registros después de calcular promedios móviles) exigió soluciones de procesamiento eficientes para evitar problemas de memoria.

---

#### **Metodología implementada**
1. **Extracción de datos:**
   - Se utilizó una función (`get_station_data`) para consultar el servidor del IDEAM y descargar los datos en formato comprimido. Esto incluía el manejo de tiempos de espera, descargas parciales y errores en el formato de los archivos.
   - Cada variable meteorológica se almacenó por separado en archivos CSV.

2. **Consolidación de datos:**
   - Se creó una función para unificar todos los archivos descargados en un solo dataset. Durante este proceso:
     - Se homogenizaron formatos de datos (por ejemplo, convertir fechas a tipo `datetime` y valores numéricos a `float`).
     - Se alinearon los datos temporalmente y se eliminaron filas con valores completamente nulos.
   - Los archivos individuales se integraron en un archivo único con más de 17 millones de registros.

3. **Cálculo de métricas adicionales:**
   - Se calcularon promedios móviles para diferentes períodos (1, 3, 7, 15 y 30 días) para las principales variables. Esto se realizó agrupando por estación y asegurando que los cálculos fueran consistentes y eficientes.

4. **Procesamiento paralelo:**
   - Se utilizó procesamiento en paralelo (`multiprocessing`) para manejar grandes volúmenes de datos. Esto aceleró significativamente la consolidación y el cálculo de métricas, dividiendo las estaciones en lotes y procesándolas en múltiples núcleos.

---

#### **Resultados**
1. **Calidad de los datos:**
   - Se eliminaron inconsistencias y se aseguraron formatos homogéneos en las columnas clave (`Fecha`, `CodigoEstacion`, `Valor`).
   - Los valores fueron redondeados y validados, garantizando que las transformaciones no introdujeran sesgos.

2. **Volumen procesado:**
   - El dataset consolidado incluye **17.9 millones de registros** con más de **40 columnas**, incluyendo datos crudos y métricas derivadas.

3. **Optimización del procesamiento:**
   - El uso de procesamiento paralelo y funciones optimizadas permitió manejar eficientemente el gran volumen de datos y reducir significativamente los tiempos de cálculo.

4. **Dataset final:**
   - El dataset generado incluye promedios móviles para precipitaciones, niveles, temperaturas, y humedad relativa, permitiendo un análisis más robusto y detallado para modelamiento predictivo.

---

#### **Lecciones aprendidas**
- El manejo temprano de inconsistencias en los datos (formatos y valores nulos) simplifica los pasos posteriores de análisis y modelamiento.
- Dividir el procesamiento en tareas paralelas puede ser crucial para manejar grandes volúmenes de datos, pero requiere una cuidadosa planificación de recursos y diseño modular.
- La integración y consolidación de múltiples fuentes de datos deben ser diseñadas para garantizar reproducibilidad y escalabilidad.

#### **Recomendaciones**
- **Automatización del flujo de trabajo:** Diseñar pipelines que integren extracción, procesamiento y consolidación en un flujo único, idealmente programado para manejar datos en tiempo real o históricos de forma recurrente.
- **Documentación:** Mantener un registro detallado de las transformaciones realizadas, asegurando que los pasos sean reproducibles y comprensibles para otros miembros del equipo.
- **Validación cruzada:** Implementar validaciones automáticas durante el procesamiento para garantizar la calidad del dataset final.


## Impacto del proyecto

El modelo de predicción de precipitaciones desarrollado tiene un impacto significativo en diversas áreas y sectores clave:

### Instituciones Meteorológicas y Ambientales
- **Mejora en los pronósticos:** El modelo proporciona predicciones más precisas de precipitaciones, permitiendo a las instituciones ajustar sus sistemas de alerta temprana y planificación climática.
- **Capacidad predictiva ampliada:** Con la incorporación de datos históricos y el uso de redes neuronales profundas, las instituciones pueden cubrir más regiones con precisión.

### Sector Agrícola
- **Planificación eficiente:** Los agricultores pueden optimizar el uso de recursos hídricos y planificar mejor los ciclos de siembra y cosecha basándose en predicciones confiables.
- **Mitigación de riesgos:** Identificar patrones de sequías o lluvias excesivas ayuda a reducir pérdidas económicas y mejorar la sostenibilidad.

### Gobiernos y Gestión de Riesgos
- **Gestión proactiva de emergencias:** Los gobiernos locales pueden anticiparse a fenómenos como inundaciones y sequías, tomando decisiones informadas para proteger a las comunidades.
- **Infraestructura resiliente:** Permite planificar y construir infraestructuras adaptadas a los patrones climáticos previstos.

### Sector Energético
- **Optimización de recursos:** Las compañías hidroeléctricas y de energías renovables pueden ajustar su producción basándose en pronósticos precisos de lluvias.
- **Reducción de riesgos:** Minimiza las interrupciones causadas por fenómenos climáticos inesperados.

### Compañías de Seguros
- **Gestión de riesgos climáticos:** El modelo puede integrarse en la evaluación de riesgos, permitiendo ajustar pólizas y calcular primas de manera más efectiva.

## Identificación de Áreas de Mejora y Oportunidades de Desarrollo Futuras

   - En trabajos futuros podría ser útil explorar el uso de datos satelitales o modelos globales como ENSO (El Niño–Oscilación del Sur) para enriquecer las predicciones.
   - Se puede investigar el uso de redes de grafos (GNN) para capturar relaciones entre estaciones.
   - Se podrían implementar mecanismos para procesamiento de datos y actualización de modelos en tiempo real para asegurar que el modelo se encuentre actualizado.
   - Se podría probar el modelo en regiones adicionales y con datos más recientes para evaluar su capacidad de generalización.
   - Escalar el modelo para su integración en plataformas existentes utilizadas por los stakeholders.
   - Utilizar técnicas de interpretabilidad como SHAP para identificar cómo cada variable impacta las predicciones, aumentando la confianza en los resultados.
   - Involucrar expertos de diferentes campos para enriquecer las capacidades predictivas y asegurar que el modelo cumpla con las expectativas de los stakeholders

## Conclusiones

## Resumen de los Resultados y Principales Logros del Proyecto

1. **Desarrollo exitoso del modelo predictivo:**
   - El modelo de redes neuronales profundas (DNN) alcanzó un MAE de ~0.044, estableciendo un valor de referencia para futuros trabajos.
   - Se logró predecir con precisión valores de precipitación en regiones geográficas diversas.

2. **Creación de un dataset robusto:**
   - Se consolidó un dataset con más de 17.9 millones de registros. Se incluyeron métricas avanzadas como promedios móviles.

3. **Automatización de procesos:**
   - Se implementaron flujos eficientes de extracción, consolidación y preprocesamiento de datos, aprovechando técnicas de procesamiento paralelo.

4. **Despliegue funcional:**
   - El modelo fue desplegado con éxito en un entorno de prueba mediante FastAPI y visualizado interactivamente con Folium.

5. **Impacto tangible en los sectores clave:**
   - La herramienta desarrollada tiene aplicaciones directas en meteorología, agricultura, gestión de riesgos, y otros sectores.

## Conclusiones Finales y Recomendaciones para Futuros Proyectos

### Conclusiones Finales

El proyecto de predicción de precipitaciones utilizando redes neuronales profundas logró:
- **Precisión:** Métricas de referencia satisfactorias y resultados consistentes.
- **Relevancia práctica:** Beneficiar directamente a stakeholders mediante una herramienta escalable y aplicable.
- **Robustez metodológica:** Combinar técnicas avanzadas de preprocesamiento, modelamiento y despliegue.


## Agradecimientos

- Agradecimientos al equipo de trabajo y a los colaboradores que hicieron posible este proyecto.
- Agradecimientos especiales a los patrocinadores y financiadores del proyecto.
