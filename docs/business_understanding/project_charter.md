# Project Charter - Entendimiento del Negocio

## Nombre del Proyecto

**Predicción de Precipitaciones Utilizando Deep Learning**

## Objetivo del Proyecto

Desarrollar un modelo de predicción de precipitaciones basado en técnicas de Deep Learning, específicamente utilizando redes neuronales LSTM, para mejorar la precisión en los pronósticos meteorológicos. Este proyecto es crucial para ayudar a instituciones meteorológicas, gobiernos, sector agrícola, compañías de seguros y empresas energéticas en la planificación, gestión de riesgos y toma de decisiones informadas.

## Alcance del Proyecto

### Incluye:

- **Descripción de los datos disponibles**: Utilización de datos históricos de precipitaciones y variables meteorológicas recopilados por estaciones del IDEAM desde el año 2000 hasta 2023. Los datos incluyen información geográfica (latitud, longitud, altitud) y temporal.

- **Descripción de los resultados esperados**: Desarrollo de un modelo predictivo que utilice LSTM para anticipar niveles de precipitación en puntos geográficos específicos con alta precisión.

- **Criterios de éxito del proyecto**:
  - El modelo debe superar el rendimiento de modelos tradicionales como ARIMA.
  - Capacidad de generalización del modelo en datos de prueba.
  - Entrega de un informe y presentación final que detallen la metodología y resultados obtenidos.

### Excluye:

- **Desarrollo de una interfaz de usuario o API para clientes finales**: El proyecto se centrará en el desarrollo del modelo y no en la creación de aplicaciones o interfaces para su uso directo.

- **Integración con sistemas existentes de los beneficiarios**: No se realizará la adaptación o integración del modelo en plataformas o sistemas actuales de los stakeholders.

- **Consideración de variables externas no incluidas en el dataset**: No se incorporarán datos adicionales como fenómenos climáticos globales o información satelital que no formen parte del conjunto de datos original.

## Metodología

Se adoptará una metodología estructurada que incluye:

1. **Entendimiento del negocio y carga de datos**: Comprender las necesidades y objetivos del proyecto, y obtener los datos necesarios del IDEAM.

2. **Preprocesamiento y análisis exploratorio**: Limpieza y transformación de los datos, análisis descriptivo y visualización para identificar patrones y anomalías.

3. **Modelamiento y extracción de características**: Diseño e implementación de modelos LSTM, incluyendo la ingeniería de características y selección de hiperparámetros.

4. **Entrenamiento y validación**: Entrenamiento de los modelos, optimización y evaluación utilizando métricas como MAE y RMSE.

5. **Evaluación y entrega final**: Interpretación de resultados, documentación y presentación de hallazgos, incluyendo recomendaciones para futuras mejoras.

## Cronograma

| No. | Actividad                                          | Detalles                                                            | Fecha         |
|-----|----------------------------------------------------|---------------------------------------------------------------------|---------------|
| 1   | **Entendimiento del negocio y carga de datos**     | - Código de la carga de datos                                        | Del 8 al 15 de noviembre       |
|     |                                                    | - Marco de proyecto                                                  | Del 8 al 15 de noviembre        |
|     |                                                    | - Creación de diccionarios de datos                                  | Del 8 al 15 de noviembre        |
| 2   | **Preprocesamiento, análisis exploratorio**        | - Código del preprocesamiento y análisis exploratorio                | Del 15 al 22 de noviembre       |
|     |                                                    | - Definición de los datos                                            | Del 15 al 22 de noviembre       |
|     |                                                    | - Reporte del resumen de los datos                                   | Del 22 al 28 de noviembre       |
| 3   | **Modelamiento y extracción de características**   | - Código de extracción de características                             | Del 28 noviembre al 5 de diciembre      |
|     |                                                    | - Código del modelamiento                                            | Del 28 noviembre al 5 de diciembre       |
|     |                                                    | - Reporte de la línea base de los modelos                            | Del 28 noviembre al 5 de diciembre       |
|     |                                                    | - Reporte del modelo final                                           | Del 5 al 12 de diciembre       |
| 4   | **Despliegue**                                     | - Código del despliegue                                              | Del 12 al 19 de diciembre       |
|     |                                                    | - Documentación del despliegue                                       | Del 12 al 19 de diciembre       |
|     |                                                    | - Documentación de la infraestructura                                | Del 12 al 19 de diciembre       |
| 5   | **Evaluación y entrega final**                     | - Código de evaluación del modelo                                    | Del 19 al 21 de diciembre       |
|     |                                                    | - Interpretación de los resultados                                   | Del 19 al 21 de diciembre       |
|     |                                                    | - Video con presentación del proyecto                                | Del 19 al 21 de diciembre       |


*Nota: Las fechas son estimadas y pueden ajustarse según el progreso del proyecto.*

## Equipo del Proyecto

- **Líder del proyecto**: *Juan Diego Mogollón Oviedo*
- **Miembros del equipo**:
  - **David Alejandro Pabón Correa**
  - **Juan Diego Mogollón Oviedo**
  - **Cristian Camilo Moreno Valbuena**

## Presupuesto

El proyecto no cuenta con un presupuesto asignado específico. Se utilizarán recursos disponibles y herramientas de código abierto para su desarrollo, optimizando al máximo los recursos existentes.

## Stakeholders

- **Instituciones meteorológicas y ambientales**: Necesitan modelos predictivos precisos para anticipar fenómenos climáticos.

- **Gobiernos locales y autoridades de gestión de emergencias**: Requieren pronósticos para gestionar riesgos de inundaciones y planificar infraestructuras.

- **Sector agrícola**: Dependiente de las precipitaciones para la planificación de cultivos y riego.

- **Compañías de seguros**: Utilizan predicciones para ajustar pólizas y calcular riesgos asociados a fenómenos climáticos.

- **Sector energético**: Empresas hidroeléctricas y de energías renovables que necesitan optimizar la producción basada en recursos hídricos.

**Relación con los stakeholders**:

El proyecto busca proporcionar una herramienta que mejore la precisión en la predicción de precipitaciones, lo que beneficiará directamente las operaciones y planificación de los stakeholders.

**Expectativas de los stakeholders**:

- **Precisión**: Obtener predicciones confiables y precisas de las precipitaciones futuras.

- **Aplicabilidad**: Que el modelo sea aplicable a diferentes regiones y escalable.

- **Utilidad práctica**: Mejorar la toma de decisiones y gestión de recursos en sus respectivos sectores.

