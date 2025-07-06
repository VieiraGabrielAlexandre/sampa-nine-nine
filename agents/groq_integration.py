"""
Groq AI Integration Module

This module provides integration with the Groq AI platform for the Airdrop Optimizer project.
It handles communication with Groq's API for enhanced predictions and sentiment analysis.
"""

import os
import json
import time
import logging
import requests
from typing import Dict, List, Any, Optional, Union
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("groq_integration")

# Default model to use
DEFAULT_MODEL = "llama3-70b-8192"

class GroqAIClient:
    """
    A client for interacting with the Groq AI platform.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Groq AI client.

        Args:
            api_key (str, optional): The Groq API key. If not provided, will look for GROQ_API_KEY environment variable.
        """
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            logger.warning("No Groq API key provided. Please set GROQ_API_KEY environment variable or pass api_key parameter.")

        self.base_url = "https://api.groq.com/openai/v1"
        self.model = DEFAULT_MODEL

        logger.info(f"Initialized Groq AI client with model: {self.model}")

    def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a request to the Groq API.

        Args:
            endpoint (str): The API endpoint to call.
            data (dict): The request payload.

        Returns:
            dict: The API response.
        """
        if not self.api_key:
            raise ValueError("Groq API key is required. Set GROQ_API_KEY environment variable or pass api_key parameter.")

        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request to Groq API: {str(e)}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response: {e.response.text}")
            raise

    def generate_text(self, prompt: str, max_tokens: int = 100, temperature: float = 0.7) -> str:
        """
        Generate text using the Groq API.

        Args:
            prompt (str): The prompt to generate text from.
            max_tokens (int): Maximum number of tokens to generate.
            temperature (float): Sampling temperature, between 0 and 1.

        Returns:
            str: The generated text.
        """
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        try:
            response = self._make_request("chat/completions", data)
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            return ""

def analyze_market_sentiment(token: str, news_data: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Analyze market sentiment for a token using Groq AI.

    Args:
        token (str): The token symbol.
        news_data (list, optional): List of news headlines or articles about the token.

    Returns:
        dict: Sentiment analysis results.
    """
    client = GroqAIClient()

    # If no news data is provided, use a generic prompt
    if not news_data:
        prompt = f"""
        Analyze the current market sentiment for {token} cryptocurrency.
        Consider recent market trends, community sentiment, and any relevant news.
        Provide a sentiment score between -1 (extremely negative) and 1 (extremely positive),
        and a brief explanation of your analysis.
        Format your response as a JSON object with the following structure:
        {{
            "sentiment_score": (float between -1 and 1),
            "explanation": (string explaining the sentiment),
            "recommendation": (string, one of "BUY", "SELL", or "HOLD")
        }}
        """
    else:
        # If news data is provided, include it in the prompt
        news_text = "\n".join([f"- {item}" for item in news_data])
        prompt = f"""
        Analyze the market sentiment for {token} cryptocurrency based on the following news:

        {news_text}

        Provide a sentiment score between -1 (extremely negative) and 1 (extremely positive),
        and a brief explanation of your analysis.
        Format your response as a JSON object with the following structure:
        {{
            "sentiment_score": (float between -1 and 1),
            "explanation": (string explaining the sentiment),
            "recommendation": (string, one of "BUY", "SELL", or "HOLD")
        }}
        """

    try:
        response_text = client.generate_text(prompt, max_tokens=500, temperature=0.3)

        # Extract JSON from response
        try:
            # Find JSON object in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                result = json.loads(json_str)
            else:
                # Fallback if JSON not found
                result = {
                    "sentiment_score": 0,
                    "explanation": "Could not parse response",
                    "recommendation": "HOLD"
                }
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON from response: {response_text}")
            result = {
                "sentiment_score": 0,
                "explanation": "Error parsing response",
                "recommendation": "HOLD"
            }

        logger.info(f"Sentiment analysis for {token}: {result['sentiment_score']}")
        return result

    except Exception as e:
        logger.error(f"Error analyzing sentiment for {token}: {str(e)}")
        return {
            "sentiment_score": 0,
            "explanation": f"Error: {str(e)}",
            "recommendation": "HOLD"
        }

