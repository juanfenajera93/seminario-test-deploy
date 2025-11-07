import pandas as pd

# creacion de funcion
def cargar_datos(path):
    print(f"Cargando datos desde {path}...")
    
    try:
        games = pd.read_csv(path)
        print("Datos han sido cargados!!!")
        return games
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo en {path}")
        print("Asegurate de tener el archivo en la carpeta 'data'.")
        return None
    except Exception as e:
        print(f"Ocurrió un error inesperado {e}")
        return None
    
