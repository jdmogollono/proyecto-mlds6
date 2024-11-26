from data_dictionaries import create_data_dictionaries

def main():
    # Ejecutar el pipeline completo y obtener los diccionarios de datos
    data_dictionaries = create_data_dictionaries()

  print(f"Se han creado {len(data_dictionaries)} registros en los diccionarios de datos.")

if __name__ == "__main__":
    main()
