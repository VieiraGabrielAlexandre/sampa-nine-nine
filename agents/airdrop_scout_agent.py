import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import random
import time

def get_airdrop_campaigns():
    """
    Scrapes the Binance airdrop page to extract campaign information.
    In this implementation, we're simulating the scraping process.

    Returns:
        list: A list of dictionaries containing campaign information.
    """
    try:
        print("[Scout] Iniciando scraping da página de airdrops da Binance...")

        url = "https://www.binance.com/bapi/asset/v1/friendly/asset-service/airdrop/list"
        response = requests.get(url)

        campaigns = []
        filtered_json = [item for item in response.json()["data"] if item["airdropStatus"] == "ON_GOING"]
        for item in filtered_json:
            if item["airdropStatus"] == "ON_GOING":
                campaigns.append({
                    "token": item["airdropAsset"],
                    "start_date": datetime.fromtimestamp(item["airdropPeriodStart"] / 1000).strftime("%Y-%m-%d"),
                    "end_date": datetime.fromtimestamp(item["airdropPeriodEnd"] / 1000).strftime("%Y-%m-%d"),
                    "period_days": (item["airdropPeriodEnd"] - item["airdropPeriodStart"]) / (1000 * 60 * 60 * 24), 
                    "url": item["link"],
                })
            else:
                continue
                
        # exibir o json filtrado como json
        print(json.dumps(campaigns, indent=4))

        # Analisando a viabilidade de cada campanha
        for campaign in campaigns:
            analyze_campaign_viability(campaign)

        print(f"[Scout] {len(campaigns)} campanhas coletadas e analisadas")

        return campaigns

    except Exception as e:
        print(f"[Scout] Erro ao coletar campanhas: {str(e)}")
        # Retorna algumas campanhas de fallback em caso de erro
        return [
            {"token": "ABC", "volume_required": 1000, "reward": 50, "viability_score": 6.0},
            {"token": "XYZ", "volume_required": 500, "reward": 20, "viability_score": 5.5}
        ]

def analyze_campaign_viability(campaign):
    """
    Analyzes the viability of a campaign based on its parameters.

    Args:
        campaign (dict): The campaign to analyze.

    Returns:
        float: A viability score between 0 and 10.
    """
    # Em um ambiente real, usaríamos um algoritmo mais sofisticado
    # Aqui estamos apenas simulando uma análise básica

    # Calculando o retorno sobre o investimento (ROI)
    volume = campaign["volume_required"]
    reward = campaign["reward"]
    period = campaign.get("period_days", 7)  # Padrão de 7 dias se não especificado

    # Simulando custos de trading (taxas, spread, etc.)
    estimated_costs = volume * 0.001  # 0.1% de custo

    # Calculando ROI diário
    daily_roi = (reward - estimated_costs) / period

    # Calculando a pontuação de viabilidade com base no ROI
    # Fórmula simples: quanto maior o ROI diário, maior a pontuação
    # Limitando entre 0 e 10
    viability_score = min(10, max(0, daily_roi * period / reward * 10))

    # Arredondando para uma casa decimal
    viability_score = round(viability_score, 1)

    print(f"[Scout] Campanha {campaign['token']} analisada: Score de viabilidade = {viability_score}")

    return viability_score
