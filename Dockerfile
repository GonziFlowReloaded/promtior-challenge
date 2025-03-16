# Usa la imagen oficial de Python como base
FROM python:3.12-slim
# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de tu aplicación al contenedor
COPY . /app/


# Instala las dependencias necesarias desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expon el puerto 8000 para acceder a la aplicación
EXPOSE 8000

# Ejecuta el servidor Uvicorn para FastAPI
CMD ["python", "app.py"]
