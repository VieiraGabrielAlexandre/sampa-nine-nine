from trading_agent import TradingAgent

def create_trading_agents(campaigns):
    agents = []
    print('[Creator] Criando agentes de trading...')
    for campaign in campaigns:
        agent = TradingAgent(campaign)
        agents.append(agent)
    return agents