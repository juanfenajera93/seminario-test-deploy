import pandas as pd


def crear_ventas_totales(df):
    """
    crea la columna 'ventas_totales' sumando
    las ventas regionales que hay
    """
    print("Creando la columna 'ventas_totales'...")
    
    df["total_sales"] = df["na_sales"] + df["eu_sales"] + df["jp_sales"] + df["other_sales"]
    
    return df


def asignar_generacion(plataforma):
    """
    función adicional: en base a la plataforma, 
    agrupa en generaciones para reducir la cantidad de 
    datos categóricos
    """ 
    if plataforma in ["NES", "2600", "TG16"]:
        return "3ª Gen"
    elif plataforma in ["SNES", "GEN", "GB", "SCD"]:
        return "4ª Gen"
    elif plataforma in ["PS", "N64", "SAT"]:
        return "5ª Gen"
    elif plataforma in ["PS2", "GC", "XB", "GBA"]:
        return "6ª Gen"
    elif plataforma in ["PS3", "X360", "Wii", "PSP", "DS"]:
        return "7ª Gen"
    elif plataforma in ["PS4", "XOne", "WiiU", "3DS", "PSV"]:
        return "8ª Gen"
    elif plataforma in ["PC"]:
        return "PC"
    else:
        return "Otras/Retro"
    


def crear_generacion_por_plataforma(df):
    """
    usa la función asignar_generacion para crear una nueva 
    columna que se llama gen_platform y así tener nuevas 
    clasificaciones
    """
    print("Creando la columna 'gen_platform'...")
    df_nuevo = df.copy()
    
    df_nuevo["gen_platform"] = df_nuevo["platform"].apply(asignar_generacion)
    
    return df_nuevo


def clasificar_user_score(score):
    """
    función adicional: agrupación de 'user_score' 
    para tener una nueva columna categórica en base 
    a los datos numéricos
    """
    if pd.isnull(score):
        return "Without score"
    elif score >= 8.5:
        return "Excellent"
    elif score >= 7:
        return "Good"
    elif score >= 5.5:
        return "Regular"
    else:
        return "Bad"
    

def crear_clasificacion_user_score(df):
    """
    creación nueva columna 'classification_user_score' en base 
    a los datos numéricos de la columna 'user_score' 
    """
    print("Creando la columna 'classification_user_score'...")
    df_nuevo = df.copy()
    
    df_nuevo["classification_user_score"] = df["user_score"].apply(clasificar_user_score)
    
    return df_nuevo