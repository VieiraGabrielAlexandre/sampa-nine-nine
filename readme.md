# Airdrop Optimizer - Hackathon Fetch.ai

## 🔍 Visão Geral
Este projeto simula um ecossistema de agentes autônomos capazes de identificar e participar de campanhas de airdrop, otimizando operações de **spot trading** na Binance. Os agentes são implementados em Python com uma arquitetura modular e orientada a componentes.

---

## ⚙️ Componentes do Sistema

### 1. `airdrop_scout_agent.py`
- Simula scraping da página de airdrops da Binance.
- Gera campanhas fictícias com informações como token, volume, recompensa e viabilidade.

### 2. `campaign_agent_creator.py`
- Cria instâncias de agentes de trading com base nas campanhas recebidas.

### 3. `trading_agent.py`
- Executa ordens de compra/venda com base nas recomendações do agente de previsão.
- Simula operações até atingir o volume de trading exigido pela campanha.

### 4. `prediction_agent.py`
- Fornece decisões de trading simples (BUY, SELL, HOLD) com base em média móvel.

### 5. `main.py`
- Orquestra a execução de todo o sistema: coleta campanhas, cria agentes e executa as negociações simuladas.

---

## 📦 Instalação

1. Clone o repositório ou baixe os arquivos.
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## 🚀 Como Executar

Basta rodar o arquivo principal:

```bash
python main.py
```

Você verá logs no terminal simulando a identificação de airdrops, criação de agentes e execução de trades.

---

## 📁 Estrutura de Pastas

```
├── airdrop_scout_agent.py
├── campaign_agent_creator.py
├── trading_agent.py
├── prediction_agent.py
├── main.py
├── requirements.txt
└── README.md
```
