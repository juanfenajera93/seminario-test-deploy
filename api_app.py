import pandas as pd
import os
import joblib
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional, List


# las rutas para cargar el modelo y el encoder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENCODER_PATH = os.path.join(BASE_DIR, "models", "onehot_encoder.joblib")
MODEL_PATH = os.path.join(BASE_DIR, "models", "lgbm_regressor_default.joblib")
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "games_clean.csv")

modelo = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)
games_clean = pd.read_csv(DATA_PATH)

app = FastAPI(title="API de Videojuegos")

class FeaturesInput(BaseModel):
    platform: str 
    genre: str
    rating_esrb: str
    gen_platform: str
    classification_user_score: str 
    year_of_release: int
    user_score: float
    critic_score: float
    
    class Config: 
        json_schema_extra = {
            "example": {
                "platform": "PS4", 
                "genre": "Action", 
                "rating_esrb": "M", 
                "gen_platform": "8ª Gen", 
                "classification_user_score": "Good", 
                "year_of_release": 2016, 
                "user_score": 8.1, 
                "critic_score": 86.0 
            }
        }
        
@app.post(
    "/ml/predict", 
    description="Endpoint de ML. Recibe las 8 variables de un videojuego y devuelve la predicción de ventas globales en millones."
)
def predict_sales(input_data: FeaturesInput):
    
    # serializa los datos almacenados y los convierte en un objeto de Pydantic a un diccionario
    input_dict = input_data.model_dump()
    
    # definir las columnas en el orden exacto de arriba
    col_categoricas = ["platform", "genre", "rating_esrb", "gen_platform", "classification_user_score"]
    col_numericas = ["year_of_release", "user_score", "critic_score"]
    
    # convertir a dataframe de una sola fila
    input_df_cat = pd.DataFrame([input_dict], columns=col_categoricas)
    input_df_num = pd.DataFrame([input_dict], columns=col_numericas)
    
    try: 
        input_cat_encoded = encoder.transform(input_df_cat)
        nuevas_columnas_encoded = encoder.get_feature_names_out(col_categoricas)
                
        input_df_encoded = pd.DataFrame(input_cat_encoded, columns=nuevas_columnas_encoded)
                
        X_final = pd.concat([input_df_num.reset_index(drop=True), input_df_encoded.reset_index(drop=True)], axis=1)
                
        prediccion = modelo.predict(X_final)
        prediccion_valor = prediccion[0]
                
        return {
            "prediccion_ventas_globales_millones": round(prediccion_valor, 2)
        }
                    
    except Exception as e:
        return {"error": str(e)}
    
    
# endpoints del EDA
@app.get(
    "/eda/filters", 
    description="Devuelve las listas de opciones únicas para todos los filtros del dashboard."
)
def get_options_filters():
    if games_clean.empty:
        return {"error": "Datos no cargados en la API"}
    
    generos_lista = sorted(games_clean["genre"].unique())
    min_year = int(games_clean["year_of_release"].min())
    max_year = int(games_clean["year_of_release"].max())
    
    platform_options = sorted(games_clean["platform"].unique())
    genre_options =  sorted(games_clean["genre"].unique())
    rating_options = sorted(games_clean["rating_esrb"].unique())
    gen_platform_options = sorted(games_clean["gen_platform"].unique())
    class_score_options = sorted(games_clean["classification_user_score"].unique())
    
    return {
        "generos": generos_lista, 
        "min_year": min_year, 
        "max_year": max_year, 
        "platforms": platform_options,
        "ratings":rating_options, 
        "gen_platforms": gen_platform_options, 
        "class_scores": class_score_options, 
        "genre": genre_options
    }
    
@app.get(
    "/eda/data_specific_filters", 
    description="Filtra los datos del df y devuelve los KPIs y datos para los gráficos"
)
def get_data_eda(
    generos: List[str] = Query(None),
    anio_inicio: int = 1980, 
    anio_fin: int = 2016
):
    if games_clean.empty:
        return {"error": "Datos no cargados en la API"}
    
    if generos: 
        filtro_genero = games_clean["genre"].isin(generos)
        filtro_anio = (games_clean["year_of_release"] >= anio_inicio) & (games_clean["year_of_release"] <= anio_fin)
        games_filtrado = games_clean[filtro_genero & filtro_anio]
        
    else:
        # si no se selecciona ninguno, se crea un df vacío para evitar errores
        games_filtrado = pd.DataFrame(columns=games_clean.columns)
        
    if not games_filtrado.empty:
        # KPIs
        # métricas para mostrar valores numéricos grandes
        total_sales_global = games_filtrado["total_sales"].sum()
        total_videogames = games_filtrado["videogame_names"].count()
        total_platforms = games_filtrado["platform"].nunique()
        avg_critic_score = games_filtrado["critic_score"].mean()
        avg_user_score = games_filtrado["user_score"].mean()
    else:
        total_sales_global = 0
        total_videogames = 0
        total_platforms = 0
        avg_critic_score = 0
        avg_user_score = 0
        
    kpis = {
        "total_sales_global": f"${total_sales_global:,.0f} M", 
        "total_videogames": f"{total_videogames}", 
        "total_platforms": total_platforms, 
        "avg_critic_score": f"{avg_critic_score:,.1f}",
        "avg_user_score": f"{avg_user_score:,.1f}"
    }
    
    top_10_platforms_df = games_filtrado.groupby("platform")["total_sales"].sum().nlargest(10).reset_index()
    
    datos_top_platforms = top_10_platforms_df.to_dict("records")
    
    total_na = games_filtrado["na_sales"].sum()
    total_eu = games_filtrado["eu_sales"].sum()
    total_jp = games_filtrado["jp_sales"].sum()
    total_other = games_filtrado["other_sales"].sum()
    
    datos_treemap = [
        {"region": "Norteamérica", "ventas": total_na},
        {"region": "Europa", "ventas": total_eu}, 
        {"region": "Japón", "ventas": total_jp}, 
        {"region": "Otros", "ventas": total_other} 
    ]
    
    sales_per_region_df = games_clean.groupby("year_of_release")[
        ["na_sales", "eu_sales", "jp_sales", "other_sales"]
    ].sum().reset_index()
    
    sales_per_region_melt_df = sales_per_region_df.melt(
        id_vars="year_of_release", 
        value_vars=["na_sales", "eu_sales", "jp_sales", "other_sales"], 
        var_name="region", 
        value_name="sales"
    )
    
    datos_graf_ventas_totales = sales_per_region_melt_df.to_dict("records")
    
    return {
        "kpis": kpis, 
        "datos_top_platforms": datos_top_platforms, 
        "datos_treemap": datos_treemap, 
        "datos_graf_ventas_totales": datos_graf_ventas_totales
    }