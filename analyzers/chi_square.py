import numpy as np
from scipy.stats import chi2_contingency, chisquare
from collections import Counter

class ChiSquareAnalyzer:
    """
    Análise Qui-Quadrado para identificar padrões de frequência
    dos números sorteados na Mega-Sena
    """

    def __init__(self, results_data):
        """
        results_data: lista de dicionários com os resultados
        Espera-se que cada resultado tenha campos como bola1, bola2, ..., bola6
        """
        self.results_data = results_data
        self.all_numbers = self._extract_all_numbers()

    def _extract_all_numbers(self):
        """Extrai todos os números sorteados de todos os concursos"""
        all_numbers = []
        for result in self.results_data:
            for i in range(1, 7):
                key = f'bola{i}'
                if key in result:
                    all_numbers.append(result[key])
        return all_numbers

    def frequency_analysis(self):
        """Calcula a frequência de cada número (1-60)"""
        counter = Counter(self.all_numbers)
        # Garantir que todos os números de 1 a 60 estejam representados
        frequency = {i: counter.get(i, 0) for i in range(1, 61)}
        return frequency

    def chi_square_test(self):
        """
        Realiza o teste qui-quadrado para verificar se a distribuição
        dos números é uniforme (hipótese nula: todos os números têm mesma probabilidade)
        """
        frequency = self.frequency_analysis()
        observed = np.array([frequency[i] for i in range(1, 61)])

        # Frequência esperada (distribuição uniforme)
        expected_freq = np.mean(observed)
        expected = np.full(60, expected_freq)

        # Teste qui-quadrado
        chi2_stat, p_value = chisquare(observed, expected)

        return {
            'chi2_statistic': chi2_stat,
            'p_value': p_value,
            'observed_frequencies': frequency,
            'is_uniform': p_value > 0.05  # Se p > 0.05, não rejeitamos H0 (é uniforme)
        }

    def predict_numbers(self, n=6):
        """
        Predição baseada em qui-quadrado:
        Identifica números com menor frequência (assumindo que devem 'compensar')
        e números com maior frequência (hot numbers)
        Combina ambas as estratégias
        """
        frequency = self.frequency_analysis()

        # Ordenar números por frequência
        sorted_by_freq = sorted(frequency.items(), key=lambda x: x[1])

        # Estratégia: pegar os 3 números menos sorteados e 3 mais sorteados
        cold_numbers = [num for num, freq in sorted_by_freq[:30]]
        hot_numbers = [num for num, freq in sorted_by_freq[-30:]]

        # Selecionar aleatoriamente com peso
        # Números frios têm peso maior (compensação)
        cold_selected = np.random.choice(cold_numbers, size=3, replace=False)
        hot_selected = np.random.choice(hot_numbers, size=3, replace=False)

        prediction = sorted(list(cold_selected) + list(hot_selected))

        return {
            'prediction': prediction,
            'method': 'Chi-Square (Cold + Hot Numbers)',
            'cold_numbers_used': list(cold_selected),
            'hot_numbers_used': list(hot_selected)
        }

    def get_statistics(self):
        """Retorna estatísticas gerais da análise"""
        frequency = self.frequency_analysis()
        frequencies = list(frequency.values())

        return {
            'total_draws': len(self.results_data),
            'total_numbers_drawn': len(self.all_numbers),
            'most_frequent': max(frequency.items(), key=lambda x: x[1]),
            'least_frequent': min(frequency.items(), key=lambda x: x[1]),
            'mean_frequency': np.mean(frequencies),
            'std_frequency': np.std(frequencies),
            'median_frequency': np.median(frequencies)
        }
