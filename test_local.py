"""
Script para testes locais da aplicação
Execute: python test_local.py
"""

import requests
import json
from pprint import pprint

BASE_URL = "http://localhost:5000"


def test_health():
    """Testa o health check"""
    print("\n" + "="*50)
    print("TESTANDO HEALTH CHECK")
    print("="*50)

    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    pprint(response.json())


def test_ultimo_sorteio():
    """Testa endpoint de último sorteio"""
    print("\n" + "="*50)
    print("TESTANDO ÚLTIMO SORTEIO")
    print("="*50)

    response = requests.get(f"{BASE_URL}/resultado-ultimo-sorteio")
    print(f"Status: {response.status_code}")
    pprint(response.json())


def test_qui_quadrado():
    """Testa análise qui-quadrado"""
    print("\n" + "="*50)
    print("TESTANDO ANÁLISE QUI-QUADRADO")
    print("="*50)

    response = requests.get(f"{BASE_URL}/analise-qui-quadrado")
    print(f"Status: {response.status_code}")

    data = response.json()

    # Exibir apenas partes relevantes
    print("\nEstatísticas:")
    pprint(data.get('estatisticas'))

    print("\nTeste Qui-Quadrado:")
    pprint(data.get('teste_qui_quadrado'))

    print("\nPrevisão:")
    pprint(data.get('previsao'))


def test_lorenz():
    """Testa análise de Lorenz"""
    print("\n" + "="*50)
    print("TESTANDO ATRATORES DE LORENZ")
    print("="*50)

    response = requests.get(f"{BASE_URL}/atratores-de-lorenz")
    print(f"Status: {response.status_code}")

    data = response.json()

    print("\nAnálise de Caos:")
    pprint(data.get('analise_caos'))

    print("\nPrevisão:")
    pprint(data.get('previsao'))

    print("\nVisualização disponível: ", 'visualizacao' in data)
    if 'visualizacao' in data:
        print(f"Tamanho da imagem base64: {len(data['visualizacao']['data'])} caracteres")


def test_quantica():
    """Testa análise quântica"""
    print("\n" + "="*50)
    print("TESTANDO ANÁLISE QUÂNTICA")
    print("="*50)

    response = requests.get(f"{BASE_URL}/analise-quantica")
    print(f"Status: {response.status_code}")

    data = response.json()

    print("\nEstatísticas:")
    pprint(data.get('estatisticas'))

    print("\nPrevisão Método 1:")
    pprint(data.get('previsao_metodo_1'))

    print("\nPrevisão Método 2:")
    pprint(data.get('previsao_metodo_2'))


def test_previsao():
    """Testa previsão combinada"""
    print("\n" + "="*50)
    print("TESTANDO PREVISÃO COMBINADA")
    print("="*50)

    response = requests.get(f"{BASE_URL}/previsao")
    print(f"Status: {response.status_code}")

    data = response.json()

    print("\n🎯 PREVISÃO FINAL:")
    print(data.get('previsao_final'))

    print("\nMétodos utilizados:")
    pprint(data.get('metodos_utilizados'))

    print("\nPrevisões individuais:")
    for metodo, pred in data.get('previsoes_individuais', {}).items():
        print(f"\n  {metodo}:")
        pprint(pred)


def test_cego():
    """Testa análise cega"""
    print("\n" + "="*50)
    print("TESTANDO ANÁLISE CEGA (Concurso 2000 -> 2001)")
    print("="*50)

    payload = {
        "concurso_limite": 2000
    }

    response = requests.post(
        f"{BASE_URL}/teste-cego",
        json=payload,
        headers={'Content-Type': 'application/json'}
    )

    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()

        print(f"\nTreino até concurso: {data.get('concurso_treino_ate')}")
        print(f"Concurso testado: {data.get('concurso_testado')}")
        print(f"\nPrevisão: {data.get('previsao')}")
        print(f"Resultado Real: {data.get('resultado_real')}")
        print(f"\n✅ Acertos: {data.get('acertos')}/6 ({data.get('taxa_acerto')})")
    else:
        print(f"Erro: {response.text}")


def menu():
    """Menu interativo"""
    while True:
        print("\n" + "="*50)
        print("MEGA-SENA HACKER - TESTES LOCAIS")
        print("="*50)
        print("1. Health Check")
        print("2. Último Sorteio")
        print("3. Análise Qui-Quadrado")
        print("4. Atratores de Lorenz")
        print("5. Análise Quântica")
        print("6. Previsão Combinada")
        print("7. Teste Cego")
        print("8. Executar Todos os Testes")
        print("0. Sair")

        escolha = input("\nEscolha uma opção: ")

        try:
            if escolha == "1":
                test_health()
            elif escolha == "2":
                test_ultimo_sorteio()
            elif escolha == "3":
                test_qui_quadrado()
            elif escolha == "4":
                test_lorenz()
            elif escolha == "5":
                test_quantica()
            elif escolha == "6":
                test_previsao()
            elif escolha == "7":
                test_cego()
            elif escolha == "8":
                test_health()
                test_ultimo_sorteio()
                test_qui_quadrado()
                test_lorenz()
                test_quantica()
                test_previsao()
                test_cego()
            elif escolha == "0":
                print("\nEncerrando...")
                break
            else:
                print("\nOpção inválida!")

        except requests.exceptions.ConnectionError:
            print("\n❌ ERRO: Não foi possível conectar à API.")
            print("Certifique-se de que a aplicação está rodando em http://localhost:5000")
        except Exception as e:
            print(f"\n❌ ERRO: {str(e)}")

        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    menu()
