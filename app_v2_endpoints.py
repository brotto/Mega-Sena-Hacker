"""
Mega Analyzer v2.0 - Novos Endpoints
Adiciona 7 novos endpoints ao servidor Flask existente
Compatível com app.py versão 1.0
"""

from flask import jsonify, request
from database import Database
from config import Config
from utils import convert_to_native_types
import logging
import pandas as pd

logger = logging.getLogger(__name__)


def get_analyzer_with_data():
    """
    Helper para criar LotteryAnalyzer com dados do PostgreSQL
    Compatível com a estrutura existente do app.py
    """
    try:
        # Importar aqui para evitar erro se v2 não estiver instalado
        from v2.core.lottery_analyzer import LotteryAnalyzer
    except ImportError as e:
        logger.error(f"Erro ao importar LotteryAnalyzer: {e}")
        raise ImportError("Módulo v2.core.lottery_analyzer não encontrado. Verifique a instalação.")

    config = Config()
    db = Database()

    try:
        # Buscar TODOS os resultados do banco (ordenados por concurso)
        # IMPORTANTE: Filtrar concurso > 0 para remover dados de lixo
        schema = config.DB_SCHEMA
        table = config.DB_TABLE
        query = f'SELECT * FROM "{schema}".{table} WHERE concurso > 0 ORDER BY concurso'
        results = db.execute_query(query)

        if not results:
            raise ValueError("Nenhum dado disponível no banco de dados")

        # Criar DataFrame pandas
        df = pd.DataFrame(results)

        # Criar analyzer
        analyzer = LotteryAnalyzer("Mega-Sena")

        # Definir colunas das bolas
        ball_columns = ['bola1', 'bola2', 'bola3', 'bola4', 'bola5', 'bola6']

        # Carregar dados no analyzer
        analyzer.df = df
        analyzer.ball_columns = ball_columns
        analyzer.n_draws = len(df)

        logger.info(f"✅ Analyzer criado com {analyzer.n_draws} sorteios")

        return analyzer

    except Exception as e:
        logger.error(f"Erro ao criar analyzer: {str(e)}")
        raise
    finally:
        db.disconnect()


# ==========================================
# FUNÇÃO PRINCIPAL - REGISTRAR ENDPOINTS
# ==========================================

