import pandas as pd
import numpy as np

def imputacion_anios(df):
    """
    rellena 'year_of_release' datos faltantes usando la moda
    del mismo juego en otras plataformas
    luego elimina las filas que aún queden con anio nulo
    """
    print("Iniciando imputación de 'year_of_release'...")
    
    df_imputado = df.copy()
    
    df_imputado["year_of_release"] = df_imputado.groupby("videogame_names")["year_of_release"].transform(
        lambda x: x.fillna(x.mode().iloc[0]) if not x.mode().empty else x
    )
    
    print("Eliminando filas nulas restantes de 'year_of_release'...")
    
    filas_antes = len(df_imputado)
    
    df_limpio = df_imputado.dropna(
        subset="year_of_release", 
        how="all"
    ).reset_index(drop=True)
    
    filas_despues = len(df_limpio)
    
    print(f"Filas eliminadas en este paso: {filas_antes - filas_despues}")
    
    return df_limpio



def rellenar_valores_mediana(serie_scores):
    """
    función adicional: recibe un Series de puntuaciones de un juego
    calcula la mediana (en caso de que exista) y la usa para rellenar los nulos
    """
    
    # calcula mediana solo de valores que existen
    mediana = serie_scores.dropna().median()
    
    # revisa si la mediana es número válido
    # si serie esta vacía, la mediana será NaN
    if pd.notna(mediana):
        return serie_scores.fillna(mediana)
    else:
        return serie_scores


def imputacion_scores(df):
    """
    imputa 'user_score' y 'critic_score' basándose en la mediana
    de las puntuaciones de ese mismo juego en otras plataformas.
    elimina las filas que no pudieron ser imputadas
    """
    print("Iniciando imputación de 'user_score'...")
    
    # evita warnings y errores futuros
    df_imputado = df.copy()
    
    filas_iniciales_user_score = len(df_imputado["user_score"])
    
    # imputar user_score
    df_imputado["user_score"] =  df_imputado.groupby("videogame_names")["user_score"].transform(
        rellenar_valores_mediana
    )
    
    filas_finales_user_score = len(df_imputado["user_score"])
    
    # print(f"Imputación de 'user_score' terminada, filas rellenadas: {filas_finales_user_score - filas_iniciales_user_score}")
    
    # imputar critic_score
    print("Iniciando imputación de 'critic_score'...")
    
    filas_iniciales_critic_score = len(df_imputado["critic_score"])

    df_imputado["critic_score"] =  df_imputado.groupby("videogame_names")["critic_score"].transform(
        rellenar_valores_mediana
    )
    
    filas_finales_critic_score = len(df_imputado["critic_score"])
    
    # print(f"Imputación de 'critic_score' terminada, filas rellenadas: {filas_finales_critic_score - filas_iniciales_critic_score}")
    
    # eliminar filas restantes
    print("Eliminando filas restantes con 'critic_score' o 'user_score' nulos...") 
    filas_antes = len(df_imputado)
    
    df_limpio = df_imputado.dropna(
        subset=["critic_score", "user_score"], 
        how="any"
    ).reset_index(drop=True)
    
    filas_despues = len(df_limpio)
    
    print(f"Filas eliminadas en este paso - {filas_antes - filas_despues}")
    
    return df_limpio
    