def predict_price_movement(token: str, price_history: List[float], time_horizon: str = "short") -> Dict[str, Any]:
    """
    Predict price movement for a token using Groq AI.

    Args:
        token (str): The token symbol.
        price_history (list): List of historical prices.
        time_horizon (str): Time horizon for prediction ("short", "medium", "long").

    Returns:
        dict: Price prediction results.
    """
    client = GroqAIClient()

    # Format price history for the prompt
    prices_str = ", ".join([f"{price:.2f}" for price in price_history[-10:]])

    prompt = f"""
    Analyze the price history for {token} cryptocurrency and predict the likely price movement.

    Recent prices (from oldest to newest): {prices_str}
    Current price: {price_history[-1]:.2f}
    Time horizon: {time_horizon} term

    Based on this data, predict whether the price is likely to increase, decrease, or remain stable.
    Provide a prediction score between -1 (strong decrease) and 1 (strong increase),
    and a brief explanation of your prediction.
    Format your response as a JSON object with the following structure:
    {{
        "prediction_score": (float between -1 and 1),
        "explanation": (string explaining the prediction),
        "recommendation": (string, one of "BUY", "SELL", or "HOLD")
    }}
    """

    try:
        response_text = client.generate_text(prompt, max_tokens=500, temperature=0.3)

        # Extract JSON from response
        try:
            # Find JSON object in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                result = json.loads(json_str)
            else:
                # Fallback if JSON not found
                result = {
                    "prediction_score": 0,
                    "explanation": "Could not parse response",
                    "recommendation": "HOLD"
                }
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON from response: {response_text}")
            result = {
                "prediction_score": 0,
                "explanation": "Error parsing response",
                "recommendation": "HOLD"
            }

        logger.info(f"Price prediction for {token}: {result['prediction_score']}")
        return result

    except Exception as e:
        logger.error(f"Error predicting price for {token}: {str(e)}")
        return {
            "prediction_score": 0,
            "explanation": f"Error: {str(e)}",
            "recommendation": "HOLD"
        }

def get_trading_recommendation(token: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get a comprehensive trading recommendation for a token using Groq AI.

    Args:
        token (str): The token symbol.
        market_data (dict): Market data including price history, technical indicators, etc.

    Returns:
        dict: Trading recommendation.
    """
    client = GroqAIClient()

    # Format market data for the prompt
    market_data_str = json.dumps(market_data, indent=2)

    prompt = f"""
    You are an expert cryptocurrency trading advisor. Analyze the following market data for {token} and provide a trading recommendation.

    Market Data:
    {market_data_str}

    Based on this data, provide a comprehensive trading recommendation.
    Consider technical indicators, market sentiment, and recent price movements.
    Format your response as a JSON object with the following structure:
    {{
        "recommendation": (string, one of "BUY", "SELL", or "HOLD"),
        "confidence": (float between 0 and 1),
        "explanation": (string explaining the recommendation),
        "risk_level": (string, one of "LOW", "MEDIUM", "HIGH")
    }}
    """

    try:
        response_text = client.generate_text(prompt, max_tokens=800, temperature=0.3)

        # Extract JSON from response
        try:
            # Find JSON object in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                result = json.loads(json_str)
            else:
                # Fallback if JSON not found
                result = {
                    "recommendation": "HOLD",
                    "confidence": 0.5,
                    "explanation": "Could not parse response",
                    "risk_level": "MEDIUM"
                }
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON from response: {response_text}")
            result = {
                "recommendation": "HOLD",
                "confidence": 0.5,
                "explanation": "Error parsing response",
                "risk_level": "MEDIUM"
            }

        logger.info(f"Trading recommendation for {token}: {result['recommendation']} (confidence: {result['confidence']})")
        return result

    except Exception as e:
        logger.error(f"Error getting trading recommendation for {token}: {str(e)}")
        return {
            "recommendation": "HOLD",
            "confidence": 0.5,
            "explanation": f"Error: {str(e)}",
            "risk_level": "MEDIUM"
        }
