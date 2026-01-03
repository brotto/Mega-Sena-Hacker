# ========================================================================
# PASSO 4: CONFIGURAR n8n COM NOVOS ENDPOINTS
# ========================================================================

NOVOS COMANDOS PARA ADICIONAR AO WORKFLOW 3:
--------------------------------------------

No Workflow "Callback Análise Mega-Sena Whats Business API"
Node: "busca análises auto" (Switch)

ADICIONAR ESTAS 7 NOVAS CONDITIONS:
-----------------------------------

```json
{
  "conditions": [
    // ... CONDIÇÕES EXISTENTES ...
    
    // === NOVOS COMANDOS v2.0 ===
    
    {
      "leftValue": "={{ $item(\"0\").$node[\"Start\"].json[\"body\"][\"opcao\"] }}",
      "rightValue": "Teste de Runs",
      "operator": { "type": "string", "operation": "equals" }
    },
    {
      "leftValue": "={{ $item(\"0\").$node[\"Start\"].json[\"body\"][\"opcao\"] }}",
      "rightValue": "Velocidade de Cobertura",
      "operator": { "type": "string", "operation": "equals" }
    },
    {
      "leftValue": "={{ $item(\"0\").$node[\"Start\"].json[\"body\"][\"opcao\"] }}",
      "rightValue": "Coeficiente de Variação",
      "operator": { "type": "string", "operation": "equals" }
    },
    {
      "leftValue": "={{ $item(\"0\").$node[\"Start\"].json[\"body\"][\"opcao\"] }}",
      "rightValue": "Relatório Completo",
      "operator": { "type": "string", "operation": "equals" }
    },
    {
      "leftValue": "={{ $item(\"0\").$node[\"Start\"].json[\"body\"][\"opcao\"] }}",
      "rightValue": "Mega Virada 2025",
      "operator": { "type": "string", "operation": "equals" }
    },
    {
      "leftValue": "={{ $item(\"0\").$node[\"Start\"].json[\"body\"][\"opcao\"] }}",
      "rightValue": "Brasil vs EUA",
      "operator": { "type": "string", "operation": "equals" }
    },
    {
      "leftValue": "={{ $item(\"0\").$node[\"Start\"].json[\"body\"][\"opcao\"] }}",
      "rightValue": "Classificação Automática",
      "operator": { "type": "string", "operation": "equals" }
    }
  ]
}
```

CRIAR 7 NOVOS NODES HTTP REQUEST:
---------------------------------

### 1. Node: "Teste de Runs"
```json
{
  "name": "Teste de Runs",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "http://firecrawl_mega-sena-hacker:5555/v2/runs-test",
    "method": "GET",
    "options": {}
  }
}
```

### 2. Node: "Velocidade de Cobertura"
```json
{
  "name": "Velocidade de Cobertura",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "http://firecrawl_mega-sena-hacker:5555/v2/coverage-speed",
    "method": "GET",
    "options": {}
  }
}
```

### 3. Node: "Coeficiente de Variação"
```json
{
  "name": "Coeficiente de Variação",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "http://firecrawl_mega-sena-hacker:5555/v2/coefficient-variation",
    "method": "GET",
    "options": {}
  }
}
```

### 4. Node: "Relatório Completo"
```json
{
  "name": "Relatório Completo",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "http://firecrawl_mega-sena-hacker:5555/v2/full-report",
    "method": "GET",
    "options": {}
  }
}
```

### 5. Node: "Mega Virada 2025"
```json
{
  "name": "Mega Virada 2025",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "http://firecrawl_mega-sena-hacker:5555/v2/mega-virada-2025",
    "method": "GET",
    "options": {}
  }
}
```

### 6. Node: "Brasil vs EUA"
```json
{
  "name": "Brasil vs EUA",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "http://firecrawl_mega-sena-hacker:5555/v2/comparative-analysis",
    "method": "GET",
    "options": {}
  }
}
```

### 7. Node: "Classificação Automática"
```json
{
  "name": "Classificação Automática",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "http://firecrawl_mega-sena-hacker:5555/v2/classification",
    "method": "GET",
    "options": {}
  }
}
```

CRIAR 7 NOVOS NODES WHATSAPP (Send Message):
--------------------------------------------

### Template Base (adaptar para cada endpoint):

