import pandas as pd
import numpy as np

def limpieza_nombres_columnas(df):
    """
    toma un df, renombra las columnas específicas y luego
    convierte todos los nombres de la columna en minúsculas
    """
    print("Iniciando limpieza de nombres de columnas...")
    
    df_renombrado = df.rename(
        columns={
            "Name": "Videogame_Names", 
            "Rating": "Rating_ESRB"
        }
    )
    
    df_renombrado.columns = df_renombrado.columns.str.lower()
    
    print("Nombres de columnas limpias.")
    
    return df_renombrado



def convertir_anio_int(df):
    """
    convierte 'year_of_release' de float64 a Int64
    """
    print("Convirtiendo 'year_of_release' a Int64...")
    
    df["year_of_release"] = df["year_of_release"].astype("Int64")
    
    return df


def limpieza_user_score_tbd(df):
    """
    reemplaza el valor 'tbd' (to be determined) por NaN
    y convierte la columna a tipo numérico (float)
    """
    print("Limpiando 'user_score' (reemplazando 'tbd' por NaN)...")
    
    df["user_score"] = df["user_score"].replace("tbd", np.nan)
    df["user_score"] = df["user_score"].astype("float64")
    
    return df


def eliminar_filas_info_faltantes(df):
    """
    elimina filas que no contienen información 
    en la mayoría de columnas 
    primero ('videogame_names' y 'genre')
    de ahí ("year_of_release", "critic_score", "user_score", "rating_esrb")
    """
    print("Iniciando eliminación de filas con información faltante...")
    
    df_limpio = df.dropna(
        subset=["videogame_names", "genre"], 
        how="all"
    )
    
    df_limpio = df_limpio.dropna(
        subset=["year_of_release", "critic_score", "user_score", "rating_esrb"], 
        how="all"
    )
    
    df_limpio = df_limpio.reset_index(drop=True)
    
    print(f"Las filas han sido eliminadas. Tamaño del DataFrame antes: {len(df)} - después {len(df_limpio)}.")
    
    return df_limpio


def rellenar_valores_esrb(df):
    """
    en la columna 'rating_esrb' rellena los NaNs
    con RP (Rating Pending), asumiendo que si no hay valor
    está pendiente la calificación
    """
    print("Iniciando limpieza de 'NaN' en 'rating_esrb' con valor 'RP'...")
    
    df["rating_esrb"] = df["rating_esrb"].fillna("RP")
    
    return df