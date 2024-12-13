# Reporte del Modelo Final

# Informe del Modelo de Predicción de Precipitación Diaria

## **Resumen Ejecutivo**
El modelo desarrollado para predecir valores de precipitación diaria (PTPM_CON) basado en variables climáticas y geográficas alcanzó un desempeño sobresaliente, con un MAE (Error Absoluto Medio) en el conjunto de prueba de **0.0425** y una pérdida total de **0.0144**. Estos resultados reflejan la capacidad del modelo para realizar predicciones precisas, siendo útil para aplicaciones donde la estimación de precipitación es crítica, como la gestión hídrica y la planificación agrícola. La metodología incluyó un ajuste fino de hiperparámetros mediante RandomSearch y la aplicación de un modelo DNN con activaciones LeakyReLU, capas densas optimizadas y una pérdida personalizada para manejar errores grandes.

---

## **Descripción del Problema**
El problema abordado consiste en predecir la precipitación diaria en estaciones climatológicas distribuidas geográficamente. Este problema es fundamental para sectores como el agrícola, el energético, y el manejo de riesgos climáticos, donde contar con predicciones precisas de lluvias es esencial para la toma de decisiones.

- **Contexto:** Las precipitaciones son una variable crítica en estudios hidrológicos y climáticos. En regiones con estaciones de monitoreo, predecir la precipitación basada en variables relacionadas como el nivel promedio del río (NV_MEDIA_D), la altitud, y características temporales puede mejorar significativamente la precisión de los modelos actuales.
- **Objetivos:** El principal objetivo fue construir un modelo capaz de predecir la precipitación diaria a partir de un conjunto de datos históricos, considerando información climática, geográfica y temporal.
- **Justificación:** Un modelo automatizado para este tipo de predicciones puede reducir el tiempo y esfuerzo necesarios para análisis manuales, permitiendo una mejor planificación basada en datos.

---

## **Descripción del Modelo**
Se utilizó un modelo de redes neuronales profundas (DNN) con las siguientes características:

- **Arquitectura:** 
  - **Entrada:** 49 características (incluyendo variables escaladas y codificadas).
  - **Capas ocultas:**
    1. 96 neuronas con LeakyReLU (alpha=0.11) y Dropout (10%).
    2. 64 neuronas con LeakyReLU (alpha=0.21) y Dropout (10%).
    3. 32 neuronas con LeakyReLU (alpha=0.06).
  - **Salida:** Una única neurona con activación sigmoide para regresión.
- **Metodología:**
  - **Preprocesamiento:**
    - Variables continuas escaladas por estación (`CodigoEstacion`) para manejar variaciones específicas.
    - Codificación one-hot de las estaciones.
  - **Optimización de hiperparámetros:** RandomSearch con `val_mae` como métrica objetivo.
  - **Función de pérdida:** Una modificación de la pérdida Huber para penalizar errores grandes.
- **Técnicas adicionales:**
  - Regularización con Dropout para prevenir sobreajuste.
  - Optimización mediante el optimizador Adam con una tasa de aprendizaje ajustada a 0.0001.

---

## **Evaluación del Modelo**
La evaluación del modelo incluyó conjuntos separados para entrenamiento (80%), validación (10%), y prueba (10%).

- **Métricas utilizadas:**
  - **MAE (Mean Absolute Error):** Mide el error promedio entre las predicciones y los valores reales.
  - **Pérdida personalizada:** Combina MSE y MAE con penalización para errores grandes.
- **Resultados:**
  - **Conjunto de entrenamiento:** Indicó una convergencia adecuada sin signos de sobreajuste.
  - **Conjunto de validación:** Alcanzó un MAE de 0.0443 en la última época, validando la capacidad del modelo para generalizar.
  - **Conjunto de prueba:** Logró un MAE de 0.0425, destacando la robustez del modelo.

- **Interpretación:** El MAE obtenido demuestra que el modelo puede predecir precipitaciones con un error promedio de 0.0425, lo cual es significativo dado el rango y la naturaleza de los datos. La combinación de técnicas de preprocesamiento, ajuste de hiperparámetros y regularización permitió optimizar el desempeño del modelo para datos geográficamente diversos.

---

## **Conclusiones y Recomendaciones**

### **Conclusiones**
1. El modelo de redes neuronales profundas (DNN) demostró un alto desempeño, especialmente en la predicción de precipitaciones en estaciones climatológicas geográficamente diversas.
2. La inclusión de técnicas como el escalado por estación y la pérdida personalizada mejoró significativamente la capacidad del modelo para manejar datos desbalanceados o variables críticas.
3. Los resultados obtenidos son prometedores para aplicaciones prácticas, como la gestión hídrica, predicción de riesgos climáticos y planificación agrícola.

### **Recomendaciones**
1. **Exploración de Modelos Alternativos:** Aunque el modelo DNN ofrece resultados sólidos, explorar enfoques como modelos de grafos (GNN) podría capturar mejor las relaciones espaciales entre estaciones.
2. **Validación con Nuevos Datos:** Evaluar el modelo con datos recientes o en nuevas regiones para garantizar su capacidad de generalización.
3. **Optimización del Preprocesamiento:** Considerar técnicas adicionales de ingeniería de características para identificar correlaciones no lineales entre las variables.
4. **Despliegue e Integración:** Implementar el modelo en sistemas operativos con pipelines de datos automatizados para facilitar su uso en tiempo real.
5. **Monitorización Continua:** Establecer procesos para monitorizar la precisión del modelo y ajustarlo en función de cambios climáticos o nuevos patrones en los datos.

---


## Referencias

En esta sección se deben incluir las referencias bibliográficas y fuentes de información utilizadas en el desarrollo del modelo.
