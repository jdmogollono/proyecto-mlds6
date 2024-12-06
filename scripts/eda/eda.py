import os
import missingno as msno
import matplotlib.pyplot as plt
import seaborn as sns

# Definir la ruta de la carpeta de datos
WORKSPACE = os.path.abspath(os.path.join(os.getcwd(), '../../'))
DATA_FOLDER = os.path.join(WORKSPACE, 'data')

print("Workspace:", WORKSPACE)
print("Data folder:", DATA_FOLDER)
# Ajustar directorios de trabajo

def resumen_general(df):
    print("Número de documentos en el dataset:")
    print(len(df))

    print("\nTipos de datos por columna:")
    print(df.dtypes)

    file_path = os.path.join(DATA_FOLDER, 'data.csv')
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    print(f"\nTamaño del dataset: {file_size_mb:.2f} MB")

def datos_faltante(df):
    print("Visualización de datos faltantes:")
    msno.matrix(df)
    plt.show()
    
    missing_percentage = df.isnull().mean() * 100

    # Mostrar el porcentaje de valores faltantes de cada columna
    print("Porcentaje de datos faltantes por columna:")
    print(missing_percentage)
    
    # Calcular la cantidad de datos faltantes por columna
    missing_count = df.isnull().sum()

    # Mostrar la cantidad de datos faltantes por columna
    print("Cantidad de datos faltantes por columna:")
    print(missing_count)

def distribucion_variable_objetivo(df):
    # Guardar la gráfica como imagen
    plt.figure(figsize=(10, 6))
    sns.histplot(df['PTPM_CON'], bins=30, kde=True, color='blue')

    # Títulos y etiquetas
    plt.title('Distribución de la variable PTPM_CON', fontsize=16)
    plt.xlabel('PTPM_CON', fontsize=14)
    plt.ylabel('Frecuencia', fontsize=14)

    # Guardar la gráfica como PNG
    plt.savefig('PTPM_CON_Distribucion.png', dpi=300, bbox_inches='tight')

    # Mostrar la gráfica (opcional)
    plt.show()

def estadisticas_descriptivas(df):
    # Calcular estadísticas descriptivas para las variables seleccionadas
    variables = [
        'HR_CAL_MN_D', 'HR_CAL_MX_D', 'NV_MEDIA_D',
        'NV_MN_D', 'NV_MX_D', 'TMN_CON', 'TMX_CON'
    ]

    # Obtener estadísticas descriptivas
    descriptive_stats = df[variables].describe()

    # Mostrar las estadísticas descriptivas
    print(descriptive_stats)
    
    print(df['PTPM_CON'].describe())

def distribucion_variables(df):
    # Filtrar el DataFrame eliminando las columnas DOY, MOY, WOY, Fecha y CodigoEstacion
    df_analisis = df.drop(columns=['DOY', 'MOY', 'WOY', 'Fecha', 'CodigoEstacion'], errors='ignore')

    # Variable objetivo
    target_column = 'PTPM_CON'

    if target_column in df_analisis.columns:
        print(f"La variable objetivo '{target_column}' está presente en el dataset.")
        print(f"La variable '{target_column}' es continua.")

        # Graficar la distribución de la variable objetivo
        sns.histplot(df_analisis[target_column], kde=True)
        plt.title(f"Distribución de la variable '{target_column}'")
        plt.show()

    # Identificar las variables adicionales
    additional_columns = [col for col in df_analisis.columns if col != target_column]

    if additional_columns:
        print("\nEl conjunto de datos cuenta con las siguientes variables adicionales:")
        print(additional_columns)

        # Análisis descriptivo de las variables adicionales
        print("\nAnálisis descriptivo de las variables adicionales:")
        print(df_analisis[additional_columns].describe())

        # Graficar la distribución de las variables adicionales
        for col in additional_columns:
            if df_analisis[col].dtype == 'object':
                sns.countplot(x=df_analisis[col])
            else:
                sns.histplot(df_analisis[col], kde=True)
            plt.title(f"Distribución de la variable '{col}'")
            plt.show()