```json
{
  "name": "Send message - [Nome do Teste]",
  "type": "n8n-nodes-base.whatsApp",
  "typeVersion": 1.1,
  "parameters": {
    "operation": "send",
    "phoneNumberId": "926770023855130",
    "recipientPhoneNumber": "={{ $item(\"0\").$node[\"Start\"].json[\"body\"][\"telefone\"] }}",
    "textBody": "=📊 [TÍTULO DO TESTE]

[FORMATAÇÃO ESPECÍFICA DE CADA TESTE]

{{ $json.metodo }}

Resultado: {{ $json.interpretacao.classificacao }}
Nível de Suspeita: {{ $json.interpretacao.nivel_suspeita }}

⚠️ Aviso: Esta é uma análise estatística. A Mega-Sena permanece aleatória.",
    "additionalFields": {}
  }
}
```

EXEMPLOS DE FORMATAÇÃO:

### 1. Teste de Runs:
```
🔬 Teste de Runs (Wald-Wolfowitz)

Detecta padrões de agrupamento não-aleatório nas sequências.

Z-score: {{ $('Teste de Runs').item.json.interpretacao.z_score }}
Classificação: {{ $('Teste de Runs').item.json.interpretacao.classificacao }}
Nível de Suspeita: {{ $('Teste de Runs').item.json.interpretacao.nivel_suspeita }}

Interpretação:
• Z-score < -10 ou > 10: PRNG (agrupamento extremo)
• |Z-score| < 2: RNG (aleatório)

⚠️ Esta análise é puramente estatística.
```

### 2. Relatório Completo:
```
📋 Relatório Completo - Classificação PRNG/RNG

🎯 Classificação: {{ $('Relatório Completo').item.json.classificacao }}
📊 Confiança: {{ $('Relatório Completo').item.json.confianca }}%

Anomalias Detectadas:
🔴 Críticas: {{ $('Relatório Completo').item.json.anomalias_criticas }}
🟠 Altas: {{ $('Relatório Completo').item.json.anomalias_altas }}

Resumo:
{{ $('Relatório Completo').item.json.resumo_executivo }}

⚠️ Análise baseada em {{ $('Relatório Completo').item.json.total_concursos }} concursos.
```

### 3. Mega Virada 2025:
```
🎊 Mega da Virada 2025 - Análise de Anomalias

Números Sorteados: 09, 13, 21, 32, 33, 59
Ganhadores: 6 (esperado: 12)
Razão Quina/Sena: 654 (esperado: 324)

📊 Probabilidade de Manipulação: {{ $('Mega Virada 2025').item.json.conclusao.probabilidade_manipulacao }}
🔍 Anomalias: {{ $('Mega Virada 2025').item.json.conclusao.anomalias_encontradas }}
⚠️ Nível: {{ $('Mega Virada 2025').item.json.conclusao.nivel_suspeita }}

Anomalias Circunstanciais:
• Atraso de 13 horas (inédito)
• Globo não transmitiu (1ª vez em 15 anos)
• Dados não divulgados

Este é um estudo estatístico das anomalias observadas.
```

CRIAR 7 NOVOS NODES REDIS:
--------------------------

Após cada "Send message", adicionar Redis save:

```json
{
  "name": "Redis - [Nome do Teste]",
  "type": "n8n-nodes-base.redis",
  "typeVersion": 1,
  "parameters": {
    "operation": "set",
    "key": "=analise_user:{{ $json.data.key.remoteJid }}",
    "value": "={{ JSON.stringify($json.data.message.conversation) }}",
    "expire": true,
    "ttl": 300
  },
  "credentials": {
    "redis": {
      "id": "sZNxuhWjx4fuB5VA",
      "name": "Redis account 2"
    }
  }
}
```

MENU WHATSAPP ATUALIZADO (TypeBot):
-----------------------------------

Adicionar ao menu do TypeBot:

```
Escolha a análise:

📊 Análises Existentes:
1️⃣ Resultado do último sorteio
2️⃣ Análise Qui-quadrado
3️⃣ Análise por atratores de Lorenz
4️⃣ Análise quântica
5️⃣ Análise estatística geral
6️⃣ Teste cego

🚀 Novas Análises v2.0:
7️⃣ Teste de Runs
8️⃣ Velocidade de Cobertura
9️⃣ Coeficiente de Variação
🔟 Relatório Completo
1️⃣1️⃣ Mega Virada 2025
1️⃣2️⃣ Brasil vs EUA
1️⃣3️⃣ Classificação Automática
```

TESTES APÓS CONFIGURAÇÃO:
-------------------------

1. Testar CADA novo comando via WhatsApp
2. Verificar se respostas chegam formatadas
3. Confirmar que Redis salva resultados
4. Testar AI Agent com novos comandos

PRÓXIMO PASSO:
-------------
Testar tudo em produção!
