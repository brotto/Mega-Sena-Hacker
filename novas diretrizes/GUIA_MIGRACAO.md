# 🚀 GUIA DE MIGRAÇÃO - MEGA ANALYZER

## 📍 Situação Atual

- **Projeto Antigo:** `/Users/alebrotto/Mega-Sena-Hacker`
- **Projeto Novo:** Este diretório (`mega_analyzer`)
- **Objetivo:** Substituir completamente o projeto antigo no GitHub

---

## 🔄 PASSO A PASSO DE MIGRAÇÃO

### **OPÇÃO 1: Substituição Completa (RECOMENDADO)**

Esta opção mantém o histórico Git mas substitui todo o conteúdo.

```bash
# 1. Navegar até o projeto antigo
cd /Users/alebrotto/Mega-Sena-Hacker

# 2. Verificar status atual
git status
git remote -v  # Ver se está conectado ao GitHub

# 3. BACKUP do projeto antigo (segurança)
cd /Users/alebrotto
cp -r Mega-Sena-Hacker Mega-Sena-Hacker.backup.$(date +%Y%m%d)

# 4. Voltar ao projeto
cd /Users/alebrotto/Mega-Sena-Hacker

# 5. Remover todos os arquivos antigos (MANTÉM .git)
find . -maxdepth 1 ! -name '.git' ! -name '.' ! -name '..' -exec rm -rf {} +

# 6. Copiar TODOS os arquivos novos
cp -r /caminho/para/mega_analyzer/* .
cp -r /caminho/para/mega_analyzer/.* . 2>/dev/null || true

# 7. Adicionar todos os arquivos novos
git add .

# 8. Commit das mudanças
git commit -m "🎲 Mega Analyzer v2.0 - Reescrita completa

- Nova arquitetura modular com LotteryAnalyzer
- 5 testes estatísticos implementados
- Análise comparativa Brasil vs EUA vs Canadá
- Análise específica Mega da Virada 2025
- Sistema de classificação automática PRNG vs RNG
- Documentação completa
- Descobertas: Mega-Sena apresenta características PRNG
- Thread para X/Twitter incluída"

# 9. Push forçado (CUIDADO: sobrescreve histórico remoto)
git push origin main --force

# OU, se preferir preservar o histórico:
git push origin main
```

---

### **OPÇÃO 2: Novo Repositório (Mais Limpo)**

Se preferir começar do zero no GitHub.

```bash
# 1. Navegar até o diretório dos projetos
cd /Users/alebrotto

# 2. Renomear o projeto antigo
mv Mega-Sena-Hacker Mega-Sena-Hacker.old

# 3. Criar novo diretório
mkdir Mega-Sena-Hacker
cd Mega-Sena-Hacker

# 4. Copiar arquivos novos
cp -r /caminho/para/mega_analyzer/* .
cp -r /caminho/para/mega_analyzer/.* . 2>/dev/null || true

# 5. Inicializar Git
git init
git add .
git commit -m "🎲 Mega Analyzer v2.0 - Sistema completo de análise"

# 6. Conectar ao GitHub
# Se quiser usar o mesmo repositório:
git remote add origin <URL_DO_SEU_REPO>
git push origin main --force

# OU criar novo repositório no GitHub e:
git remote add origin <URL_NOVO_REPO>
git branch -M main
git push -u origin main
```

---

### **OPÇÃO 3: Branch Paralelo (Mais Seguro)**

Mantém o antigo em uma branch e o novo em outra.

```bash
# 1. Ir ao projeto
cd /Users/alebrotto/Mega-Sena-Hacker

# 2. Criar branch do estado atual (backup)
git checkout -b v1-backup
git push origin v1-backup

# 3. Voltar para main
git checkout main

# 4. Remover conteúdo antigo
find . -maxdepth 1 ! -name '.git' ! -name '.' ! -name '..' -exec rm -rf {} +

# 5. Copiar novo projeto
cp -r /caminho/para/mega_analyzer/* .

# 6. Commit e push
git add .
git commit -m "🎲 Mega Analyzer v2.0 - Reescrita completa"
git push origin main
```

---

## 📁 ESTRUTURA DE ARQUIVOS PARA COPIAR

Certifique-se de copiar todos estes arquivos do `mega_analyzer`:

