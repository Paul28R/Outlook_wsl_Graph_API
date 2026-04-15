# 1. Imagen base de python
FROM python:3.11-slim
# 2. Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los requerimientos e instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el código y los modelos (.pkl)
# y el token de Outlook
COPY . .

#ejecutamos el extractor (o el script que desees)
CMD ["python", "extractor.ML.py"]