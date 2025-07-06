from worker import app
from agents.prediction_agent import predict_action
import random
import time
import json

class TradingMetrics:
    def __init__(self):
        self.total_trades = 0
        self.successful_trades = 0
        self.failed_trades = 0
        self.profit_loss = 0.0
        self.start_time = time.time()
        self.end_time = None
        self.trade_history = []

    def add_trade(self, action, price, amount, success, profit=0.0):
        self.total_trades += 1
        if success:
            self.successful_trades += 1
        else:
            self.failed_trades += 1

        self.profit_loss += profit

        self.trade_history.append({
            "timestamp": time.time(),
            "action": action,
            "price": price,
            "amount": amount,
            "success": success,
            "profit": profit
        })

    def complete(self):
        self.end_time = time.time()

    def get_summary(self):
        duration = (self.end_time or time.time()) - self.start_time
        success_rate = (self.successful_trades / self.total_trades * 100) if self.total_trades > 0 else 0

        return {
            "total_trades": self.total_trades,
            "successful_trades": self.successful_trades,
            "failed_trades": self.failed_trades,
            "success_rate": round(success_rate, 2),
            "profit_loss": round(self.profit_loss, 2),
            "duration_seconds": round(duration, 2)
        }

@app.task
def execute_trading(agent_config):
    """
    Executes trading for a specific campaign based on predictions.

    Args:
        agent_config (dict): The configuration for the trading agent.

    Returns:
        dict: A summary of the trading results.
    """
    token = agent_config['token']
    volume_required = agent_config['volume_required']
    risk_level = agent_config.get('risk_level', 'MEDIUM')
    agent_id = agent_config.get('agent_id', f"trader-{token}")

    # Inicializando métricas
    metrics = TradingMetrics()

    # Configurando parâmetros de trading com base no nível de risco
    trade_config = configure_trading_parameters(risk_level)

    traded_volume = 0
    wallet_balance = 10000.0  # Saldo inicial simulado
    token_balance = 0.0

    print(f"[{agent_id}] Iniciando trading para {token}...")
    print(f"[{agent_id}] Configuração: {json.dumps(trade_config)}")

    # Loop principal de trading
    while traded_volume < volume_required:
        try:
            # Obtendo recomendação do Prediction Agent
            action = predict_action(token)

            # Simulando preço de mercado
            market_price = simulate_market_price(token)

            # Calculando quantidade a ser negociada
            trade_amount = calculate_trade_amount(
                wallet_balance, 
                token_balance, 
                market_price, 
                trade_config
            )

            # Executando a ordem
            if action == "BUY" and wallet_balance >= trade_amount * market_price:
                success, profit = execute_buy_order(token, market_price, trade_amount, trade_config)
                if success:
                    wallet_balance -= trade_amount * market_price
                    token_balance += trade_amount
                    traded_volume += trade_amount * market_price
                metrics.add_trade("BUY", market_price, trade_amount, success, profit)

            elif action == "SELL" and token_balance >= trade_amount:
                success, profit = execute_sell_order(token, market_price, trade_amount, trade_config)
                if success:
                    wallet_balance += trade_amount * market_price
                    token_balance -= trade_amount
                    traded_volume += trade_amount * market_price
                metrics.add_trade("SELL", market_price, trade_amount, success, profit)

            else:
                print(f"[{agent_id}] Mantendo posição... Preço atual: ${market_price}")

            # Verificando stop loss
            if check_stop_loss(wallet_balance, token_balance, market_price, trade_config):
                print(f"[{agent_id}] Stop loss acionado! Vendendo todas as posições.")
                if token_balance > 0:
                    success, profit = execute_sell_order(token, market_price, token_balance, trade_config)
                    if success:
                        wallet_balance += token_balance * market_price
                        traded_volume += token_balance * market_price
                        token_balance = 0
                    metrics.add_trade("STOP_LOSS", market_price, token_balance, success, profit)

            # Status do trading
            print(f"[{agent_id}] Status: Volume negociado: ${traded_volume:.2f}/{volume_required} | " +
                  f"Saldo: ${wallet_balance:.2f} | {token}: {token_balance:.4f}")

            # Simulando espera entre trades
            time.sleep(trade_config['trade_interval'])

        except Exception as e:
            print(f"[{agent_id}] Erro durante trading: {str(e)}")
            time.sleep(5)  # Espera mais tempo em caso de erro

    # Finalizando métricas
    metrics.complete()
    results = metrics.get_summary()

    print(f"[{agent_id}] Volume atingido. Trading finalizado.")
    print(f"[{agent_id}] Resultados: {json.dumps(results)}")

    return results

