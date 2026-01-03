#!/bin/bash

# ========================================================================
# MEGA ANALYZER v2.0 - SETUP COMPLETO NO MAC
# ========================================================================
# 
# Execute: chmod +x SETUP_COMPLETO_MAC.sh && ./SETUP_COMPLETO_MAC.sh
# 
# ========================================================================

set -e  # Para no primeiro erro

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   🚀 MEGA ANALYZER v2.0 - SETUP AUTOMÁTICO               ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Ir para o diretório do projeto
cd /Users/alebrotto/Mega-Sena-Hacker || {
    echo "❌ Erro: Diretório /Users/alebrotto/Mega-Sena-Hacker não encontrado!"
    echo "Por favor, execute este script do diretório correto."
    exit 1
}

echo "📁 Diretório atual: $(pwd)"
echo ""

# ========================================
# 1. CRIAR ESTRUTURA DE DIRETÓRIOS
# ========================================
echo "📂 [1/8] Criando estrutura de diretórios..."

mkdir -p v2/core
mkdir -p v2/analyzers
mkdir -p v2/utils
mkdir -p tests
mkdir -p docs
mkdir -p data

echo "   ✅ Diretórios criados"

# ========================================
# 2. CRIAR __init__.py FILES
# ========================================
echo "📝 [2/8] Criando arquivos __init__.py..."

cat > v2/__init__.py << 'EOF'
"""
Mega Analyzer v2.0 - Sistema Avançado de Análise Estatística
Detecta comportamento PRNG vs RNG em loterias
"""

__version__ = "2.0.0"
__author__ = "Ale Brotto"

from .core.lottery_analyzer import LotteryAnalyzer

__all__ = ['LotteryAnalyzer']
EOF

cat > v2/core/__init__.py << 'EOF'
"""Core modules for advanced lottery analysis"""
from .lottery_analyzer import LotteryAnalyzer
__all__ = ['LotteryAnalyzer']
EOF

cat > v2/analyzers/__init__.py << 'EOF'
"""Specialized analyzers for specific lottery events"""
from .megavirada_analyzer import MegaDaVirada2025Analyzer
__all__ = ['MegaDaVirada2025Analyzer']
EOF

touch v2/utils/__init__.py

echo "   ✅ Arquivos __init__.py criados"

# ========================================
# 3. COPIAR lottery_analyzer.py
# ========================================
echo "📥 [3/8] Copiando lottery_analyzer.py..."

if [ -f ~/Downloads/mega_analyzer/lottery_analyzer.py ]; then
    cp ~/Downloads/mega_analyzer/lottery_analyzer.py v2/core/
    echo "   ✅ Copiado de ~/Downloads/mega_analyzer/"
elif [ -f /mnt/user-data/outputs/mega_analyzer/lottery_analyzer.py ]; then
    cp /mnt/user-data/outputs/mega_analyzer/lottery_analyzer.py v2/core/
    echo "   ✅ Copiado de /mnt/user-data/outputs/"
else
    echo "   ⚠️  lottery_analyzer.py não encontrado"
    echo "   📝 Será necessário criar manualmente ou baixar"
fi

# ========================================
# 4. COPIAR megavirada_analyzer.py
# ========================================
echo "📥 [4/8] Copiando megavirada_analyzer.py..."

if [ -f ~/Downloads/mega_analyzer/analise_mega_virada_2025.py ]; then
    cp ~/Downloads/mega_analyzer/analise_mega_virada_2025.py v2/analyzers/megavirada_analyzer.py
    echo "   ✅ Copiado de ~/Downloads/mega_analyzer/"
elif [ -f /mnt/user-data/outputs/mega_analyzer/analise_mega_virada_2025.py ]; then
    cp /mnt/user-data/outputs/mega_analyzer/analise_mega_virada_2025.py v2/analyzers/megavirada_analyzer.py
    echo "   ✅ Copiado de /mnt/user-data/outputs/"
else
    echo "   ⚠️  megavirada_analyzer.py não encontrado"
    echo "   📝 Será necessário criar manualmente ou baixar"
