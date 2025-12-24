# 📋 Instruções para Deploy no EasyPanel

## ✅ Repositório GitHub Criado

**URL do Repositório**: https://github.com/brotto/Mega-Sena-Hacker

**Visibilidade**: 🔒 PRIVADO

**Branch Principal**: `main`

---

## 🚀 Informações para Deploy no EasyPanel

### 1️⃣ Repositório
```
brotto/Mega-Sena-Hacker
```
ou
```
https://github.com/brotto/Mega-Sena-Hacker
```

### 2️⃣ Variáveis de Ambiente

**COPIAR E COLAR NO EASYPANEL**:

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

### 3️⃣ Branch
```
main
```

### 4️⃣ Caminho de Build
```
/
```
(Raiz do projeto - deixar vazio ou usar `/`)

### 5️⃣ Porta
```
5555
```

---

## 🐳 Configuração Docker

O projeto já possui `Dockerfile` configurado corretamente:

- ✅ Base: Python 3.11-slim
- ✅ Dependências: gcc, g++, libpq-dev
- ✅ Framework: Gunicorn com 2 workers
- ✅ Timeout: 120 segundos
- ✅ Porta: 5555 (variável de ambiente)

**Não é necessário configurar nada além das variáveis de ambiente!**

---

## 📝 Passo a Passo no EasyPanel

### Passo 1: Criar Nova Aplicação
1. Login no EasyPanel
2. Clique em **"Create"**
3. Selecione **"GitHub App"**

### Passo 2: Conectar Repositório
1. Autorize acesso ao GitHub (se necessário)
2. Selecione o repositório: **`brotto/Mega-Sena-Hacker`**
3. Branch: **`main`**

### Passo 3: Configurar Build
| Campo | Valor |
|-------|-------|
| Build Method | **Dockerfile** |
| Dockerfile Path | `./Dockerfile` |
| Build Context | `/` |

### Passo 4: Configurar Porta
- Porta exposta: **5555**
- Porta interna: **5555**

### Passo 5: Adicionar Variáveis de Ambiente
Copie e cole as variáveis listadas acima na seção "Environment Variables":

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

### Passo 6: Configurar Rede
**IMPORTANTE**:
- Selecione a mesma rede Docker que o PostgreSQL (`utils_postgress`)
- Isso permite comunicação interna entre containers

### Passo 7: Deploy
1. Clique em **"Deploy"** ou **"Create"**
2. Aguarde o build (~3-5 minutos na primeira vez)
3. Monitore os logs

---

## ✅ Verificação Pós-Deploy

### Teste 1: Health Check
```bash
curl https://SEU_DOMINIO.easypanel.host/health
```

**Resposta esperada**:
```json
{
  "status": "healthy",
  "service": "Mega-Sena Hacker API"
}
```

### Teste 2: Último Sorteio
```bash
curl https://SEU_DOMINIO.easypanel.host/resultado-ultimo-sorteio
```

**Resposta esperada**:
```json
{
  "concurso": 2954,
  "data": "2025-12-20",
  "numeros": [1, 9, 37, 39, 42, 44]
}
```

### Teste 3: Previsão Rápida
```bash
curl https://SEU_DOMINIO.easypanel.host/analise-qui-quadrado
```

Deve retornar uma previsão em ~10 segundos.

---

## ⚠️ Diferenças Local vs Produção

| Configuração | Local (Desenvolvimento) | Produção (EasyPanel) |
|--------------|------------------------|----------------------|
| DB_HOST | `31.97.172.217` | `utils_postgress` |
| Porta | `5555` | `5555` |
| Acesso DB | Via IP público | Via rede Docker interna |

---

## 🔧 Troubleshooting

### ❌ Erro: "Connection refused" ao acessar banco

**Causa**: App não consegue conectar ao PostgreSQL

**Soluções**:
1. Verificar que `DB_HOST=utils_postgress` (não o IP)
2. Confirmar que ambos estão na mesma rede Docker
3. Verificar se PostgreSQL está rodando

### ❌ Erro: Build falha

**Causa**: Dependências não instalam

**Soluções**:
1. Verificar logs do build
2. Qiskit pode demorar ~5-10 min (é normal)
3. Tentar rebuild forçado

### ❌ Erro: App não inicia

**Causa**: Porta ou configuração errada

**Soluções**:
1. Verificar logs da aplicação
2. Confirmar `PORT=5555`
3. Verificar que todas as variáveis de ambiente foram configuradas

---

## 📊 Performance Esperada

| Endpoint | Tempo |
|----------|-------|
| /health | < 1s |
| /resultado-ultimo-sorteio | < 1s |
| /analise-qui-quadrado | 5-10s |
| /atratores-de-lorenz | 5-8s |
| /analise-quantica | 30-45s |
| /previsao | 60-90s |
| /teste-cego | 60-90s |

---

## 🔄 Auto-Deploy

Para habilitar deploy automático em cada push:

1. Vá em **Settings** da aplicação
2. Ative **"Auto Deploy"**
3. Selecione branch `main`
4. Agora cada push para `main` fará rebuild automático

---

## 📚 Documentação Adicional

- **Testes Completos**: Ver [TESTES_COMPLETOS.md](TESTES_COMPLETOS.md)
- **Análise Quântica**: Ver [ANALISE_QUANTICA_DETALHADA.md](ANALISE_QUANTICA_DETALHADA.md)
- **Integração n8n**: Ver [N8N_INTEGRATION.md](N8N_INTEGRATION.md)
- **Deploy Detalhado**: Ver [DEPLOY_EASYPANEL.md](DEPLOY_EASYPANEL.md)

---

## ✅ Checklist Final

Antes de considerar deploy completo:

- [ ] Repositório GitHub acessível
- [ ] App criado no EasyPanel
- [ ] Todas as variáveis de ambiente configuradas
- [ ] Rede Docker configurada
- [ ] Build concluído sem erros
- [ ] `/health` respondendo 200 OK
- [ ] `/resultado-ultimo-sorteio` retornando dados
- [ ] Logs sem erros críticos
- [ ] Integração n8n testada (opcional)

---

## 🎉 Após Deploy Bem-Sucedido

1. **Anotar URL pública** fornecida pelo EasyPanel
2. **Configurar workflows n8n** com a nova URL
3. **Testar todos os endpoints** em produção
4. **Monitorar logs** nas primeiras horas
5. **Documentar** qualquer ajuste necessário

---

## 📞 Suporte

Se encontrar problemas:

1. **Logs**: Verifique logs no painel EasyPanel
2. **Status**: Use endpoint `/health`
3. **Banco**: Teste conexão com `test_db_connection.py`
4. **Documentação**: Revise arquivos `.md` do projeto

---

**Repositório**: https://github.com/brotto/Mega-Sena-Hacker

**Status**: ✅ Pronto para deploy!
