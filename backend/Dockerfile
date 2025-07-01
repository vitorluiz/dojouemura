# backend/Dockerfile

# Usamos uma versão estável e recente do Python
FROM python:3.12-slim

# Define variáveis de ambiente com a sintaxe moderna
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Garante que o pip está atualizado
RUN python -m pip install --upgrade pip

# Copia e instala as dependências
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia o resto do código do seu projeto
COPY . .
