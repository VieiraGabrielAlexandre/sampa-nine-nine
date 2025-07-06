from worker import app
from agents.trading_agent import execute_trading
import time

@app.task
def create_trading_agent(campaign):
    """
    Creates a trading agent for a specific campaign.

    Args:
        campaign (dict): The campaign information.

    Returns:
        str: The ID of the created trading agent.
    """
    token = campaign['token']
    print(f"[Creator] Iniciando criação de Trading Agent para token: {token}")

    # Verificando a viabilidade da campanha
    viability_score = campaign.get('viability_score', 0)
    if viability_score < 5.0:
        print(f"[Creator] Campanha {token} rejeitada: score de viabilidade muito baixo ({viability_score})")
        return None

    # Configurando parâmetros do agente
    agent_config = {
        "token": token,
        "volume_required": campaign['volume_required'],
        "reward": campaign['reward'],
        "period_days": campaign.get('period_days', 7),
        "risk_level": calculate_risk_level(viability_score),
        "agent_id": f"trader-{token}-{int(time.time())}"
    }

    print(f"[Creator] Trading Agent configurado para {token} com ID: {agent_config['agent_id']}")
    print(f"[Creator] Nível de risco: {agent_config['risk_level']}")

    # Em um ambiente real, registraríamos o agente na rede Fetch.ai
    # register_agent_on_fetchai_network(agent_config)

    # Iniciando a execução do trading (assíncrono com Celery)
    execute_trading.delay(agent_config)

    print(f"[Creator] Trading Agent para {token} criado e iniciado com sucesso")
    return agent_config['agent_id']

def calculate_risk_level(viability_score):
    """
    Calculates the risk level based on the viability score.

    Args:
        viability_score (float): The viability score of the campaign.

    Returns:
        str: The risk level (LOW, MEDIUM, HIGH).
    """
    if viability_score >= 8.0:
        return "LOW"
    elif viability_score >= 6.0:
        return "MEDIUM"
    else:
        return "HIGH"

@app.task
def create_trading_agents(campaigns):
    """
    Creates trading agents for multiple campaigns.

    Args:
        campaigns (list): A list of campaign information dictionaries.

    Returns:
        list: A list of created agent IDs.
    """
    print(f"[Creator] Criando Trading Agents para {len(campaigns)} campanhas")
    agent_ids = []

    for campaign in campaigns:
        agent_id = create_trading_agent(campaign)
        if agent_id:
            agent_ids.append(agent_id)

    print(f"[Creator] {len(agent_ids)} Trading Agents criados com sucesso")
    return agent_ids
