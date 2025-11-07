# libreria general
import os
# funciones de los scripts
from scripts.data_loader import cargar_datos
from scripts.data_cleaning import (
    limpieza_nombres_columnas, 
    convertir_anio_int, 
    limpieza_user_score_tbd, 
    eliminar_filas_info_faltantes, 
    rellenar_valores_esrb
)
from scripts.data_imputation import (
    imputacion_anios, 
    imputacion_scores
)
from scripts.data_new_features import (
    crear_ventas_totales, 
    crear_generacion_por_plataforma,
    crear_clasificacion_user_score
)
from scripts.data_saving import guardar_datos_limpios

# ruta absoluta de la carpeta donde está el script (.../scripts/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# construir la ruta del archivo csv de data
DATA_PATH = os.path.join(SCRIPT_DIR, ".", "data", "games.csv")

# nueva ruta de salida
PROCESSED_DATA_PATH = os.path.join(SCRIPT_DIR, "data", "processed", "games_clean.csv")

# ¿este archivo se está ejecutando directamente por el usuario o está siendo importado por otro script?
if __name__ == "__main__":
    # indica dónde está el script actual
    print(f"Ejecutando script desde: {os.path.abspath(__file__)}")
    
    # llama a la función de arriba para cargar el csv
    dataframe_juegos = cargar_datos(DATA_PATH)
    
    if dataframe_juegos is not None:
        # MÓDULO LIMPIEZA DE DATOS
        print("\n---INICIANDO LIMPIEZA DE DATOS---")
        
        df_limpio = limpieza_nombres_columnas(dataframe_juegos)
        df_limpio = convertir_anio_int(df_limpio)
        df_limpio = limpieza_user_score_tbd(df_limpio)
        df_limpio = eliminar_filas_info_faltantes(df_limpio)
        df_limpio = rellenar_valores_esrb(df_limpio)
        
        print("\n---LIMPIEZA DE DATOS TERMINADO---")
        
        # MÓDULO IMPUTACIÓN DE DATOS
        print("\n---INICIANDO IMPUTACIÓN DE DATOS---")
        df_procesado = imputacion_anios(df_limpio)
        df_procesado = imputacion_scores(df_procesado)
        
        print("\n---IMPUTACIÓN DE DATOS TERMINADO---")
        
        # MÓDULO NUEVAS COLUMNAS 
        print("\n---INICIANDO AGREGACIÓN NUEVAS COLUMNAS---")
        df_final = crear_ventas_totales(df_procesado)
        df_final = crear_generacion_por_plataforma(df_final)
        df_final = crear_clasificacion_user_score(df_final)
        
        print("\n---AGREGACIÓN NUEVAS COLUMNAS TERMINADO---")
        
        # GUARDAR DATOS
        guardar_datos_limpios(df_final, PROCESSED_DATA_PATH)
        
        # AQUÍ TERMINÓ EL PIPELINE DE LIMPIEZA
        print("\n---PIPELINE TERMINADO---")
        
        print("\n---Información del DataFrame---")
        df_final.info(show_counts=True)
        
    else: 
        print("Ha ocurrido un error en la carga de datos")