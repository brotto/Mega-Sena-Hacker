# 🎲 MEGA ANALYZER - Sistema de Análise de Aleatoriedade em Loterias

Sistema completo para detectar características de **PRNG (pseudo-aleatoriedade)** vs **RNG (aleatoriedade verdadeira)** em sistemas de loteria, desenvolvido baseado em análises estatísticas profundas da Mega-Sena brasileira.

## 🎯 Objetivo

Fornecer ferramentas científicas para:
- Detectar padrões de equalização artificial
- Comparar sistemas de loteria internacionalmente
- Identificar anomalias estatísticas
- Gerar relatórios técnicos fundamentados

## 📊 Descobertas Principais

### 🇧🇷 **Mega-Sena (Brasil)** - Comportamento PRNG

- ⚠️ **Equalização Extremamente Rápida**: Todos os 60 números aparecem em apenas 41 sorteios (teoria prevê ~246)
- ⚠️ **CV Artificialmente Baixo**: 6,69% (vs 12,77% da Mega Millions)
- ⚠️ **Runs Test Anômalo**: Z-score = -46,2 (agrupamento não-aleatório extremo)
- ⚠️ **Chi-Quadrado Suspeito**: P = 0,04 (rejeita uniformidade)

### 🇺🇸 **Mega Millions (EUA)** - Comportamento RNG

- ✅ **Variação Natural**: CV = 12,77%
- ✅ **Runs Test Normal**: Z-score = 0,70
- ✅ **Chi-Quadrado Normal**: P = 0,26
- ✅ **Cobertura Esperada**: +15% (dentro da variância normal)

### 🎊 **Mega da Virada 2025** - Caso Especial

**ANOMALIAS CRÍTICAS IDENTIFICADAS:**

1. **Estatísticas:**
   - Apenas 6 ganhadores (esperado: 12) - P = 4,1%
   - Razão Quina/Sena: 654 (esperado: 324) - **DOBRO!**
   - 3º maior razão da história

2. **Circunstanciais:**
   - Atraso de 13 horas (inédito)
   - Globo não transmitiu (1ª vez em 15 anos)
   - Dados não divulgados até agora
   - Sorteio em 01/01 (não foi "da virada")

## 🏗️ Estrutura do Projeto

```
mega_analyzer/
├── lottery_analyzer.py              # Classe principal de análise
├── exemplo_analise_completa.py      # Exemplo: Mega-Sena vs Mega Millions
├── analise_mega_virada_2025.py      # Análise específica da Virada 2025
├── requirements.txt                 # Dependências Python
└── README.md                        # Este arquivo
```

## 🔧 Instalação

### Requisitos

- Python 3.8+
- macOS, Linux ou Windows

### Instalar Dependências

```bash
pip install -r requirements.txt --break-system-packages  # macOS
```

ou

```bash
pip install -r requirements.txt  # Linux/Windows
```

## 🚀 Uso

### Análise Completa (Brasil vs EUA)

```bash
python3 exemplo_analise_completa.py
```

Executa todos os testes e gera relatórios comparativos.

### Análise da Mega da Virada 2025

```bash
python3 analise_mega_virada_2025.py
```

Analisa especificamente as anomalias da Virada 2025.

### Uso Programático

```python
from lottery_analyzer import LotteryAnalyzer

# Criar analisador
analyzer = LotteryAnalyzer("Mega-Sena")

# Carregar dados
ball_cols = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']
analyzer.load_data('dados.xlsx', ball_cols)

# Executar testes
analyzer.chi_square_test(n_possible=60)
analyzer.runs_test()
analyzer.coverage_speed_test(n_possible=60)
analyzer.coefficient_variation_evolution()

# Gerar relatório
report = analyzer.generate_final_report()

print(f"Classificação: {report['classification']}")
print(f"Confiança: {report['confidence']}%")
```

## 🧪 Testes Implementados

### 1. **Teste Chi-Quadrado** 
Verifica uniformidade da distribuição.
- PRNG: P-valor muito alto (>0.9) ou muito baixo (<0.05)
- RNG: P-valor moderado (0.1-0.9)

