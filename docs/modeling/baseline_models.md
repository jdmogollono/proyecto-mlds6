# Reporte del Modelo Baseline

Este documento presenta el análisis del modelo baseline utilizado como referencia inicial para la predicción de precipitaciones. El objetivo es establecer un punto de partida cuantitativo que permita evaluar el desempeño de los modelos entrenados a partir del ajuste de parámetros.

## Descripción del modelo

El modelo desarrollado se basa en una red neuronal profunda (DNN) entrenada para predecir niveles de precipitación. Se ha elegido esta arquitectura por su capacidad para modelar relaciones complejas entre múltiples variables meteorológicas y la precipitación. La construcción del modelo incluyó:

- **Capa de entrada**: Recibe variables meteorológicas normalizadas y codificadas (incluyendo la estación como variables One-Hot).
- **Capas ocultas**: Varias capas densas con función de activación Leaky ReLU, número de neuronas y tasa de Dropout ajustadas mediante la búsqueda de hiperparámetros.
- **Capa de salida**: Una neurona con activación sigmoidal que produce un valor escalado entre 0 y 1, el cual se reescala posteriormente para obtener la precipitación en sus unidades originales.

## Variables de Entrada

Las variables de entrada incluyen indicadores meteorológicos históricamente recopilados por estaciones del IDEAM. Entre estas variables se encuentran:

- Latitud, longitud, altitud de la estación.
- Variables meteorológicas normalizadas (ej. precipitación, humedad relativa, temperatura, nivel del agua, etc.).
- Identificador de la estación codificado mediante One-Hot Encoding, permitiendo al modelo diferenciar información geográfica y contextual.

  Todos estos valores se escalan en función del máximo observado por estación para mejorar la estabilidad del entrenamiento.
## Variable Objetivo

La variable objetivo es la precipitación desplazada en el tiempo ("PTPM_CON_shifted"), que representa el nivel de precipitación futura a predecir en milímetros. El objetivo del modelo es anticipar este valor con la mayor precisión posible, teniendo en cuenta las variables de entrada históricas y las características de la estación.

## Evaluación del Modelo

Para evaluar el modelo, se utilizaron las siguientes métricas:

- **MAE (Mean Absolute Error)**: Promedio de las diferencias absolutas entre las predicciones y los valores reales. Un MAE más bajo indica mejor rendimiento. El MAE es una métrica sencilla y fácilmente interpretable. Su fórmula es:  
$$\text{MAE} = \frac{1}{n}\sum_{i=1}^{n}|y_i - \hat{y}_i|\$$  
donde:
- $\( n \)$ es el número total de muestras.
- $\( y_i \)$ es el valor real.
- $\( \hat{y}_i \)$ es el valor predicho por el modelo.

Un MAE más bajo indica que, en promedio, las predicciones se desvían menos de los valores reales. Al estar en las mismas unidades que la variable objetivo, es sencillo comprender su significado en el contexto de la predicción de precipitaciones.

- **Función de pérdida personalizada**: Combina MSE, MAE y una penalización adicional por errores grandes, buscando reducir tanto los errores promedio como las desviaciones excesivas.


$$\text{loss}(y_{\text{true}}, y_{\text{pred}}) = \frac{1}{n} \sum_{i=1}^{n} \Big[ 0.6 \cdot (y_{\text{true},i} - y_{\text{pred},i})^2 + 0.2 \cdot |y_{\text{true},i} - y_{\text{pred},i}| + 0.2 \cdot \mathbb{I}(|y_{\text{true},i} - y_{\text{pred},i}| > \text{threshold}) \cdot 2 \cdot |y_{\text{true},i} - y_{\text{pred},i}| \Big]$$
Donde:

$$\mathbb{I}(x > \text{threshold}) =
\begin{cases} 
1, & \text{si } x > \text{threshold}, \\
0, & \text{en otro caso}.
\end{cases}$$

En el código se emplea una función de pérdida personalizada que combina diferentes componentes para penalizar en mayor medida los errores grandes. Esta función integra un factor adicional que se activa cuando el error supera un cierto umbral. Esto permite que, además de castigar de forma promedio a los errores, se dé un peso mayor a aquellos casos donde la predicción se aleja significativamente del valor real.

La idea detrás de esta combinación es balancear la sensibilidad del modelo ante errores pequeños (al estilo MSE/MAE) con una penalización específica para grandes desviaciones. De esta forma, el modelo no solo busca reducir el error medio, sino también minimizar la frecuencia e impacto de grandes errores.

## Búsqueda de Hiperparámetros

Durante el desarrollo del modelo, se realizó un proceso de optimización de hiperparámetros utilizando **KerasTuner**. Esta herramienta permitió explorar diferentes configuraciones para encontrar aquella que ofreciera el mejor desempeño sobre el conjunto de validación.

### Hiperparámetros y Rango de Valores

A continuación se presenta una tabla que describe los hiperparámetros optimizados durante el proceso de búsqueda, incluyendo sus rangos y una breve descripción de su función en el modelo:

