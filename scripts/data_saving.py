import pandas as pd
import os

def guardar_datos_limpios(df, path): 
    """
    guardar el df final en una nueva ruta
    asegurándose de que la carpeta 'processed' exista
    """
    try: 
        print("Se está guardando el archivo final limpio...")
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        df.to_csv(path, index=False)
        
        print("\nArchivo guardado en:")
        print(f"{path}")
        
        return True
    
    except Exception as e:
        print(f"Error al guardar los datos: {e}")
        
        return False