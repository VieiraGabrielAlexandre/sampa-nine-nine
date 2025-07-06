import random

class PredictionAgent:
    def __init__(self, token):
        self.token = token
        self.prices = [1.0, 0.95, 1.05, 0.98, 1.02]  # Histórico fictício

    def get_action(self):
        current_price = random.uniform(0.8, 1.2)
        moving_avg = sum(self.prices[-5:]) / 5
        self.prices.append(current_price)

        if current_price < moving_avg * 0.97:
            return 'BUY'
        elif current_price > moving_avg * 1.03:
            return 'SELL'
        else:
            return 'HOLD'