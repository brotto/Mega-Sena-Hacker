# ========================================================================
# PASSO 3: DEPLOY NA VPS
# ========================================================================

PASSO A PASSO:
--------------

1. PUSH PARA GITHUB (NO MAC)
   
   cd /Users/alebrotto/Mega-Sena-Hacker
   
   # Ver o que vai subir
   git status
   git diff
   
   # Push
   git push origin main

2. SSH NA VPS
   
   ssh usuario@31.97.172.217
   # Ou como você costuma acessar

3. NAVEGAR PARA O DIRETÓRIO DO PROJETO
   
   # Encontre onde está o projeto
   docker ps
   # Veja o nome do container: firecrawl_mega-sena-hacker
   
   # Entrar no container
   docker exec -it firecrawl_mega-sena-hacker bash
   
   # Você vai estar em /app

4. PULL DO GITHUB
   
   cd /app
   
   # Fazer pull
   git pull origin main
   
   # Ver o que foi atualizado
   git log -1
   ls -la v2/

5. INSTALAR NOVAS DEPENDÊNCIAS (SE HOUVER)
   
   pip install -r requirements.txt --upgrade

6. TESTAR IMPORTS (SEM REINICIAR)
   
   python3 -c "from v2.core.lottery_analyzer import LotteryAnalyzer; print('✅ v2 OK')"
   python3 -c "from app_v2_endpoints import register_v2_routes; print('✅ endpoints OK')"

7. REINICIAR SERVIDOR
   
   # OPÇÃO A: Se roda com gunicorn/supervisord
   # Sair do container primeiro (Ctrl+D)
   docker restart firecrawl_mega-sena-hacker
   
   # OPÇÃO B: Se roda direto
   # Dentro do container:
   pkill -f "python.*app.py"
   python3 app.py &
   
   # OPÇÃO C: Se tem script de restart
   ./restart.sh

8. VERIFICAR SE SUBIU
   
   # Testar health check
   curl http://localhost:5555/health
   
   # Testar endpoint antigo (garantir que não quebrou)
   curl http://localhost:5555/resultado-ultimo-sorteio
   
   # Testar endpoint novo
   curl http://localhost:5555/v2/classification

9. VER LOGS
   
   # Se tiver logs
   tail -f /app/*.log
   
   # Ou ver output do Docker
   docker logs firecrawl_mega-sena-hacker --tail=50

CHECKLIST DE SUCESSO:
--------------------

- [ ] git pull executado com sucesso
- [ ] Novos arquivos presentes (ls -la v2/)
- [ ] Imports funcionando (teste python3 -c)
- [ ] Servidor reiniciado
- [ ] /health retorna 200
- [ ] Endpoints antigos funcionando
- [ ] Endpoints novos funcionando (curl v2/...)
- [ ] Sem erros nos logs

SE ALGO DER ERRADO:
------------------

ROLLBACK RÁPIDO:

```bash
cd /app
git log --oneline -5
git reset --hard HEAD~1  # Voltar para commit anterior
docker restart firecrawl_mega-sena-hacker
```

TROUBLESHOOTING COMUM:
---------------------

**Erro: ModuleNotFoundError: No module named 'v2'**
```bash
# Verificar PYTHONPATH
cd /app
python3 -c "import sys; print(sys.path)"

# Se não tiver /app, adicionar ao início do app.py:
# import sys
# sys.path.insert(0, '/app')
```

**Erro: No module named 'openpyxl'**
```bash
pip install openpyxl seaborn
docker restart firecrawl_mega-sena-hacker
```

**Endpoints v2 não respondem**
```bash
# Ver se app_v2_endpoints.py foi carregado
grep "Endpoints v2.0 carregados" /var/log/...
# Ou
docker logs firecrawl_mega-sena-hacker | grep "v2.0"
```

PRÓXIMO PASSO:
-------------
Após deploy bem-sucedido, configurar n8n (ver N8N_SETUP.md)
