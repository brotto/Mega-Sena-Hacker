# ========================================================================
# PASSO 2: INTEGRAR NOVOS ENDPOINTS AO app.py
# ========================================================================
# 
# EXECUTE APÓS TER CRIADO A ESTRUTURA v2/
# 
# ========================================================================

OBJETIVO:
---------
Adicionar os 7 novos endpoints v2.0 ao arquivo app.py existente.

MÉTODO: Edição Manual Simples
------------------------------

1. ABRIR app.py NO VSCODE
   
   code /Users/alebrotto/Mega-Sena-Hacker/app.py

2. LOCALIZAR O FINAL DO ARQUIVO
   
   Procure por:
   ```python
   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=config.PORT, debug=config.DEBUG)
   ```

3. ADICIONAR IMPORTS NO INÍCIO DO ARQUIVO
   
   Logo após os imports existentes (linha ~10), adicionar:
   
   ```python
   # === NOVOS IMPORTS v2.0 ===
   import sys
   sys.path.append('/app')  # Garantir que v2 está no path
   ```

4. ADICIONAR REGISTRO DOS ENDPOINTS v2
   
   ANTES da linha `if __name__ == '__main__':`, adicionar:
   
   ```python
   # ==========================================
   # REGISTRAR ENDPOINTS v2.0
   # ==========================================
   from app_v2_endpoints import register_v2_routes
   register_v2_routes(app)
   logger.info("✅ Endpoints v2.0 carregados")
   ```

ARQUIVO FINAL DEVE FICAR ASSIM:
-------------------------------

```python
from flask import Flask, request, jsonify, send_file
from database import Database
from analyzers.chi_square import ChiSquareAnalyzer
from analyzers.lorenz_attractor import LorenzAttractorAnalyzer
from analyzers.quantum_analyzer import QuantumAnalyzer
from config import Config
from utils import convert_to_native_types
import base64
from io import BytesIO
import logging

# === NOVOS IMPORTS v2.0 ===
import sys
sys.path.append('/app')

app = Flask(__name__)
config = Config()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ... (TODO o código existente dos endpoints atuais) ...

# ==========================================
# REGISTRAR ENDPOINTS v2.0
# ==========================================
from app_v2_endpoints import register_v2_routes
register_v2_routes(app)
logger.info("✅ Endpoints v2.0 carregados")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.PORT, debug=config.DEBUG)
```

5. SALVAR E COMMITAR
   
   git add app.py
   git commit -m "🔌 Integrate v2.0 endpoints into app.py"

ALTERNATIVA: Deixar Claude Code CLI Fazer
------------------------------------------

Ou peça ao Claude Code CLI:

```
Edite o arquivo app.py em /Users/alebrotto/Mega-Sena-Hacker:

1. Adicione após os imports existentes (linha ~10):
   ```python
   # === NOVOS IMPORTS v2.0 ===
   import sys
   sys.path.append('/app')
   ```

2. Adicione ANTES de `if __name__ == '__main__':`:
   ```python
   # ==========================================
   # REGISTRAR ENDPOINTS v2.0
   # ==========================================
   from app_v2_endpoints import register_v2_routes
   register_v2_routes(app)
   logger.info("✅ Endpoints v2.0 carregados")
   ```

3. Salve o arquivo
4. Mostre as linhas modificadas
```

TESTANDO LOCALMENTE (OPCIONAL):
-------------------------------

Se quiser testar antes de fazer deploy:

```bash
# No Mac:
cd /Users/alebrotto/Mega-Sena-Hacker

# Instalar deps (se não tiver)
pip3 install -r requirements.txt --break-system-packages

# NÃO VAI FUNCIONAR sem PostgreSQL, mas vai mostrar se imports estão OK:
python3 app.py

# Se aparecer:
# "✅ Endpoints v2.0 carregados"
# "Running on http://0.0.0.0:5000"
# 
# Significa que ESTÁ OK para fazer deploy!
```

PRÓXIMO PASSO:
--------------
Após integrar, ir para DEPLOY_VPS.md
