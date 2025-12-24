import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend sem GUI para evitar crashes
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import odeint
from io import BytesIO
import base64

class LorenzAttractorAnalyzer:
    """
    Análise baseada em Atratores Estranhos de Lorenz
    Usa a sequência temporal dos números sorteados como perturbações
    no sistema de Lorenz para identificar padrões caóticos
    """

    def __init__(self, results_data):
        self.results_data = results_data
        self.numbers_sequence = self._extract_temporal_sequence()

    def _extract_temporal_sequence(self):
        """Extrai sequência temporal de todos os números sorteados"""
        sequence = []
        for result in self.results_data:
            draw = []
            for i in range(1, 7):
                key = f'bola{i}'
                if key in result:
                    draw.append(result[key])
            sequence.append(draw)
        return sequence

    def lorenz_system(self, state, t, sigma=10, rho=28, beta=8/3):
        """
        Sistema de equações de Lorenz:
        dx/dt = sigma * (y - x)
        dy/dt = x * (rho - z) - y
        dz/dt = x * y - beta * z
        """
        x, y, z = state
        dx_dt = sigma * (y - x)
        dy_dt = x * (rho - z) - y
        dz_dt = x * y - beta * z
        return [dx_dt, dy_dt, dz_dt]

    def generate_lorenz_trajectory(self, initial_state, t_span, dt=0.01):
        """Gera trajetória do atrator de Lorenz"""
        t = np.arange(0, t_span, dt)
        trajectory = odeint(self.lorenz_system, initial_state, t)
        return trajectory

    def map_numbers_to_attractor(self):
        """
        Mapeia os números sorteados para estados do atrator de Lorenz
        Usa os números como sementes para estados iniciais
        """
        trajectories = []

        for draw in self.numbers_sequence:
            # Normalizar números para usar como estado inicial
            x0 = (draw[0] - 30) / 10  # Centralizar em torno de 0
            y0 = (draw[1] - 30) / 10
            z0 = (draw[2] - 30) / 10

            initial_state = [x0, y0, z0]

            # Gerar pequena trajetória
            trajectory = self.generate_lorenz_trajectory(initial_state, t_span=5, dt=0.05)
            trajectories.append(trajectory)

        return trajectories

    def generate_plot(self, save_path=None):
        """
        Gera visualização 3D do atrator de Lorenz com os dados da Mega-Sena
        """
        trajectories = self.map_numbers_to_attractor()

        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111, projection='3d')

        # Plotar apenas algumas trajetórias para não sobrecarregar
        sample_size = min(50, len(trajectories))
        for i, trajectory in enumerate(trajectories[-sample_size:]):
            ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2],
                   alpha=0.3, linewidth=0.5)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Atrator de Lorenz - Análise Mega-Sena')

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')

        # Retornar imagem em base64 para uso em API
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()

        return image_base64

    def predict_numbers(self, n=6):
        """
        Predição baseada no atrator de Lorenz:
        Usa o último sorteio como estado inicial e projeta a trajetória
        """
        if not self.numbers_sequence:
            return {'prediction': [], 'method': 'Lorenz Attractor', 'error': 'No data'}

        last_draw = self.numbers_sequence[-1]

        # Estado inicial baseado nos últimos números
        x0 = (last_draw[0] - 30) / 10
        y0 = (last_draw[1] - 30) / 10
        z0 = (last_draw[2] - 30) / 10

        # Gerar trajetória
        trajectory = self.generate_lorenz_trajectory([x0, y0, z0], t_span=10, dt=0.1)

        # Pegar pontos ao longo da trajetória e mapear de volta para números
        prediction_indices = np.linspace(20, len(trajectory)-1, n).astype(int)
        raw_predictions = []

        for idx in prediction_indices:
            point = trajectory[idx]
            # Mapear coordenadas de volta para números 1-60
            num = int((point[0] * 10 + 30) % 60) + 1
            if num < 1:
                num = 1
            if num > 60:
                num = 60
            raw_predictions.append(num)

        # Garantir números únicos
        prediction = []
        for num in raw_predictions:
            if num not in prediction:
                prediction.append(num)

        # Se não temos 6 números únicos, completar com números aleatórios
        available = [i for i in range(1, 61) if i not in prediction]
        while len(prediction) < n:
            num = np.random.choice(available)
            prediction.append(num)
            available.remove(num)

        return {
            'prediction': sorted(prediction[:n]),
            'method': 'Lorenz Attractor',
            'last_draw_used': last_draw
        }

    def analyze_chaos(self):
        """Análise de características caóticas da sequência"""
        trajectories = self.map_numbers_to_attractor()

        # Calcular estatísticas sobre as trajetórias
        all_points = np.vstack(trajectories)

        return {
            'total_draws_analyzed': len(self.numbers_sequence),
            'trajectory_mean': np.mean(all_points, axis=0).tolist(),
            'trajectory_std': np.std(all_points, axis=0).tolist(),
            'trajectory_min': np.min(all_points, axis=0).tolist(),
            'trajectory_max': np.max(all_points, axis=0).tolist()
        }
