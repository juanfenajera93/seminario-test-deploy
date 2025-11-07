# 1. LA BASE (El S.O. + Python)
# Empezamos desde una imagen oficial de Python ligera
FROM python:3.10-slim

# 2. EL DIRECTORIO DE TRABAJO
# Creamos una carpeta 'app' DENTRO del contenedor donde vivirá todo
WORKDIR /app

# 3. OPTIMIZACIÓN DE CACHÉ (Pregunta Reactivo #19)
# Copiamos SÓLO el archivo de requisitos primero.
# Docker guarda esto en una 'capa'.
COPY requirements-api.txt .

# 4.1 INSTALAR DEPENDENCIAS (¡AQUÍ ESTÁ EL CAMBIO!)
# Primero, actualizamos la lista de paquetes de Linux e instalamos la librería del sistema
# -y confirma automáticamente la instalación
RUN apt-get update && apt-get install -y libgomp1

# 4.2 INSTALAR DEPENDENCIAS (Pregunta Reactivo #22 - RUN)
# RUN se ejecuta UNA VEZ, al construir la imagen.
# Si no cambiamos el .txt, Docker REÚSA esta capa y el build es instantáneo.
RUN pip install --no-cache-dir -r requirements-api.txt

# 5. COPIAR TODO LO DEMÁS
# Copiamos nuestro código, modelos y datos.
# El primer '.' es nuestro proyecto local.
# El segundo '.' es el WORKDIR (/app) dentro del contenedor.
# (Asegúrense de que los paths en api_app.py sean relativos, ej: "models/lgbm...")
COPY . .

# 6. EL COMANDO DE ARRANQUE (Pregunta Reactivo #22 - CMD)
# CMD especifica el comando para EJECUTAR la app cuando el contenedor se INICIA.
# 0.0.0.0 es una dirección IP especial que le dice al servidor que escuche peticiones 
# desde cualquier interfaz de red, permitiendo que las peticiones de la máquina anfitriona
# lleguen al contenedor.
CMD ["uvicorn", "api_app:app", "--host", "0.0.0.0", "--port", "8000"]

