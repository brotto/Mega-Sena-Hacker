# Integração PRNG/RNG Analyzer - Resumo da Implementação

## 📅 Data: 02/01/2026

## ✅ O Que Foi Feito

### 1. Integração de Novos Analyzers

#### Arquivos Adicionados:
- **`analyzers/lottery_analyzer.py`**: Classe principal com 4 testes estatísticos
  - Teste Chi-Quadrado
  - Teste de Runs (Wald-Wolfowitz)
  - Velocidade de Cobertura (Coupon Collector)
  - Coeficiente de Variação Temporal

- **`analyzers/prng_detector.py`**: Adapter para PostgreSQL
  - Carrega dados do banco
  - Executa análises PRNG vs RNG
  - Fornece classificação automática

### 2. Novos Endpoints API

#### `/analise-prng-rng` (GET/POST)
Análise rápida PRNG vs RNG
- Retorna classificação (PRNG ou RNG)
- Confiança percentual
- Indicadores Chi-Quadrado e Runs Test

**Exemplo de Resposta:**
```json
{
  "classificacao": "PRNG (Pseudo-Aleatório)",
  "confianca": "80%",
  "total_concursos_analisados": 3274,
  "indicadores": {
    "chi_quadrado": {
      "p_value": 0.0,
      "nivel_suspeita": "MODERADO"
    },
    "teste_runs": {
      "z_score": -936.04,
      "nivel_suspeita": "CRÍTICO"
    }
  }
}
```

#### `/analise-prng-completa` (GET/POST)
Análise completa com todos os 4 testes estatísticos
- Chi-Quadrado completo
- Runs Test detalhado
- Velocidade de Cobertura
- Evolução do Coeficiente de Variação
- Relatório final com classificação

#### `/estatisticas-distribuicao` (GET/POST)
Estatísticas descritivas da distribuição
- Números mais/menos sorteados
- Frequência média e desvio padrão
- Coeficiente de variação

### 3. Ambiente Virtual e Dependências

#### Criado:
- Ambiente virtual Python 3.9 em `/Users/alebrotto/Mega-Sena-Hacker/venv`

#### Instalado:
```
pandas==2.3.3
numpy==2.0.2
scipy==1.13.1
matplotlib==3.9.4
seaborn==0.13.2
openpyxl==3.1.5
flask==3.1.2
psycopg2-binary==2.9.11
python-dotenv==1.2.1
gunicorn==23.0.0
qiskit==2.2.3
qiskit-aer==0.17.2
```

### 4. Configuração

#### Arquivo `.env` criado:
```env
DB_USER=alebrotto
DB_PASSWORD=BrottoK@was0975
DB_HOST=31.97.172.217
DB_PORT=5432
DB_NAME=utils
DB_SCHEMA=public
DB_TABLE=megasena
PORT=5555
DEBUG=False
```

### 5. Documentação Atualizada

- [README.md](README.md): Adicionadas seções sobre novos endpoints
- Exemplos de uso dos novos endpoints
- Descrição dos métodos de análise PRNG/RNG

## 🔬 Como Funcionam as Análises PRNG/RNG

### O Que Detectamos

**PRNG (Pseudo-Random Number Generator)**:
- Equalização artificial muito rápida
- Padrões de agrupamento não-aleatórios
- Coeficiente de variação artificialmente estável

**RNG (Random Number Generator)**:
- Variação natural esperada
- Distribuição verdadeiramente aleatória
- Comportamento estatístico normal

### Testes Implementados

1. **Chi-Quadrado de Pearson**
   - Verifica uniformidade da distribuição
   - P-valor muito baixo ou muito alto = suspeito

2. **Teste de Runs (Wald-Wolfowitz)**
   - Detecta agrupamento artificial
   - Z-score extremo (|Z| > 10) = PRNG

3. **Velocidade de Cobertura**
   - Analisa rapidez para cobrir todos os números
   - Muito mais rápido que teoria = PRNG

4. **Coeficiente de Variação**
   - Monitora estabilidade ao longo do tempo
   - CV muito estável = PRNG

## 🎯 Resultados Iniciais

### Mega-Sena Brasil
- **Classificação**: PRNG (Pseudo-Aleatório)
- **Confiança**: 80%
- **Z-score Runs Test**: -936 (extremamente anômalo)
- **P-value Chi-Quadrado**: 0.0 (rejeita uniformidade)

## 🚀 Como Usar no VPS

### Iniciar Servidor
```bash
cd /Users/alebrotto/Mega-Sena-Hacker
source venv/bin/activate
PORT=5555 python app.py
```

### Ou com Gunicorn (produção)
```bash
gunicorn -w 4 -b 0.0.0.0:5555 app:app
```

### Testar Localmente
```bash
# Análise rápida PRNG
curl http://localhost:5555/analise-prng-rng

# Análise completa
curl http://localhost:5555/analise-prng-completa

# Estatísticas
curl http://localhost:5555/estatisticas-distribuicao
```

## 📊 Endpoints Mantidos

Todos os endpoints anteriores continuam funcionando:
- `/health`
- `/resultado-ultimo-sorteio`
- `/analise-qui-quadrado`
- `/atratores-de-lorenz`
- `/analise-quantica`
- `/previsao`
- `/teste-cego`

## ⚙️ Para Deploy no VPS

1. **Fazer push para GitHub**
```bash
git add -A
git commit -m "Add PRNG/RNG detection endpoints"
git push origin main
```

2. **No VPS, fazer pull**
```bash
cd /caminho/projeto
git pull origin main
```

3. **Instalar dependências**
```bash
pip install -r requirements.txt
```

4. **Atualizar variáveis de ambiente** (se necessário)
```bash
# No VPS, usar host interno do Docker
DB_HOST=utils_postgress
```

5. **Reiniciar serviço**
```bash
systemctl restart mega-sena-api
# ou
supervisorctl restart mega-sena-api
```

## 📝 Notas Importantes

- O sistema mantém **total compatibilidade** com a API anterior
- Novos endpoints são **adicionais**, não substituem os existentes
- PostgreSQL continua sendo a fonte de dados
- Todos os testes passam com os dados atuais
- Análise PRNG detectou características não-aleatórias na Mega-Sena

## 🔗 Integração com n8n

Os novos endpoints podem ser usados em workflows n8n da mesma forma que os anteriores:

```javascript
// n8n HTTP Request Node
{
  "method": "GET",
  "url": "https://seu-vps.com/analise-prng-rng",
  "authentication": "none",
  "responseFormat": "json"
}
```

## ✅ Testes Realizados

- ✅ Import de módulos
- ✅ Conexão com PostgreSQL
- ✅ Endpoints antigos funcionando
- ✅ Endpoint `/analise-prng-rng` funcionando
- ✅ Endpoint `/analise-prng-completa` funcionando
- ✅ Endpoint `/estatisticas-distribuicao` funcionando
- ✅ Classificação PRNG detectada corretamente
- ✅ Documentação atualizada

## 🎉 Conclusão

A integração foi bem-sucedida! O projeto agora possui:
- **7 endpoints originais** para previsões
- **3 novos endpoints** para análise PRNG/RNG
- **Total: 10 endpoints funcionais**

Todos acessíveis via API REST mantendo a compatibilidade completa com integrações existentes.
