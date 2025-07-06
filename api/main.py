from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from agents.airdrop_scout_agent import get_airdrop_campaigns, analyze_campaign_viability
from agents.campaign_creator import create_trading_agent
import random
import time

app = FastAPI(
    title="Airdrop Optimizer API",
    description="API para o sistema de otimização de airdrops com agentes autônomos",
    version="1.0.0"
)

# Simulação de armazenamento de agentes (em produção seria um banco de dados)
agent_store = {}

class CampaignRequest(BaseModel):
    token: str = Field(..., description="Símbolo do token da campanha")
    volume_required: int = Field(..., description="Volume de trading necessário em USD")
    reward: float = Field(..., description="Recompensa da campanha em USD")
    period_days: Optional[int] = Field(7, description="Duração da campanha em dias")
    url: Optional[str] = Field(None, description="URL da página de detalhes da campanha")

    class Config:
        schema_extra = {
            "example": {
                "token": "BTC",
                "volume_required": 1000,
                "reward": 50,
                "period_days": 7,
                "url": "https://www.binance.com/pt-BR/airdrop/btc"
            }
        }

class AgentStatusResponse(BaseModel):
    agent_id: str
    token: str
    status: str
    progress: float
    last_update: float
    trades_executed: int

    class Config:
        schema_extra = {
            "example": {
                "agent_id": "trader-BTC-1621234567",
                "token": "BTC",
                "status": "running",
                "progress": 75.5,
                "last_update": 1621234567.89,
                "trades_executed": 42
            }
        }

@app.post("/airdrop", response_model=Dict[str, Any], tags=["Campanhas"])
async def receive_airdrop_campaign(campaign: CampaignRequest):
    """
    Recebe uma nova campanha de airdrop e cria um agente de trading para ela.
    """
    print(f"[API] Nova campanha recebida: {campaign.token}")

    # Adiciona viability_score à campanha
    campaign_dict = campaign.dict()
    campaign_dict["viability_score"] = analyze_campaign_viability({
        "token": campaign.token,
        "volume_required": campaign.volume_required,
        "reward": campaign.reward,
        "period_days": campaign.period_days
    })

    # Cria o agente de trading (assíncrono com Celery)
    agent_id = create_trading_agent.delay(campaign_dict)

    # Simula armazenamento do agente
    agent_store[str(agent_id)] = {
        "agent_id": str(agent_id),
        "token": campaign.token,
        "status": "initializing",
        "progress": 0.0,
        "last_update": time.time(),
        "trades_executed": 0,
        "campaign": campaign_dict
    }

    return {
        "message": f"Campanha {campaign.token} recebida e processada.",
        "agent_id": str(agent_id),
        "viability_score": campaign_dict["viability_score"]
    }

@app.get("/airdrop/list", response_model=Dict[str, List[Dict[str, Any]]], tags=["Campanhas"])
async def list_airdrops():
    """
    Lista todas as campanhas de airdrop disponíveis.
    """
    campaigns = get_airdrop_campaigns()
    return {"campaigns": campaigns}

@app.get("/agents", response_model=Dict[str, List[AgentStatusResponse]], tags=["Agentes"])
async def list_agents():
    """
    Lista todos os agentes de trading ativos.
    """
    agents = []
    for agent_id, agent_data in agent_store.items():
        # Atualiza o progresso simulado
        if agent_data["status"] == "running":
            progress = min(100.0, agent_data["progress"] + random.uniform(5, 15))
            agent_data["progress"] = progress
            agent_data["trades_executed"] += random.randint(1, 5)
            agent_data["last_update"] = time.time()

            if progress >= 100.0:
                agent_data["status"] = "completed"

        agents.append(AgentStatusResponse(**agent_data))

    return {"agents": agents}

@app.get("/agents/{agent_id}", response_model=AgentStatusResponse, tags=["Agentes"])
async def get_agent_status(agent_id: str):
    """
    Obtém o status de um agente de trading específico.
    """
    if agent_id not in agent_store:
        raise HTTPException(status_code=404, detail=f"Agente {agent_id} não encontrado")

    agent_data = agent_store[agent_id]

    # Atualiza o progresso simulado
    if agent_data["status"] == "running":
        progress = min(100.0, agent_data["progress"] + random.uniform(5, 15))
        agent_data["progress"] = progress
        agent_data["trades_executed"] += random.randint(1, 5)
        agent_data["last_update"] = time.time()

        if progress >= 100.0:
            agent_data["status"] = "completed"

    return AgentStatusResponse(**agent_data)

@app.post("/agents/{agent_id}/start", response_model=Dict[str, Any], tags=["Agentes"])
async def start_agent(agent_id: str):
    """
    Inicia a execução de um agente de trading.
    """
    if agent_id not in agent_store:
        raise HTTPException(status_code=404, detail=f"Agente {agent_id} não encontrado")

    agent_data = agent_store[agent_id]

    if agent_data["status"] != "initializing":
        raise HTTPException(status_code=400, detail=f"Agente {agent_id} não pode ser iniciado (status atual: {agent_data['status']})")

    agent_data["status"] = "running"
    agent_data["last_update"] = time.time()

    return {
        "message": f"Agente {agent_id} iniciado com sucesso",
        "status": "running"
    }

@app.post("/agents/{agent_id}/stop", response_model=Dict[str, Any], tags=["Agentes"])
async def stop_agent(agent_id: str):
    """
    Interrompe a execução de um agente de trading.
    """
    if agent_id not in agent_store:
        raise HTTPException(status_code=404, detail=f"Agente {agent_id} não encontrado")

    agent_data = agent_store[agent_id]

    if agent_data["status"] != "running":
        raise HTTPException(status_code=400, detail=f"Agente {agent_id} não está em execução (status atual: {agent_data['status']})")

    agent_data["status"] = "stopped"
    agent_data["last_update"] = time.time()

    return {
        "message": f"Agente {agent_id} interrompido com sucesso",
        "status": "stopped"
    }

@app.get("/", tags=["Sistema"])
async def root():
    """
    Endpoint raiz que fornece informações básicas sobre a API.
    """
    return {
        "name": "Airdrop Optimizer API",
        "version": "1.0.0",
        "description": "API para o sistema de otimização de airdrops com agentes autônomos",
        "endpoints": {
            "POST /airdrop": "Recebe uma nova campanha de airdrop",
            "GET /airdrop/list": "Lista todas as campanhas de airdrop disponíveis",
            "GET /agents": "Lista todos os agentes de trading ativos",
            "GET /agents/{agent_id}": "Obtém o status de um agente específico",
            "POST /agents/{agent_id}/start": "Inicia a execução de um agente",
            "POST /agents/{agent_id}/stop": "Interrompe a execução de um agente"
        }
    }
