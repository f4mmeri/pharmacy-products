# Usar Python 3.11 como imagen base
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema (para PyMySQL)
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero (para aprovechar cache de Docker)
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear directorio para SQLite si se usa
RUN mkdir -p /app/data

# Exponer el puerto 8000
EXPOSE 8000

# Variables de entorno por defecto
ENV DATABASE_URL="sqlite:///./data/farmacia.db"
ENV PYTHONPATH=/app

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]