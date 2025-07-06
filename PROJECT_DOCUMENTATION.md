# Airdrop Optimizer: Arquitetura e Funcionamento

## Sumário

1. [Visão Geral do Projeto](#1-visão-geral-do-projeto)
2. [Arquitetura do Sistema](#2-arquitetura-do-sistema)
3. [Componentes Principais](#3-componentes-principais)
   - [Airdrop Scout Agent](#31-airdrop-scout-agent)
   - [Campaign Creator Agent](#32-campaign-creator-agent)
   - [Trading Agent](#33-trading-agent)
   - [Prediction Agent](#34-prediction-agent)
4. [Fluxo de Trabalho](#4-fluxo-de-trabalho)
5. [API RESTful](#5-api-restful)
6. [Processamento Assíncrono](#6-processamento-assíncrono)
7. [Estratégias de Trading](#7-estratégias-de-trading)
8. [Análise de Viabilidade](#8-análise-de-viabilidade)
9. [Execução e Testes](#9-execução-e-testes)
10. [Considerações Técnicas](#10-considerações-técnicas)

## 1. Visão Geral do Projeto

O Airdrop Optimizer é um sistema de agentes autônomos projetado para maximizar recompensas em campanhas de airdrop de criptomoedas. O sistema identifica automaticamente campanhas de airdrop na Binance, analisa sua viabilidade, cria agentes de trading específicos para cada campanha e executa operações de spot trading para atingir os volumes necessários e obter as recompensas.

O projeto foi desenvolvido como parte do Hackathon Fetch.ai, demonstrando o uso de agentes autônomos para otimizar operações no mercado de criptomoedas.

## 2. Arquitetura do Sistema

O sistema segue uma arquitetura modular baseada em agentes, onde cada agente é especializado em uma função específica. A comunicação entre os agentes é assíncrona, utilizando o framework Celery com Redis como broker de mensagens.

**Diagrama de Arquitetura:**

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Airdrop Scout  │────▶│ Campaign Creator│────▶│  Trading Agent  │
│     Agent       │     │     Agent       │     │                 │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        │
                                                        ▼
                                              ┌─────────────────┐
                                              │                 │
                                              │  Prediction     │
                                              │     Agent       │
                                              │                 │
                                              └─────────────────┘
```

O sistema pode ser acessado de duas formas:
1. **Interface CLI**: Através do script `main.py`
2. **API RESTful**: Através do servidor FastAPI em `api/main.py`

## 3. Componentes Principais

### 3.1 Airdrop Scout Agent

**Arquivo:** `agents/airdrop_scout_agent.py`

**Função:** Responsável por identificar e analisar campanhas de airdrop disponíveis.

**Funcionalidades:**
- Web scraping da página de airdrops da Binance (simulado)
- Extração de informações como token, volume necessário, recompensa e período
- Análise de viabilidade de cada campanha
- Cálculo de um score de viabilidade (0-10) baseado no ROI estimado

**Métodos principais:**
- `get_airdrop_campaigns()`: Coleta campanhas de airdrop disponíveis
- `analyze_campaign_viability()`: Analisa a viabilidade econômica de uma campanha

**Exemplo de saída:**
```python
{
    "token": "BTC",
    "volume_required": 1000,
    "reward": 50,
    "period_days": 7,
    "url": "https://www.binance.com/pt-BR/airdrop/btc",
    "viability_score": 8.5
}
```

### 3.2 Campaign Creator Agent

**Arquivo:** `agents/campaign_creator.py`

**Função:** Cria e configura agentes de trading específicos para cada campanha viável.

**Funcionalidades:**
- Avaliação da viabilidade das campanhas recebidas
- Configuração de parâmetros de trading baseados no nível de risco
- Criação de agentes de trading para campanhas viáveis
- Registro dos agentes no sistema (simulado)

**Métodos principais:**
- `create_trading_agent()`: Cria um agente de trading para uma campanha específica
- `create_trading_agents()`: Cria múltiplos agentes para várias campanhas
- `calculate_risk_level()`: Determina o nível de risco baseado no score de viabilidade

**Níveis de risco:**
- **LOW**: Para campanhas com score ≥ 8.0
- **MEDIUM**: Para campanhas com score entre 6.0 e 8.0
- **HIGH**: Para campanhas com score < 6.0

### 3.3 Trading Agent

**Arquivo:** `agents/trading_agent.py`

**Função:** Executa operações de compra e venda para atingir o volume de trading exigido pela campanha.

**Funcionalidades:**
- Execução de ordens de compra e venda baseadas em recomendações
- Gerenciamento de saldo e posições
- Implementação de stop loss para gerenciamento de risco
- Rastreamento de métricas de trading (trades executados, taxa de sucesso, lucro/prejuízo)

**Métodos principais:**
- `execute_trading()`: Loop principal de trading
- `execute_buy_order()`: Simula a execução de uma ordem de compra
- `execute_sell_order()`: Simula a execução de uma ordem de venda
- `check_stop_loss()`: Verifica se o stop loss deve ser acionado

**Parâmetros de trading (baseados no nível de risco):**
- Tamanho da posição (% do saldo)
- Percentual de stop loss
- Percentual de take profit
- Intervalo entre trades
- Slippage máximo permitido

### 3.4 Prediction Agent

**Arquivo:** `agents/prediction_agent.py`

**Função:** Analisa o mercado e fornece recomendações de trading (BUY, SELL, HOLD).

**Funcionalidades:**
- Análise técnica usando indicadores como médias móveis e RSI
- Análise de sentimento do mercado (simulada)
- Previsão de preços usando modelos de séries temporais simples
- Combinação de diferentes estratégias para uma recomendação final

**Métodos principais:**
- `predict_action()`: Fornece uma recomendação de trading para um token
- `get_technical_recommendation()`: Recomendação baseada em análise técnica
- `get_sentiment_recommendation()`: Recomendação baseada em análise de sentimento
- `get_time_series_recommendation()`: Recomendação baseada em previsão de preços

**Pesos das estratégias:**
- Análise técnica: 50%
- Análise de sentimento: 30%
- Previsão de séries temporais: 20%

## 4. Fluxo de Trabalho

O fluxo de trabalho completo do sistema segue estas etapas:

1. **Identificação de Campanhas**
   - O Airdrop Scout Agent coleta campanhas de airdrop disponíveis
   - Cada campanha é analisada e recebe um score de viabilidade

2. **Criação de Agentes**
   - O Campaign Creator avalia as campanhas e cria agentes de trading
   - Apenas campanhas com score de viabilidade ≥ 5.0 são consideradas
   - Cada agente recebe uma configuração baseada no nível de risco

3. **Execução de Trading**
   - O Trading Agent inicia operações para atingir o volume exigido
   - Consulta o Prediction Agent para obter recomendações de trading
   - Executa ordens de compra e venda conforme as recomendações
   - Implementa mecanismos de gerenciamento de risco (stop loss)

4. **Monitoramento e Relatórios**
   - O sistema monitora o progresso de cada agente
   - Gera relatórios com métricas de desempenho
   - Atualiza o status dos agentes (initializing, running, completed, stopped)

## 5. API RESTful

**Arquivo:** `api/main.py`

O sistema oferece uma API RESTful para interação com os agentes e campanhas:

### Endpoints:

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | / | Informações básicas sobre a API |
| GET | /airdrop/list | Lista todas as campanhas de airdrop disponíveis |
| POST | /airdrop | Recebe uma nova campanha de airdrop |
| GET | /agents | Lista todos os agentes de trading ativos |
| GET | /agents/{agent_id} | Obtém o status de um agente específico |
| POST | /agents/{agent_id}/start | Inicia a execução de um agente |
| POST | /agents/{agent_id}/stop | Interrompe a execução de um agente |

### Modelos de Dados:

**CampaignRequest:**
```json
{
  "token": "BTC",
  "volume_required": 1000,
  "reward": 50,
  "period_days": 7,
  "url": "https://www.binance.com/pt-BR/airdrop/btc"
}
```

**AgentStatusResponse:**
```json
{
  "agent_id": "trader-BTC-1621234567",
  "token": "BTC",
  "status": "running",
  "progress": 75.5,
  "last_update": 1621234567.89,
  "trades_executed": 42
}
```

## 6. Processamento Assíncrono

**Arquivos:** `worker.py`, `celeryconfig.py`

O sistema utiliza Celery para processamento assíncrono de tarefas:

- **Broker de mensagens**: Redis
- **Tarefas assíncronas**:
  - `create_trading_agent`: Cria um agente de trading
  - `create_trading_agents`: Cria múltiplos agentes
  - `execute_trading`: Executa operações de trading

Este design permite que o sistema escale horizontalmente e processe múltiplas campanhas e agentes simultaneamente.

## 7. Estratégias de Trading

O sistema implementa várias estratégias de trading:

### Análise Técnica
- **Médias Móveis**: Compara médias móveis de curto e longo prazo
- **RSI (Índice de Força Relativa)**: Identifica condições de sobrecompra e sobrevenda
- **Níveis de Suporte e Resistência**: Simulados através de variações de preço

### Análise de Sentimento
- Simula a análise de sentimento do mercado em relação a um token
- Escala de -1 (extremamente negativo) a +1 (extremamente positivo)
- Influencia as decisões de trading (comprar quando positivo, vender quando negativo)

### Previsão de Séries Temporais
- Modelo simples baseado na tendência recente de preços
- Prevê movimentos de preço de curto prazo
- Recomenda ações baseadas na direção prevista do preço

## 8. Análise de Viabilidade

A análise de viabilidade de campanhas considera:

1. **ROI (Retorno sobre Investimento)**
   - Recompensa da campanha vs. volume de trading exigido
   - Custos estimados (taxas, spread, slippage)
   - Período da campanha

2. **Fórmula de Cálculo**
   ```
   daily_roi = (reward - estimated_costs) / period_days
   viability_score = min(10, max(0, daily_roi * period_days / reward * 10))
   ```

3. **Interpretação do Score**
   - 0-5: Baixa viabilidade (rejeitada)
   - 5-7: Viabilidade média (risco alto)
   - 7-8: Boa viabilidade (risco médio)
   - 8-10: Excelente viabilidade (risco baixo)

## 9. Execução e Testes

### Modos de Execução

1. **Modo CLI**
   ```bash
   python main.py
   ```
   Executa uma simulação completa do sistema, desde a coleta de campanhas até a execução de trades.

2. **Modo API**
   ```bash
   uvicorn api.main:app --reload
   ```
   Inicia o servidor da API em `http://localhost:8000`.

### Testes da API

O projeto inclui ferramentas para testar a API:

1. **Script de Teste**
   ```bash
   python test_api.py
   ```
   Demonstra como usar todos os endpoints da API.

2. **Interface Swagger**
   Acesse `http://localhost:8000/docs` para testar a API interativamente.

3. **Guia de Teste**
   Consulte o arquivo `API_TESTING.md` para instruções detalhadas.

## 10. Considerações Técnicas

### Simulações vs. Implementação Real

O projeto atual é uma simulação que demonstra o conceito. Em uma implementação real:

1. **Web Scraping Real**
   - Implementação de scraping real da página de airdrops da Binance
   - Tratamento de captchas, rate limiting e mudanças na estrutura da página

2. **Integração com Exchange**
   - Uso da API oficial da Binance para execução de ordens
   - Autenticação e gerenciamento de chaves de API
   - Tratamento de erros e retry logic

3. **Modelos de ML Avançados**
   - Modelos de machine learning mais sofisticados para previsão de preços
   - Análise de sentimento baseada em dados reais de redes sociais e notícias
   - Backtesting e otimização de estratégias

4. **Persistência de Dados**
   - Banco de dados para armazenar campanhas, agentes e histórico de trades
   - Logging avançado para auditoria e análise de desempenho

5. **Segurança**
   - Proteção de chaves de API e credenciais
   - Monitoramento de atividades suspeitas
   - Limites de risco e mecanismos de failsafe

### Escalabilidade

O sistema foi projetado para ser escalável:

- **Arquitetura baseada em agentes**: Permite adicionar novos tipos de agentes
- **Processamento assíncrono**: Permite processar múltiplas campanhas simultaneamente
- **Design modular**: Facilita a substituição ou melhoria de componentes individuais