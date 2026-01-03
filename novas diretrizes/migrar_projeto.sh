#!/bin/bash
# =============================================================================
# SCRIPT DE MIGRAÇÃO AUTOMÁTICA - MEGA ANALYZER
# =============================================================================
# Este script facilita a migração do projeto antigo para o novo
# 
# Uso: ./migrar_projeto.sh
# =============================================================================

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir com cor
print_color() {
    color=$1
    shift
    echo -e "${color}$@${NC}"
}

print_color $BLUE "========================================"
print_color $BLUE "   MEGA ANALYZER - MIGRAÇÃO v2.0"
print_color $BLUE "========================================"
echo ""

# 1. Verificar diretórios
PROJETO_ANTIGO="/Users/alebrotto/Mega-Sena-Hacker"
PROJETO_NOVO="${PWD}"

print_color $YELLOW "[1/8] Verificando diretórios..."

if [ ! -d "$PROJETO_ANTIGO" ]; then
    print_color $RED "❌ Diretório do projeto antigo não encontrado: $PROJETO_ANTIGO"
    exit 1
fi

if [ ! -f "lottery_analyzer.py" ]; then
    print_color $RED "❌ Este script deve ser executado no diretório do novo projeto (mega_analyzer)"
    exit 1
fi

print_color $GREEN "✓ Diretórios verificados"

# 2. Criar backup
print_color $YELLOW "[2/8] Criando backup do projeto antigo..."

BACKUP_DIR="${PROJETO_ANTIGO}.backup.$(date +%Y%m%d_%H%M%S)"
cp -r "$PROJETO_ANTIGO" "$BACKUP_DIR"

print_color $GREEN "✓ Backup criado em: $BACKUP_DIR"

# 3. Verificar Git
print_color $YELLOW "[3/8] Verificando Git no projeto antigo..."

cd "$PROJETO_ANTIGO"

if [ ! -d ".git" ]; then
    print_color $YELLOW "⚠️  Projeto antigo não tem Git inicializado"
    read -p "Deseja inicializar Git? (s/n): " init_git
    
    if [ "$init_git" = "s" ]; then
        git init
        print_color $GREEN "✓ Git inicializado"
    else
        print_color $RED "❌ Abortado pelo usuário"
        exit 1
    fi
fi

# Verificar se tem remote
if ! git remote | grep -q "origin"; then
    print_color $YELLOW "⚠️  Nenhum remote configurado"
    read -p "Deseja configurar remote agora? (s/n): " config_remote
    
    if [ "$config_remote" = "s" ]; then
        read -p "URL do repositório GitHub: " repo_url
        git remote add origin "$repo_url"
        print_color $GREEN "✓ Remote configurado"
    fi
fi

print_color $GREEN "✓ Git verificado"

# 4. Salvar estado atual
print_color $YELLOW "[4/8] Salvando estado atual em branch backup..."

git checkout -b v1-backup 2>/dev/null || git checkout v1-backup
git add -A
git commit -m "Backup antes da migração para v2.0" 2>/dev/null || true

# 5. Limpar projeto antigo
print_color $YELLOW "[5/8] Limpando projeto antigo..."

git checkout main 2>/dev/null || git checkout -b main

# Remover todos os arquivos exceto .git
find . -maxdepth 1 ! -name '.git' ! -name '.' ! -name '..' -exec rm -rf {} +

print_color $GREEN "✓ Projeto limpo"

# 6. Copiar novos arquivos
print_color $YELLOW "[6/8] Copiando novos arquivos..."

cp -r "${PROJETO_NOVO}"/* .
cp "${PROJETO_NOVO}/.gitignore" . 2>/dev/null || true

print_color $GREEN "✓ Arquivos copiados"

# 7. Instalar dependências
print_color $YELLOW "[7/8] Instalando dependências..."

if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt --break-system-packages
    print_color $GREEN "✓ Dependências instaladas"
else
    print_color $YELLOW "⚠️  pip3 não encontrado. Instale manualmente:"
    print_color $YELLOW "   pip3 install -r requirements.txt --break-system-packages"
fi

# 8. Commit final
print_color $YELLOW "[8/8] Fazendo commit das mudanças..."

git add .
git commit -m "🎲 Mega Analyzer v2.0 - Reescrita completa

- Nova arquitetura modular com LotteryAnalyzer
- 5 testes estatísticos implementados
- Análise comparativa Brasil vs EUA vs Canadá
- Análise específica Mega da Virada 2025
- Sistema de classificação automática PRNG vs RNG
- Documentação completa
- Descobertas: Mega-Sena apresenta características PRNG
- Thread para X/Twitter incluída"

print_color $GREEN "✓ Commit realizado"

# Finalização
echo ""
print_color $BLUE "========================================"
print_color $GREEN "   ✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!"
print_color $BLUE "========================================"
echo ""

print_color $YELLOW "Próximos passos:"
echo "  1. Revisar as mudanças: git status"
echo "  2. Testar o projeto: python3 exemplo_analise_completa.py"
echo "  3. Push para GitHub: git push origin main"
echo ""
print_color $YELLOW "Backup salvo em: $BACKUP_DIR"
echo ""
