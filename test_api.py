#!/usr/bin/env python3
"""
Script para testar os endpoints da API do Airdrop Optimizer.

Este script demonstra como usar os endpoints da API usando Python requests.
Também inclui exemplos de como usar curl para testar os mesmos endpoints.

Uso:
    1. Inicie o servidor da API em um terminal:
       $ uvicorn api.main:app --reload
    
    2. Execute este script em outro terminal:
       $ python test_api.py
"""

import requests
import json
import time
import sys

# URL base da API (ajuste se necessário)
BASE_URL = "http://localhost:8000"

def print_section(title):
    """Imprime um título de seção formatado."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def print_request(method, url, data=None):
    """Imprime informações sobre a requisição."""
    print(f"\n> {method} {url}")
    if data:
        print(f"> Dados: {json.dumps(data, indent=2)}")

def print_response(response):
    """Imprime informações sobre a resposta."""
    print(f"< Status: {response.status_code}")
    try:
        print(f"< Resposta: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"< Resposta: {response.text}")

def print_curl_example(method, url, data=None):
    """Imprime um exemplo de como fazer a mesma requisição usando curl."""
    curl_cmd = f"curl -X {method} {url}"
    
    if data:
        curl_cmd += f" -H 'Content-Type: application/json' -d '{json.dumps(data)}'"
    
    print(f"\nExemplo com curl:")
    print(curl_cmd)

def test_root_endpoint():
    """Testa o endpoint raiz (/)."""
    print_section("Testando o endpoint raiz (/)")
    
    url = f"{BASE_URL}/"
    print_request("GET", url)
    
    response = requests.get(url)
    print_response(response)
    
    print_curl_example("GET", url)

def test_list_airdrops():
    """Testa o endpoint para listar airdrops (/airdrop/list)."""
    print_section("Testando o endpoint para listar airdrops (/airdrop/list)")
    
    url = f"{BASE_URL}/airdrop/list"
    print_request("GET", url)
    
    response = requests.get(url)
    print_response(response)
    
    print_curl_example("GET", url)
    
    return response.json()

def test_create_airdrop():
    """Testa o endpoint para criar uma campanha de airdrop (/airdrop)."""
    print_section("Testando o endpoint para criar uma campanha de airdrop (/airdrop)")
    
    url = f"{BASE_URL}/airdrop"
    data = {
        "token": "BTC",
        "volume_required": 1000,
        "reward": 50,
        "period_days": 7,
        "url": "https://www.binance.com/pt-BR/airdrop/btc"
    }
    
    print_request("POST", url, data)
    
    response = requests.post(url, json=data)
    print_response(response)
    
    print_curl_example("POST", url, data)
    
    return response.json()

def test_list_agents():
    """Testa o endpoint para listar agentes (/agents)."""
    print_section("Testando o endpoint para listar agentes (/agents)")
    
    url = f"{BASE_URL}/agents"
    print_request("GET", url)
    
    response = requests.get(url)
    print_response(response)
    
    print_curl_example("GET", url)
    
    return response.json()

def test_get_agent_status(agent_id):
    """Testa o endpoint para obter o status de um agente (/agents/{agent_id})."""
    print_section(f"Testando o endpoint para obter o status de um agente (/agents/{agent_id})")
    
    url = f"{BASE_URL}/agents/{agent_id}"
    print_request("GET", url)
    
    response = requests.get(url)
    print_response(response)
    
    print_curl_example("GET", url)
    
    return response.json()

def test_start_agent(agent_id):
    """Testa o endpoint para iniciar um agente (/agents/{agent_id}/start)."""
    print_section(f"Testando o endpoint para iniciar um agente (/agents/{agent_id}/start)")
    
    url = f"{BASE_URL}/agents/{agent_id}/start"
    print_request("POST", url)
    
    response = requests.post(url)
    print_response(response)
    
    print_curl_example("POST", url)
    
    return response.json()

def test_stop_agent(agent_id):
    """Testa o endpoint para parar um agente (/agents/{agent_id}/stop)."""
    print_section(f"Testando o endpoint para parar um agente (/agents/{agent_id}/stop)")
    
    url = f"{BASE_URL}/agents/{agent_id}/stop"
    print_request("POST", url)
    
    response = requests.post(url)
    print_response(response)
    
    print_curl_example("POST", url)
    
    return response.json()

def run_all_tests():
    """Executa todos os testes em sequência."""
    try:
        # Testa o endpoint raiz
        test_root_endpoint()
        
        # Testa a listagem de airdrops
        test_list_airdrops()
        
        # Cria uma campanha de airdrop
        airdrop_response = test_create_airdrop()
        agent_id = airdrop_response.get("agent_id")
        
        if not agent_id:
            print("\nErro: Não foi possível obter o ID do agente da resposta.")
            return
        
        print(f"\nAgente criado com ID: {agent_id}")
        
        # Espera um pouco para o agente ser inicializado
        time.sleep(2)
        
        # Lista os agentes
        test_list_agents()
        
        # Obtém o status do agente
        test_get_agent_status(agent_id)
        
        # Inicia o agente
        test_start_agent(agent_id)
        
        # Espera um pouco para o agente começar a executar
        time.sleep(2)
        
        # Obtém o status atualizado do agente
        test_get_agent_status(agent_id)
        
        # Para o agente
        test_stop_agent(agent_id)
        
        # Obtém o status final do agente
        test_get_agent_status(agent_id)
        
        print("\nTodos os testes foram concluídos com sucesso!")
        
    except requests.exceptions.ConnectionError:
        print("\nErro: Não foi possível conectar ao servidor da API.")
        print("Certifique-se de que o servidor está em execução com o comando:")
        print("  uvicorn api.main:app --reload")
        
    except Exception as e:
        print(f"\nErro durante a execução dos testes: {str(e)}")

def print_usage():
    """Imprime instruções de uso."""
    print_section("Como testar os endpoints da API do Airdrop Optimizer")
    
    print("""
Para testar os endpoints da API, siga estas etapas:

1. Inicie o servidor da API em um terminal:
   $ uvicorn api.main:app --reload

2. Execute este script em outro terminal:
   $ python test_api.py

Ou teste endpoints individuais:
   $ python test_api.py root            # Testa o endpoint raiz
   $ python test_api.py list_airdrops   # Lista airdrops
   $ python test_api.py create_airdrop  # Cria uma campanha de airdrop
   $ python test_api.py list_agents     # Lista agentes

Você também pode usar a interface Swagger da API acessando:
http://localhost:8000/docs
    """)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "root":
            test_root_endpoint()
        elif command == "list_airdrops":
            test_list_airdrops()
        elif command == "create_airdrop":
            test_create_airdrop()
        elif command == "list_agents":
            test_list_agents()
        else:
            print(f"Comando desconhecido: {command}")
            print_usage()
    else:
        print_usage()
        choice = input("\nDeseja executar todos os testes? (s/n): ")
        if choice.lower() == 's':
            run_all_tests()