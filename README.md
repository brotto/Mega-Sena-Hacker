# Mega-Sena Hacker 🎰

Sistema avançado de análise preditiva para resultados da Mega-Sena utilizando múltiplos métodos científicos e computacionais.

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)]()
[![Tests](https://img.shields.io/badge/tests-7%2F7%20passing-brightgreen.svg)]()

## 📋 Descrição

Este projeto combina análises estatísticas, teoria do caos e simulação quântica para gerar previsões de números da Mega-Sena. Os dados são obtidos de um banco PostgreSQL hospedado no EasyPanel/Hostinger.

**✅ Status Atual**: Todos os testes passando (7/7) - Sistema totalmente funcional!

## 🔬 Métodos de Análise

### 1. Qui-Quadrado (χ²)
Análise estatística de frequência dos números sorteados para identificar padrões de distribuição e números "quentes" e "frios".

### 2. Atratores Estranhos (Lorenz)
Utiliza a teoria do caos e atratores de Lorenz para mapear a sequência temporal dos sorteios em um espaço tridimensional, identificando padrões caóticos.

### 3. Computação Quântica (Simulada)
Emprega simulação quântica usando Qiskit para explorar superposição, entrelaçamento e interferência quântica na geração de previsões.

## 🚀 Funcionalidades

### Endpoints da API

| Trigger | Endpoint | Descrição |
|---------|----------|-----------|
| "Resultado do último sorteio" | `/resultado-ultimo-sorteio` | Retorna o último resultado do banco |
| "Análise Qui-Quadrado" | `/analise-qui-quadrado` | Análise estatística χ² completa |
| "Atratores de Lorenz" | `/atratores-de-lorenz` | Análise caótica + visualização 3D |
| "Análise quântica" | `/analise-quantica` | Simulação quântica com Qiskit |
| "Previsão" | `/previsao` | Previsão combinada (todos os métodos) |

## 📦 Instalação

### Requisitos
- Python 3.11+
- PostgreSQL (remoto via EasyPanel)
- Docker (opcional)

### Instalação Local

```bash
# Clone o repositório
git clone <seu-repo>
cd Mega-Sena-Hacker

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas credenciais

# Execute a aplicação
python app.py
```

### Instalação com Docker

```bash
# Build da imagem
docker build -t mega-sena-hacker .

# Executar container
docker run -p 5000:5000 --env-file .env mega-sena-hacker

# Ou usar docker-compose
docker-compose up -d
```

## 🗄️ Configuração do Banco de Dados

Credenciais PostgreSQL (EasyPanel/Hostinger):

```
Usuário: alebrotto
Senha: BrottoK@was0975
Host: utils_postgress
Porta: 5432
Database: utils
Schema: Mega-Sena-4
```

**Estrutura esperada da tabela:**
```sql
CREATE TABLE "Mega-Sena-4".resultados (
    concurso INTEGER PRIMARY KEY,
    data DATE,
    bola1 INTEGER,
    bola2 INTEGER,
    bola3 INTEGER,
    bola4 INTEGER,
    bola5 INTEGER,
    bola6 INTEGER
);
```

## 🧪 Testes Locais (Fase 1)

O sistema inclui testes "cegos" para validação das previsões:

```bash
# Execute o script de testes interativo
python test_local.py
```

### Metodologia de Teste Cego

1. Utiliza dados parciais (ex: até concurso 2000)
2. Gera previsão para o próximo concurso (2001)
3. Compara com resultado real
4. Calcula taxa de acerto

```python
# Exemplo via API
POST /teste-cego
{
    "concurso_limite": 2000
}
```

## 🔌 Integração com n8n

Consulte [N8N_INTEGRATION.md](N8N_INTEGRATION.md) para detalhes completos de integração.

### Exemplo de Workflow n8n

```
Webhook Trigger
    ↓
Switch (baseado em palavra-chave)
    ↓
HTTP Request → API Endpoint
    ↓
Return Response
```

## 📊 Estrutura do Projeto

```
Mega-Sena-Hacker/
├── analyzers/
│   ├── __init__.py
│   ├── chi_square.py          # Análise Qui-Quadrado
│   ├── lorenz_attractor.py    # Atratores de Lorenz
│   └── quantum_analyzer.py    # Simulação Quântica
├── app.py                      # API Flask principal
├── database.py                 # Conexão PostgreSQL
├── config.py                   # Configurações
├── test_local.py              # Testes interativos
├── requirements.txt           # Dependências Python
├── Dockerfile                 # Container Docker
├── docker-compose.yml         # Orquestração Docker
├── .env.example               # Template de variáveis
├── N8N_INTEGRATION.md         # Docs integração n8n
└── README.md                  # Este arquivo
```

## 🎯 Uso da API

### Exemplo: Obter Previsão

```bash
curl http://localhost:5000/previsao
```

**Resposta:**
```json
{
  "previsao_final": [7, 14, 21, 28, 35, 42],
  "metodos_utilizados": [
    "Qui-Quadrado",
    "Atratores de Lorenz",
    "Análise Quântica"
  ],
  "previsoes_individuais": {
    "qui_quadrado": {...},
    "lorenz": {...},
    "quantica": {...}
  },
  "total_concursos_analisados": 2900
}
```

### Exemplo: Visualizar Atrator de Lorenz

```bash
curl http://localhost:5000/atratores-de-lorenz
```

A resposta inclui uma imagem PNG em base64 do diagrama 3D.

## 🚢 Deploy no EasyPanel

1. **Criar Aplicação Customizada no EasyPanel:**
   - Tipo: GitHub App
   - Repositório: seu-usuario/Mega-Sena-Hacker
   - Build Command: `docker build -t mega-sena-hacker .`
   - Start Command: configurado no Dockerfile

2. **Configurar Variáveis de Ambiente:**
   ```
   DB_USER=alebrotto
   DB_PASSWORD=BrottoK@was0975
   DB_HOST=utils_postgress
   DB_PORT=5432
   DB_NAME=utils
   DB_SCHEMA=Mega-Sena-4
   PORT=5000
   ```

3. **Conectar ao PostgreSQL:**
   - O banco já está rodando no EasyPanel
   - Usar o host interno: `utils_postgress`

## 📈 Roadmap

### ✅ Fase 1: Testes Locais
- [x] Implementação dos 3 métodos de análise
- [x] Sistema de testes cegos
- [x] API REST completa
- [ ] Refinamento baseado em resultados

### 🔄 Fase 2: Validação
- [ ] Testes com múltiplos cenários
- [ ] Comparação de performance entre métodos
- [ ] Ajustes de parâmetros
- [ ] Documentação de resultados

### 🚀 Fase 3: Deploy
- [ ] Push para GitHub
- [ ] Deploy no EasyPanel
- [ ] Configuração de workflows n8n
- [ ] Monitoramento e logs

## 🧮 Como Funcionam os Métodos

### Qui-Quadrado
1. Calcula frequência de cada número (1-60)
2. Testa se distribuição é uniforme
3. Identifica números "frios" (menos sorteados)
4. Identifica números "quentes" (mais sorteados)
5. Combina estratégias para previsão

### Atratores de Lorenz
1. Mapeia números sorteados para estados 3D
2. Gera trajetórias no espaço de fase
3. Identifica padrões caóticos
4. Projeta próximo estado
5. Converte de volta para números 1-60

### Simulação Quântica
1. Cria circuitos quânticos com 6 qubits
2. Aplica superposição (Hadamard gates)
3. Entrelaça qubits (CNOT gates)
4. Rotações baseadas em dados históricos
5. Aplica QFT (Quantum Fourier Transform)
6. Mede resultados e mapeia para números

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## ⚠️ Disclaimer

Este projeto é apenas para fins educacionais e de pesquisa. Loterias são jogos de azar e não existe método científico que possa garantir previsões precisas. Use por sua conta e risco.

## 📄 Licença

MIT License - veja LICENSE para detalhes.

## 👤 Autor

**alebrotto**

## 🙏 Agradecimentos

- Qiskit (IBM Quantum)
- SciPy e NumPy communities
- Flask framework
- PostgreSQL
