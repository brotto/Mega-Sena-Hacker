#!/usr/bin/env python3
"""
Script para testar todos os endpoints da API
"""
import requests
import json
import time

BASE_URL = "http://localhost:5555"

def test_endpoint(name, url, method='GET', data=None, timeout=30):
    """Testa um endpoint e retorna o resultado"""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}")

    try:
        if method == 'GET':
            r = requests.get(url, timeout=timeout)
        else:
            r = requests.post(url, json=data, timeout=timeout)

        print(f"Status: {r.status_code}")

        if r.status_code == 200:
            response_data = r.json()

            if 'error' in response_data:
                print(f"❌ ERRO: {response_data['error']}")
                return False
            else:
                # Mostrar informações relevantes
                if 'previsao_final' in response_data:
                    print(f"Previsão Final: {response_data['previsao_final']}")
                elif 'previsao' in response_data:
                    pred = response_data['previsao']
                    if isinstance(pred, dict) and 'prediction' in pred:
                        print(f"Previsão: {pred['prediction']}")
                    else:
                        print(f"Previsão: {pred}")

                if 'concurso' in response_data:
                    print(f"Concurso: {response_data['concurso']}")

                if 'numeros' in response_data:
                    print(f"Números: {response_data['numeros']}")

                print(f"✅ SUCESSO")
                return True
        else:
            print(f"❌ HTTP {r.status_code}")
            print(f"Response: {r.text[:200]}")
            return False

    except requests.Timeout:
        print(f"❌ TIMEOUT ({timeout}s)")
        return False
    except Exception as e:
        print(f"❌ ERRO: {str(e)[:200]}")
        return False

def main():
    print("\n" + "="*60)
    print("MEGA-SENA HACKER - TESTE COMPLETO DE ENDPOINTS")
    print("="*60)

    results = {}

    # Test 1: Health Check
    results['health'] = test_endpoint(
        "Health Check",
        f"{BASE_URL}/health"
    )

    time.sleep(1)

    # Test 2: Último Sorteio
    results['ultimo_sorteio'] = test_endpoint(
        "Último Sorteio",
        f"{BASE_URL}/resultado-ultimo-sorteio"
    )

    time.sleep(1)

    # Test 3: Qui-Quadrado
    results['qui_quadrado'] = test_endpoint(
        "Análise Qui-Quadrado",
        f"{BASE_URL}/analise-qui-quadrado",
        timeout=45
    )

    time.sleep(2)

    # Test 4: Lorenz (pode demorar)
    results['lorenz'] = test_endpoint(
        "Atratores de Lorenz",
        f"{BASE_URL}/atratores-de-lorenz",
        timeout=45
    )

    time.sleep(2)

    # Test 5: Quântica (pode demorar muito)
    print("\n⚠️  Análise Quântica pode demorar 30-60 segundos...")
    results['quantica'] = test_endpoint(
        "Análise Quântica",
        f"{BASE_URL}/analise-quantica",
        timeout=90
    )

    time.sleep(2)

    # Test 6: Previsão Combinada (demora bastante)
    print("\n⚠️  Previsão Combinada pode demorar 60-90 segundos...")
    results['previsao'] = test_endpoint(
        "Previsão Combinada",
        f"{BASE_URL}/previsao",
        timeout=120
    )

    time.sleep(2)

    # Test 7: Teste Cego
    results['teste_cego'] = test_endpoint(
        "Teste Cego (concurso 2500)",
        f"{BASE_URL}/teste-cego",
        method='POST',
        data={'concurso_limite': 2500},
        timeout=120
    )

    # Resumo
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60)

    total = len(results)
    passed = sum(1 for v in results.values() if v)

    for name, passed_test in results.items():
        status = "✅ PASSOU" if passed_test else "❌ FALHOU"
        print(f"{name:20s} : {status}")

    print(f"\n{passed}/{total} testes passaram")

    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
    else:
        print(f"\n⚠️  {total - passed} teste(s) falharam")

    print("="*60)

if __name__ == "__main__":
    main()