| Hiperparámetro  | Rango de Valores                       | Descripción                                                                                     |
|-----------------|-----------------------------------------|-------------------------------------------------------------------------------------------------|
| units_1          | 64 a 256 (incrementos de 32)           | Número de neuronas en la primera capa oculta; controla la capacidad de representación del modelo. |
| units_2          | 32 a 128 (incrementos de 32)           | Número de neuronas en la segunda capa oculta; refina la representación de las características.    |
| units_3          | 16 a 64 (incrementos de 16)            | Número de neuronas en la tercera capa oculta; ajusta la complejidad final del modelo.             |
| leaky_relu_1     | 0.01 a 0.3 (incrementos de 0.05)       | Pendiente negativa de la función Leaky ReLU en la primera capa; evita saturación de gradiente.     |
| leaky_relu_2     | 0.01 a 0.3 (incrementos de 0.05)       | Pendiente negativa de la función Leaky ReLU en la segunda capa; mantiene gradientes estables.      |
| leaky_relu_3     | 0.01 a 0.3 (incrementos de 0.05)       | Pendiente negativa de la función Leaky ReLU en la tercera capa; busca un balance adecuado.         |
| dropout_1        | 0.1 a 0.5 (incrementos de 0.1)         | Tasa de dropout en la primera capa; ayuda a prevenir el sobreajuste.                              |
| dropout_2        | 0.1 a 0.5 (incrementos de 0.1)         | Tasa de dropout en la segunda capa; reduce la co-adaptación de las neuronas.                      |
| learning_rate     | {1e-2, 1e-3, 1e-4}                   | Tasa de aprendizaje del optimizador Adam; determina la velocidad de ajuste de pesos.              |

### Mejores Hiperparámetros

Después de realizar la búsqueda con KerasTuner, la configuración óptima de hiperparámetros encontrada fue:

| Hiperparámetro | Valor Óptimo |
|----------------|--------------|
| units_1        | 96           |
| leaky_relu_1    | 0.11         |
| dropout_1       | 0.1          |
| units_2        | 64           |
| leaky_relu_2    | 0.21         |
| dropout_2       | 0.1          |
| units_3        | 32           |
| leaky_relu_3    | 0.06         |
| learning_rate   | 0.0001       |
Interpretación:

Esta pérdida personalizada obliga al modelo a esforzarse no solo en reducir el error general, sino también en evitar predicciones muy desfasadas.
El objetivo final es obtener mayor estabilidad y robustez en la predicción, mejorando la calidad del pronóstico en escenarios críticos.


## Resultados

A partir del proceso de búsqueda de hiperparámetros y entrenamiento del modelo, se obtuvieron los siguientes resultados principales:

| Métrica              | Conjunto        | Valor     |
|----------------------|-----------------|-----------|
| Mejor MAE de Validación | Validación      | ~0.04418   |
| Mejor Conjunto de Hiperparámetros | -             | `units_1=96, leaky_relu_1=0.11, dropout_1=0.1, units_2=64, leaky_relu_2=0.21, dropout_2=0.1, units_3=32, leaky_relu_3=0.06, learning_rate=0.0001` |

Estos resultados muestran que el modelo, tras ajustar sus hiperparámetros, alcanza un MAE de aproximadamente 0.044 en el conjunto de validación (en escala normalizada), lo cual se considera una mejora notable con respecto a un modelo baseline o no optimizado.
## Conclusiones
### Rendimiento General
El modelo baseline establece una referencia inicial de desempeño y permite identificar tendencias generales en los datos. Sin embargo, sus limitaciones destacan la necesidad de modelos más avanzados para lograr predicciones precisas y útiles en contextos prácticos.

### Fortalezas
- **Rapidez en el desarrollo:** El modelo baseline es fácil de implementar y ofrece resultados rápidos para una evaluación inicial.
- **Estabilidad:** Los resultados son consistentes y predecibles, proporcionando un marco confiable para comparación.
- **Interpretabilidad:** Su simplicidad permite analizar los resultados sin dificultad, facilitando la identificación de errores o problemas en los datos.

### Debilidades
- **Capacidad de generalización limitada:** No captura relaciones no lineales o patrones complejos, lo que afecta la precisión de las predicciones.
- **Desempeño moderado:** Las métricas de error indican que el modelo no es adecuado para aplicaciones críticas, como predicciones detalladas de precipitaciones.
- **Subutilización de los datos:** No aprovecha al máximo las características avanzadas del conjunto de datos, lo que reduce su efectividad.

### Posibles Áreas de Mejora
1. **Incorporación de modelos avanzados:**
   - Utilizar arquitecturas de redes neuronales profundas (DNN) o modelos especializados como LSTM para capturar patrones temporales y no lineales.
2. **Optimización de hiperparámetros:**
   - Ajustar los parámetros del modelo para mejorar su desempeño en conjuntos de datos de prueba y validación.
3. **Preprocesamiento mejorado:**
   - Explorar técnicas adicionales de limpieza y transformación de datos para maximizar la calidad de las entradas.
4. **Integración de variables adicionales:**
   - Incluir datos externos relevantes, como información climática global, para enriquecer el contexto predictivo.
5. **Evaluación iterativa:**
   - Comparar continuamente los modelos más avanzados contra el baseline para asegurar mejoras significativas en el rendimiento.
     
## Referencias

Lista de referencias utilizadas para construir el modelo baseline y evaluar su rendimiento.
