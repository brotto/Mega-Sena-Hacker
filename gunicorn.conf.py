"""
Configuração Gunicorn para Mega Analyzer v2.0
Aumenta timeout para suportar processamento de 1.3M+ registros
"""

# Bind
bind = "0.0.0.0:5555"

# Workers
workers = 2
worker_class = "sync"

# TIMEOUTS (CRÍTICO - Aumentado para processamento pesado!)
timeout = 300        # 5 minutos (300 segundos) - Padrão era 30s
keepalive = 5
graceful_timeout = 30

# Logging
loglevel = "info"
accesslog = "-"      # stdout
errorlog = "-"       # stderr
capture_output = True

# Performance
max_requests = 1000           # Restart worker após 1000 requests
max_requests_jitter = 50      # Variação aleatória para evitar restart simultâneo
preload_app = False           # Não preload para facilitar debug

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190
