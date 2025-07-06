import random
import numpy as np
import time
from collections import deque
from agents.groq_integration import analyze_market_sentiment, predict_price_movement, get_trading_recommendation

# Simulação de dados históricos para cada token
price_history = {}
sentiment_data = {}

# Parâmetros para análise técnica
SHORT_WINDOW = 5
LONG_WINDOW = 20
RSI_PERIOD = 14
OVERSOLD_THRESHOLD = 30
OVERBOUGHT_THRESHOLD = 70

def predict_action(token):
    """
    Predicts the best trading action for a given token using technical analysis,
    sentiment analysis, and Groq AI.

    Args:
        token (str): The token symbol.

    Returns:
        str: The recommended action (BUY, SELL, HOLD).
    """
    # Inicializa o histórico de preços se não existir
    if token not in price_history:
        initialize_price_history(token)

    # Atualiza o histórico de preços com um novo preço simulado
    update_price_history(token)

    # Atualiza os dados de sentimento
    update_sentiment_data(token)

    # Obtém as recomendações de cada modelo
    technical_recommendation = get_technical_recommendation(token)
    sentiment_recommendation = get_sentiment_recommendation(token)
    time_series_recommendation = get_time_series_recommendation(token)

    # Obtém recomendação do Groq AI
    groq_recommendation = get_groq_recommendation(token)

    # Combina as recomendações (pesos: Groq 40%, técnica 30%, sentimento 20%, série temporal 10%)
    recommendations = {
        "BUY": 0,
        "SELL": 0,
        "HOLD": 0
    }

    recommendations[technical_recommendation] += 0.3
    recommendations[sentiment_recommendation] += 0.2
    recommendations[time_series_recommendation] += 0.1
    recommendations[groq_recommendation] += 0.4  # Groq AI tem o maior peso

    # Escolhe a ação com maior peso
    action = max(recommendations, key=recommendations.get)

    # Adiciona um pouco de aleatoriedade (5% de chance de mudar a recomendação)
    if random.random() < 0.05:  # Reduzido de 10% para 5% para dar mais peso às análises
        alternative_actions = [a for a in ["BUY", "SELL", "HOLD"] if a != action]
        action = random.choice(alternative_actions)
        print(f"[Prediction] Alterando recomendação aleatoriamente para {action}")

    print(f"[Prediction] Análise para {token}:")
    print(f"  - Técnica: {technical_recommendation}")
    print(f"  - Sentimento: {sentiment_recommendation}")
    print(f"  - Série Temporal: {time_series_recommendation}")
    print(f"  - Groq AI: {groq_recommendation}")
    print(f"  - Recomendação final: {action}")

    return action

def initialize_price_history(token):
    """
    Initializes price history for a token.

    Args:
        token (str): The token symbol.
    """
    # Define um preço base para o token
    base_prices = {
        "BTC": 50000,
        "ETH": 3000,
        "SOL": 100,
        "ABC": 10,
        "XYZ": 5
    }
    base_price = base_prices.get(token, 1.0)

    # Cria um histórico de preços simulado com alguma tendência
    trend = random.choice([-1, 1])  # -1 para baixa, 1 para alta
    volatility = random.uniform(0.01, 0.05)  # Volatilidade entre 1% e 5%

    history = deque(maxlen=50)  # Mantém os últimos 50 preços

    # Gera 30 preços históricos iniciais
    current_price = base_price
    for _ in range(30):
        # Adiciona um movimento aleatório com tendência
        movement = random.normalvariate(0.001 * trend, volatility)
        current_price *= (1 + movement)
        history.append(current_price)

    price_history[token] = history

    # Inicializa dados de sentimento
    sentiment_data[token] = {
        "sentiment_score": random.uniform(-1, 1),  # Entre -1 (negativo) e 1 (positivo)
        "last_update": time.time()
    }

    print(f"[Prediction] Histórico de preços inicializado para {token}")

def update_price_history(token):
    """
    Updates the price history with a new simulated price.

    Args:
        token (str): The token symbol.
    """
    history = price_history[token]
    last_price = history[-1]

    # Simula um novo preço com base no último preço
    volatility = random.uniform(0.005, 0.02)  # 0.5% a 2% de volatilidade
    movement = random.normalvariate(0, volatility)
    new_price = last_price * (1 + movement)

    # Adiciona o novo preço ao histórico
    history.append(new_price)

    return new_price

def update_sentiment_data(token):
    """
    Updates sentiment data for a token.

    Args:
        token (str): The token symbol.
    """
    # Atualiza o sentimento a cada 5 segundos
    current_time = time.time()
    if token not in sentiment_data or current_time - sentiment_data[token]["last_update"] > 5:
        # Simula uma mudança gradual no sentimento
        current_sentiment = sentiment_data.get(token, {"sentiment_score": 0})["sentiment_score"]
        new_sentiment = max(-1, min(1, current_sentiment + random.uniform(-0.2, 0.2)))

        sentiment_data[token] = {
            "sentiment_score": new_sentiment,
            "last_update": current_time
        }

def get_technical_recommendation(token):
    """
    Gets a trading recommendation based on technical analysis.

    Args:
        token (str): The token symbol.

    Returns:
        str: The recommended action (BUY, SELL, HOLD).
    """
    prices = list(price_history[token])

    # Calcula médias móveis
    if len(prices) >= LONG_WINDOW:
        short_ma = np.mean(prices[-SHORT_WINDOW:])
        long_ma = np.mean(prices[-LONG_WINDOW:])

        # Calcula RSI
        rsi = calculate_rsi(prices)

        # Lógica de decisão
        if short_ma > long_ma and rsi < OVERBOUGHT_THRESHOLD:
            # Tendência de alta e não está sobrecomprado
            return "BUY"
        elif short_ma < long_ma and rsi > OVERSOLD_THRESHOLD:
            # Tendência de baixa e não está sobrevendido
            return "SELL"
        elif rsi > OVERBOUGHT_THRESHOLD:
            # Sobrecomprado
            return "SELL"
        elif rsi < OVERSOLD_THRESHOLD:
            # Sobrevendido
            return "BUY"

    return "HOLD"

