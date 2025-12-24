#!/usr/bin/env python3
"""
Script para explorar a estrutura do banco de dados
"""

import psycopg2
from config import Config

def explore_database():
    config = Config()

    print("="*60)
    print("EXPLORANDO BANCO DE DADOS")
    print("="*60)

    conn = psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        database=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD
    )

    cursor = conn.cursor()

    # Listar todos os schemas
    print("\n📁 SCHEMAS disponíveis:")
    cursor.execute("""
        SELECT schema_name
        FROM information_schema.schemata
        WHERE schema_name NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
        ORDER BY schema_name
    """)
    schemas = cursor.fetchall()
    for schema in schemas:
        print(f"   - {schema[0]}")

    # Listar todas as tabelas de todos os schemas
    print("\n📊 TABELAS em cada schema:")
    cursor.execute("""
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
        ORDER BY table_schema, table_name
    """)
    tables = cursor.fetchall()

    current_schema = None
    for schema, table in tables:
        if schema != current_schema:
            print(f"\n   Schema: {schema}")
            current_schema = schema
        print(f"      └─ {table}")

    # Tentar encontrar tabelas com nome parecido com 'mega' ou 'sena' ou 'resultado'
    print("\n🔍 Procurando tabelas relacionadas a Mega-Sena:")
    cursor.execute("""
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
        AND (
            LOWER(table_name) LIKE '%mega%'
            OR LOWER(table_name) LIKE '%sena%'
            OR LOWER(table_name) LIKE '%resultado%'
            OR LOWER(table_name) LIKE '%concurso%'
            OR LOWER(table_name) LIKE '%loteria%'
        )
    """)
    related_tables = cursor.fetchall()

    if related_tables:
        for schema, table in related_tables:
            print(f"   ✅ {schema}.{table}")

            # Mostrar estrutura da tabela
            cursor.execute(f"""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = %s AND table_name = %s
                ORDER BY ordinal_position
            """, (schema, table))
            columns = cursor.fetchall()

            print(f"      Colunas:")
            for col_name, col_type in columns:
                print(f"         - {col_name} ({col_type})")

            # Contar registros
            try:
                cursor.execute(f'SELECT COUNT(*) FROM "{schema}"."{table}"')
                count = cursor.fetchone()[0]
                print(f"      Total de registros: {count}")
            except:
                pass
    else:
        print("   ⚠️  Nenhuma tabela encontrada com nomes relacionados")

    cursor.close()
    conn.close()

    print("\n" + "="*60)

if __name__ == "__main__":
    explore_database()
