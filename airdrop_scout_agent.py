from bs4 import BeautifulSoup
import requests
import json

def get_airdrop_campaigns():
    # Simulação de scraping (normalmente usaria Selenium devido ao JS da Binance)
    url = 'https://www.binance.com/pt-BR/airdrop'  # Página real, mas para o MVP simulamos
    print('[Scout] Coletando campanhas de airdrop...')

    # Simulação de resposta
    campaigns = [
        {
            'token': 'ABC',
            'link': 'https://binance.com/airdrop/abc',
            'volume_required': 100,
            'reward': 10,
            'duration_days': 5,
            'viability_score': 7.8
        }
    ]
    return campaigns