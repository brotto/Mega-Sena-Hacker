# Integração com n8n

Este documento descreve como integrar a API do Mega-Sena Hacker com workflows do n8n.

## Endpoints Disponíveis

Todos os endpoints aceitam requisições GET e POST.

### 1. Health Check
**Endpoint:** `/health`
**Método:** GET
**Descrição:** Verifica se a API está funcionando

**Exemplo de uso no n8n:**
```
HTTP Request Node
- Method: GET
- URL: http://seu-servidor:5000/health
```

### 2. Resultado do Último Sorteio
**Endpoint:** `/resultado-ultimo-sorteio`
**Método:** GET ou POST
**Trigger:** "Resultado do último sorteio"

**Resposta:**
```json
{
  "concurso": 2900,
  "data": "2024-01-15",
  "numeros": [5, 12, 23, 34, 45, 58]
}
```

**Exemplo n8n:**
```
HTTP Request Node
- Method: GET
- URL: http://seu-servidor:5000/resultado-ultimo-sorteio
```

### 3. Análise Qui-Quadrado
**Endpoint:** `/analise-qui-quadrado`
**Método:** GET ou POST
**Trigger:** "Análise Qui-Quadrado"

**Resposta:**
```json
{
  "metodo": "Análise Qui-Quadrado",
  "estatisticas": {...},
  "teste_qui_quadrado": {...},
  "previsao": {
    "prediction": [3, 15, 27, 38, 42, 59],
    "method": "Chi-Square (Cold + Hot Numbers)"
  }
}
```

### 4. Atratores de Lorenz
**Endpoint:** `/atratores-de-lorenz`
**Método:** GET ou POST
**Trigger:** "Atratores de Lorenz"

**Resposta:**
```json
{
  "metodo": "Atratores de Lorenz",
  "analise_caos": {...},
  "previsao": {...},
  "visualizacao": {
    "tipo": "image/png",
    "data": "base64_encoded_image",
    "descricao": "Diagrama de Atratores de Lorenz"
  }
}
```

Para exibir a imagem no n8n, você pode decodificar o base64.

### 5. Análise Quântica
**Endpoint:** `/analise-quantica`
**Método:** GET ou POST
**Trigger:** "Análise quântica"

**Resposta:**
```json
{
  "metodo": "Análise Quântica (Simulação)",
  "estatisticas": {...},
  "previsao_metodo_1": {...},
  "previsao_metodo_2": {...}
}
```

### 6. Previsão Combinada
**Endpoint:** `/previsao`
**Método:** GET ou POST
**Trigger:** "Previsão"

**Resposta:**
```json
{
  "previsao_final": [7, 14, 21, 28, 35, 42],
  "metodos_utilizados": ["Qui-Quadrado", "Atratores de Lorenz", "Análise Quântica"],
  "previsoes_individuais": {...}
}
```

### 7. Teste Cego
**Endpoint:** `/teste-cego`
**Método:** POST
**Body:**
```json
{
  "concurso_limite": 2000
}
```

**Resposta:**
```json
{
  "concurso_treino_ate": 2000,
  "concurso_testado": 2001,
  "previsao": [1, 12, 23, 34, 45, 56],
  "resultado_real": [2, 13, 24, 35, 46, 57],
  "acertos": 0,
  "taxa_acerto": "0.00%"
}
```

## Workflow n8n Exemplo

### Workflow 1: Previsão Diária
```
1. Schedule Trigger (diariamente às 10h)
   ↓
2. HTTP Request → /previsao
   ↓
3. Set Node (formatar dados)
   ↓
4. Email/Slack/Telegram (enviar previsão)
```

### Workflow 2: Webhook para Análises sob Demanda
```
1. Webhook Trigger
   ↓
2. Switch Node (baseado em "trigger_word")
   - "Análise quântica" → /analise-quantica
   - "Análise Qui-Quadrado" → /analise-qui-quadrado
   - "Atratores de Lorenz" → /atratores-de-lorenz
   - "Previsão" → /previsao
   - "Resultado do último sorteio" → /resultado-ultimo-sorteio
   ↓
3. HTTP Request (endpoint apropriado)
   ↓
4. Return Response
```

### Workflow 3: Testes Automatizados
```
1. Schedule Trigger (semanalmente)
   ↓
2. HTTP Request → /teste-cego
   Body: {"concurso_limite": 2500}
   ↓
3. Set Node (calcular métricas)
   ↓
4. Google Sheets (salvar resultados)
   ↓
5. Email (relatório de performance)
```

## Configuração no n8n

### HTTP Request Node Settings:
- **Authentication:** None (ou configure se adicionar auth)
- **Request Method:** GET ou POST
- **URL:** `http://seu-servidor:5000/endpoint`
- **Response Format:** JSON
- **Timeout:** 60000ms (alguns métodos podem demorar)

### Headers Recomendados:
```json
{
  "Content-Type": "application/json",
  "Accept": "application/json"
}
```

## Deployment

Quando fizer deploy no EasyPanel:
1. A aplicação estará acessível via URL pública
2. Use essa URL nos workflows do n8n
3. Considere adicionar autenticação (Bearer Token) para produção

Exemplo de URL final:
```
https://mega-sena-hacker.seu-dominio.com/previsao
```

## Observações

- Todos os endpoints podem demorar alguns segundos para responder (especialmente análise quântica)
- Configure timeouts adequados no n8n
- A visualização de Lorenz retorna imagem em base64
- Para produção, adicione rate limiting e autenticação
