# ============================
# Base image
# ============================
FROM node:24-bookworm-slim

# ============================
# Atualizações e sudo (opcional)
# ============================
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        gnupg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ============================
# Criar usuário não-root
# ============================
#RUN useradd -m -s /bin/bash appuser

# ============================
# Diretório de trabalho
# ============================
WORKDIR /app

# ============================
# Ajustar permissões
# ============================
#RUN chown -R appuser:appuser /app

# ============================
# Mudar para o usuário não-root
# ============================

#RUN useradd -m appuser
#USER appuser  <-- remover

# ============================
# Copiar e instalar dependências
# (essa etapa é opcional aqui — normalmente o GitLab faz isso no job)
# ============================
# COPY package*.json ./
# RUN npm ci --unsafe-perm

# ============================
# HEALTHCHECK (opcional)
# ============================
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/ || exit 1