def configure_trading_parameters(risk_level):
    """
    Configures trading parameters based on the risk level.

    Args:
        risk_level (str): The risk level (LOW, MEDIUM, HIGH).

    Returns:
        dict: Trading parameters.
    """
    if risk_level == "LOW":
        return {
            "position_size_percent": 0.05,  # 5% do saldo por trade
            "stop_loss_percent": 0.02,      # 2% de perda máxima
            "take_profit_percent": 0.01,    # 1% de lucro alvo
            "trade_interval": 2,            # 2 segundos entre trades
            "max_slippage": 0.001           # 0.1% de slippage máximo
        }
    elif risk_level == "MEDIUM":
        return {
            "position_size_percent": 0.10,  # 10% do saldo por trade
            "stop_loss_percent": 0.05,      # 5% de perda máxima
            "take_profit_percent": 0.02,    # 2% de lucro alvo
            "trade_interval": 1,            # 1 segundo entre trades
            "max_slippage": 0.002           # 0.2% de slippage máximo
        }
    else:  # HIGH
        return {
            "position_size_percent": 0.20,  # 20% do saldo por trade
            "stop_loss_percent": 0.10,      # 10% de perda máxima
            "take_profit_percent": 0.05,    # 5% de lucro alvo
            "trade_interval": 0.5,          # 0.5 segundos entre trades
            "max_slippage": 0.005           # 0.5% de slippage máximo
        }

def simulate_market_price(token):
    """
    Simulates the current market price for a token.

    Args:
        token (str): The token symbol.

    Returns:
        float: The simulated market price.
    """
    base_prices = {
        "BTC": 50000,
        "ETH": 3000,
        "SOL": 100,
        "ABC": 10,
        "XYZ": 5
    }

    base_price = base_prices.get(token, 1.0)
    variation = random.uniform(-0.02, 0.02)  # -2% a +2% de variação

    return round(base_price * (1 + variation), 2)

def calculate_trade_amount(wallet_balance, token_balance, market_price, trade_config):
    """
    Calculates the amount to trade based on the wallet balance and position size.

    Args:
        wallet_balance (float): The available balance in the wallet.
        token_balance (float): The current token balance.
        market_price (float): The current market price of the token.
        trade_config (dict): The trading configuration.

    Returns:
        float: The amount to trade.
    """
    position_size = wallet_balance * trade_config['position_size_percent']
    return round(position_size / market_price, 4)

def execute_buy_order(token, price, amount, trade_config):
    """
    Simulates executing a buy order.

    Args:
        token (str): The token to buy.
        price (float): The price to buy at.
        amount (float): The amount to buy.
        trade_config (dict): The trading configuration.

    Returns:
        tuple: (success, profit)
    """
    # Simulando slippage
    actual_price = price * (1 + random.uniform(0, trade_config['max_slippage']))

    # Simulando sucesso/falha da ordem (95% de chance de sucesso)
    success = random.random() < 0.95

    if success:
        print(f"[Trader-{token}] Comprando {amount:.4f} {token} a ${actual_price:.2f}")
        return True, 0.0
    else:
        print(f"[Trader-{token}] Falha ao comprar {token}: ordem rejeitada")
        return False, 0.0

def execute_sell_order(token, price, amount, trade_config):
    """
    Simulates executing a sell order.

    Args:
        token (str): The token to sell.
        price (float): The price to sell at.
        amount (float): The amount to sell.
        trade_config (dict): The trading configuration.

    Returns:
        tuple: (success, profit)
    """
    # Simulando slippage
    actual_price = price * (1 - random.uniform(0, trade_config['max_slippage']))

    # Simulando sucesso/falha da ordem (95% de chance de sucesso)
    success = random.random() < 0.95

    # Simulando lucro/prejuízo
    profit = amount * actual_price * random.uniform(-0.01, 0.02)

    if success:
        print(f"[Trader-{token}] Vendendo {amount:.4f} {token} a ${actual_price:.2f}")
        return True, profit
    else:
        print(f"[Trader-{token}] Falha ao vender {token}: ordem rejeitada")
        return False, 0.0

def check_stop_loss(wallet_balance, token_balance, market_price, trade_config):
    """
    Checks if the stop loss should be triggered.

    Args:
        wallet_balance (float): The available balance in the wallet.
        token_balance (float): The current token balance.
        market_price (float): The current market price of the token.
        trade_config (dict): The trading configuration.

    Returns:
        bool: True if stop loss should be triggered, False otherwise.
    """
    # Simulando verificação de stop loss (5% de chance de acionar)
    return random.random() < 0.05
