from prediction_agent import PredictionAgent
import random

class TradingAgent:
    def __init__(self, campaign_data):
        self.token = campaign_data['token']
        self.volume_required = campaign_data['volume_required']
        self.reward = campaign_data['reward']
        self.duration_days = campaign_data['duration_days']
        self.prediction_agent = PredictionAgent(self.token)
        self.current_volume = 0

    def execute_trades(self):
        print(f'[Trader-{self.token}] Iniciando trades para {self.token}...')
        while self.current_volume < self.volume_required:
            action = self.prediction_agent.get_action()
            price = random.uniform(0.8, 1.2)  # Simula preço
            if action == 'BUY':
                print(f'[Trader-{self.token}] Comprando {self.token} a ${price:.2f}')
                self.current_volume += 10
            elif action == 'SELL':
                print(f'[Trader-{self.token}] Vendendo {self.token} a ${price:.2f}')
            else:
                print(f'[Trader-{self.token}] Mantendo posição...')
        print(f'[Trader-{self.token}] Volume atingido. Trading finalizado.')