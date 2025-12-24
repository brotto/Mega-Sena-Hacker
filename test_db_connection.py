#!/usr/bin/env python3
"""
Script para testar conexão com o banco de dados PostgreSQL
"""

import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(__file__))

try:
    import psycopg2
    print("✅ psycopg2 instalado")
except ImportError:
    print("❌ psycopg2 NÃO instalado")
    print("Execute: pip install psycopg2-binary")
    sys.exit(1)

from config import Config

def test_connection():
    """Testa conexão com o banco de dados"""
    print("\n" + "="*60)
    print("TESTE DE CONEXÃO - BANCO DE DADOS POSTGRESQL")
    print("="*60)

    config = Config()

    print("\n📋 Configurações:")
    print(f"   Host: {config.DB_HOST}")
    print(f"   Porta: {config.DB_PORT}")
    print(f"   Database: {config.DB_NAME}")
    print(f"   Usuário: {config.DB_USER}")
    print(f"   Schema: {config.DB_SCHEMA}")
    print(f"   Senha: {'*' * len(config.DB_PASSWORD)}")

    print("\n🔌 Tentando conectar...")

    try:
        # Tentar conexão
        conn = psycopg2.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            connect_timeout=10
        )

        print("   ✅ Conexão estabelecida com sucesso!")

        # Testar query
        cursor = conn.cursor()

        # Query para listar tabelas no schema
        query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = %s
        """

        cursor.execute(query, (config.DB_SCHEMA,))
        tables = cursor.fetchall()

        print(f"\n📊 Tabelas encontradas no schema '{config.DB_SCHEMA}':")
        if tables:
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print(f"   ⚠️  Nenhuma tabela encontrada no schema '{config.DB_SCHEMA}'")
            print("   Verifique se o nome do schema está correto")

        # Tentar contar registros na tabela resultados
        try:
            count_query = f'SELECT COUNT(*) FROM "{config.DB_SCHEMA}".resultados'
            cursor.execute(count_query)
            count = cursor.fetchone()[0]
            print(f"\n🎰 Total de concursos na tabela 'resultados': {count}")

            # Pegar um exemplo
            example_query = f'SELECT * FROM "{config.DB_SCHEMA}".resultados ORDER BY concurso DESC LIMIT 1'
            cursor.execute(example_query)

            columns = [desc[0] for desc in cursor.description]
            row = cursor.fetchone()

            print(f"\n📝 Último concurso registrado:")
            for col, val in zip(columns, row):
                print(f"   {col}: {val}")

        except Exception as e:
            print(f"\n⚠️  Erro ao acessar tabela 'resultados': {str(e)}")
            print("   Verifique se a tabela existe no schema correto")

        cursor.close()
        conn.close()

        print("\n" + "="*60)
        print("✅ TESTE CONCLUÍDO COM SUCESSO!")
        print("="*60)
        return True

    except psycopg2.OperationalError as e:
        print(f"\n❌ ERRO DE CONEXÃO:")
        print(f"   {str(e)}")
        print("\n💡 Possíveis soluções:")
        print("   1. Verifique se o host está correto (deve ser externo/público)")
        print("   2. Verifique se a porta está exposta e acessível")
        print("   3. Verifique as credenciais (usuário/senha)")
        print("   4. Verifique se há firewall bloqueando a porta")
        print("   5. Verifique se o banco de dados está rodando")
        print("\n📝 Configuração atual no .env:")
        print(f"   DB_HOST={config.DB_HOST}")
        print(f"   DB_PORT={config.DB_PORT}")
        print("="*60)
        return False

    except Exception as e:
        print(f"\n❌ ERRO INESPERADO:")
        print(f"   {str(e)}")
        print("="*60)
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
