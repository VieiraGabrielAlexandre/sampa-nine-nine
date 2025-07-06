#!/usr/bin/env python3
"""
Script to test the fix for the /airdrop endpoint.

This script makes a POST request to the /airdrop endpoint with the same payload
that was causing the error. If the fix works, the request should succeed and
return a 200 OK response with the expected data.

Usage:
    1. Make sure the API server is running:
       $ uvicorn api.main:app --reload
    
    2. Run this script:
       $ python test_fix.py
"""

import requests
import json

# URL of the API endpoint
URL = "http://localhost:8000/airdrop"

# Payload that was causing the error
payload = {
    "token": "BTC",
    "volume_required": 1000,
    "reward": 50,
    "period_days": 7,
    "url": "https://www.binance.com/pt-BR/airdrop/btc"
}

def test_airdrop_endpoint():
    """Test the /airdrop endpoint with the payload that was causing the error."""
    print(f"Making POST request to {URL} with payload:")
    print(json.dumps(payload, indent=2))
    
    try:
        response = requests.post(URL, json=payload)
        
        print(f"\nResponse status code: {response.status_code}")
        
        if response.status_code == 200:
            print("Request succeeded! The fix worked.")
            print("\nResponse data:")
            print(json.dumps(response.json(), indent=2))
        else:
            print("Request failed with status code:", response.status_code)
            print("\nResponse data:")
            print(response.text)
    
    except Exception as e:
        print(f"Error making request: {str(e)}")
        print("Make sure the API server is running with: uvicorn api.main:app --reload")

if __name__ == "__main__":
    test_airdrop_endpoint()