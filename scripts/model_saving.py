import joblib
import os

def guardar_archivos_modelo(modelo, encoder, model_path, encoder_path):
    """
    guarda el modelo y el encoder entrenados en las rturas específicas
    """
    
    try:
        MODEL_DIR = os.path.dirname(model_path)
        os.makedirs(MODEL_DIR, exist_ok=True)
        
        joblib.dump(encoder, encoder_path)
        print(f"Encoder guardado en: {encoder_path}")
        
        joblib.dump(modelo, model_path)
        print(f"Modelo guardo en: {model_path}")
        
        return True
    except Exception as e:
        print(f"Error al guardar los archivos: {e}")
        return False