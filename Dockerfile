# Usa una imagen base con Python
FROM python:3.10

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto
COPY src /app
COPY requirements.txt /app

# Instala las dependencias
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expone el puerto 8080 (Cloud Run usa este puerto por defecto)
EXPOSE 8080

# Comando para ejecutar la API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]