fi

# ========================================
# 5. ATUALIZAR requirements.txt
# ========================================
echo "📦 [5/8] Atualizando requirements.txt..."

# Verificar se já tem as dependências
if ! grep -q "openpyxl" requirements.txt; then
    cat >> requirements.txt << 'EOF'

# === v2.0 additions ===
openpyxl>=3.1.0
seaborn>=0.12.0
EOF
    echo "   ✅ Dependências v2.0 adicionadas"
else
    echo "   ℹ️  Dependências já existem"
fi

# ========================================
# 6. CRIAR .gitignore
# ========================================
echo "🚫 [6/8] Criando .gitignore..."

cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*.so
*.egg-info/
venv/
env/

# IDEs
.vscode/
.idea/

# OS
.DS_Store
.env

# Dados sensíveis
*.xlsx
*.csv
data/
!data/.gitkeep

# Outputs
plots/
outputs/
*.png
*.pdf

# Logs
*.log
EOF

touch data/.gitkeep

echo "   ✅ .gitignore criado"

# ========================================
# 7. CRIAR DOCUMENTAÇÃO
# ========================================
echo "📚 [7/8] Criando documentação..."

cat > docs/NOVOS_ENDPOINTS_V2.md << 'EOF'
# 🚀 Novos Endpoints v2.0

## 📋 Resumo
7 novos endpoints para análises estatísticas avançadas PRNG/RNG

## 🔌 Endpoints

1. **GET /v2/runs-test** - Teste de Runs (Wald-Wolfowitz)
2. **GET /v2/coverage-speed** - Velocidade de Cobertura
3. **GET /v2/coefficient-variation** - Coeficiente de Variação
4. **GET /v2/full-report** - Relatório Completo
5. **GET /v2/mega-virada-2025** - Análise Mega Virada 2025
6. **GET /v2/comparative-analysis** - Brasil vs EUA
7. **GET /v2/classification** - Classificação Automática

## 🔗 URLs (n8n)
```
http://firecrawl_mega-sena-hacker:5555/v2/runs-test
http://firecrawl_mega-sena-hacker:5555/v2/coverage-speed
http://firecrawl_mega-sena-hacker:5555/v2/coefficient-variation
http://firecrawl_mega-sena-hacker:5555/v2/full-report
http://firecrawl_mega-sena-hacker:5555/v2/mega-virada-2025
http://firecrawl_mega-sena-hacker:5555/v2/comparative-analysis
http://firecrawl_mega-sena-hacker:5555/v2/classification
```

Ver N8N_SETUP.md para configuração completa no n8n.
EOF

echo "   ✅ Documentação criada"

# ========================================
# 8. STATUS FINAL
# ========================================
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   ✅ ESTRUTURA v2.0 CRIADA COM SUCESSO!                  ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "📁 ARQUIVOS CRIADOS:"
echo ""
find v2 -type f -name "*.py" 2>/dev/null | head -20
echo ""
echo "📝 PRÓXIMOS PASSOS:"
echo ""
echo "1️⃣  Baixar lottery_analyzer.py e megavirada_analyzer.py"
echo "    (se ainda não foram copiados automaticamente)"
echo ""
echo "2️⃣  Criar app_v2_endpoints.py com:"
echo "    cat ARQUIVO_APP_V2_ENDPOINTS.py > app_v2_endpoints.py"
echo ""
echo "3️⃣  Integrar ao app.py:"
echo "    - Adicionar import do app_v2_endpoints"
echo "    - Chamar register_v2_routes(app)"
echo ""
echo "4️⃣  Testar localmente (opcional)"
echo ""
echo "5️⃣  Git commit + push"
echo ""
echo "6️⃣  Deploy na VPS"
echo ""
echo "🔗 Ver instruções detalhadas:"
echo "   - INTEGRACAO_APP.md"
echo "   - DEPLOY_VPS.md"
echo "   - N8N_SETUP.md"
echo ""
echo "✅ Setup concluído!"
