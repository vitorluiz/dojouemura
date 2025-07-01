# backend/Dockerfile

# Usamos uma versão estável e recente do Python
FROM python:3.12-slim

# Define variáveis de ambiente com a sintaxe moderna
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# --- NOVO: Instala as dependências de sistema para o WeasyPrint ---
# Esta lista é baseada na documentação oficial do WeasyPrint para Debian/Ubuntu.
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-cffi \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Garante que o pip está atualizado
RUN python -m pip install --upgrade pip

# Copia e instala as dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código do seu projeto
COPY . .
