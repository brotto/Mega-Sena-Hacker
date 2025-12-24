#!/usr/bin/env python3
"""
Script de validação do ambiente
Verifica se tudo está configurado corretamente
"""

import sys
import os

def check_python_version():
    """Verifica versão do Python"""
    print("🐍 Verificando versão do Python...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"   ⚠️  Python {version.major}.{version.minor}.{version.micro}")
        print(f"   Recomendado: Python 3.11+")
        return False


def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    print("\n📦 Verificando dependências...")

    dependencies = {
        'flask': 'Flask',
        'psycopg2': 'psycopg2-binary',
        'numpy': 'NumPy',
        'scipy': 'SciPy',
        'matplotlib': 'Matplotlib',
        'qiskit': 'Qiskit',
        'pandas': 'Pandas',
        'dotenv': 'python-dotenv'
    }

    missing = []
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"   ✅ {name}")
        except ImportError:
            print(f"   ❌ {name} (não instalado)")
            missing.append(name)

    if missing:
        print(f"\n   ⚠️  Faltam {len(missing)} dependências")
        print(f"   Execute: pip install -r requirements.txt")
        return False
    else:
        print(f"   ✅ Todas as dependências instaladas!")
        return True


def check_env_file():
    """Verifica se o arquivo .env existe e tem as variáveis necessárias"""
    print("\n⚙️  Verificando arquivo .env...")

    env_path = os.path.join(os.path.dirname(__file__), '.env')

    if not os.path.exists(env_path):
        print("   ❌ Arquivo .env não encontrado")
        print("   Execute: cp .env.example .env")
        return False

    print("   ✅ Arquivo .env existe")

    # Verificar variáveis
    required_vars = ['DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_SCHEMA']
    missing_vars = []

    with open(env_path, 'r') as f:
        content = f.read()
        for var in required_vars:
            if var not in content:
                missing_vars.append(var)
                print(f"   ⚠️  {var} não encontrado")
            else:
                print(f"   ✅ {var}")

    if missing_vars:
        print(f"\n   ⚠️  Faltam {len(missing_vars)} variáveis no .env")
        return False
    else:
        print("   ✅ Todas as variáveis configuradas!")
        return True


def check_database_connection():
    """Testa conexão com o banco de dados"""
    print("\n🗄️  Testando conexão com banco de dados...")

    try:
        from database import Database
        from config import Config

        config = Config()
        print(f"   Host: {config.DB_HOST}")
        print(f"   Porta: {config.DB_PORT}")
        print(f"   Database: {config.DB_NAME}")
        print(f"   Schema: {config.DB_SCHEMA}")

        db = Database()
        db.connect()

        # Tentar query simples
        total = db.get_total_contests(schema=config.DB_SCHEMA)
        db.disconnect()

        print(f"   ✅ Conexão bem-sucedida!")
        print(f"   ✅ Total de concursos encontrados: {total}")
        return True

    except Exception as e:
        print(f"   ❌ Erro na conexão: {str(e)}")
        print("\n   Verifique:")
        print("   - Credenciais no arquivo .env")
        print("   - Conectividade com o servidor PostgreSQL")
        print("   - Nome do schema está correto")
        return False


def check_files():
    """Verifica se os arquivos principais existem"""
    print("\n📁 Verificando arquivos do projeto...")

    required_files = [
        'app.py',
        'database.py',
        'config.py',
        'requirements.txt',
        'Dockerfile',
        'analyzers/chi_square.py',
        'analyzers/lorenz_attractor.py',
        'analyzers/quantum_analyzer.py'
    ]

    missing = []
    for file in required_files:
        file_path = os.path.join(os.path.dirname(__file__), file)
        if os.path.exists(file_path):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file}")
            missing.append(file)

    if missing:
        print(f"\n   ⚠️  Faltam {len(missing)} arquivos")
        return False
    else:
        print("   ✅ Todos os arquivos principais presentes!")
        return True


def main():
    """Executa todas as verificações"""
    print("="*60)
    print("MEGA-SENA HACKER - VERIFICAÇÃO DE AMBIENTE")
    print("="*60)

    checks = [
        ('Python Version', check_python_version),
        ('Dependencies', check_dependencies),
        ('Environment File', check_env_file),
        ('Project Files', check_files),
        ('Database Connection', check_database_connection)
    ]

    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n   ❌ Erro inesperado: {str(e)}")
            results.append((name, False))

    # Resumo
    print("\n" + "="*60)
    print("RESUMO")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")

    print("\n" + "="*60)
    if passed == total:
        print("🎉 TUDO CERTO! Ambiente configurado corretamente.")
        print("\nPróximos passos:")
        print("1. Execute: python app.py")
        print("2. Acesse: http://localhost:5000")
        print("3. Teste: python test_local.py")
    else:
        print(f"⚠️  {total - passed} verificações falharam.")
        print("\nCorrija os problemas acima antes de continuar.")
        print("\nAjuda:")
        print("- Dependências: pip install -r requirements.txt")
        print("- Arquivo .env: cp .env.example .env")
        print("- Documentação: README.md")

    print("="*60)

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
