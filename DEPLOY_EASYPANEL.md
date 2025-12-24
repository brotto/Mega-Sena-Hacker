# 🚀 Guia de Deploy no EasyPanel

## Informações do Repositório GitHub

**Repositório**: `alebrotto/Mega-Sena-Hacker` (PRIVADO)
**Branch**: `main`
**Porta**: `5555`

---

## 📋 Variáveis de Ambiente para EasyPanel

Configure as seguintes variáveis de ambiente no EasyPanel:

```env
DB_USER=alebrotto
DB_PASSWORD=BrottoK@was0975
DB_HOST=utils_postgress
DB_PORT=5432
DB_NAME=utils
DB_SCHEMA=public
DB_TABLE=megasena
PORT=5555
DEBUG=False
```

### ⚠️ IMPORTANTE: Diferenças Local vs Deploy

| Variável | Local (Dev) | EasyPanel (Produção) |
|----------|-------------|----------------------|
| `DB_HOST` | `31.97.172.217` (IP público) | `utils_postgress` (nome interno Docker) |
| `PORT` | `5555` | `5555` |

---

## 🐳 Configuração no EasyPanel

### 1. Criar Nova Aplicação

1. Acesse o painel do EasyPanel
2. Clique em **"Create"** → **"GitHub App"**
3. Selecione o repositório **`alebrotto/Mega-Sena-Hacker`**

### 2. Configurações de Build

| Campo | Valor |
|-------|-------|
| **Build Method** | Dockerfile |
| **Dockerfile Path** | `./Dockerfile` |
| **Branch** | `main` |
| **Port** | `5555` |
| **Caminho de Build** | `/` (raiz do projeto) |

### 3. Variáveis de Ambiente

Adicione todas as variáveis listadas acima na seção "Environment Variables" do EasyPanel.

**Copiar e colar**:
```
DB_USER=alebrotto
DB_PASSWORD=BrottoK@was0975
DB_HOST=utils_postgress
DB_PORT=5432
DB_NAME=utils
DB_SCHEMA=public
DB_TABLE=megasena
PORT=5555
DEBUG=False
```

### 4. Configuração de Rede

**CRÍTICO**: A aplicação precisa estar na mesma rede Docker que o PostgreSQL.

- **Rede**: Selecione a mesma rede do container `utils_postgress`
- Ou configure manualmente para permitir comunicação entre containers

### 5. Deploy

1. Clique em **"Deploy"**
2. Aguarde o build (pode demorar 3-5 minutos)
3. Verifique os logs para confirmar que iniciou corretamente

---

## ✅ Verificação Pós-Deploy

### 1. Teste de Health Check

```bash
curl https://seu-app.easypanel.host/health
```

**Resposta esperada**:
```json
{
  "status": "healthy",
  "service": "Mega-Sena Hacker API"
}
```

### 2. Teste de Último Sorteio

```bash
curl https://seu-app.easypanel.host/resultado-ultimo-sorteio
```

**Resposta esperada**:
```json
{
  "concurso": 2954,
  "data": "2025-12-20",
  "numeros": [1, 9, 37, 39, 42, 44]
}
```

### 3. Verificar Logs

No painel do EasyPanel:
- Vá em **Logs** da aplicação
- Procure por: `* Running on http://0.0.0.0:5555`
- Não deve haver erros de conexão com banco

---

## 🔧 Troubleshooting

### Erro: "Connection refused" (Banco de Dados)

**Problema**: App não consegue conectar ao PostgreSQL

**Soluções**:
1. Verifique se `DB_HOST=utils_postgress` (nome interno, não IP)
2. Confirme que ambos os containers estão na mesma rede
3. Verifique se o PostgreSQL está rodando

### Erro: "Port 5555 already in use"

**Problema**: Porta já está sendo usada

**Soluções**:
1. Verifique se não há outra aplicação na porta 5555
2. Mude para outra porta (ex: 5000, 8000)
3. Atualize variável `PORT` e Dockerfile

### Erro: "ModuleNotFoundError"

**Problema**: Dependências não instaladas

**Soluções**:
1. Verifique se o `requirements.txt` está na raiz
2. Force rebuild do container
3. Verifique logs do build

### Build Muito Lento

**Problema**: Instalação do Qiskit demora

**Solução**:
- É normal! Qiskit é pesado (~5-10 min no primeiro build)
- Builds subsequentes usarão cache

---

## 📊 Performance Esperada

| Endpoint | Tempo de Resposta |
|----------|-------------------|
| `/health` | < 1s |
| `/resultado-ultimo-sorteio` | < 1s |
| `/analise-qui-quadrado` | 5-10s |
| `/atratores-de-lorenz` | 5-8s |
| `/analise-quantica` | 30-45s |
| `/previsao` | 60-90s |

---

## 🔐 Segurança

### Recomendações para Produção

1. **Adicionar Autenticação**
   ```python
   # Adicionar Bearer Token
   from flask import request

   @app.before_request
   def check_auth():
       token = request.headers.get('Authorization')
       if token != 'Bearer SEU_TOKEN_SECRETO':
           return jsonify({'error': 'Unauthorized'}), 401
   ```

2. **Rate Limiting**
   ```python
   from flask_limiter import Limiter

   limiter = Limiter(app, default_limits=["100 per hour"])
   ```

3. **HTTPS Obrigatório**
   - EasyPanel geralmente fornece SSL automático
   - Verifique se está habilitado

4. **Logs de Acesso**
   - Configure logging em arquivo
   - Monitore acessos suspeitos

---

## 🌐 Integração n8n

Após deploy, use a URL pública nos workflows n8n:

```
https://mega-sena-hacker.seu-dominio.com/previsao
```

Ver detalhes completos em: [N8N_INTEGRATION.md](N8N_INTEGRATION.md)

---

## 📝 Checklist de Deploy

- [ ] Repositório criado no GitHub (privado)
- [ ] Push do código realizado
- [ ] App criado no EasyPanel
- [ ] Variáveis de ambiente configuradas
- [ ] Rede Docker configurada
- [ ] Deploy iniciado
- [ ] Health check respondendo
- [ ] Último sorteio funcionando
- [ ] Logs sem erros
- [ ] Teste de previsão executado

---

## 🔄 Atualizações Futuras

### Deploy Automático

O EasyPanel pode ser configurado para:
- Detectar pushes na branch `main`
- Fazer rebuild automático
- Restart da aplicação

Para habilitar:
1. Vá em **Settings** → **Auto Deploy**
2. Ative "Deploy on push"
3. Selecione branch `main`

### Rollback

Se algo der errado:
1. Vá em **Deployments**
2. Selecione versão anterior
3. Clique em **Rollback**

---

## 📞 Suporte

- **Logs**: Verifique logs no painel EasyPanel
- **Status**: Use `/health` endpoint
- **Testes**: Execute `run_all_tests.py` localmente contra URL de produção
- **Documentação**: Ver [TESTES_COMPLETOS.md](TESTES_COMPLETOS.md)

---

## 📊 Recursos Necessários

### Container
- **CPU**: 1-2 cores
- **RAM**: 512 MB - 1 GB
- **Disco**: 2 GB (com dependências)

### Banco de Dados
- **Conexão**: Persistente
- **Schema**: `public`
- **Tabela**: `megasena` (3,274 registros)

---

## ✅ Checklist Final

Antes de considerar deploy completo:

- [ ] URL pública acessível
- [ ] Todos os 7 endpoints funcionando
- [ ] Integração n8n testada
- [ ] Logs sem erros críticos
- [ ] Performance aceitável
- [ ] Documentação atualizada

**Após tudo OK**: Sistema pronto para uso em produção! 🎉
