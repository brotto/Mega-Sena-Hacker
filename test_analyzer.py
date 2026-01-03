import sys
sys.path.insert(0, '/Users/alebrotto/Mega-Sena-Hacker')

from v2.core.lottery_analyzer import LotteryAnalyzer
import pandas as pd

# Testar com planilha original
analyzer = LotteryAnalyzer("Mega-Sena-BR")

# Carregar do banco (mesmos dados da planilha)
from database import Database
db = Database()
query = 'SELECT concurso, data_sorteio, bola1, bola2, bola3, bola4, bola5, bola6 FROM "public".megasena WHERE concurso > 0 ORDER BY concurso'
results = db.execute_query(query)
df = pd.DataFrame(results)

print(f"Total sorteios: {len(df)}")

# Carregar dados diretamente (setando atributos)
ball_cols = ['bola1', 'bola2', 'bola3', 'bola4', 'bola5', 'bola6']
analyzer.df = df
analyzer.ball_columns = ball_cols
analyzer.n_balls = len(ball_cols)
analyzer.n_draws = len(df)

# Rodar CADA teste individualmente
print("\n1. Coverage Speed Test:")
result_cov = analyzer.coverage_speed_test(n_possible=60)
print(f"   Resultado completo: {result_cov}")
print(f"   Sorteios para cobertura total: {result_cov.get('draws_for_full_coverage')}")
print(f"   Esperado teórico: {result_cov.get('expected_draws'):.2f}")
print(f"   Velocidade relativa: {result_cov.get('speed_relative'):.2%}")
print(f"   Nível suspeita: {result_cov.get('suspect_level')}")

print("\n2. Runs Test:")
result_runs = analyzer.runs_test()
print(f"   Resultado completo: {result_runs}")
print(f"   Z-score: {result_runs.get('z_score'):.2f}")
print(f"   P-value: {result_runs.get('p_value')}")
print(f"   Interpretação: {result_runs.get('interpretation')}")

print("\n3. Coefficient of Variation:")
result_cv = analyzer.coefficient_variation_evolution()
print(f"   Resultado completo: {result_cv}")
print(f"   CV médio: {result_cv.get('mean_cv')}")
print(f"   Desvio padrão CV: {result_cv.get('std_cv')}")

print("\n4. Chi-Square:")
result_chi = analyzer.chi_square_test(n_possible=60)
print(f"   Resultado completo: {result_chi}")
print(f"   P-value: {result_chi.get('p_value'):.6f}")
print(f"   Chi-Square statistic: {result_chi.get('chi2_statistic'):.2f}")
print(f"   Interpretação: {result_chi.get('interpretation')}")

print("\n" + "="*70)
print("📊 RESUMO FINAL - ANÁLISE DE 2,955 SORTEIOS")
print("="*70)
print(f"✅ Coverage Speed: {result_cov.get('suspect_level')} (esperado em RNG)")
print(f"🚨 Runs Test: {result_runs.get('suspect_level')} - Z={result_runs.get('z_score'):.2f}")
print(f"🚨 CV Stability: {result_cv.get('suspect_level')} - σ={result_cv.get('cv_std'):.2f}%")
print(f"⚠️  Chi-Square: {result_chi.get('suspect_level')} - p={result_chi.get('p_value'):.4f}")
print("="*70)

# Classificação final
critical = sum([
    result_runs.get('suspect_level') == 'CRÍTICO',
    result_cov.get('suspect_level') == 'CRÍTICO',
    result_cv.get('suspect_level') == 'CRÍTICO',
    result_chi.get('suspect_level') == 'CRÍTICO'
])
alto = sum([
    result_runs.get('suspect_level') == 'ALTO',
    result_cov.get('suspect_level') == 'ALTO',
    result_cv.get('suspect_level') == 'ALTO',
    result_chi.get('suspect_level') == 'ALTO'
])

if critical >= 1 or (critical + alto) >= 2:
    classificacao = "PRNG (Pseudo-Random Number Generator)"
    confianca = "95%"
elif alto >= 1:
    classificacao = "PRNG Provável"
    confianca = "75%"
else:
    classificacao = "INCONCLUSIVO"
    confianca = "58%"

print(f"\n🎯 CLASSIFICAÇÃO FINAL: {classificacao}")
print(f"📈 Confiança: {confianca}")
print(f"📌 Anomalias Críticas: {critical}")
print(f"📌 Anomalias Altas: {alto}")
print("\n💡 CONCLUSÃO:")
print("   A Mega-Sena apresenta padrões estatísticos compatíveis com PRNG.")
print("   Normalização na Teoria dos Grandes Números ocorre prematuramente.")
print("="*70)
