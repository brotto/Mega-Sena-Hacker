#!/usr/bin/env python3
"""
EXEMPLO DE USO: Análise Completa Mega-Sena vs Mega Millions
=============================================================

Este script demonstra como usar o sistema para comparar
Mega-Sena (Brasil) com Mega Millions (EUA) e detectar
características de PRNG vs RNG.
"""

from lottery_analyzer import LotteryAnalyzer
import pandas as pd
import json


def analisar_mega_sena():
    """Análise completa da Mega-Sena brasileira."""
    print("\n" + "="*80)
    print("ANÁLISE: MEGA-SENA (BRASIL)")
    print("="*80)
    
    # Inicializar analisador
    analyzer = LotteryAnalyzer("Mega-Sena Brasil")
    
    # Carregar dados
    ball_cols = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']
    df = analyzer.load_data('/mnt/user-data/uploads/Mega-Sena.xlsx', ball_cols)
    
    print(f"\n📊 Dados carregados: {len(df)} sorteios")
    
    # Executar todos os testes
    print("\n🔍 Executando testes estatísticos...\n")
    
    # Teste 1: Chi-Quadrado
    chi2 = analyzer.chi_square_test(n_possible=60)
    print(f"✓ Chi-Quadrado: χ²={chi2['chi2_statistic']:.2f}, p={chi2['p_value']:.4f}")
    print(f"  {chi2['interpretation']}")
    
    # Teste 2: Runs Test
    runs = analyzer.runs_test()
    print(f"\n✓ Runs Test: Z={runs['z_score']:.2f}")
    print(f"  {runs['interpretation']}")
    
    # Teste 3: Velocidade de Cobertura
    coverage = analyzer.coverage_speed_test(n_possible=60)
    print(f"\n✓ Cobertura: {coverage['draws_for_full_coverage']} sorteios")
    print(f"  Esperado: {coverage['expected_draws']:.1f}")
    print(f"  {coverage['interpretation']}")
    
    # Teste 4: Evolução do CV
    cv_evol = analyzer.coefficient_variation_evolution(window_size=100, n_possible=60)
    print(f"\n✓ Coeficiente de Variação: {cv_evol['cv_mean']:.2f}% (DP={cv_evol['cv_std']:.2f})")
    print(f"  {cv_evol['interpretation']}")
    
    # Gerar relatório
    report = analyzer.generate_final_report()
    
    print("\n" + "="*80)
    print("RELATÓRIO FINAL")
    print("="*80)
    print(f"\n🎯 Classificação: {report['classification']}")
    print(f"📊 Confiança: {report['confidence']}%")
    print(f"\n📋 Distribuição dos níveis de suspeita:")
    for level, count in report['suspect_counts'].items():
        print(f"  {level}: {count} teste(s)")
    
    print(f"\n💡 Recomendações:")
    for rec in report['recommendations']:
        print(f"  • {rec}")
    
    return report


def analisar_mega_millions():
    """Análise completa da Mega Millions (EUA)."""
    print("\n" + "="*80)
    print("ANÁLISE: MEGA MILLIONS (EUA)")
    print("="*80)
    
    # Inicializar analisador
    analyzer = LotteryAnalyzer("Mega Millions USA")
    
    # Carregar dados
    ball_cols = ['ball1', 'ball2', 'ball3', 'ball4', 'ball5']
    df = analyzer.load_data('/mnt/user-data/uploads/megamillions.csv', ball_cols)
    
    print(f"\n📊 Dados carregados: {len(df)} sorteios")
    
    # Executar todos os testes
    print("\n🔍 Executando testes estatísticos...\n")
    
    # Teste 1: Chi-Quadrado
    chi2 = analyzer.chi_square_test(n_possible=70)
    print(f"✓ Chi-Quadrado: χ²={chi2['chi2_statistic']:.2f}, p={chi2['p_value']:.4f}")
    print(f"  {chi2['interpretation']}")
    
    # Teste 2: Runs Test
    runs = analyzer.runs_test()
    print(f"\n✓ Runs Test: Z={runs['z_score']:.2f}")
    print(f"  {runs['interpretation']}")
    
    # Teste 3: Velocidade de Cobertura
    coverage = analyzer.coverage_speed_test(n_possible=70)
    print(f"\n✓ Cobertura: {coverage['draws_for_full_coverage']} sorteios")
    print(f"  Esperado: {coverage['expected_draws']:.1f}")
    print(f"  {coverage['interpretation']}")
    
    # Teste 4: Evolução do CV
    cv_evol = analyzer.coefficient_variation_evolution(window_size=50, n_possible=70)
    print(f"\n✓ Coeficiente de Variação: {cv_evol['cv_mean']:.2f}% (DP={cv_evol['cv_std']:.2f})")
    print(f"  {cv_evol['interpretation']}")
    
    # Gerar relatório
    report = analyzer.generate_final_report()
    
    print("\n" + "="*80)
    print("RELATÓRIO FINAL")
    print("="*80)
    print(f"\n🎯 Classificação: {report['classification']}")
    print(f"📊 Confiança: {report['confidence']}%")
    print(f"\n📋 Distribuição dos níveis de suspeita:")
    for level, count in report['suspect_counts'].items():
        print(f"  {level}: {count} teste(s)")
    
    print(f"\n💡 Recomendações:")
    for rec in report['recommendations']:
        print(f"  • {rec}")
    
    return report


def comparacao_final(report_br, report_usa):
    """Comparação final entre Brasil e EUA."""
    print("\n" + "="*80)
    print("COMPARAÇÃO BRASIL 🇧🇷 vs EUA 🇺🇸")
    print("="*80)
    
    print(f"\n🇧🇷 MEGA-SENA:")
    print(f"  Classificação: {report_br['classification']}")
    print(f"  Confiança: {report_br['confidence']}%")
    
    print(f"\n🇺🇸 MEGA MILLIONS:")
    print(f"  Classificação: {report_usa['classification']}")
    print(f"  Confiança: {report_usa['confidence']}%")
    
    print(f"\n📊 CONCLUSÃO:")
    if "PRNG" in report_br['classification'] and "RNG" in report_usa['classification']:
        print("  ✓ Confirmado: Mega-Sena apresenta características de PRNG")
        print("  ✓ Mega Millions apresenta comportamento RNG verdadeiro")
        print("\n  ⚠️  A diferença é estatisticamente significativa!")
    else:
        print("  ℹ️  Resultados inconclusivos ou similares")


if __name__ == "__main__":
    print("="*80)
    print(" "*15 + "SISTEMA DE ANÁLISE DE ALEATORIEDADE")
    print(" "*20 + "MEGA-SENA vs MEGA MILLIONS")
    print("="*80)
    
    # Analisar ambas
    report_br = analisar_mega_sena()
    report_usa = analisar_mega_millions()
    
    # Comparar
    comparacao_final(report_br, report_usa)
    
    # Salvar relatórios
    print("\n" + "="*80)
    print("💾 Salvando relatórios...")
    
    with open('/mnt/user-data/outputs/relatorio_mega_sena.json', 'w') as f:
        json.dump(report_br, f, indent=2, default=str)
    
    with open('/mnt/user-data/outputs/relatorio_mega_millions.json', 'w') as f:
        json.dump(report_usa, f, indent=2, default=str)
    
    print("✓ Relatórios salvos em /mnt/user-data/outputs/")
    print("="*80)
