#!/bin/bash

# Script para executar a aplicação localmente

echo "======================================"
echo "Mega-Sena Hacker - Execução Local"
echo "======================================"

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Instalar/atualizar dependências
echo "Instalando dependências..."
pip install -r requirements.txt

# Verificar se o arquivo .env existe
if [ ! -f ".env" ]; then
    echo "⚠️  Arquivo .env não encontrado!"
    echo "Copiando .env.example para .env..."
    cp .env.example .env
    echo "⚠️  Por favor, edite o arquivo .env com suas credenciais antes de continuar."
    exit 1
fi

# Executar aplicação
echo ""
echo "======================================"
echo "Iniciando aplicação..."
echo "API disponível em: http://localhost:5000"
echo "======================================"
echo ""

python app.py
