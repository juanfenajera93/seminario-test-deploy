import streamlit as st
import plotly.express as px
import requests

# configuración de nuestra página
st.set_page_config(layout="wide")

# las URLs 
API_BASE_URL = "http://localhost:8000"
API_URL_PREDICT = f"{API_BASE_URL}/ml/predict"
API_URL_FILTROS = f"{API_BASE_URL}/eda/filters"
API_URL_DATOS_EDA = f"{API_BASE_URL}/eda/data_specific_filters"

# cargar datos
@st.cache_data
def cargar_opciones_filtros():
    """llama a la API para obtener las opciones de los filtros"""
    try:
        response = requests.get(API_URL_FILTROS)
        response.raise_for_status()
        print("Filtros cargados desde la API")
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar filtros desde la API: {e}")
        return None


# titulo
st.title("🎮Dashboard de Videojuegos🎮")
st.caption("Seminario Complexivo de Titulación | UniAndes | Profesor: Juan Felipe Nájera")
st.subheader("Análisis Exploratorio de Datos y Predicción de Ventas")

# crear pestañas
tab1, tab2 = st.tabs(["Análisis Exploratorio (EDA)", "Predicción de Ventas (ML)"])

data_filtros = cargar_opciones_filtros()

if data_filtros and "error" not in data_filtros:
    generos_lista = data_filtros.get("generos", [])
    min_year = data_filtros.get("min_year", 1980)
    max_year = data_filtros.get("max_year", 2016)
    
    platform_options = data_filtros.get("platforms", [])
    genre_options =  data_filtros.get("genre", [])
    rating_options = data_filtros.get("ratings", [])
    gen_platform_options = data_filtros.get("gen_platforms", [])
    class_score_options = data_filtros.get("class_scores", [])

else:
    st.error("No se pudieron cargar los datos de los filtros desde la API")
    generos_lista = []
    min_year = 1980
    max_year = 2016
    platform_options = []
    genre_options =  []
    rating_options = []
    gen_platform_options = []
    class_score_options = []


# PESTAÑA 1
with tab1: 
    st.header("Análisis Exploratorio de Ventas")
    
    col_filtro1, col_filtro2 = st.columns(2)
    
    # filtro de géneros
    with col_filtro1:
        # selector 
        genero_seleccionado = st.multiselect(
            "Selecciona Géneros:", 
            options=generos_lista, 
            default=generos_lista
        )
    with col_filtro2:
        #st.slider
        rango_anios = st.slider(
            "Selecciona un rango de años:",
            min_value=min_year, 
            max_value=max_year, 
            value=(min_year, max_year) # valor mínimo, valor máximo, default del ragno
        )
        
    if genero_seleccionado:
        
        params = {
            "generos": genero_seleccionado, 
            "anio_inicio": rango_anios[0],
            "anio_fin": rango_anios[1] 
        }
        
        try: 
            response_datos = requests.get(API_URL_DATOS_EDA, params=params)
            response_datos.raise_for_status()
            data = response_datos.json()
            
            kpis = data.get("kpis", {})
            datos_top_platforms = data.get("datos_top_platforms", [])
            datos_treemap = data.get("datos_treemap", [])
            datos_graf_ventas_totales = data.get("datos_graf_ventas_totales", [])
    
            col1, col2, col3, col4, col5 = st.columns(5)
            
            # MÉTRICAS
            with col1:
                st.metric(
                    label="Ventas Globales (Millones)", 
                    value=kpis.get("total_sales_global", "N/A")
                )
            with col2:
                st.metric(
                    label="Total Videojuegos", 
                    value=kpis.get("total_videogames", "N/A")
                )
            with col3:
                st.metric(
                    label="Total Consolas", 
                    value=kpis.get("total_platforms", "N/A")
                )
            with col4:
                st.metric(
                    label="Puntaje Promedio de Críticos", 
                    value=kpis.get("avg_critic_score", "N/A")
                )
            with col5:
                st.metric(
                    label="Puntaje Promedio de Usuarios", 
                    value=kpis.get("avg_user_score", "N/A")
                )
        except requests.exceptions.RequestException as e:
            st.error(f"Error al cargar datos del EDA desde la API: {e}")
            kpis = {}
            datos_top_platforms = []
            datos_treemap = []
            datos_graf_ventas_totales = []
        
    st.markdown("---")
    
    # GRÁFICO VENTAS TOTALES POR REGIÓN
    st.subheader("Evolución de Ventas por Región")
    
    
    fig_sales_per_region = px.line(
        datos_graf_ventas_totales, 
        x = "year_of_release", 
        y = "sales",
        color="region", 
        title="Evolución de Ventas por Región (Millones)",
        labels={
            "year_of_release": "Año de lanzamiento", 
            "sales": "Ventas Totales (Millones)", 
            "region": "Región"
        }, 
        markers=True
    )
    
    # añadir slider 
    fig_sales_per_region.update_layout(xaxis_rangeslider_visible=True)
    
    # mostrar la figura en streamlit
    st.plotly_chart(fig_sales_per_region, use_container_width=True)
    st.caption("Filtro para mover el rango de años en el gráfico")
    
    st.markdown("---")
    st.subheader("Análisis de Plataformas y Composición del Mercado")
    
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
    
        fig_bar_platform = px.bar(
            datos_top_platforms, 
            x="platform",
            y="total_sales", 
            title="Top 10 Plataformas por Ventas Totales", 
            labels={
                "platform": "Plataforma", 
                "total_sales": "Ventas Totales (Millones)", 
            },
            color="total_sales", 
            color_continuous_scale="Blues", 
            text_auto=".2s"
        )
        
        fig_bar_platform.update_layout(showlegend=False, title_x=0.5, plot_bgcolor="rosybrown")

        st.plotly_chart(fig_bar_platform, use_container_width=True)
        
    with col_graf2:
        st.write("##### Composición de Ventas por Región (%)")
        
        
        fig_treemap = px.treemap(
            datos_treemap, 
            path=[px.Constant("Ventas Totales"), "region"], 
            values="ventas", 
            color="ventas", 
            color_continuous_scale="Blues", 
            title="Distribución de Ventas por Región (%)",
            labels={
                "ventas": "Ventas (Millones)" 
            } 
        )
        
        st.plotly_chart(fig_treemap, use_container_width=True)
    
