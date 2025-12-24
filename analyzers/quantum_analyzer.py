import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from collections import Counter

class QuantumAnalyzer:
    """
    Análise Quântica (Simulada) para predição de números da Mega-Sena
    Usa conceitos de superposição quântica e medição para gerar predições
    """

    def __init__(self, results_data):
        self.results_data = results_data
        self.numbers_sequence = self._extract_all_numbers()
        self.simulator = AerSimulator()

    def _extract_all_numbers(self):
        """Extrai todos os números sorteados"""
        all_numbers = []
        for result in self.results_data:
            draw = []
            for i in range(1, 7):
                key = f'bola{i}'
                if key in result:
                    draw.append(result[key])
            all_numbers.extend(draw)
        return all_numbers

    def create_quantum_circuit(self, n_qubits=6):
        """
        Cria circuito quântico para geração de números
        Usa superposição e entrelaçamento
        """
        qr = QuantumRegister(n_qubits, 'q')
        cr = ClassicalRegister(n_qubits, 'c')
        qc = QuantumCircuit(qr, cr)

        # Colocar todos os qubits em superposição
        for i in range(n_qubits):
            qc.h(i)

        # Aplicar rotações baseadas em dados históricos
        # Usar os últimos números como parâmetros de fase
        if len(self.numbers_sequence) >= n_qubits:
            last_numbers = self.numbers_sequence[-n_qubits:]
            for i, num in enumerate(last_numbers):
                # Normalizar número para ângulo (0 a 2π)
                angle = (num / 60) * 2 * np.pi
                qc.rz(angle, i)

        # Aplicar entrelaçamento
        for i in range(n_qubits - 1):
            qc.cx(i, i + 1)

        # Mais rotações baseadas em padrões de frequência
        frequency = Counter(self.numbers_sequence)
        most_common = [num for num, _ in frequency.most_common(n_qubits)]
        for i, num in enumerate(most_common):
            angle = (num / 60) * np.pi
            qc.ry(angle, i)

        # Aplicar mais entrelaçamento e rotações em vez de QFT
        # (QFT tem problemas de compatibilidade)
        for i in range(n_qubits):
            qc.rx(np.pi / 4, i)
            if i < n_qubits - 1:
                qc.cz(i, i + 1)

        # Medir
        qc.measure(qr, cr)

        return qc

    def run_quantum_circuit(self, circuit, shots=1000):
        """Executa o circuito quântico e retorna resultados"""
        job = self.simulator.run(circuit, shots=shots)
        result = job.result()
        counts = result.get_counts(circuit)
        return counts

    def predict_numbers(self, n=6):
        """
        Predição baseada em computação quântica simulada
        Executa múltiplos circuitos quânticos e agrega resultados
        """
        predictions_pool = []

        # Executar múltiplas simulações quânticas
        for iteration in range(10):
            qc = self.create_quantum_circuit(n_qubits=6)
            counts = self.run_quantum_circuit(qc, shots=100)

            # Converter resultados quânticos em números
            for bitstring, count in counts.items():
                # Converter bitstring para número (0-63)
                decimal = int(bitstring, 2)
                # Mapear para 1-60
                number = (decimal % 60) + 1

                predictions_pool.extend([number] * count)

        # Selecionar os 6 números mais frequentes nas medições quânticas
        frequency = Counter(predictions_pool)
        top_numbers = [num for num, _ in frequency.most_common(n * 2)]

        # Garantir 6 números únicos
        prediction = []
        for num in top_numbers:
            if num not in prediction:
                prediction.append(num)
            if len(prediction) == n:
                break

        # Se ainda faltam números, completar com números menos sorteados historicamente
        if len(prediction) < n:
            historical_freq = Counter(self.numbers_sequence)
            least_common = [num for num, _ in sorted(historical_freq.items(), key=lambda x: x[1])]
            for num in least_common:
                if num not in prediction:
                    prediction.append(num)
                if len(prediction) == n:
                    break

        return {
            'prediction': sorted(prediction[:n]),
            'method': 'Quantum Simulation (Qiskit)',
            'quantum_measurements': len(predictions_pool),
            'circuit_iterations': 10
        }

    def quantum_interference_prediction(self, n=6):
        """
        Método alternativo usando interferência quântica
        Cria padrões de interferência baseados em dados históricos
        """
        qc = QuantumCircuit(6, 6)

        # Estado inicial com superposição
        for i in range(6):
            qc.h(i)

        # Aplicar portas de fase baseadas em padrões históricos
        if len(self.results_data) > 0:
            last_draw = []
            for i in range(1, 7):
                key = f'bola{i}'
                if key in self.results_data[-1]:
                    last_draw.append(self.results_data[-1][key])

            for i, num in enumerate(last_draw):
                phase = (num / 60) * 2 * np.pi
                qc.p(phase, i)

        # Interferência entre qubits
        for i in range(5):
            qc.cx(i, i + 1)
            qc.h(i)

        qc.measure(range(6), range(6))

        # Executar múltiplas vezes
        counts = self.run_quantum_circuit(qc, shots=1024)

        # Converter resultados em números
        numbers_generated = []
        for bitstring, count in counts.items():
            for i, bit in enumerate(bitstring):
                if bit == '1':
                    # Mapear posição do qubit para número
                    num = ((i + 1) * int(bitstring, 2)) % 60 + 1
                    numbers_generated.extend([num] * count)

        # Selecionar os mais frequentes
        frequency = Counter(numbers_generated)
        prediction = [num for num, _ in frequency.most_common(n)]

        # Garantir 6 números únicos
        while len(set(prediction)) < n:
            additional = np.random.randint(1, 61)
            if additional not in prediction:
                prediction.append(additional)

        return {
            'prediction': sorted(list(set(prediction))[:n]),
            'method': 'Quantum Interference Pattern',
            'total_measurements': sum(counts.values())
        }

    def get_quantum_statistics(self):
        """Retorna estatísticas sobre o sistema quântico"""
        return {
            'total_historical_numbers': len(self.numbers_sequence),
            'total_draws': len(self.results_data),
            'simulator': 'Qiskit Aer',
            'quantum_backend': 'AerSimulator'
        }
