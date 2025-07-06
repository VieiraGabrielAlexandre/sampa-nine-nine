from airdrop_scout_agent import get_airdrop_campaigns
from campaign_agent_creator import create_trading_agents

if __name__ == '__main__':
    print('--- Airdrop Optimizer - MVP ---')
    campaigns = get_airdrop_campaigns()
    agents = create_trading_agents(campaigns)

    for agent in agents:
        agent.execute_trades()

    print('--- Fim da Execução ---')
