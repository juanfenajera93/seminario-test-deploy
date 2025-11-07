import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

def preparar_datos_modelo(df):
    """
    toma el df_limpio, aplica el OneHotEncoding y devuelve
    X, y, el encoder
    """
    print("Iniciando preparación de X/y...")
    
    # definir columnas
    col_categoricas = ["platform", "genre", "rating_esrb", "gen_platform", "classification_user_score"]
    col_numericas = ["year_of_release", "user_score", "critic_score"]
    
    target = "total_sales"

    X_categoricas = df[col_categoricas]
    X_numericas = df[col_numericas]
    y = df[target]

    # aplicar el OneHotEncoding
    print("Aplicando OneHotEncoder")
    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    X_categoricas_encoded = encoder.fit_transform(X_categoricas)

    nuevas_columnas = encoder.get_feature_names_out(col_categoricas)

    games_encoded = pd.DataFrame(
        X_categoricas_encoded, 
        columns = nuevas_columnas
    )

    X = pd.concat([X_numericas.reset_index(drop=True), games_encoded], axis=1)
    
    print(f"Preparación lista. FilasxColumnas de X: {X.shape}, FilasxColumnas de y: {y.shape}")
    
    return X, y, encoder


def dividir_datos(X, y): 
    """
    aplica train_test_split con los parámetros definidos
    """
    
    RANDOM_STATE = 50 
    TEST_SIZE = 0.25
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    
    print(f"Tamaño X_train: {X_train.shape}, tamaño X_test: {X_test.shape}")
    
    return X_train, X_test, y_train, y_test