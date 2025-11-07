from lightgbm import LGBMRegressor
from sklearn.metrics import root_mean_squared_error

def entrenar_y_evaluar_modelo(X_train, X_test, y_train, y_test):
    """
    entrena, evalúa y devuelve el modelo LGBM y su RMSE
    """
    RANDOM_STATE = 50
    
    print("Entrenando LGBMRegressor...")
    modelo_lgbm = LGBMRegressor(random_state=RANDOM_STATE, n_jobs=-1)
    modelo_lgbm.fit(X_train, y_train)
    predicciones_lgbm = modelo_lgbm.predict(X_test)
    rmse_lgbm = root_mean_squared_error(y_test, predicciones_lgbm)
    print(f"RMSE (LightGBM): {rmse_lgbm:.4f}")
    
    return modelo_lgbm