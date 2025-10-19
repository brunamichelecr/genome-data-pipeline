# ----------------------------------------------------
# Dockerfile para Aplicação Web Python (Flask/Pipeline)
# ----------------------------------------------------

# Imagem base Python (leve e ideal para webapps)
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências primeiro para cache
COPY requirements.txt .

# 🚨 CORREÇÃO CRÍTICA: Instala dependências de sistema.
# Isso resolve o erro "Can't connect to HTTPS URL because o SSL module is not available."
# E instala o 'libpq-dev' necessário para o psycopg2.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libssl-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instala todas as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto (incluindo init_db.py, application.py, etc.)
COPY . /app

# Define a porta que o container irá escutar.
# O ECS Fargate irá mapear esta porta.
EXPOSE 80 

# Define o comando de execução principal (Gunicorn para produção).
# Usa a porta 80 e o objeto 'application' do módulo 'application'.
CMD ["gunicorn", "--bind", "0.0.0.0:80", "application:application"]

# Variável para logs (boa prática)
ENV PYTHONUNBUFFERED 1