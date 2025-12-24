# Quick Start Guide 🚀

Guia rápido para começar a usar o Mega-Sena Hacker.

## Setup Inicial (5 minutos)

### 1. Clone/Configure o Projeto

```bash
cd "/Users/alebrotto/Documents/Mega-Sena Hacker"
```

### 2. Configure o Ambiente

```bash
# Criar arquivo .env com credenciais
cp .env.example .env
# O .env já está configurado com as credenciais corretas do PostgreSQL
```

### 3. Execute Local

```bash
# Opção 1: Script automatizado (recomendado)
./run_local.sh

# Opção 2: Manual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

A API estará disponível em: **http://localhost:5000**

## Testar a API (2 minutos)

### Opção 1: Script de Testes Interativo

```bash
python test_local.py
```

Escolha uma opção do menu para testar os endpoints.

### Opção 2: Testes com cURL

```bash
# Health check
curl http://localhost:5000/health

# Último sorteio
curl http://localhost:5000/resultado-ultimo-sorteio

# Previsão combinada
curl http://localhost:5000/previsao

# Análise Qui-Quadrado
curl http://localhost:5000/analise-qui-quadrado

# Atratores de Lorenz
curl http://localhost:5000/atratores-de-lorenz

# Análise Quântica
curl http://localhost:5000/analise-quantica

# Teste Cego
curl -X POST http://localhost:5000/teste-cego \
  -H "Content-Type: application/json" \
  -d '{"concurso_limite": 2000}'
```

## Endpoints Principais

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/health` | GET | Status da API |
| `/resultado-ultimo-sorteio` | GET | Último resultado |
| `/previsao` | GET | **Previsão combinada (recomendado)** |
| `/analise-qui-quadrado` | GET | Análise estatística |
| `/atratores-de-lorenz` | GET | Análise caótica + gráfico |
| `/analise-quantica` | GET | Simulação quântica |
| `/teste-cego` | POST | Validação preditiva |

## Respostas Esperadas

### ✅ Sucesso: Status 200
```json
{
  "previsao_final": [7, 14, 21, 28, 35, 42],
  "metodos_utilizados": ["Qui-Quadrado", "Lorenz", "Quântica"],
  ...
}
```

### ❌ Erro: Status 500
```json
{
  "error": "Descrição do erro"
}
```

Erros comuns:
- **Conexão com banco:** Verifique credenciais no `.env`
- **Dependências:** Execute `pip install -r requirements.txt`
- **Porta ocupada:** Mude `PORT` no `.env`

## Fase 1: Testes Cegos

### Objetivo
Validar a precisão das previsões usando dados históricos.

### Como Funciona
1. Usa dados até o concurso N
2. Prevê o concurso N+1
3. Compara com resultado real
4. Calcula taxa de acerto

### Executar Teste

```bash
# Via script de testes
python test_local.py
# Escolha opção 7

# Via cURL
curl -X POST http://localhost:5000/teste-cego \
  -H "Content-Type: application/json" \
  -d '{"concurso_limite": 2500}'
```

### Exemplo de Resultado
```json
{
  "concurso_treino_ate": 2500,
  "concurso_testado": 2501,
  "previsao": [3, 15, 27, 38, 44, 59],
  "resultado_real": [5, 17, 29, 40, 46, 60],
  "acertos": 0,
  "taxa_acerto": "0.00%"
}
```

## Deploy no EasyPanel (10 minutos)

### 1. Push para GitHub

```bash
git init
git add .
git commit -m "Initial commit: Mega-Sena Hacker"
git remote add origin https://github.com/SEU-USUARIO/Mega-Sena-Hacker.git
git push -u origin main
```

Ver detalhes completos em: [GITHUB_SETUP.md](GITHUB_SETUP.md)

### 2. Criar App no EasyPanel

1. Acesse seu painel EasyPanel
2. **Create → GitHub App**
3. Selecione o repositório `Mega-Sena-Hacker`
4. Configure:
   - Build: Dockerfile
   - Port: 5000

### 3. Configurar Variáveis

No painel do EasyPanel, adicione:

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

### 4. Deploy

- EasyPanel fará build automático
- Aguarde conclusão (~3-5 min)
- Acesse via URL fornecida

## Integração n8n (5 minutos)

### Workflow Básico

1. **Criar Webhook no n8n:**
   - Trigger: Webhook
   - Path: `/mega-sena-trigger`

2. **Adicionar HTTP Request:**
   - Method: GET
   - URL: `https://sua-url.com/previsao`

3. **Processar Resposta:**
   - Extract: `$.previsao_final`

4. **Enviar Notificação:**
   - Email, Slack, Telegram, etc.

Ver detalhes completos em: [N8N_INTEGRATION.md](N8N_INTEGRATION.md)

## Estrutura de Arquivos

```
Mega-Sena-Hacker/
├── analyzers/           # Módulos de análise
│   ├── chi_square.py        # Qui-Quadrado
│   ├── lorenz_attractor.py  # Lorenz
│   └── quantum_analyzer.py  # Quântica
├── app.py              # API Flask
├── database.py         # Conexão PostgreSQL
├── config.py           # Configurações
├── test_local.py       # Testes interativos
├── Dockerfile          # Container
└── README.md           # Documentação completa
```

## Troubleshooting

### Problema: "ModuleNotFoundError"
**Solução:**
```bash
pip install -r requirements.txt
```

### Problema: "Connection refused" (Banco de Dados)
**Solução:**
- Verifique credenciais no `.env`
- Teste conexão com o banco:
```bash
psql -h utils_postgress -p 5432 -U alebrotto -d utils
```

### Problema: "Port 5000 already in use"
**Solução:**
```bash
# Mudar porta no .env
echo "PORT=5001" >> .env

# Ou matar processo
lsof -ti:5000 | xargs kill -9
```

### Problema: Análise quântica muito lenta
**Normal:** A simulação quântica pode levar 10-30 segundos.
**Solução:** Reduzir `shots` no código ou usar endpoint `/previsao` que é otimizado.

## Próximos Passos

- [ ] Executar testes cegos com múltiplos concursos
- [ ] Refinar parâmetros de análise
- [ ] Comparar performance dos métodos
- [ ] Deploy no EasyPanel
- [ ] Configurar workflow n8n
- [ ] Documentar resultados

## Recursos

- 📖 [README.md](README.md) - Documentação completa
- 🐙 [GITHUB_SETUP.md](GITHUB_SETUP.md) - Setup do repositório
- 🔌 [N8N_INTEGRATION.md](N8N_INTEGRATION.md) - Integração n8n
- 🧪 [test_local.py](test_local.py) - Script de testes

## Suporte

Em caso de dúvidas ou problemas:
1. Consulte a documentação completa no README.md
2. Verifique os logs da aplicação
3. Teste conexão com banco de dados
4. Verifique variáveis de ambiente

---

**Lembre-se:** Este é um projeto educacional. Loterias são jogos de azar.
