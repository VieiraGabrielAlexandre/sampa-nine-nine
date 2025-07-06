# Guia de Teste da API do Airdrop Optimizer

Este guia explica como testar os endpoints da API do Airdrop Optimizer usando diferentes métodos.

## Índice

1. [Visão Geral da API](#visão-geral-da-api)
2. [Iniciando o Servidor da API](#iniciando-o-servidor-da-api)
3. [Métodos de Teste](#métodos-de-teste)
   - [Usando o Script de Teste](#usando-o-script-de-teste)
   - [Usando Curl](#usando-curl)
   - [Usando a Interface Swagger](#usando-a-interface-swagger)
4. [Endpoints Disponíveis](#endpoints-disponíveis)
5. [Exemplos de Requisições](#exemplos-de-requisições)

## Visão Geral da API

A API do Airdrop Optimizer permite gerenciar campanhas de airdrop e agentes de trading. Ela oferece endpoints para:

- Listar campanhas de airdrop disponíveis
- Criar novas campanhas de airdrop
- Listar agentes de trading
- Obter o status de um agente específico
- Iniciar e parar agentes de trading

## Iniciando o Servidor da API

Para iniciar o servidor da API, execute o seguinte comando no terminal:

```bash
uvicorn api.main:app --reload
```

O servidor será iniciado em `http://localhost:8000`.

## Métodos de Teste

### Usando o Script de Teste

O projeto inclui um script de teste (`test_api.py`) que demonstra como usar todos os endpoints da API.

Para executar o script:

```bash
python test_api.py
```

Você pode testar endpoints específicos passando o nome do endpoint como argumento:

```bash
python test_api.py root            # Testa o endpoint raiz
python test_api.py list_airdrops   # Lista airdrops
python test_api.py create_airdrop  # Cria uma campanha de airdrop
python test_api.py list_agents     # Lista agentes
```

O script também oferece a opção de executar todos os testes em sequência.

### Usando Curl

Você pode testar os endpoints diretamente usando curl. Exemplos:

**Endpoint Raiz:**
```bash
curl -X GET http://localhost:8000/
```

**Listar Airdrops:**
```bash
curl -X GET http://localhost:8000/airdrop/list
```

**Criar Campanha de Airdrop:**
```bash
curl -X POST http://localhost:8000/airdrop \
  -H 'Content-Type: application/json' \
  -d '{"token": "BTC", "volume_required": 1000, "reward": 50, "period_days": 7, "url": "https://www.binance.com/pt-BR/airdrop/btc"}'
```

**Listar Agentes:**
```bash
curl -X GET http://localhost:8000/agents
```

**Obter Status de um Agente:**
```bash
curl -X GET http://localhost:8000/agents/{agent_id}
```

**Iniciar um Agente:**
```bash
curl -X POST http://localhost:8000/agents/{agent_id}/start
```

**Parar um Agente:**
```bash
curl -X POST http://localhost:8000/agents/{agent_id}/stop
```

### Usando a Interface Swagger

FastAPI gera automaticamente uma interface Swagger UI para testar a API. Para acessá-la:

1. Inicie o servidor da API
2. Abra um navegador e acesse `http://localhost:8000/docs`

A interface Swagger permite:
- Ver todos os endpoints disponíveis
- Ler a documentação de cada endpoint
- Testar os endpoints diretamente no navegador
- Ver os modelos de dados esperados

## Endpoints Disponíveis

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | / | Informações básicas sobre a API |
| GET | /airdrop/list | Lista todas as campanhas de airdrop disponíveis |
| POST | /airdrop | Recebe uma nova campanha de airdrop |
| GET | /agents | Lista todos os agentes de trading ativos |
| GET | /agents/{agent_id} | Obtém o status de um agente específico |
| POST | /agents/{agent_id}/start | Inicia a execução de um agente |
| POST | /agents/{agent_id}/stop | Interrompe a execução de um agente |

## Exemplos de Requisições

### Criar uma Campanha de Airdrop

**Requisição:**
```json
POST /airdrop
{
  "token": "BTC",
  "volume_required": 1000,
  "reward": 50,
  "period_days": 7,
  "url": "https://www.binance.com/pt-BR/airdrop/btc"
}
```

**Resposta:**
```json
{
  "message": "Campanha BTC recebida e processada.",
  "agent_id": "trader-BTC-1621234567",
  "viability_score": 8.5
}
```

### Obter Status de um Agente

**Requisição:**
```
GET /agents/trader-BTC-1621234567
```

**Resposta:**
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

### Iniciar um Agente

**Requisição:**
```
POST /agents/trader-BTC-1621234567/start
```

**Resposta:**
```json
{
  "message": "Agente trader-BTC-1621234567 iniciado com sucesso",
  "status": "running"
}
```

### Parar um Agente

**Requisição:**
```
POST /agents/trader-BTC-1621234567/stop
```

**Resposta:**
```json
{
  "message": "Agente trader-BTC-1621234567 interrompido com sucesso",
  "status": "stopped"
}
```