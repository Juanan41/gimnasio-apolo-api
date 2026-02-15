# Imagen base oficial de Python
FROM python:3.11-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /code

# Copiamos requirements primero (mejos práctica para cachear dependencias)
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código de la aplicación
COPY . .    

# Comando para ejecutar la aplicación con Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