```
mega_analyzer/
├── lottery_analyzer.py          ← CORE do sistema
├── exemplo_analise_completa.py  ← Demo Brasil vs EUA
├── analise_mega_virada_2025.py  ← Análise Virada 2025
├── README.md                     ← Documentação principal
├── requirements.txt              ← Dependências
├── GUIA_MIGRACAO.md             ← Este arquivo
└── .gitignore                    ← (criar se não existir)
```

---

## 📝 CRIAR .gitignore (SE NÃO EXISTIR)

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Jupyter
.ipynb_checkpoints/
*.ipynb

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Dados sensíveis
*.xlsx
*.csv
*.json
dados/

# Outputs
outputs/
graficos/
*.png
*.pdf

# Logs
*.log
EOF
```

---

## 🎯 COMANDOS LOCAIS NO MAC MINI

### **1. Copiar projeto do Downloads/Claude**

Assumindo que você baixou os arquivos:

```bash
# Localizar onde o Claude salvou
# Geralmente em: ~/Downloads/

# Copiar para o projeto
cd /Users/alebrotto/Mega-Sena-Hacker
cp -r ~/Downloads/mega_analyzer/* .
```

### **2. Instalar dependências**

```bash
cd /Users/alebrotto/Mega-Sena-Hacker
pip install -r requirements.txt --break-system-packages
```

### **3. Testar o sistema**

```bash
# Teste 1: Análise completa
python3 exemplo_analise_completa.py

# Teste 2: Mega da Virada 2025
python3 analise_mega_virada_2025.py
```

### **4. Abrir no VSCode**

```bash
cd /Users/alebrotto/Mega-Sena-Hacker
code .
```

---

## 📊 ATUALIZAR README.md NO GITHUB

Após o push, adicione badges no topo do README.md:

```markdown
# 🎲 MEGA ANALYZER

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

Sistema completo para análise de aleatoriedade em loterias...
```

---

## ⚠️ CHECKLIST ANTES DO PUSH

- [ ] Backup do projeto antigo criado
- [ ] Todos os arquivos novos copiados
- [ ] `.gitignore` configurado
- [ ] Dependências instaladas localmente
- [ ] Scripts testados e funcionando
- [ ] README.md revisado
- [ ] Dados sensíveis removidos (.xlsx, .csv)
- [ ] Commit message descritivo

---

## 🔍 VERIFICAR APÓS O PUSH

```bash
# Ver o repositório no GitHub
# https://github.com/SEU_USUARIO/Mega-Sena-Hacker

# Verificar localmente
git log --oneline -5  # Ver últimos commits
git status            # Verificar estado
git remote -v         # Verificar remoto
```

---

## 💡 DICAS IMPORTANTES

### **1. Dados Sensíveis**

NÃO faça commit de:
- Arquivos `.xlsx` ou `.csv` com dados completos
- Chaves de API
- Informações pessoais

### **2. Arquivos Grandes**

Se tiver arquivos grandes (>100MB):
```bash
# Use Git LFS
git lfs install
git lfs track "*.xlsx"
git lfs track "*.csv"
git add .gitattributes
```

### **3. Organização**

Estrutura sugerida no repositório:
```
Mega-Sena-Hacker/
├── src/                      # Código fonte
│   ├── lottery_analyzer.py
│   └── ...
├── examples/                 # Exemplos de uso
│   ├── exemplo_analise_completa.py
│   └── analise_mega_virada_2025.py
├── docs/                     # Documentação extra
├── tests/                    # Testes unitários (futuro)
├── data/                     # Dados (não no Git)
│   └── .gitkeep
├── outputs/                  # Outputs (não no Git)
│   └── .gitkeep
├── README.md
├── requirements.txt
└── .gitignore
```

---

## 🚨 TROUBLESHOOTING

### Erro: "Permission denied"
```bash
sudo chmod -R 755 /Users/alebrotto/Mega-Sena-Hacker
```

### Erro: "Git push rejected"
```bash
# Forçar push (CUIDADO!)
git push origin main --force

# OU resolver conflitos
git pull origin main --rebase
git push origin main
```

### Erro: "pip install failed"
```bash
# Mac Mini (Apple Silicon)
pip install -r requirements.txt --break-system-packages

# Se não funcionar
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt --break-system-packages
```

---

## ✅ SUCESSO!

Quando tudo estiver funcionando:

1. ✅ Projeto migrado com sucesso
2. ✅ GitHub atualizado
3. ✅ Sistema testado localmente
4. ✅ Documentação completa
5. ✅ Pronto para desenvolvimento futuro

---

**Última atualização:** Janeiro 2025  
**Autor:** Ale Brotto
