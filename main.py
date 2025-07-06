from agents.airdrop_scout_agent import get_airdrop_campaigns
from agents.campaign_creator import create_trading_agents
import time
import json

def run_airdrop_optimizer():
    """
    Main function to run the Airdrop Optimizer system.
    """
    print('\n' + '='*50)
    print('=== Airdrop Optimizer - Hackathon Fetch.ai ===')
    print('='*50 + '\n')

    print('Iniciando sistema de agentes autônomos...\n')

    # Etapa 1: Airdrop Scout Agent - Coleta campanhas de airdrop
    print('\n--- Etapa 1: Airdrop Scout Agent ---')
    print('Buscando campanhas de airdrop na Binance...')
    campaigns = get_airdrop_campaigns()

    if not campaigns:
        print('Nenhuma campanha encontrada. Encerrando execução.')
        return

    print(f'\nForam encontradas {len(campaigns)} campanhas:')
    for i, campaign in enumerate(campaigns, 1):
        print(f"  {i}. {campaign['token']} - Volume: ${campaign['volume_required']} - " +
              f"Recompensa: ${campaign['reward']} - Viabilidade: {campaign['viability_score']}/10")

    # Etapa 2: Campaign Agent Creator - Cria agentes de trading
    print('\n--- Etapa 2: Campaign Agent Creator ---')
    print('Criando agentes de trading para as campanhas viáveis...')

    # Chamada assíncrona para criar agentes
    agent_ids = create_trading_agents(campaigns)

    # Em um ambiente real, esperaríamos os agentes serem criados
    # Aqui vamos simular uma espera
    print('\nAguardando criação dos agentes...')
    time.sleep(3)

    if not agent_ids:
        print('Nenhum agente de trading foi criado. Encerrando execução.')
        return

    print(f'\nForam criados {len(agent_ids)} agentes de trading:')
    for agent_id in agent_ids:
        print(f"  - {agent_id}")

    # Etapa 3: Trading Agents - Executam operações (já iniciados pelo Campaign Creator)
    print('\n--- Etapa 3: Trading Agents ---')
    print('Os agentes de trading estão executando operações em background...')
    print('(Em um ambiente real, os agentes estariam operando de forma autônoma)')

    # Simulando espera pelos resultados
    print('\nAguardando resultados das operações...')
    time.sleep(5)

    # Simulando resultados
    print('\n--- Resultados Finais ---')

    # Resultados simulados para cada agente
    for i, agent_id in enumerate(agent_ids):
        token = agent_id.split('-')[1]
        results = {
            "total_trades": random.randint(20, 100),
            "successful_trades": random.randint(15, 80),
            "failed_trades": random.randint(0, 10),
            "success_rate": round(random.uniform(80, 98), 2),
            "profit_loss": round(random.uniform(-100, 500), 2),
            "duration_seconds": round(random.uniform(300, 1800), 2)
        }

        print(f"\nAgente {agent_id}:")
        print(f"  - Token: {token}")
        print(f"  - Trades realizados: {results['total_trades']}")
        print(f"  - Taxa de sucesso: {results['success_rate']}%")
        print(f"  - Lucro/Prejuízo: ${results['profit_loss']}")
        print(f"  - Duração: {results['duration_seconds'] / 60:.1f} minutos")

    print('\n' + '='*50)
    print('=== Execução Finalizada com Sucesso ===')
    print('='*50 + '\n')

if __name__ == '__main__':
    import random  # Importado aqui para simular resultados
    run_airdrop_optimizer()
