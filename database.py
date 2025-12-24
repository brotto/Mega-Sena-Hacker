import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

class Database:
    def __init__(self):
        self.config = Config()
        self.connection = None

    def connect(self):
        """Estabelece conexão com o banco de dados PostgreSQL"""
        try:
            self.connection = psycopg2.connect(
                host=self.config.DB_HOST,
                port=self.config.DB_PORT,
                database=self.config.DB_NAME,
                user=self.config.DB_USER,
                password=self.config.DB_PASSWORD
            )
            return self.connection
        except Exception as e:
            raise Exception(f"Erro ao conectar ao banco de dados: {str(e)}")

    def disconnect(self):
        """Fecha a conexão com o banco de dados"""
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params=None):
        """Executa uma query e retorna os resultados"""
        try:
            if not self.connection:
                self.connect()

            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            raise Exception(f"Erro ao executar query: {str(e)}")

    def get_all_results(self, schema='public', table='megasena', limit=None):
        """Obtém todos os resultados da Mega-Sena"""
        query = f'SELECT * FROM "{schema}".{table} ORDER BY concurso ASC'
        if limit:
            query += f' LIMIT {limit}'
        return self.execute_query(query)

    def get_last_result(self, schema='public', table='megasena'):
        """Obtém o último resultado da Mega-Sena"""
        query = f'SELECT * FROM "{schema}".{table} ORDER BY concurso DESC LIMIT 1'
        results = self.execute_query(query)
        return results[0] if results else None

    def get_results_until(self, concurso_number, schema='public', table='megasena'):
        """Obtém resultados até um determinado concurso (para testes cegos)"""
        query = f'SELECT * FROM "{schema}".{table} WHERE concurso <= %s ORDER BY concurso ASC'
        return self.execute_query(query, (concurso_number,))

    def get_total_contests(self, schema='public', table='megasena'):
        """Retorna o número total de concursos"""
        query = f'SELECT COUNT(*) as total FROM "{schema}".{table}'
        result = self.execute_query(query)
        return result[0]['total'] if result else 0
