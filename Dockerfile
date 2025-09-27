FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV PYTHONPATH=/app

ENV DATABASE_URL="mysql+pymysql://farmacia_user:farmacia_pass@mysql:3306/farmacia_db"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]