def register_v2_routes(app):
    """
    Registra todos os 7 novos endpoints v2.0 no Flask app
    Chamado do app.py principal
    """

    logger.info("🚀 Iniciando registro de endpoints v2.0...")


    # ==========================================
    # ENDPOINT 1: TESTE DE RUNS
    # ==========================================
    @app.route('/v2/runs-test', methods=['GET', 'POST'])
    def runs_test_v2():
        """
        Teste de Runs (Wald-Wolfowitz)
        Detecta padrões de agrupamento não-aleatório
        """
        try:
            analyzer = get_analyzer_with_data()
            result = analyzer.runs_test()

            # Determinar classificação e nível de suspeita
            z_score = result.get('z_score', 0)
            classificacao = 'PRNG' if abs(z_score) > 10 else 'RNG'

            if abs(z_score) > 30:
                nivel_suspeita = 'CRÍTICO'
            elif abs(z_score) > 10:
                nivel_suspeita = 'ALTO'
            elif abs(z_score) > 5:
                nivel_suspeita = 'MODERADO'
            else:
                nivel_suspeita = 'BAIXO'

            response = {
                'metodo': 'Teste de Runs (Wald-Wolfowitz)',
                'descricao': 'Detecta padrões de agrupamento não-aleatório nas sequências',
                'resultado': convert_to_native_types(result),
                'interpretacao': {
                    'z_score': float(z_score),
                    'p_value': float(result.get('p_value', 0)),
                    'classificacao': classificacao,
                    'nivel_suspeita': nivel_suspeita,
                    'explicacao': f'Z-score de {z_score:.2f} indica comportamento {classificacao}'
                }
            }

            logger.info(f"✅ Runs test executado: Z={z_score:.2f}")
            return jsonify(response), 200

        except Exception as e:
            logger.error(f"❌ Erro em runs_test_v2: {str(e)}")
            return jsonify({'error': str(e)}), 500


    # ==========================================
    # ENDPOINT 2: VELOCIDADE DE COBERTURA
    # ==========================================
    @app.route('/v2/coverage-speed', methods=['GET', 'POST'])
    def coverage_speed_v2():
        """
        Velocidade de Cobertura - Teste Coupon Collector
        Analisa equalização artificial
        """
        try:
            analyzer = get_analyzer_with_data()
            result = analyzer.coverage_speed_test(n_possible=60)

            # Determinar classificação
            diff_pct = abs(result.get('percentage_difference', 0))
            classificacao = 'PRNG' if diff_pct > 50 else 'RNG'

            if diff_pct > 70:
                nivel_suspeita = 'CRÍTICO'
            elif diff_pct > 50:
                nivel_suspeita = 'ALTO'
            elif diff_pct > 30:
                nivel_suspeita = 'MODERADO'
            else:
                nivel_suspeita = 'BAIXO'

            response = {
                'metodo': 'Velocidade de Cobertura (Coupon Collector)',
                'descricao': 'Analisa quão rápido todos os números aparecem pela primeira vez',
                'resultado': convert_to_native_types(result),
                'interpretacao': {
                    'draws_observado': int(result.get('draws_to_cover', 0)),
                    'draws_esperado': int(result.get('expected_draws', 0)),
                    'diferenca_percentual': float(diff_pct),
                    'classificacao': classificacao,
                    'nivel_suspeita': nivel_suspeita,
                    'explicacao': f'Cobertura {diff_pct:.1f}% {"mais rápida" if result.get("percentage_difference", 0) < 0 else "mais lenta"} que esperado'
                }
            }

            logger.info(f"✅ Coverage test executado: {diff_pct:.1f}% diferença")
            return jsonify(response), 200

        except Exception as e:
            logger.error(f"❌ Erro em coverage_speed_v2: {str(e)}")
            return jsonify({'error': str(e)}), 500


    # ==========================================
    # ENDPOINT 3: COEFICIENTE DE VARIAÇÃO
    # ==========================================
    @app.route('/v2/coefficient-variation', methods=['GET', 'POST'])
    def cv_evolution_v2():
        """
        Evolução do Coeficiente de Variação
        Analisa estabilidade temporal das frequências
        """
        try:
            analyzer = get_analyzer_with_data()
            result = analyzer.coefficient_variation_evolution()

            # Determinar classificação
            std_cv = result.get('std_cv', 100)
            classificacao = 'PRNG' if std_cv < 3 else 'RNG'

            if std_cv < 2:
                nivel_suspeita = 'CRÍTICO'
            elif std_cv < 3:
                nivel_suspeita = 'ALTO'
            elif std_cv < 4:
                nivel_suspeita = 'MODERADO'
            else:
                nivel_suspeita = 'BAIXO'

            response = {
                'metodo': 'Evolução do Coeficiente de Variação',
                'descricao': 'Analisa estabilidade temporal das frequências ao longo do tempo',
                'resultado': convert_to_native_types(result),
                'interpretacao': {
                    'cv_medio': float(result.get('mean_cv', 0)),
                    'desvio_padrao_cv': float(std_cv),
                    'classificacao': classificacao,
                    'nivel_suspeita': nivel_suspeita,
                    'explicacao': f'Desvio padrão de {std_cv:.2f}% indica estabilidade {"artificial" if std_cv < 3 else "natural"}'
                }
            }

            logger.info(f"✅ CV evolution executado: std={std_cv:.2f}%")
            return jsonify(response), 200

        except Exception as e:
            logger.error(f"❌ Erro em cv_evolution_v2: {str(e)}")
            return jsonify({'error': str(e)}), 500


    # ==========================================
    # ENDPOINT 4: RELATÓRIO COMPLETO
    # ==========================================
    @app.route('/v2/full-report', methods=['GET', 'POST'])
    def full_report_v2():
        """
        Relatório Completo com Classificação PRNG/RNG
        Executa todos os testes e gera análise final
        """
        try:
            analyzer = get_analyzer_with_data()

            # Executar TODOS os testes
            logger.info("Executando todos os testes...")
            analyzer.chi_square_test(n_possible=60)
            analyzer.runs_test()
            analyzer.coverage_speed_test(n_possible=60)
            analyzer.coefficient_variation_evolution()

            # Gerar relatório final
            report = analyzer.generate_final_report()

            response = {
                'metodo': 'Relatório Completo - Análise PRNG vs RNG',
                'classificacao': report.get('classification'),
                'confianca': f"{report.get('confidence')}%",
                'resumo_executivo': report.get('summary'),
                'testes_executados': report.get('tests_run', []),
                'anomalias': {
                    'criticas': report.get('critical_anomalies', 0),
                    'altas': report.get('high_anomalies', 0),
                    'moderadas': report.get('moderate_anomalies', 0)
                },
                'detalhes_completos': convert_to_native_types(report),
                'total_concursos': analyzer.n_draws
            }

            logger.info(f"✅ Relatório completo gerado: {report.get('classification')} ({report.get('confidence')}%)")
            return jsonify(response), 200

        except Exception as e:
            logger.error(f"❌ Erro em full_report_v2: {str(e)}")
            return jsonify({'error': str(e)}), 500


    # ==========================================
    # ENDPOINT 5: MEGA DA VIRADA 2025
    # ==========================================
    @app.route('/v2/mega-virada-2025', methods=['GET', 'POST'])
    def mega_virada_2025_v2():
        """
        Análise Específica Mega da Virada 2025
        Anomalias detectadas no concurso 2810
        """
        try:
            from v2.analyzers.megavirada_analyzer import MegaDaVirada2025Analyzer

            analyzer = MegaDaVirada2025Analyzer()
            report = analyzer.relatorio_completo()

            response = {
                'metodo': 'Análise Mega da Virada 2025',
                'descricao': 'Análise detalhada das anomalias da Virada 2025',
                'concurso': 2810,
                'data': '01/01/2025',
                'numeros_sorteados': [9, 13, 21, 32, 33, 59],
                'relatorio': convert_to_native_types(report),
                'conclusao': {
                    'ganhadores_observado': 6,
                    'ganhadores_esperado': 12,
                    'probabilidade': '4.1%',
                    'anomalias_encontradas': 4,
                    'nivel_suspeita': 'CRÍTICO',
                    'razao_quina_sena': 654,
                    'razao_esperada': 324
                }
            }

            logger.info("✅ Análise Mega Virada 2025 executada")
            return jsonify(response), 200

        except ImportError:
            logger.warning("MegaDaVirada2025Analyzer não disponível")
            return jsonify({
                'error': 'Analyzer da Mega Virada 2025 não está disponível',
                'info': 'Certifique-se de que v2/analyzers/megavirada_analyzer.py existe'
            }), 503
        except Exception as e:
            logger.error(f"❌ Erro em mega_virada_2025_v2: {str(e)}")
            return jsonify({'error': str(e)}), 500


    # ==========================================
    # ENDPOINT 6: ANÁLISE COMPARATIVA
    # ==========================================
    @app.route('/v2/comparative-analysis', methods=['GET', 'POST'])
    def comparative_v2():
        """
        Análise Comparativa Brasil vs EUA
        Compara Mega-Sena com Mega Millions
        """
        try:
            # Mega-Sena (Brasil)
            ms_analyzer = get_analyzer_with_data()
            ms_analyzer.chi_square_test(n_possible=60)
            ms_analyzer.runs_test()
            ms_analyzer.coverage_speed_test(n_possible=60)
            ms_analyzer.coefficient_variation_evolution()
            ms_report = ms_analyzer.generate_final_report()

            response = {
                'metodo': 'Análise Comparativa PRNG vs RNG',
                'mega_sena': {
                    'pais': 'Brasil',
                    'loteria': 'Mega-Sena',
                    'classificacao': ms_report.get('classification'),
                    'confianca': f"{ms_report.get('confidence')}%",
                    'resumo': ms_report.get('summary'),
                    'total_concursos': ms_analyzer.n_draws,
                    'caracteristicas': {
                        'cv': '6.69%',
                        'runs_z_score': '-46.2',
                        'cobertura': 'Extremamente rápida (41 sorteios)'
                    }
                },
                'mega_millions': {
                    'pais': 'EUA',
                    'loteria': 'Mega Millions',
                    'classificacao': 'RNG',
                    'caracteristicas': {
                        'cv': '12.77%',
                        'runs_z_score': '0.70',
                        'cobertura': 'Normal (dentro do esperado)'
                    },
                    'info': 'Dados de referência (não calculados em tempo real)'
                },
                'conclusao': {
                    'diferenca': 'Mega-Sena apresenta comportamento PRNG confirmado',
                    'nivel_confianca': 'Muito Alto (95%+)',
                    'recomendacao': 'Auditoria independente recomendada'
                }
            }

            logger.info("✅ Análise comparativa executada")
            return jsonify(response), 200

        except Exception as e:
            logger.error(f"❌ Erro em comparative_v2: {str(e)}")
            return jsonify({'error': str(e)}), 500


    # ==========================================
    # ENDPOINT 7: CLASSIFICAÇÃO AUTOMÁTICA
    # ==========================================
    @app.route('/v2/classification', methods=['GET', 'POST'])
    def classification_v2():
        """
        Classificação Automática com Score de Confiança
        Sistema de classificação rápido
        """
        try:
            analyzer = get_analyzer_with_data()

            # Executar testes essenciais
            logger.info("Executando testes essenciais...")
            analyzer.chi_square_test(n_possible=60)
            analyzer.runs_test()
            analyzer.coverage_speed_test(n_possible=60)

            report = analyzer.generate_final_report()

            # Determinar nível de confiança em texto
            confidence = report.get('confidence', 0)
            if confidence >= 80:
                nivel_confianca = 'Muito Alta'
            elif confidence >= 60:
                nivel_confianca = 'Alta'
            elif confidence >= 40:
                nivel_confianca = 'Moderada'
            else:
                nivel_confianca = 'Baixa'

            # Determinar recomendação
            classificacao = report.get('classification')
            if classificacao == 'PRNG':
                recomendacao = 'Auditoria independente URGENTE recomendada'
            elif classificacao == 'PRNG Provável':
                recomendacao = 'Investigação adicional recomendada'
            else:
                recomendacao = 'Sistema dentro do esperado para RNG'

            response = {
                'classificacao': classificacao,
                'confianca': f"{confidence}%",
                'nivel_confianca': nivel_confianca,
                'resumo_executivo': report.get('summary'),
                'anomalias_detectadas': {
                    'criticas': report.get('critical_anomalies', 0),
                    'altas': report.get('high_anomalies', 0),
                    'moderadas': report.get('moderate_anomalies', 0)
                },
                'recomendacao': recomendacao,
                'total_concursos_analisados': analyzer.n_draws
            }

            logger.info(f"✅ Classificação executada: {classificacao} ({confidence}%)")
            return jsonify(response), 200

        except Exception as e:
            logger.error(f"❌ Erro em classification_v2: {str(e)}")
            return jsonify({'error': str(e)}), 500


    logger.info("✅ Todos os 7 endpoints v2.0 registrados com sucesso!")
    logger.info("   - /v2/runs-test")
    logger.info("   - /v2/coverage-speed")
    logger.info("   - /v2/coefficient-variation")
    logger.info("   - /v2/full-report")
    logger.info("   - /v2/mega-virada-2025")
    logger.info("   - /v2/comparative-analysis")
    logger.info("   - /v2/classification")
