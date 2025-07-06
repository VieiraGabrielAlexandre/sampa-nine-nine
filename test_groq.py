#!/usr/bin/env python3
"""
Test script for Groq AI integration in the Airdrop Optimizer project.

This script tests the Groq AI integration by:
1. Testing the GroqAIClient
2. Testing sentiment analysis
3. Testing price prediction
4. Testing trading recommendations

Usage:
    python test_groq.py
"""

import os
import sys
import json
import time
from dotenv import load_dotenv
from agents.groq_integration import (
    GroqAIClient, 
    analyze_market_sentiment, 
    predict_price_movement, 
    get_trading_recommendation
)

# Load environment variables
load_dotenv()

def print_section(title):
    """Print a section title."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def test_groq_client():
    """Test the Groq AI client."""
    print_section("Testing Groq AI Client")
    
    # Check if GROQ_API_KEY is set
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY environment variable is not set.")
        print("Please set it in a .env file or export it in your shell:")
        print("  export GROQ_API_KEY=your_api_key_here")
        return False
    
    try:
        # Create client
        client = GroqAIClient()
        
        # Test a simple prompt
        prompt = "Hello, can you tell me what Groq is in one sentence?"
        print(f"Sending test prompt to Groq: '{prompt}'")
        
        response = client.generate_text(prompt, max_tokens=50)
        
        if response:
            print(f"✅ Successfully received response from Groq API:")
            print(f"   {response}")
            return True
        else:
            print("❌ Received empty response from Groq API.")
            return False
    except Exception as e:
        print(f"❌ Error testing Groq client: {str(e)}")
        return False

def test_sentiment_analysis():
    """Test sentiment analysis with Groq."""
    print_section("Testing Sentiment Analysis")
    
    # Test tokens
    tokens = ["BTC", "ETH", "SOL"]
    
    for token in tokens:
        try:
            print(f"Analyzing sentiment for {token}...")
            
            # Create some test news data
            news_data = [
                f"{token} reaches new all-time high as institutional adoption increases",
                f"Major exchange announces support for {token} staking",
                f"Developers release new update for {token} network, improving scalability"
            ]
            
            # Get sentiment analysis
            result = analyze_market_sentiment(token, news_data)
            
            if "sentiment_score" in result:
                print(f"✅ Successfully analyzed sentiment for {token}:")
                print(f"   Score: {result['sentiment_score']}")
                print(f"   Recommendation: {result['recommendation']}")
                print(f"   Explanation: {result['explanation']}")
            else:
                print(f"❌ Failed to analyze sentiment for {token}: Invalid response format")
        except Exception as e:
            print(f"❌ Error analyzing sentiment for {token}: {str(e)}")

def test_price_prediction():
    """Test price prediction with Groq."""
    print_section("Testing Price Prediction")
    
    # Test tokens with simulated price history
    test_data = {
        "BTC": [48000, 49000, 50000, 49500, 51000, 52000, 51500, 52500, 53000, 52800],
        "ETH": [2800, 2850, 2900, 2950, 3000, 2950, 3050, 3100, 3050, 3150],
        "SOL": [90, 92, 95, 94, 98, 100, 102, 101, 105, 108]
    }
    
    for token, prices in test_data.items():
        try:
            print(f"Predicting price movement for {token}...")
            
            # Get price prediction
            result = predict_price_movement(token, prices, "short")
            
            if "prediction_score" in result:
                print(f"✅ Successfully predicted price movement for {token}:")
                print(f"   Score: {result['prediction_score']}")
                print(f"   Recommendation: {result['recommendation']}")
                print(f"   Explanation: {result['explanation']}")
            else:
                print(f"❌ Failed to predict price for {token}: Invalid response format")
        except Exception as e:
            print(f"❌ Error predicting price for {token}: {str(e)}")

def test_trading_recommendation():
    """Test trading recommendations with Groq."""
    print_section("Testing Trading Recommendations")
    
    # Test tokens with simulated market data
    test_data = {
        "BTC": {
            "token": "BTC",
            "current_price": 52800,
            "price_history": [48000, 49000, 50000, 49500, 51000, 52000, 51500, 52500, 53000, 52800],
            "technical": {
                "short_ma": 52560,
                "long_ma": 50980,
                "rsi": 58.5
            },
            "sentiment": 0.7
        },
        "ETH": {
            "token": "ETH",
            "current_price": 3150,
            "price_history": [2800, 2850, 2900, 2950, 3000, 2950, 3050, 3100, 3050, 3150],
            "technical": {
                "short_ma": 3090,
                "long_ma": 2980,
                "rsi": 62.3
            },
            "sentiment": 0.5
        },
        "SOL": {
            "token": "SOL",
            "current_price": 108,
            "price_history": [90, 92, 95, 94, 98, 100, 102, 101, 105, 108],
            "technical": {
                "short_ma": 104,
                "long_ma": 98.5,
                "rsi": 68.7
            },
            "sentiment": 0.8
        }
    }
    
    for token, market_data in test_data.items():
        try:
            print(f"Getting trading recommendation for {token}...")
            
            # Get trading recommendation
            result = get_trading_recommendation(token, market_data)
            
            if "recommendation" in result:
                print(f"✅ Successfully got trading recommendation for {token}:")
                print(f"   Recommendation: {result['recommendation']}")
                print(f"   Confidence: {result['confidence']}")
                print(f"   Risk Level: {result['risk_level']}")
                print(f"   Explanation: {result['explanation']}")
            else:
                print(f"❌ Failed to get recommendation for {token}: Invalid response format")
        except Exception as e:
            print(f"❌ Error getting recommendation for {token}: {str(e)}")

def main():
    """Main function to run all tests."""
    print_section("Groq AI Integration Test")
    print("This script tests the integration with the Groq AI platform.")
    print("Note: You need a valid Groq API key to run these tests.")
    print("Set your API key in a .env file or as an environment variable: GROQ_API_KEY=your_key")
    
    # Test the Groq client first
    client_ok = test_groq_client()
    
    if not client_ok:
        print("\n❌ Groq client test failed. Skipping remaining tests.")
        return 1
    
    # Run the other tests
    test_sentiment_analysis()
    test_price_prediction()
    test_trading_recommendation()
    
    print_section("Test Summary")
    print("✅ All tests completed.")
    print("Note: Check the output above for any individual test failures.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())