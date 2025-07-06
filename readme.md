# Airdrop Optimizer - Hackathon Fetch.ai

## 🔍 Visão Geral
Este projeto simula um ecossistema de agentes autônomos capazes de identificar e participar de campanhas de airdrop, otimizando operações de **spot trading** na Binance. Os agentes são implementados em Python com uma arquitetura modular e orientada a componentes. O sistema inclui uma API RESTful para interagir com os agentes.

Para uma documentação detalhada sobre a arquitetura e funcionamento do sistema, consulte o arquivo [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md).

---

## ⚙️ Componentes do Sistema

### 1. Agentes Autônomos
#### `agents/airdrop_scout_agent.py`
- Simula scraping da página de airdrops da Binance.
- Gera campanhas fictícias com informações como token, volume, recompensa e viabilidade.

#### `agents/campaign_creator.py`
- Cria instâncias de agentes de trading com base nas campanhas recebidas.

#### `agents/trading_agent.py`
- Executa ordens de compra/venda com base nas recomendações do agente de previsão.
- Simula operações até atingir o volume de trading exigido pela campanha.

#### `agents/prediction_agent.py`
- Fornece decisões de trading simples (BUY, SELL, HOLD) com base em média móvel.

### 2. API e Orquestração
#### `api/main.py`
- Implementa uma API RESTful para interagir com o sistema.
- Fornece endpoints para gerenciar campanhas e agentes.

#### `main.py`
- Orquestra a execução de todo o sistema: coleta campanhas, cria agentes e executa as negociações simuladas.

#### `worker.py`
- Configura o worker Celery para processamento assíncrono de tarefas.

---

## 📦 Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/sampa-nine-nine.git
cd sampa-nine-nine
```

2. Crie e ative um ambiente virtual:

```bash
# Linux/macOS
python -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configuração do Redis (necessário para processamento assíncrono):

   **Opção 1:** Usando Docker (recomendado):
   ```bash
   docker-compose up -d redis
   ```

   **Opção 2:** Instalação manual do Redis:
   - [Instruções de instalação do Redis](https://redis.io/docs/getting-started/installation/)
   - Inicie o servidor Redis na porta 6380:
     ```bash
     redis-server --port 6380
     ```

---

## 🚀 Como Executar

O sistema pode ser executado de duas formas: via CLI (linha de comando) ou como uma API RESTful.

### Modo CLI

Este modo executa uma simulação completa do sistema em um único processo:

1. Certifique-se de que o ambiente virtual está ativado:
   ```bash
   # Linux/macOS
   source .venv/bin/activate

   # Windows
   .venv\Scripts\activate
   ```

2. Execute o arquivo principal:
   ```bash
   python main.py
   ```

3. Você verá logs no terminal simulando:
   - Identificação de campanhas de airdrop
   - Criação de agentes de trading
   - Execução de operações de compra e venda
   - Resultados finais das operações

### Modo API

Este modo inicia um servidor web que expõe endpoints RESTful para interagir com o sistema:

1. Inicie o servidor Redis (se ainda não estiver rodando):
   ```bash
   docker-compose up -d redis
   ```

2. Inicie o worker Celery em um terminal separado:
   ```bash
   # Linux/macOS
   source .venv/bin/activate
   celery -A worker worker --loglevel=info

   # Windows
   .venv\Scripts\activate
   celery -A worker worker --loglevel=info
   ```

3. Inicie o servidor da API em outro terminal:
   ```bash
   # Linux/macOS
   source .venv/bin/activate
   uvicorn api.main:app --reload

   # Windows
   .venv\Scripts\activate
   uvicorn api.main:app --reload
   ```

4. A API estará disponível em `http://localhost:8000`

#### Documentação da API
- **Swagger UI**: Acesse `http://localhost:8000/docs` para uma interface interativa
- **ReDoc**: Acesse `http://localhost:8000/redoc` para documentação detalhada
- **Guia de Teste**: Consulte [API_TESTING.md](API_TESTING.md) para instruções detalhadas

---

## 🧪 Testando a API

Após iniciar o servidor da API e o worker Celery, você pode testar os endpoints usando várias ferramentas:

1. **Script de Teste Automatizado**: 
   ```bash
   python test_api.py
   ```
   Este script demonstra como usar todos os endpoints da API e oferece a opção de executar todos os testes em sequência.

2. **Teste de Correção**:
   ```bash
   python test_fix.py
   ```
   Este script testa especificamente o endpoint `/airdrop` para verificar se ele está funcionando corretamente.

3. **Interface Swagger**: Acesse `http://localhost:8000/docs` no navegador para testar a API interativamente através de uma interface gráfica.

4. **Comandos Curl**: Consulte o arquivo [API_TESTING.md](API_TESTING.md) para exemplos de como testar cada endpoint usando curl.

---

## 📁 Estrutura de Pastas

```
├── agents/                      # Módulos dos agentes autônomos
│   ├── __init__.py
│   ├── airdrop_scout_agent.py   # Agente que identifica campanhas de airdrop
│   ├── campaign_creator.py      # Agente que cria agentes de trading
│   ├── prediction_agent.py      # Agente que fornece recomendações de trading
│   └── trading_agent.py         # Agente que executa operações de trading
├── api/                         # API RESTful
│   ├── __init__.py
│   └── main.py                  # Implementação da API com FastAPI
├── main.py                      # Script principal para execução via CLI
├── worker.py                    # Configuração do worker Celery
├── celeryconfig.py              # Configuração do Celery
├── test_api.py                  # Script para testar os endpoints da API
├── test_fix.py                  # Script para testar correções específicas
├── API_TESTING.md               # Guia detalhado para testar a API
├── PROJECT_DOCUMENTATION.md     # Documentação detalhada do projeto
├── requirements.txt             # Dependências do projeto
├── docker-compose.yaml          # Configuração do Docker para Redis
└── README.md                    # Este arquivo
```

---

## 📝 Notas Importantes

### Sobre o Projeto
Este projeto foi desenvolvido como parte do Hackathon Fetch.ai para demonstrar o uso de agentes autônomos em operações de trading de criptomoedas. É uma **simulação** e não realiza operações reais de trading.

### Limitações Atuais
- O web scraping da página de airdrops da Binance é simulado
- As operações de trading são simuladas e não interagem com exchanges reais
- Os modelos de previsão são simplificados para fins de demonstração

### Próximos Passos
Para uma implementação em produção, seria necessário:
- Implementar web scraping real com tratamento de captchas e rate limiting
- Integrar com a API oficial da Binance para execução de ordens reais
- Implementar modelos de machine learning mais sofisticados
- Adicionar persistência de dados com banco de dados
- Implementar medidas de segurança para proteção de chaves de API

Para mais detalhes sobre considerações técnicas e implementação, consulte a [documentação detalhada do projeto](PROJECT_DOCUMENTATION.md#10-considerações-técnicas).
