FROM mcr.microsoft.com/devcontainers/python:3.13

# Instala dependências do sistema para PostgreSQL
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends postgresql-client \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Configura o PYTHONPATH
ENV PYTHONPATH=/workspace

WORKDIR /workspace

