# Setup do Repositório GitHub

Guia passo a passo para criar e configurar o repositório no GitHub.

## Passo 1: Criar Repositório no GitHub

1. Acesse [GitHub](https://github.com)
2. Clique em "New repository"
3. Configure:
   - **Nome:** `Mega-Sena-Hacker`
   - **Descrição:** "Sistema de análise preditiva para Mega-Sena usando Qui-Quadrado, Atratores de Lorenz e Computação Quântica"
   - **Visibilidade:** Private ou Public (sua escolha)
   - **NÃO** marque "Initialize with README" (já temos um)
4. Clique em "Create repository"

## Passo 2: Inicializar Git Local

Execute no terminal, dentro da pasta do projeto:

```bash
# Inicializar repositório git
git init

# Adicionar todos os arquivos
git add .

# Primeiro commit
git commit -m "Initial commit: Mega-Sena Hacker with Chi-Square, Lorenz and Quantum analysis"

# Adicionar remote (substitua SEU-USUARIO pelo seu username)
git remote add origin https://github.com/SEU-USUARIO/Mega-Sena-Hacker.git

# Renomear branch para main (se necessário)
git branch -M main

# Push inicial
git push -u origin main
```

## Passo 3: Criar .env Local

**IMPORTANTE:** O arquivo `.env` não será enviado ao GitHub (está no `.gitignore`).

Crie manualmente no servidor/local:

```bash
cp .env.example .env
# Edite com suas credenciais reais
nano .env  # ou use seu editor preferido
```

## Passo 4: Configurar GitHub Actions (Opcional)

Crie `.github/workflows/docker-build.yml`:

```yaml
name: Docker Build and Test

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Build Docker image
      run: docker build -t mega-sena-hacker .

    - name: Test Docker image
      run: docker run --rm mega-sena-hacker python -c "import app; print('OK')"
```

## Passo 5: Proteger Credenciais

### Secrets no GitHub

Se for fazer deploy automatizado, adicione secrets:

1. Vá em Settings → Secrets and variables → Actions
2. Adicione:
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_HOST`
   - `DB_PORT`
   - `DB_NAME`
   - `DB_SCHEMA`

### Nunca commite

- `.env` (credenciais)
- `__pycache__/`
- `*.pyc`
- Arquivos de log
- Imagens geradas (`plots/`)

Tudo isso já está no `.gitignore`.

## Passo 6: Deploy no EasyPanel

### 6.1 Conectar GitHub ao EasyPanel

1. Acesse seu painel EasyPanel
2. Crie nova aplicação → GitHub App
3. Autorize acesso ao repositório
4. Selecione `Mega-Sena-Hacker`

### 6.2 Configurar Build

- **Build Method:** Dockerfile
- **Dockerfile Path:** `./Dockerfile`
- **Port:** 5000

### 6.3 Variáveis de Ambiente

Configure no painel do EasyPanel:

```
DB_USER=alebrotto
DB_PASSWORD=BrottoK@was0975
DB_HOST=utils_postgress
DB_PORT=5432
DB_NAME=utils
DB_SCHEMA=Mega-Sena-4
PORT=5000
DEBUG=False
```

### 6.4 Network

Configure a aplicação para estar na mesma rede do PostgreSQL:
- Rede: mesma do container `utils_postgress`

## Passo 7: Workflow de Desenvolvimento

### Criar nova feature

```bash
# Criar branch
git checkout -b feature/nova-analise

# Fazer alterações...
git add .
git commit -m "feat: adiciona nova análise XYZ"

# Push
git push origin feature/nova-analise
```

### Merge para main

```bash
git checkout main
git merge feature/nova-analise
git push origin main
```

### Deploy automático

Após push para `main`, o EasyPanel pode ser configurado para:
- Detectar mudanças
- Fazer rebuild automático
- Restart da aplicação

## Passo 8: Documentação no GitHub

### README.md

Já criado! Aparecerá na página inicial do repositório.

### Topics/Tags

Adicione tags ao repositório:
- `lottery`
- `mega-sena`
- `quantum-computing`
- `chaos-theory`
- `chi-square`
- `python`
- `flask`
- `api`
- `docker`

### Releases

Quando estiver estável:

```bash
git tag -a v1.0.0 -m "Primeira versão estável"
git push origin v1.0.0
```

No GitHub: Releases → Create new release

## Comandos Úteis

```bash
# Ver status
git status

# Ver histórico
git log --oneline

# Desfazer alterações não commitadas
git checkout -- arquivo.py

# Atualizar do remoto
git pull origin main

# Ver branches
git branch -a

# Deletar branch local
git branch -d feature/antiga

# Deletar branch remota
git push origin --delete feature/antiga
```

## Troubleshooting

### Erro: "remote: Repository not found"

Verifique a URL do remote:
```bash
git remote -v
git remote set-url origin https://github.com/SEU-USUARIO/Mega-Sena-Hacker.git
```

### Erro: "Permission denied"

Configure SSH ou use HTTPS com token:
```bash
git remote set-url origin https://TOKEN@github.com/SEU-USUARIO/Mega-Sena-Hacker.git
```

### Conflitos de merge

```bash
# Resolver manualmente os arquivos com conflito
# Depois:
git add .
git commit -m "resolve: merge conflicts"
```

## Boas Práticas

1. **Commits frequentes** com mensagens descritivas
2. **Branches** para features novas
3. **Pull Requests** para revisão de código
4. **Tags** para versões estáveis
5. **Issues** para rastrear bugs e features
6. **Wiki** para documentação adicional
7. **Nunca commitar** credenciais ou dados sensíveis

## Próximos Passos

- [ ] Criar repositório no GitHub
- [ ] Primeiro push
- [ ] Configurar deploy no EasyPanel
- [ ] Testar integração n8n
- [ ] Criar primeiro release
- [ ] Documentar resultados dos testes