# PESTAÑA 2
with tab2:
    st.header("Predicción de Ventas Globales")
    st.write("Esta pestaña utiliza el modelo de ML cargado localmente para predecir las ventas")
            
    # dos nuevas columnas
    col_inputs, col_resultado = st.columns(2)
    
    with col_inputs:
        st.subheader("Parámetros del Videojuego")
        
        with st.form("prediction_form"):
            
            # inputs categóricos
            st.write("##### Características Categóricas")
            platform = st.selectbox("Plataforma:", options=platform_options)
            genre = st.selectbox("Género:", options=genre_options)
            rating_esrb = st.selectbox("Clasificación ESRB:", options=rating_options)
            gen_platform = st.selectbox("Generación de Plataformas:", options=gen_platform_options)
            classification_user_score = st.selectbox("Clasificación de Usuarios:", options=class_score_options)
            
            # inputs numéricos
            st.write("##### Catacterísticas Numéricas")
            year_of_release = st.slider("Año de Lanzamiento:", 1980, 2016, 2010)
            critic_score = st.slider("Puntaje de Crítica (0-100):", 0.0, 100.0, 80.0)
            user_score = st.slider("Puntaje de Usuario (0-10):", 0.0, 10.0, 8.0, step=0.1)
            
            # botón de submit el form
            submit_button = st.form_submit_button(label="Predecir Ventas") 
            
        if submit_button:
            # recolar los inputs en un diccionario
            input_data = {
                "platform":platform, 
                "genre": genre, 
                "rating_esrb": rating_esrb, 
                "gen_platform": gen_platform, 
                "classification_user_score": classification_user_score, 
                "year_of_release": year_of_release, 
                "user_score": user_score, 
                "critic_score": critic_score 
            }
            
            try: 
                response = requests.post(API_URL_PREDICT, json=input_data)
                
                response.raise_for_status()
                
                resultado = response.json()
                
                if "prediccion_ventas_globales_millones" in resultado:
                    prediccion_valor = resultado["prediccion_ventas_globales_millones"]
                    
                    with col_resultado:
                        st.subheader("Resultado de la Predicción")
                        st.metric(
                            label="Ventas Globales Predichas", 
                            value=f"$ {prediccion_valor:,.2f} Millones"
                        )
                        st.success("Predicción realizada vía API!")
                else:
                    with col_resultado:
                        st.error(f"Error en la respuesta de la API: {resultado.get("error", "Formato desconocido")}")
            
            except requests.exceptions.RequestException as e:
                with col_resultado:
                    st.error(f"Error de conexión con la API de ML: {e}")