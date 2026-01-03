"""
Mega Analyzer v2.0 - Sistema Avançado de Análise Estatística
Detecta comportamento PRNG vs RNG em loterias
"""

__version__ = "2.0.0"
__author__ = "Ale Brotto"

from .core.lottery_analyzer import LotteryAnalyzer

__all__ = ['LotteryAnalyzer']
