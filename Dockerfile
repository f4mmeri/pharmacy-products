FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Hacer el script de inicio ejecutable
RUN chmod +x start.sh

# Exponer el puerto
EXPOSE 8000

# Variables de entorno
ENV PYTHONPATH=/app
ENV DATABASE_URL="mysql+pymysql://farmacia_user:farmacia_pass@mysql:3306/farmacia_db"

# Script de entrada por defecto
CMD ["./start.sh"]