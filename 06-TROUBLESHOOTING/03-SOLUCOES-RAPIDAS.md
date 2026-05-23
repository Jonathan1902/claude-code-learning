# Soluções Rápidas

## Lookup Table: Problema → Solução

### Python - ImportError / ModuleNotFoundError

| Problema | Solução |
|---|---|
| `ModuleNotFoundError: requests` | `pip install requests` |
| `ImportError: cannot import name X` | `pip install --upgrade package` |
| Diferentes `requests` na venv e global | `which python` (verificar venv ativo) |
| `ModuleNotFoundError` no test | `PYTHONPATH=. pytest tests/` |

### Python - TypeError / AttributeError

| Problema | Solução |
|---|---|
| `TypeError: 'NoneType' object is not subscriptable` | Verifique se retorna None |
| `AttributeError: 'str' object has no attribute 'items'` | Verificar tipo (dict vs string?) |
| `TypeError: unsupported operand type(s) for +: 'str' and 'int'` | Converter tipo: `int(var)` |
| `KeyError: 'field'` | Verificar se chave existe em dict |

### Python - Database / ORM

| Problema | Solução |
|---|---|
| `ProgrammingError: relation "users" does not exist` | Rodar migrations: `python manage.py migrate` |
| `IntegrityError: duplicate key value` | Verificar unique constraints |
| `OperationalError: too many connections` | Pool de conexão cheio, aumentar `CONN_MAX_AGE` |
| `N+1 query problem` | Usar `select_related()` ou `prefetch_related()` |

### Django Específico

| Problema | Solução |
|---|---|
| `DisallowedHost` | Adicionar domínio em `ALLOWED_HOSTS` |
| `CSRF verification failed` | Adicionar `csrf_token` em template |
| Static files 404 | `python manage.py collectstatic` |
| Template not found | Verificar `TEMPLATES` em settings |

### JavaScript / Node

| Problema | Solução |
|---|---|
| `Cannot find module 'X'` | `npm install X` |
| `Port 3000 already in use` | `lsof -i :3000` (kill processo) |
| `React Hook called in wrong context` | Mover hook para dentro de componente |
| `CORS error` | Adicionar header em servidor: `Access-Control-Allow-Origin` |

### Git / Version Control

| Problema | Solução |
|---|---|
| `fatal: not a git repository` | `git init` ou clone repo |
| `Your branch is ahead of 'origin/main'` | `git push` para sincronizar |
| `merge conflict` | Editar arquivo, resolver, `git add .`, `git commit` |
| `detached HEAD` | `git checkout main` |

### Docker

| Problema | Solução |
|---|---|
| `port already in use` | `docker ps` (ver containers), `docker stop <id>` |
| `image not found` | `docker build -t myapp .` |
| `permission denied` | `sudo docker` ou adicionar user ao grupo docker |
| `Out of disk space` | `docker prune` (limpeza) |

### Database / SQL

| Problema | Solução |
|---|---|
| `Connection refused (5432)` | Verificar se PostgreSQL rodando: `psql --version` |
| `authentication failed` | Checar credentials em `DATABASE_URL` |
| `syntax error` | Rodar SQL em editor com syntax highlighting |
| `query timeout` | Adicionar index: `CREATE INDEX idx_name ON table(field)` |

### Environment / Setup

| Problema | Solução |
|---|---|
| `command not found: python3` | Install Python 3 (apt, brew, etc) |
| `pip: command not found` | `python -m pip` ou instalar pip |
| `.env not loading` | Verificar formato: `KEY=VALUE` (sem espaços) |
| `Permission denied: file.py` | `chmod +x file.py` |

---

## Quick Fixes (Um-liner)

```bash
# Python
python -m pip install -U pip                    # Atualizar pip
pip list | grep requests                        # Ver se pacote instalado
python -m pytest tests/ -v                      # Rodar tests verboso
python -m pdb script.py                         # Debug com pdb

# Django
python manage.py makemigrations && \
  python manage.py migrate                      # Migrations
python manage.py createsuperuser                # Admin user
python manage.py shell_plus                     # Shell interativo (se django-extensions)

# Git
git log --oneline -n 10                         # Últimas 10 commits
git diff filename                               # Ver mudanças
git status                                      # Estado current
git reset --hard HEAD~1                         # Desfazer último commit (cuidado!)

# Docker
docker ps -a                                    # Ver containers
docker logs <container>                         # Ver logs
docker exec -it <container> bash               # Entrar em container
docker build -t myapp:1.0 .                    # Build imagem

# Node/npm
npm install && npm start                        # Install + run
npm list --depth=0                              # Ver versão de pacotes top-level
npm update                                      # Atualizar tudo
npx create-react-app myapp                     # Criar novo React app

# PostgreSQL
psql -U user -d database                        # Conectar
\dt                                             # Listar tabelas
\d tablename                                    # Ver schema
psql -f backup.sql                              # Restaurar backup

# Linux/Mac
which python                                    # Achar executável
source venv/bin/activate                       # Ativar venv
deactivate                                      # Desativar venv
lsof -i :PORT                                   # Qual processo usa PORT
kill -9 PID                                     # Matar processo
```

---

## Conhecimento Compartilhado

### Venv Setup (Comum)
```bash
# Create
python -m venv venv

# Activate
source venv/bin/activate          # Linux/Mac
venv\Scripts\activate              # Windows

# Install
pip install -r requirements.txt
```

### Django Setup (Comum)
```bash
# Criar projeto
django-admin startproject mysite

# Criar app
python manage.py startapp myapp

# Migrations
python manage.py makemigrations
python manage.py migrate

# Rodar
python manage.py runserver
```

### FastAPI Setup (Comum)
```bash
# Install
pip install fastapi uvicorn

# main.py
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Rodar
uvicorn main:app --reload
```

### React Setup (Comum)
```bash
# Create
npx create-react-app myapp

# Run
cd myapp
npm start

# Build
npm run build
```

---

## Recursos Úteis

| Recurso | Função |
|---|---|
| StackOverflow | Buscar erro (99% das vezes já foi respondido) |
| Official Docs | Python.org, Django docs, React docs |
| ChatGPT / Claude | Explicar erro, brainstorm solução |
| Your Team | Alguém já viu isso antes? |
| Google | "python {error}" ou "django {error}" |

---

## Última Opção: Escalate

Se tudo falhar:
```
Seu relato para Claude:
1. Stack trace completo
2. Código relevante (20-50 linhas)
3. O que já tentou
4. Ambiente (Python 3.11, Django 4.2, PostgreSQL 14)
5. Comando exato que rodou

Exemplo:
```
Erro: TypeError: unsupported operand type(s) for -: 'str' and 'int'

Código (payment.py line 42):
result = tax_amount - discount_percentage

Input: tax_amount="$50", discount_percentage=10
Esperado: 50 - 10 = 40
Recebido: TypeError

Tentei:
- Converter para float: float(tax_amount) → ValueError
- Remover "$": tax_amount.replace("$", "") → funciona

Mas acho estranho. Qual é a root cause?
```

Claude conseguirá ajudar!

---

**Voltar**: [Erros Comuns](01-ERROS-COMUNS.md)
