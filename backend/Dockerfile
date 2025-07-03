# backend/Dockerfile

# Usamos uma versão estável e recente do Python
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instala as libs do sistema necessárias ao WeasyPrint e ao Django
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    python3-cffi \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia apenas o requirements para instalar dependências com cache
COPY requirements.txt .

# Instala dependências do projeto
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto
COPY . .