### 2. **Teste de Runs (Wald-Wolfowitz)**
Detecta agrupamento não-aleatório.
- PRNG: Z-score extremo (|Z| > 10)
- RNG: Z-score normal (|Z| < 2)

### 3. **Velocidade de Cobertura**
Analisa quantos sorteios para todos os números aparecerem.
- PRNG: Muito mais rápido que teoria (>50%)
- RNG: Próximo ao esperado (±20%)

### 4. **Evolução do Coeficiente de Variação**
Monitora estabilidade temporal.
- PRNG: CV estável (DP < 3%)
- RNG: CV variável naturalmente (DP > 5%)

### 5. **Razão Quina/Sena** (Mega da Virada)
Detecta viés de apostas vs sorteio.
- Normal: ~324 quinas por sena
- Anômalo: >500 quinas por sena

## 📈 Resultados

### Classificação Automática

O sistema classifica em:
- **PRNG (Pseudo-Aleatório com Equalização)** - 2+ anomalias críticas
- **PRNG Provável** - 3+ anomalias altas
- **Possivelmente PRNG** - Múltiplas anomalias moderadas
- **RNG (Verdadeiramente Aleatório)** - 3+ testes normais
- **INCONCLUSIVO** - Evidências mistas

### Níveis de Confiança

- **80-100%**: Muito alta confiança
- **60-79%**: Alta confiança
- **40-59%**: Moderada confiança
- **0-39%**: Baixa confiança

## 📁 Dados Necessários

### Formato Excel (.xlsx)

Colunas necessárias:
- `Bola1`, `Bola2`, ..., `BolaN` (números sorteados)
- `Data do Sorteio` (formato DD/MM/YYYY)
- `Ganhadores 6 acertos`, `Ganhadores 5 acertos` (opcional, para análise de viés)

### Formato CSV (.csv)

Colunas necessárias:
- `ball1`, `ball2`, ..., `ballN` (números sorteados)
- `draw_date` (data do sorteio)

## 🎓 Metodologia Científica

### Referências Teóricas

1. **Coupon Collector Problem**: E[T] = n·H(n) onde H(n) é o número harmônico
2. **Chi-Quadrado de Pearson**: χ² = Σ[(O-E)²/E]
3. **Teste de Runs**: Z = (R - E[R]) / √Var[R]
4. **Distribuição de Poisson**: Para modelar ganhadores

### Limites Estatísticos

- **α = 0.05** (nível de significância)
- **Z-crítico = ±1.96** (95% confiança)
- **χ²/df > 1.5**: Não-uniformidade suspeita

## ⚠️ Limitações

1. **Correlação ≠ Causalidade**: Anomalias estatísticas não provam manipulação
2. **Dados Limitados**: Algumas análises requerem milhares de sorteios
3. **Acesso Restrito**: Caixa não divulga dados de apostas
4. **Hipótese**: Sistema pode ser PRNG por design mecânico, não necessariamente fraude

## 💡 Recomendações

Para loterias com características PRNG:
- Auditoria independente do sistema
- Acesso ao código-fonte
- Comparação internacional
- Transparência total dos dados de apostas
- Publicação de logs de servidores

## 🤝 Contribuições

Este é um projeto científico aberto. Contribuições são bem-vindas:

- Novos testes estatísticos
- Comparações com outras loterias
- Melhorias na documentação
- Validação independente dos resultados

## 📧 Contato

Para discussões técnicas e científicas sobre as análises.

---

## 🔬 Filosofia do Projeto

> "O papel da ciência não é acusar, mas questionar.  
> Anomalias estatísticas merecem investigação,  
> não pela certeza de fraude,  
> mas pela dúvida que a ciência exige." 

**Transparência** é fundamental em sistemas que movimentam bilhões.

---

**Desenvolvido**: Janeiro 2025  
**Licença**: MIT (uso livre para fins acadêmicos e investigativos)  
**Status**: Versão 1.0 - Funcional
