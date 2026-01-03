from flask import Flask, request, jsonify, send_file
from database import Database
from analyzers.chi_square import ChiSquareAnalyzer
from analyzers.lorenz_attractor import LorenzAttractorAnalyzer
from analyzers.quantum_analyzer import QuantumAnalyzer
from config import Config
from utils import convert_to_native_types
import base64
from io import BytesIO
import logging

# === NOVOS IMPORTS v2.0 ===
import sys
sys.path.insert(0, '/app')

app = Flask(__name__)
config = Config()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_results_data(limit=None):
    """Função auxiliar para obter dados do banco"""
    db = Database()
    try:
        schema = config.DB_SCHEMA
        table = config.DB_TABLE
        if limit:
            results = db.get_results_until(limit, schema=schema, table=table)
        else:
            results = db.get_all_results(schema=schema, table=table)
        return results
    except Exception as e:
        logger.error(f"Erro ao obter dados: {str(e)}")
        raise
    finally:
        db.disconnect()


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'Mega-Sena Hacker API'
    }), 200


@app.route('/resultado-ultimo-sorteio', methods=['GET', 'POST'])
def ultimo_sorteio():
    """
    Endpoint: 'Resultado do último sorteio'
    Retorna o último resultado do banco de dados
    """
    try:
        db = Database()
        result = db.get_last_result(schema=config.DB_SCHEMA, table=config.DB_TABLE)
        db.disconnect()

        if not result:
            return jsonify({'error': 'Nenhum resultado encontrado'}), 404

        # Suportar tanto 'data' quanto 'data_sorteio'
        data_field = result.get('data_sorteio') or result.get('data')

        response = {
            'concurso': result.get('concurso'),
            'data': str(data_field) if data_field else None,
            'numeros': [
                result.get('bola1'),
                result.get('bola2'),
                result.get('bola3'),
                result.get('bola4'),
                result.get('bola5'),
                result.get('bola6')
            ]
        }

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Erro em ultimo_sorteio: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/analise-qui-quadrado', methods=['GET', 'POST'])
def analise_qui_quadrado():
    """
    Endpoint: 'Análise Qui-Quadrado'
    Realiza análise estatística qui-quadrado
    """
    try:
        results = get_results_data()

        if not results:
            return jsonify({'error': 'Nenhum dado disponível'}), 404

        analyzer = ChiSquareAnalyzer(results)

        # Realizar testes
        chi_test = analyzer.chi_square_test()
        stats = analyzer.get_statistics()
        prediction = analyzer.predict_numbers()

        response = {
            'metodo': 'Análise Qui-Quadrado',
            'estatisticas': convert_to_native_types(stats),
            'teste_qui_quadrado': convert_to_native_types({
                'chi2_statistic': chi_test['chi2_statistic'],
                'p_value': chi_test['p_value'],
                'distribuicao_uniforme': chi_test['is_uniform']
            }),
            'previsao': convert_to_native_types(prediction)
        }

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Erro em analise_qui_quadrado: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/atratores-de-lorenz', methods=['GET', 'POST'])
def atratores_lorenz():
    """
    Endpoint: 'Atratores de Lorenz'
    Retorna análise e visualização do atrator de Lorenz
    """
    try:
        results = get_results_data()

        if not results:
            return jsonify({'error': 'Nenhum dado disponível'}), 404

        analyzer = LorenzAttractorAnalyzer(results)

        # Gerar visualização
        image_base64 = analyzer.generate_plot()

        # Análise de caos
        chaos_analysis = analyzer.analyze_chaos()

        # Predição
        prediction = analyzer.predict_numbers()

        response = {
            'metodo': 'Atratores de Lorenz',
            'analise_caos': convert_to_native_types(chaos_analysis),
            'previsao': convert_to_native_types(prediction),
            'visualizacao': {
                'tipo': 'image/png',
                'data': image_base64,
                'descricao': 'Diagrama de Atratores de Lorenz baseado nos sorteios'
            }
        }

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Erro em atratores_lorenz: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/analise-quantica', methods=['GET', 'POST'])
def analise_quantica():
    """
    Endpoint: 'Análise quântica'
    Realiza análise usando simulação quântica
    """
    try:
        results = get_results_data()

        if not results:
            return jsonify({'error': 'Nenhum dado disponível'}), 404

        analyzer = QuantumAnalyzer(results)

        # Executar ambos os métodos quânticos
        prediction_1 = analyzer.predict_numbers()
        prediction_2 = analyzer.quantum_interference_prediction()

        stats = analyzer.get_quantum_statistics()

        response = {
            'metodo': 'Análise Quântica (Simulação)',
            'estatisticas': convert_to_native_types(stats),
            'previsao_metodo_1': convert_to_native_types(prediction_1),
            'previsao_metodo_2': convert_to_native_types(prediction_2),
            'descricao': 'Predição baseada em simulação de computação quântica usando Qiskit'
        }

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Erro em analise_quantica: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/previsao', methods=['GET', 'POST'])
def previsao():
    """
    Endpoint: 'Previsão'
    Combina todos os métodos para gerar uma previsão final
    """
    try:
        results = get_results_data()

        if not results:
            return jsonify({'error': 'Nenhum dado disponível'}), 404

        # Executar todas as análises
        chi_analyzer = ChiSquareAnalyzer(results)
        lorenz_analyzer = LorenzAttractorAnalyzer(results)
        quantum_analyzer = QuantumAnalyzer(results)

        pred_chi = chi_analyzer.predict_numbers()
        pred_lorenz = lorenz_analyzer.predict_numbers()
        pred_quantum = quantum_analyzer.predict_numbers()

        # Agregar previsões (votar nos números mais comuns)
        all_predictions = (
            pred_chi['prediction'] +
            pred_lorenz['prediction'] +
            pred_quantum['prediction']
        )

        from collections import Counter
        frequency = Counter(all_predictions)

        # Selecionar os 6 números mais votados
        final_prediction = [num for num, _ in frequency.most_common(6)]

        # Se não temos 6 únicos, completar com números aleatórios
        import random
        available = [i for i in range(1, 61) if i not in final_prediction]
        while len(final_prediction) < 6:
            num = random.choice(available)
            final_prediction.append(num)
            available.remove(num)

        response = {
            'previsao_final': convert_to_native_types(sorted(final_prediction[:6])),
            'metodos_utilizados': ['Qui-Quadrado', 'Atratores de Lorenz', 'Análise Quântica'],
            'previsoes_individuais': convert_to_native_types({
                'qui_quadrado': pred_chi,
                'lorenz': pred_lorenz,
                'quantica': pred_quantum
            }),
            'total_concursos_analisados': len(results)
        }

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Erro em previsao: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/teste-cego', methods=['POST'])
def teste_cego():
    """
    Endpoint para testes cegos (Fase 1)
    Recebe um número de concurso e testa a previsão contra o resultado real
    """
    try:
        data = request.get_json()
        concurso_limite = data.get('concurso_limite')

        if not concurso_limite:
            return jsonify({'error': 'Parâmetro concurso_limite é obrigatório'}), 400

        # Obter dados até o concurso limite
        results_treino = get_results_data(limit=concurso_limite)

        # Obter o próximo concurso (resultado real)
        db = Database()
        query = f'SELECT * FROM "{config.DB_SCHEMA}".{config.DB_TABLE} WHERE concurso = %s'
        resultado_real = db.execute_query(query, (concurso_limite + 1,))
        db.disconnect()

        if not resultado_real:
            return jsonify({'error': f'Concurso {concurso_limite + 1} não encontrado'}), 404

        resultado_real = resultado_real[0]

        # Fazer previsão com dados de treino
        chi_analyzer = ChiSquareAnalyzer(results_treino)
        lorenz_analyzer = LorenzAttractorAnalyzer(results_treino)
        quantum_analyzer = QuantumAnalyzer(results_treino)

        pred_chi = chi_analyzer.predict_numbers()
        pred_lorenz = lorenz_analyzer.predict_numbers()
        pred_quantum = quantum_analyzer.predict_numbers()

        # Previsão combinada
        from collections import Counter
        all_preds = (
            pred_chi['prediction'] +
            pred_lorenz['prediction'] +
            pred_quantum['prediction']
        )
        frequency = Counter(all_preds)
        previsao_final = sorted([num for num, _ in frequency.most_common(6)])

        # Resultado real
        numeros_reais = sorted([
            resultado_real['bola1'],
            resultado_real['bola2'],
            resultado_real['bola3'],
            resultado_real['bola4'],
            resultado_real['bola5'],
            resultado_real['bola6']
        ])

        # Calcular acertos
        acertos = len(set(previsao_final) & set(numeros_reais))

        response = {
            'concurso_treino_ate': int(concurso_limite),
            'concurso_testado': int(concurso_limite + 1),
            'previsao': convert_to_native_types(previsao_final),
            'resultado_real': convert_to_native_types(numeros_reais),
            'acertos': acertos,
            'taxa_acerto': f'{(acertos/6)*100:.2f}%',
            'previsoes_individuais': convert_to_native_types({
                'qui_quadrado': pred_chi['prediction'],
                'lorenz': pred_lorenz['prediction'],
                'quantica': pred_quantum['prediction']
            })
        }

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Erro em teste_cego: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ==========================================
# REGISTRAR ENDPOINTS v2.0
# ==========================================
from app_v2_endpoints import register_v2_routes
register_v2_routes(app)
logger.info("✅ Endpoints v2.0 carregados")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.PORT, debug=config.DEBUG)
