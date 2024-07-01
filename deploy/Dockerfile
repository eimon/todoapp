# Usa una imagen base oficial de Python
FROM python:3.11

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos y los instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido de la aplicación
# COPY ../app/ .

# Expone el puerto que Uvicorn usará para la aplicación
EXPOSE 8000

# Comando para correr la aplicación
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
