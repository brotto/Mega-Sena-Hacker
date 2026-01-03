"""
PRNG Detector Adapter
Adapta o LotteryAnalyzer para trabalhar com dados do PostgreSQL
"""
import pandas as pd
import numpy as np
from typing import List, Dict
from analyzers.lottery_analyzer import LotteryAnalyzer


class PRNGDetector:
    """
    Wrapper para o LotteryAnalyzer que trabalha com dados do PostgreSQL.
    Detecta características de PRNG vs RNG verdadeiro.
    """

    def __init__(self, lottery_name: str = "Mega-Sena"):
        """
        Inicializa o detector PRNG.

        Args:
            lottery_name: Nome da loteria
        """
        self.analyzer = LotteryAnalyzer(lottery_name)
        self.lottery_name = lottery_name

    def load_from_database_results(self, results: List[Dict]) -> pd.DataFrame:
        """
        Carrega dados do formato do banco PostgreSQL.

        Args:
            results: Lista de dicionários com resultados do DB

        Returns:
            DataFrame formatado
        """
        # Converter para DataFrame
        data = []
        for result in results:
            row = {
                'Concurso': result.get('concurso'),
                'Data do Sorteio': result.get('data_sorteio') or result.get('data'),
                'Bola1': result.get('bola1'),
                'Bola2': result.get('bola2'),
                'Bola3': result.get('bola3'),
                'Bola4': result.get('bola4'),
                'Bola5': result.get('bola5'),
                'Bola6': result.get('bola6'),
            }
            data.append(row)

        df = pd.DataFrame(data)

        # Configurar o analyzer
        ball_columns = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']
        self.analyzer.df = df
        self.analyzer.ball_columns = ball_columns
        self.analyzer.n_balls = len(ball_columns)

        return df

    def analyze_complete(self, n_possible: int = 60) -> Dict:
        """
        Executa análise completa PRNG vs RNG.

        Args:
            n_possible: Quantidade de números possíveis (60 para Mega-Sena)

        Returns:
            Dicionário com todos os resultados
        """
        results = {}

        # Teste 1: Chi-Quadrado
        try:
            results['chi_square'] = self.analyzer.chi_square_test(n_possible)
        except Exception as e:
            results['chi_square'] = {'error': str(e)}

        # Teste 2: Runs Test
        try:
            results['runs_test'] = self.analyzer.runs_test()
        except Exception as e:
            results['runs_test'] = {'error': str(e)}

        # Teste 3: Velocidade de Cobertura
        try:
            results['coverage_speed'] = self.analyzer.coverage_speed_test(n_possible)
        except Exception as e:
            results['coverage_speed'] = {'error': str(e)}

        # Teste 4: Coeficiente de Variação
        try:
            results['coefficient_variation'] = self.analyzer.coefficient_variation_evolution(
                window_size=100, n_possible=n_possible
            )
        except Exception as e:
            results['coefficient_variation'] = {'error': str(e)}

        # Gerar relatório final
        try:
            final_report = self.analyzer.generate_final_report()
            results['final_report'] = final_report
        except Exception as e:
            results['final_report'] = {'error': str(e)}

        return results

    def quick_analysis(self, n_possible: int = 60) -> Dict:
        """
        Análise rápida com apenas os testes principais.

        Args:
            n_possible: Quantidade de números possíveis

        Returns:
            Resumo da análise
        """
        chi_result = self.analyzer.chi_square_test(n_possible)
        runs_result = self.analyzer.runs_test()

        # Determinar classificação simplificada
        is_prng = False
        confidence = 0

        # Chi-quadrado suspeito?
        if chi_result.get('p_value', 1) < 0.05 or chi_result.get('p_value', 0) > 0.95:
            is_prng = True
            confidence += 30

        # Runs test anômalo?
        z_score = abs(runs_result.get('z_score', 0))
        if z_score > 10:
            is_prng = True
            confidence += 50
        elif z_score > 5:
            confidence += 30

        classification = "PRNG (Pseudo-Aleatório)" if is_prng else "RNG (Verdadeiramente Aleatório)"

        return {
            'classification': classification,
            'confidence': min(confidence, 95),
            'chi_square_p_value': chi_result.get('p_value'),
            'runs_z_score': runs_result.get('z_score'),
            'total_draws_analyzed': len(self.analyzer.df),
            'suspect_indicators': {
                'chi_square': chi_result.get('suspect_level', 'normal'),
                'runs_test': runs_result.get('suspect_level', 'normal')
            }
        }

    def get_statistics_summary(self) -> Dict:
        """
        Retorna estatísticas básicas dos dados.

        Returns:
            Dicionário com estatísticas
        """
        all_numbers = self.analyzer.extract_all_numbers()

        from collections import Counter
        freq = Counter(all_numbers)

        return {
            'total_draws': len(self.analyzer.df),
            'total_numbers_drawn': len(all_numbers),
            'most_common': freq.most_common(10),
            'least_common': freq.most_common()[-10:],
            'mean_frequency': np.mean(list(freq.values())),
            'std_frequency': np.std(list(freq.values())),
            'cv_frequency': np.std(list(freq.values())) / np.mean(list(freq.values())) * 100
        }