def calculate_rsi(prices):
    """
    Calculates the Relative Strength Index (RSI).

    Args:
        prices (list): List of prices.

    Returns:
        float: The RSI value.
    """
    if len(prices) < RSI_PERIOD + 1:
        return 50  # Valor neutro se não houver dados suficientes

    # Calcula as mudanças de preço
    deltas = np.diff(prices)

    # Separa ganhos e perdas
    gains = np.clip(deltas, 0, None)
    losses = -np.clip(deltas, None, 0)

    # Calcula médias de ganhos e perdas
    avg_gain = np.mean(gains[-RSI_PERIOD:])
    avg_loss = np.mean(losses[-RSI_PERIOD:])

    if avg_loss == 0:
        return 100  # Evita divisão por zero

    # Calcula RS e RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

def get_sentiment_recommendation(token):
    """
    Gets a trading recommendation based on sentiment analysis using Groq AI.

    Args:
        token (str): The token symbol.

    Returns:
        str: The recommended action (BUY, SELL, HOLD).
    """
    try:
        # Generate some simulated news data for the token
        news_data = [
            f"{token} market shows increased activity in the last 24 hours",
            f"Analysts predict positive outlook for {token} in the coming weeks",
            f"New developments in {token} ecosystem attract investor attention"
        ]

        # Use Groq AI for sentiment analysis
        result = analyze_market_sentiment(token, news_data)

        print(f"[Prediction] Groq AI sentiment analysis for {token}: {result['sentiment_score']}")

        # Return the recommendation from Groq AI
        return result["recommendation"]
    except Exception as e:
        print(f"[Prediction] Error using Groq AI for sentiment analysis: {str(e)}")
        print(f"[Prediction] Falling back to simple sentiment analysis")

        # Fallback to simple sentiment analysis if Groq AI fails
        sentiment = sentiment_data[token]["sentiment_score"]

        if sentiment > 0.3:
            return "BUY"
        elif sentiment < -0.3:
            return "SELL"
        else:
            return "HOLD"

def get_time_series_recommendation(token):
    """
    Gets a trading recommendation based on time series prediction using Groq AI.

    Args:
        token (str): The token symbol.

    Returns:
        str: The recommended action (BUY, SELL, HOLD).
    """
    prices = list(price_history[token])

    if len(prices) < 3:
        return "HOLD"

    try:
        # Use Groq AI for price prediction
        result = predict_price_movement(token, prices, "short")

        print(f"[Prediction] Groq AI price prediction for {token}: {result['prediction_score']}")

        # Return the recommendation from Groq AI
        return result["recommendation"]
    except Exception as e:
        print(f"[Prediction] Error using Groq AI for price prediction: {str(e)}")
        print(f"[Prediction] Falling back to simple time series prediction")

        # Fallback to simple time series prediction if Groq AI fails
        last_price = prices[-1]
        prev_price = prices[-2]

        # Calcula a tendência de curto prazo
        short_trend = (last_price - prev_price) / prev_price

        # Simula uma previsão para o próximo preço
        predicted_movement = short_trend * (1 + random.uniform(-0.5, 0.5))
        predicted_price = last_price * (1 + predicted_movement)

        # Decisão baseada na previsão
        if predicted_price > last_price * 1.01:  # Previsão de alta de mais de 1%
            return "BUY"
        elif predicted_price < last_price * 0.99:  # Previsão de queda de mais de 1%
            return "SELL"
        else:
            return "HOLD"

def get_groq_recommendation(token):
    """
    Gets a comprehensive trading recommendation using Groq AI.

    Args:
        token (str): The token symbol.

    Returns:
        str: The recommended action (BUY, SELL, HOLD).
    """
    if token not in price_history:
        return "HOLD"

    try:
        # Prepare market data for Groq AI
        prices = list(price_history[token])

        # Calculate some basic technical indicators
        short_ma = np.mean(prices[-SHORT_WINDOW:]) if len(prices) >= SHORT_WINDOW else prices[-1]
        long_ma = np.mean(prices[-LONG_WINDOW:]) if len(prices) >= LONG_WINDOW else prices[-1]
        rsi = calculate_rsi(prices)

        # Get sentiment score
        sentiment_score = sentiment_data[token]["sentiment_score"]

        # Prepare market data
        market_data = {
            "token": token,
            "current_price": prices[-1],
            "price_history": prices,
            "technical": {
                "short_ma": short_ma,
                "long_ma": long_ma,
                "rsi": rsi
            },
            "sentiment": sentiment_score
        }

        # Use Groq AI for comprehensive trading recommendation
        result = get_trading_recommendation(token, market_data)

        print(f"[Prediction] Groq AI trading recommendation for {token}: {result['recommendation']} (confidence: {result['confidence']})")

        # Return the recommendation from Groq AI
        return result["recommendation"]
    except Exception as e:
        print(f"[Prediction] Error using Groq AI for trading recommendation: {str(e)}")
        print(f"[Prediction] Falling back to other prediction methods")
        return "HOLD"  # Fallback to neutral recommendation
