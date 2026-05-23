# Laboratório Prático — Comandos e Sintaxe de Prompt

Bem-vindo ao laboratório de prompts! Neste guia você vai **escrever, comparar e combinar** prompts reais — experimentando na prática os 4 componentes essenciais, os 10 padrões avançados e técnicas de debugging, segurança e performance.

## Pré-requisitos

- Claude Code instalado e configurado
- Diretório de trabalho preparado para criar arquivos de teste
- Tempo disponível: ~50 minutos (trilha completa) ou ~15 minutos (trilha iniciante)

---

## Sumário de Exercícios

| # | Conceito | Exercício | Dificuldade | Tempo |
|---|----------|-----------|-------------|-------|
| 1.1 | Componentes essenciais | Prompt Ruim vs Bom: O Exercício do Logging | Fácil | ~4 min |
| 1.2 | Template de 4 componentes | Template em Ação: API FastAPI do Zero | Médio | ~5 min |
| 1.3 | Anti-padrões | Identificando e Corrigindo Anti-Padrões | Médio | ~5 min |
| 2.1 | Chain-of-Thought | Chain-of-Thought: Raciocínio em Função Bugada | Fácil | ~4 min |
| 2.2 | Role Prompting | Role Prompting: Security Review de Endpoint | Médio | ~5 min |
| 2.3 | Structured Output | Structured Output: Análise de Qualidade de Código | Médio | ~4 min |
| 2.4 | Meta-Prompting | Meta-Prompting: Claude Como Coach de Prompts | Difícil | ~6 min |
| 3.1 | Debugging completo | Debugging com Contexto Completo | Fácil | ~4 min |
| 3.2 | Few-Shot | Few-Shot para Convenção de Nomenclatura | Médio | ~5 min |
| 3.3 | Combinação de padrões | Combinando Role + CoT + Structured Output | Difícil | ~7 min |

---

## Trilhas de Aprendizado

### 🚀 Trilha Iniciante (~15 min)

Comece com os exercícios mais diretos para entender os padrões fundamentais:

- **1.1** — Experienciar a diferença entre prompt vago e prompt estruturado
- **2.1** — Aprender por que CoT revela o raciocínio escondido
- **3.1** — Aplicar o template completo de debugging
- **3.3** — Ver a sinergia de múltiplos padrões juntos

### 📚 Trilha Completa (~49 min)

Trabalhe sequencialmente através de todas as 10 exercícios para dominar prompting profundo:

1.1 → 1.2 → 1.3 → 2.1 → 2.2 → 2.3 → 2.4 → 3.1 → 3.2 → 3.3

---

## Seção 1 — Fundamentos do Prompt

---

### 1.1 — Prompt Ruim vs Prompt Bom: O Exercício do Logging

**Arquivo de Referência**: `01-PROMPT-BASICO.md` (Seção "Erros Comuns" + "Exercício 1")  
**Conceito**: A diferença concreta entre um prompt vago e um prompt com os 4 componentes essenciais.  
**Dificuldade**: Fácil | **Tempo**: ~4 min

Neste exercício você vai experimentar como cada componente do template elimina uma adivinação que Claude teria que fazer.

#### Setup

Crie um arquivo `logger_service.py`:

```bash
cat > logger_service.py << 'EOF'
import time

def process_payment(amount, user_id):
    result = amount * 0.97  # taxa de 3%
    time.sleep(0.1)         # simula chamada externa
    return result

def send_notification(user_id, message):
    # TODO: integrar com serviço de email
    pass

def generate_report(transactions):
    total = sum(t['amount'] for t in transactions)
    return {"total": total, "count": len(transactions)}
EOF
```

#### Passo 1 — Prompt Vago

Execute este prompt vago para ver como Claude adivinha:

```bash
claude "Adicione logging neste arquivo"
```

**Saída Esperada** (simulada):
```
Aqui está o arquivo com logging adicionado:

import logging
import time

logging.basicConfig(level=logging.DEBUG)

def process_payment(amount, user_id):
    logging.debug("Processando pagamento")
    result = amount * 0.97
    time.sleep(0.1)
    return result
```

**O que observar**: Claude adicionou logging genérico — nível DEBUG em todos os lugares, sem contexto de negócio, sem estrutura, sem dados importantes (user_id, amount) nas mensagens.

#### Passo 2 — Prompt com os 4 Componentes

Agora execute o mesmo objetivo com cada componente especificado:

```bash
claude "Contexto: serviço financeiro Python 3.11 em produção, usando o módulo logging padrão.

Tarefa: Adicione logging estruturado ao arquivo logger_service.py.

Restrições:
- Use logging.getLogger(__name__) (não basicConfig)
- Nível INFO para início/fim de operação, WARNING para taxas acima de 5%, ERROR para exceções
- Inclua user_id e amount em cada mensagem de log

Formato esperado: código pronto para produção, sem prints, mantenha a lógica existente intacta."
```

**Saída Esperada** (simulada):
```python
import logging
import time

logger = logging.getLogger(__name__)

def process_payment(amount, user_id):
    logger.info("Iniciando processamento de pagamento | user_id=%s | amount=%.2f", user_id, amount)
    try:
        result = amount * 0.97
        if result > 0:
            taxa = (amount - result) / amount * 100
            if taxa > 5:
                logger.warning("Taxa acima de 5%% | user_id=%s | taxa=%.1f%%", user_id, taxa)
        time.sleep(0.1)
        logger.info("Pagamento processado com sucesso | user_id=%s | result=%.2f", user_id, result)
        return result
    except Exception as e:
        logger.error("Erro ao processar pagamento | user_id=%s | amount=%.2f | erro=%s", user_id, amount, str(e))
        raise
```

**O que observar**: Cada componente do template eliminou uma adivinação. Sem o Contexto, Claude teria usado `basicConfig`. Sem a Tarefa específica, teria adicionado logs em qualquer lugar. Sem as Restrições, não saberia que níveis usar. Sem o Formato, teria misturado prints com logging.

#### Conceito Reforçado

Veja como cada componente eliminou uma adivinação:

| Componente | Eliminou... | Resultado |
|---|---|---|
| Contexto: "serviço financeiro produção" | Qual framework? Qual nível de logging? | Escolha: `getLogger(__name__)` em vez de `basicConfig` |
| Tarefa: "logging estruturado" | Onde adicionar logs? Qual granularidade? | Cobertura exata: início/fim de operação + avisos |
| Restrições | Qual nível INFO vs DEBUG? Que dados incluir? | Especificação: INFO para início/fim, WARNING para taxa, user_id + amount em cada mensagem |
| Formato | Estilo de código? Comentários? Type hints? | Qualidade: production-ready, sem prints, lógica preservada |

---

### 1.2 — Template em Ação: API FastAPI do Zero

**Arquivo de Referência**: `01-PROMPT-BASICO.md` (Seção "Estrutura Template" + "Exercício 2")  
**Conceito**: Aplicar o template de 4 componentes para gerar um endpoint FastAPI de qualidade production.  
**Dificuldade**: Médio | **Tempo**: ~5 min

Neste exercício você vai preencher o template para descrever um novo endpoint REST, vendo como cada seção resulta em um artefato de código específico.

#### Setup

Crie um arquivo `models.py` que será referenciado:

```bash
cat > models.py << 'EOF'
from pydantic import BaseModel
from typing import Optional

class Produto(BaseModel):
    id: int
    nome: str
    preco: float
    estoque: int
    categoria: Optional[str] = None
EOF
```

#### Comando

Agora execute um prompt que preenche cada seção do template:

```bash
claude "Contexto: Projeto FastAPI com Python 3.11, Pydantic v2, banco PostgreSQL. O arquivo models.py já define o model Produto (id, nome, preco, estoque, categoria).

Tarefa: Crie um endpoint GET /produtos/{produto_id} que busca um produto por ID.

Restrições:
- Retornar 404 com mensagem clara se não encontrado
- Usar async/await obrigatoriamente
- Type hints em parâmetros e retorno
- Sem dependência de banco real por enquanto (retornar dados mockados)

Formato esperado: Código pronto para produção com docstring Google-style, type hints completos e tratamento de erro correto."
```

#### Saída Esperada

```python
from fastapi import FastAPI, HTTPException
from models import Produto

app = FastAPI()

# Mock database — substitua pela conexão real ao PostgreSQL
_produtos_mock: dict[int, Produto] = {
    1: Produto(id=1, nome="Notebook", preco=3500.0, estoque=10, categoria="Eletrônicos"),
    2: Produto(id=2, nome="Mouse", preco=89.90, estoque=50, categoria="Periféricos"),
}

@app.get("/produtos/{produto_id}", response_model=Produto)
async def obter_produto(produto_id: int) -> Produto:
    """Busca um produto pelo ID.

    Args:
        produto_id: ID único do produto a buscar.

    Returns:
        Dados completos do produto encontrado.

    Raises:
        HTTPException: 404 se produto não encontrado.
    """
    produto = _produtos_mock.get(produto_id)
    if not produto:
        raise HTTPException(
            status_code=404,
            detail=f"Produto com ID {produto_id} não encontrado"
        )
    return produto
```

**O que observar**: Cada restrição gerou um artefato visível:
- `async def` vem diretamente da restrição "async/await obrigatoriamente"
- `HTTPException(404)` vem de "Retornar 404"
- Docstring Google-style vem de "Formato: Google-style docstring"
- O mock dict com type hint vem de "sem dependência real" (mock necessário)

#### Conceito Reforçado

Mapeamento direto entre template e código gerado:

| Seção do Template | O que Gerou | Onde Aparece no Código |
|---|---|---|
| Contexto: FastAPI, Pydantic v2 | Import e modelo corretos | `from fastapi import FastAPI` + `response_model=Produto` |
| Tarefa: GET /produtos/{id} | Route, parâmetro, retorno | `@app.get("/produtos/{produto_id}", response_model=Produto)` |
| Restrição: async | Função assíncrona | `async def obter_produto` |
| Restrição: 404 message | Exception handling | `raise HTTPException(status_code=404, detail=...)` |
| Formato: Google-style docstring | Documentação | Triple-quoted docstring com Args, Returns, Raises |

---

### 1.3 — Identificando e Corrigindo Anti-Padrões

**Arquivo de Referência**: `01-PROMPT-BASICO.md` (Seção "Erros Comuns" — 4 anti-padrões)  
**Conceito**: Reconhecer os 4 anti-padrões na prática e usar Meta-Prompting para corrigi-los.  
**Dificuldade**: Médio | **Tempo**: ~5 min

Neste exercício você vai experienciar como os 4 anti-padrões aparecem na prática, depois usar Claude para diagnosticá-los e corrigi-los.

#### Passo 1 — Observar o Prompt Problemático

Execute este prompt que contém múltiplos anti-padrões:

```bash
claude "Refatore e otimize o projeto todo e adicione testes e docstrings e veja se tem problemas de segurança também"
```

**Saída Esperada** (simulada):
```
Preciso de mais informações:
- Qual arquivo você quer refatorar?
- Qual é o objetivo da otimização (velocidade, memória, legibilidade)?
- Você quer testes unitários ou integração?
- Em qual contexto de segurança (web, CLI, dados sensíveis)?
- Qual é o escopo do projeto?
```

**O que observar**: Claude pede clarificações porque o prompt contém todos os 4 anti-padrões simultaneamente.

#### Passo 2 — Usar Claude Para Diagnosticar Anti-Padrões

Use Meta-Prompting para Claude diagnosticar e corrigir:

```bash
claude "Avalie o seguinte prompt original e identifique quais dos 4 anti-padrões ele contém:

'Refatore e otimize o projeto todo e adicione testes e docstrings e veja se tem problemas de segurança também'

Os 4 anti-padrões de prompting são:
1. Muito vago — não especifica qual arquivo, qual aspecto, qual objetivo
2. Assumir conhecimento — presume que Claude sabe qual projeto você está falando
3. Pedir múltiplas coisas ao mesmo tempo — refactor, optimize, tests, docs, security
4. Contexto irrelevante — sem arquivo, escopo ou restrições

Para cada anti-padrão encontrado:
- Explique por que existe neste prompt
- Proponha a versão corrigida específica

Formato: liste os anti-padrões e, depois, forneça 5 prompts corrigidos (um para cada tarefa)."
```

**Saída Esperada** (simulada):
```
## Anti-Padrões Encontrados:

### 1. Muito vago
**Por quê**: "projeto todo" não especifica qual arquivo, qual módulo
**Correção**: "Refatore o arquivo auth.py para extrair a lógica de JWT em uma classe separada"

### 2. Assumir conhecimento
**Por quê**: Nenhum arquivo foi fornecido; Claude não sabe qual é "o projeto"
**Correção**: Fornecer o arquivo ou contexto: "Aqui está o arquivo que precisa refatoração: [arquivo]"

### 3. Múltiplas coisas ao mesmo tempo
**Por quê**: Pede refactor + optimize + tests + docs + security em um único prompt
**Correção**: Quebrar em 5 tarefas:
  1. "Refatore o arquivo X para extrair..."
  2. "Otimize a função Y para reduzir de O(n²) para..."
  3. "Crie testes pytest para cobrir os casos..."
  4. "Adicione docstrings Google-style..."
  5. "Revise o código do endpoint /login para vulnerabilidades OWASP..."

### 4. Contexto irrelevante (neste caso: falta de contexto)
**Por quê**: Sem escopo, sem restrições, sem formato esperado
**Correção**: Incluir: "Python 3.11, Django 4.2, base de testes existente, resultado final pronto para merge"
```

**O que observar**: Claude identificou todos os 4 anti-padrões com exemplos específicos da correção. Em prompts reais, geralmente aparecem 2-3 anti-padrões combinados, amplificando o problema.

#### Conceito Reforçado

Como Claude detecta cada anti-padrão:

| Anti-Padrão | Detecção | Exemplo |
|---|---|---|
| Muito vago | Falta de especificidade (qual, qual, onde, qual) | "projeto todo" = qual módulo? qual arquivo? |
| Assumir conhecimento | Nenhum contexto fornecido | Sem arquivo, sem output de erro, sem versão |
| Múltiplas coisas | "e" conectando 5+ tarefas diferentes | refactor E otimize E teste E documente E revise |
| Contexto irrelevante | Sem restrições, sem scope, sem formato | Sem Python version, sem DB, sem resultado esperado |

---

## Seção 2 — Padrões Avançados

---

### 2.1 — Chain-of-Thought: Raciocínio em Função Bugada

**Arquivo de Referência**: `02-PADROES-DE-PROMPT.md` (Padrão 1: Chain-of-Thought)  
**Conceito**: CoT força Claude a mostrar raciocínio intermediário, reduzindo assunções silenciosas em bugs complexos.  
**Dificuldade**: Fácil | **Tempo**: ~4 min

Neste exercício você vai ver como pedir raciocínio passo a passo produz um diagnóstico **verificável** em vez de apenas uma correção.

#### Setup

Crie um arquivo `calcular_frete.py`:

```bash
cat > calcular_frete.py << 'EOF'
def calcular_frete(peso_kg: float, distancia_km: int, express: bool = False) -> float:
    taxa_base = 5.0
    taxa_peso = peso_kg * 1.2
    taxa_distancia = distancia_km * 0.08
    
    if express:
        multiplicador = 1.5
    
    total = taxa_base + taxa_peso + taxa_distancia * multiplicador  # BUG aqui
    return round(total, 2)
EOF
```

O bug: quando `express=False`, a variável `multiplicador` nunca é inicializada, causando `UnboundLocalError` na linha final.

#### Passo 1 — Sem CoT

Execute um prompt simples de correção:

```bash
claude "Corrija o bug em calcular_frete.py"
```

**Saída Esperada** (simulada):
```python
def calcular_frete(peso_kg: float, distancia_km: int, express: bool = False) -> float:
    taxa_base = 5.0
    taxa_peso = peso_kg * 1.2
    taxa_distancia = distancia_km * 0.08
    
    if express:
        multiplicador = 1.5
    else:
        multiplicador = 1.0  # adiciona aqui
    
    total = taxa_base + taxa_peso + taxa_distancia * multiplicador
    return round(total, 2)
```

**O que observar**: Claude corrigiu a sintaxe, mas você não vê o **raciocínio**. Ele pode estar correto por sorte, ou pode estar incorreto semanticamente (exemplo: qual deve ser o multiplicador no ramo `False`?).

#### Passo 2 — Com CoT

Agora peça raciocínio passo a passo:

```bash
claude "Analise calcular_frete.py e execute estes passos:

1. Rastreie o valor de cada variável linha por linha para uma chamada com express=False, peso_kg=10, distancia_km=100
2. Identifique em qual linha exatamente o erro ocorre e qual é o nome do erro Python
3. Explique por que o erro NÃO aparece quando express=True
4. Proponha o fix correto que preserva a lógica de negócio (frete express = 50% a mais)

Mostre o raciocínio passo a passo antes da solução."
```

**Saída Esperada** (simulada):
```
## Raciocínio Passo a Passo:

### Passo 1 - Trace com express=False:
- Linha 1: taxa_base = 5.0
- Linha 2: taxa_peso = 10 * 1.2 = 12.0
- Linha 3: taxa_distancia = 100 * 0.08 = 8.0
- Linha 4: if express (False) — pula para linha 7
- Linha 7: total = 5.0 + 12.0 + 8.0 * multiplicador  ← multiplicador NUNCA FOI DEFINIDO!
- **ERRO**: UnboundLocalError: local variable 'multiplicador' referenced before assignment

### Passo 2 - Identificação do Erro:
- **Tipo**: UnboundLocalError
- **Linha**: 7 (total = ... * multiplicador)
- **Raiz**: multiplicador só é atribuído se express=True; se False, nunca é inicializado

### Passo 3 - Por que funciona com express=True:
- if express (True) → linha 5 executa: multiplicador = 1.5
- multiplicador está definido quando a linha 7 executa
- Sem erro

### Passo 4 - Fix Correto (preservando lógica):
O multiplicador deve ser inicializado ANTES do if:

def calcular_frete(peso_kg: float, distancia_km: int, express: bool = False) -> float:
    taxa_base = 5.0
    taxa_peso = peso_kg * 1.2
    taxa_distancia = distancia_km * 0.08
    
    multiplicador = 1.0  # padrão para não-express
    if express:
        multiplicador = 1.5  # override se express
    
    total = taxa_base + taxa_peso + taxa_distancia * multiplicador
    return round(total, 2)
```

**O que observar**: O raciocínio passo a passo prova que Claude entende a semântica (frete express = 1.5x, frete padrão = 1.0x), não apenas a sintaxe. Você pode **verificar cada linha** e confirmar que a lógica está correta.

#### Conceito Reforçado

Comparação sem CoT vs com CoT:

| Aspecto | Sem CoT | Com CoT |
|---|---|---|
| Tipo de resposta | Código corrigido | Raciocínio verificável + código |
| Confiança | Depende da sorte | Alta — você vê cada passo |
| Para bugs complexos | Superficial (sintaxe) | Profundo (semântica + negócio) |
| Tempo de resposta | Rápido | Um pouco mais longo (raciocínio custa tokens) |

---

### 2.2 — Role Prompting: Security Review de Endpoint

**Arquivo de Referência**: `02-PADROES-DE-PROMPT.md` (Padrão 4: Role Prompting)  
**Conceito**: Atribuir um papel de especialista muda o foco, profundidade e frame da análise.  
**Dificuldade**: Médio | **Tempo**: ~5 min

Neste exercício você verá como um mesmo endpoint analisado como "programador genérico" vs "auditor de segurança" produz resultados radicalmente diferentes.

#### Setup

Crie um arquivo `auth_endpoint.py` intencionalmente inseguro:

```bash
cat > auth_endpoint.py << 'EOF'
from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.post("/login")
def login(username: str, password: str):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    # Verificar credenciais
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    if user:
        return {"token": f"token_{username}_logged_in"}
    return {"error": "credenciais inválidas"}
EOF
```

Este código tem vulnerabilidades propositais: SQL injection, plaintext password, token previsível, sem HTTP 401, sem rate limit.

#### Passo 1 — Sem Role (Programador Genérico)

Execute uma revisão de código genérica:

```bash
claude "Revise auth_endpoint.py"
```

**Saída Esperada** (simulada):
```
Aqui estão algumas sugestões:

1. **SQL Injection**: A query usa f-string. Use parameterized queries:
   cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))

2. **Plaintext password**: Senhas não devem ser armazenadas em texto puro. Use bcrypt ou argon2.

Isso deveria cobrir os principais problemas.
```

**O que observar**: Apenas 2 problemas encontrados, ambos superficiais. Nenhuma menção a status HTTP, rate limiting, token format, ou impacto de segurança real.

#### Passo 2 — Com Role (Auditor de Segurança OWASP)

Agora execute com Role de especialista em segurança:

```bash
claude "Você é um especialista em segurança web com 10 anos de experiência em auditorias OWASP Top 10 e penetration testing. Revise auth_endpoint.py como se fosse um relatório formal de auditoria de segurança.

Para cada vulnerabilidade encontrada, inclua:
1. Nome técnico do problema
2. Categoria OWASP (se aplicável)
3. Como um atacante exploraria
4. Correção específica com código
5. Impacto em caso de exploração

Formate como um relatório executivo: 'CRÍTICA', 'ALTA', 'MÉDIA', 'BAIXA' para cada achado."
```

**Saída Esperada** (simulada):
```
## RELATÓRIO DE AUDITORIA DE SEGURANÇA — auth_endpoint.py

### Achado 1: SQL Injection — CRÍTICA
**Categoria OWASP**: A03:2021 – Injection
**Como explorar**:
  POST /login com username = `' OR '1'='1` e password qualquer
  Query resultante: SELECT * FROM users WHERE username='' OR '1'='1' AND password='...'
  Resultado: Bypass de autenticação, acesso a qualquer conta

**Correção**:
  cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))

---

### Achado 2: Plaintext Password Storage — CRÍTICA
**Categoria OWASP**: A02:2021 – Cryptographic Failures
**Como explorar**:
  Roubo de banco de dados → senhas em texto puro podem ser usadas em sites similares (credential stuffing)
  Impacto: Comprometimento de todas as contas de usuários

**Correção**:
  import bcrypt
  hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
  cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed))

---

### Achado 3: Token Previsível — CRÍTICA
**Categoria OWASP**: A07:2021 – Identification and Authentication Failures
**Como explorar**:
  Token = f"token_{username}_logged_in"
  Padrão trivial: attacker pode gerar tokens válidos para qualquer user sem login
  Teste: curl -H "Authorization: Bearer token_admin_logged_in"

**Correção**:
  import secrets
  token = secrets.token_urlsafe(32)
  # Armazenar token em redis/DB com expiração
  return {"token": token, "expires_in": 3600}

---

### Achado 4: HTTP 200 em Falha de Autenticação — ALTA
**Categoria OWASP**: A01:2021 – Broken Access Control
**Como explorar**:
  HTTP 200 em ambos os casos (sucesso e falha) permite enumeration de usuários
  Attacker testa usernames e mede diferença de resposta

**Correção**:
  if not user:
      raise HTTPException(status_code=401, detail="Credenciais inválidas")

---

### Achado 5: Sem Rate Limiting — ALTA
**Categoria OWASP**: A05:2021 – Broken Access Control (Brute Force)
**Como explorar**:
  10.000 tentativas de senha por segundo contra a conta "admin"
  Sem delay ou bloqueio, a força bruta converge rapidamente

**Correção**:
  from slowapi import Limiter
  limiter = Limiter(key_func=get_remote_address)
  @app.post("/login")
  @limiter.limit("5/minute")
  def login(...)

---

## Sumário: 5 achados CRÍTICA/ALTA. Endpoint NÃO PRONTO PARA PRODUÇÃO.
```

**O que observar**: Role Prompting transformou uma revisão superficial em um relatório formal com 5 achados (vs 2 antes), categorias OWASP, exploits reais e correções com código. A escolha de papel mudou tudo.

#### Conceito Reforçado

Impacto do Role Prompting:

| Aspecto | Sem Role (Genérico) | Com Role (Especialista Segurança) |
|---|---|---|
| Número de problemas | 2 | 5 |
| Profundidade | Sintaxe ("use parameterized queries") | Semântica + exploit ("attacker testa usernames") |
| Formato | Genérico | Relatório estruturado OWASP |
| Recomendações | Vagas | Código específico com imports |
| Cobertura | Apenas vulnerabilidades óbvias | Enumeration, rate limiting, token design |

---

### 2.3 — Structured Output: Análise de Qualidade de Código

**Arquivo de Referência**: `02-PADROES-DE-PROMPT.md` (Padrão 5: Structured Output)  
**Conceito**: Solicitar saída em JSON/estrutura definida torna a resposta parseable e sem ambiguidade.  
**Dificuldade**: Médio | **Tempo**: ~4 min

Neste exercício você vai ver como restrições de formato forçam precisão e habilitam automação.

#### Setup

Crie um arquivo `query_lenta.py` com múltiplos problemas:

```bash
cat > query_lenta.py << 'EOF'
def buscar_produtos_populares(db_connection, categoria, limite=10):
    todos = db_connection.execute("SELECT * FROM produtos").fetchall()
    resultado = []
    for produto in todos:
        if produto['categoria'] == categoria:
            pedidos = db_connection.execute(
                f"SELECT COUNT(*) FROM pedidos WHERE produto_id={produto['id']}"
            ).fetchone()[0]
            if pedidos > 0:
                resultado.append({**produto, 'total_pedidos': pedidos})
    resultado.sort(key=lambda x: x['total_pedidos'], reverse=True)
    return resultado[:limite]
EOF
```

Problemas: N+1 query (uma SELECT por produto dentro de loop), SQL injection (produto['id'] na f-string), full table scan.

#### Passo 1 — Sem Structured Output

Execute uma análise genérica:

```bash
claude "Analise query_lenta.py e me diga os problemas"
```

**Saída Esperada** (simulada):
```
Este código tem alguns problemas de performance:

1. N+1 query problem: para cada produto, executa uma query separada. Com 10.000 produtos, são 10.001 queries.

2. SQL injection: produto['id'] é interpolado diretamente na query. Um ID como "1 OR 1=1" poderia quebrar a segurança.

3. Full table scan: SELECT * FROM produtos sem WHERE. Se a tabela tem milhões de registros, tudo é carregado na memória.

A melhor solução seria usar um SQL JOIN único:
SELECT p.*, COUNT(pd.id) as total_pedidos FROM produtos p LEFT JOIN pedidos pd ON p.id = pd.produto_id WHERE p.categoria = ? GROUP BY p.id ORDER BY total_pedidos DESC LIMIT ?
```

**O que observar**: Resposta em prosa, difícil de processar programaticamente. Se você quisesse extrair "complexidade atual" ou "ganho estimado", seria difícil fazer parse automático.

#### Passo 2 — Com Structured Output

Peça saída em JSON com schema definido:

```bash
claude "Analise query_lenta.py e retorne um JSON válido com esta estrutura EXATA:

{
  \"complexidade_atual\": \"string descrevendo Big-O\",
  \"problemas\": [
    {
      \"tipo\": \"string nome técnico\",
      \"linha\": número,
      \"descricao\": \"string\",
      \"severidade\": \"critica\" | \"alta\" | \"media\"
    }
  ],
  \"query_otimizada\": \"string com SQL sugerido\",
  \"complexidade_otimizada\": \"string descrevendo Big-O\",
  \"ganho_estimado\": \"string estimativa de melhoria\"
}

Retorne APENAS JSON válido, sem explicação adicional."
```

**Saída Esperada**:
```json
{
  "complexidade_atual": "O(n²) — n queries iniciais + n queries em loop",
  "problemas": [
    {
      "tipo": "N+1 Query",
      "linha": 6,
      "descricao": "SELECT executado dentro de loop — 1 query por produto encontrado, total: 1 + n queries",
      "severidade": "critica"
    },
    {
      "tipo": "SQL Injection",
      "linha": 8,
      "descricao": "produto['id'] interpolado diretamente em f-string dentro query SQL com f-string",
      "severidade": "critica"
    },
    {
      "tipo": "Full Table Scan",
      "linha": 3,
      "descricao": "SELECT * FROM produtos sem WHERE — carrega tabela inteira na memória",
      "severidade": "alta"
    }
  ],
  "query_otimizada": "SELECT p.*, COUNT(pd.id) as total_pedidos FROM produtos p LEFT JOIN pedidos pd ON p.id = pd.produto_id WHERE p.categoria = ? GROUP BY p.id ORDER BY total_pedidos DESC LIMIT ?",
  "complexidade_otimizada": "O(1) queries — uma única query otimizada com índice",
  "ganho_estimado": "10–100x para tabelas grandes — de (1+n) queries para 1 query com JOIN eficiente"
}
```

**O que observar**: JSON válido, parseable. Você pode extrair `ganho_estimado` diretamente para um dashboard, ou usar `severidade` para ordenar por impacto. Cada campo é preciso porque foi definido no schema.

#### Conceito Reforçado

Quando usar Structured Output:

| Cenário | Benefício |
|---|---|
| Output consumido por código (CI/CD, API) | JSON parseable, sem ambiguidade |
| Múltiplas categorias (`critica/alta/media`) | Obriga Claude a ser preciso (não "grave" vs "crítico") |
| Campos opcionais (token counts, ETA) | Schema força preenchimento |
| Relatórios automatizados | Estrutura consistente entre execuções |
| Comparação de múltiplas soluções | JSON permite sorting/filtering |

---

### 2.4 — Meta-Prompting: Claude Como Coach de Prompts

**Arquivo de Referência**: `02-PADROES-DE-PROMPT.md` (Padrão 8: Meta-Prompting)  
**Conceito**: Claude pode melhorar seus próprios prompts — use isso para aprender quais componentes faltam.  
**Dificuldade**: Difícil | **Tempo**: ~6 min

Neste exercício você vai experimentar como Meta-Prompting comprime rodadas de clarificação em uma única iteração.

#### Passo 1 — Executar Prompt Vago

Execute um prompt intencionalmente vago:

```bash
claude "Otimize o banco"
```

**Saída Esperada** (simulada):
```
Preciso de mais detalhes para ajudá-lo:

1. Qual banco de dados? (PostgreSQL, MySQL, MongoDB, Redis?)
2. Qual é o problema específico? (latência de queries, tamanho de dados, CPU)
3. Qual é o escopo? (table específica, cluster inteiro, conexões)
4. Qual é o SLA? (< 100ms, < 1s, target específico?)
5. Quais são as constraints? (pode mudar schema? adicionar índices? alterar aplicação?)
```

**O que observar**: Claude lista 5 perguntas essenciais. Responder cada uma tomaria 5 rodadas. Meta-Prompting comprime isso em 1 rodada.

#### Passo 2 — Usar Claude para Reescrever o Prompt

Execute Meta-Prompting para melhorar o prompt:

```bash
claude "Meu prompt anterior foi muito vago:
'Otimize o banco'

Aqui está contexto real que eu tenho:
- Database: PostgreSQL 15
- Tabela problemática: 'pedidos' com aproximadamente 2 milhões de registros
- Query lenta: SELECT * FROM pedidos WHERE status='pendente' ORDER BY created_at DESC
- Tempo atual: ~3 segundos
- Alvo: < 200ms
- Posso adicionar índices, mas não alterar schema

Reescreva meu prompt para seguir o template de 4 componentes (Contexto, Tarefa Específica, Restrições, Formato Esperado). Use o melhor padrão de prompting para este cenário."
```

**Saída Esperada** (simulada):
```
Aqui está seu prompt reescrito para máxima efetividade:

---

Contexto: PostgreSQL 15, tabela 'pedidos' com aproximadamente 2 milhões de registros. Query atual para dashboard operacional em produção:
SELECT * FROM pedidos WHERE status='pendente' ORDER BY created_at DESC

Performance atual: ~3 segundos. Isso impacta o dashboard usado por 50+ operadores diariamente.

Tarefa: Otimize esta query para reduzir o tempo de resposta de ~3s para <200ms.

Restrições:
- Não alterar o schema da tabela (nenhuma coluna nova)
- Pode adicionar índices (informe quais com CREATE INDEX commands)
- Manter o resultado exato (status pendente, ordenado por data crescente)
- Usar apenas PostgreSQL 15 built-ins (sem extensões)

Formato esperado:
1. Query otimizada com explicação da melhoria
2. CREATE INDEX commands exatos para os índices necessários
3. EXPLAIN ANALYZE esperado (mostrando timing)
4. Estimativa de ganho percentual e novo tempo esperado

---

Este prompt agora:
- Especifica contexto (PostgreSQL 15, 2M rows, dashboard production)
- Descreve a tarefa única (otimizar de 3s para <200ms)
- Lista restrições exatas (sem schema change, pode adicionar índices)
- Define formato (4 artefatos específicos: query + índices + EXPLAIN + estimate)
```

**O que observar**: Claude produziu um prompt que antecipa todas as 5 perguntas que teria feito na Passo 1. O Meta-Prompt eliminou a necessidade de 5 rodadas de clarificação em 1.

#### Passo 3 — Executar o Prompt Melhorado

Agora execute o prompt melhorado que Claude gerou:

```bash
claude "Contexto: PostgreSQL 15, tabela 'pedidos' com aproximadamente 2 milhões de registros. Query atual para dashboard operacional em produção:
SELECT * FROM pedidos WHERE status='pendente' ORDER BY created_at DESC

Performance atual: ~3 segundos.

Tarefa: Otimize esta query para reduzir o tempo de resposta de ~3s para <200ms.

Restrições:
- Não alterar o schema da tabela
- Pode adicionar índices
- Manter o resultado exato

Formato esperado:
1. Query otimizada com explicação
2. CREATE INDEX commands exatos
3. EXPLAIN ANALYZE esperado
4. Estimativa de ganho percentual"
```

**Saída Esperada** (simulada):
```
## Solução Otimizada

### 1. Query Otimizada
```sql
SELECT * FROM pedidos 
WHERE status='pendente' 
ORDER BY created_at DESC 
LIMIT 100;  -- adicionar limit se estiver na aplicação
```
Explicação: A query original já está bem formada, mas o problema é a falta de índice. A verdadeira otimização é o índice abaixo.

### 2. CREATE INDEX Commands
```sql
CREATE INDEX CONCURRENTLY idx_pedidos_status_created 
ON pedidos(status, created_at DESC);
```
Este é um índice composto que satisfaz BOTH o filtro (status) e a ordenação (created_at DESC), permitindo que PostgreSQL use Index-Only Scans.

### 3. EXPLAIN ANALYZE Esperado

**Antes (sem índice)**:
```
Seq Scan on pedidos  (cost=0.00..85000.00 rows=200000 width=256)
  Filter: (status = 'pendente')
  Planning Time: 0.2 ms
  Execution Time: 3000 ms
```

**Depois (com índice)**:
```
Index Scan Backward using idx_pedidos_status_created on pedidos (cost=0.42..1500.00 rows=50000 width=256)
  Index Cond: (status = 'pendente')
  Planning Time: 0.1 ms
  Execution Time: 150 ms  ← 20x mais rápido!
```

### 4. Estimativa de Ganho
- **Ganho**: 95% de redução (3000ms → 150ms)
- **Novo tempo**: ~150ms (dentro do alvo de <200ms)
- **Índice size**: ~500MB para 2M rows com 2 colunas
- **Trade-off**: +500MB em disco, +2ms por INSERT (manutenção do índice)
```

**O que observar**: A saída é altamente específica (comando CREATE INDEX exato, números EXPLAIN antes/depois, estimativa 95% de ganho), porque o prompt foi específico. Compare com o Passo 1 — "otimize o banco" — que teria gerado uma lista genérica.

#### Conceito Reforçado

O loop Meta-Prompting:

| Fase | Resultado |
|---|---|
| Prompt vago ("Otimize o banco") | 5 perguntas de clarificação de Claude |
| Meta-Prompt (Claude melhora o prompt) | Prompt reescrito com 4 componentes |
| Execução do prompt melhorado | Resposta específica (CREATE INDEX, EXPLAIN, 95% ganho) |
| **Lição** | Meta-Prompting comprime N rodadas de clarificação em 1 iteração |

---

## Seção 3 — Aplicação Real

---

### 3.1 — Debugging com Contexto Completo

**Arquivo de Referência**: `03-EXEMPLOS-REAIS.md` (Exemplo 1: Debugar Erro TypeError)  
**Conceito**: Aplicar o template de debugging completo (contexto + erro + código + objetivo) do mundo real.  
**Dificuldade**: Fácil | **Tempo**: ~4 min

Neste exercício você vai implementar o template de debugging da Seção 3 do arquivo de exemplos.

#### Setup

Crie um arquivo `process_csv.py` com um bug real:

```bash
cat > process_csv.py << 'EOF'
import pandas as pd

def calcular_total_por_cliente(arquivo_csv: str) -> dict:
    df = pd.read_csv(arquivo_csv)
    resultado = {}
    for _, row in df.iterrows():
        cliente = row['cliente_id']
        valor = row['valor']  
        if cliente in resultado:
            resultado[cliente] += valor   # BUG: TypeError aqui
        else:
            resultado[cliente] = valor
    return resultado
EOF
```

E um arquivo CSV de teste:

```bash
cat > dados.csv << 'EOF'
cliente_id,valor,data
101,150.50,2024-01-15
102,200,2024-01-15
101,75.25,2024-01-16
EOF
```

O bug: quando você executa este código, `pd.read_csv` lê a coluna `valor` como `object` (string) em vez de `float`, então `resultado[cliente] += valor` falha com `TypeError: unsupported operand type(s) for +=: 'float' and 'str'`.

#### Passo 1 — Sem Contexto Completo

Execute um prompt vago:

```bash
claude "Tem um TypeError no meu script"
```

**Saída Esperada** (simulada):
```
Preciso de mais informações:
- Qual é a mensagem de erro exata?
- Qual é a linha onde acontece?
- Qual é o arquivo CSV de entrada?
```

**O que observar**: 3 perguntas antes de poder ajudar.

#### Passo 2 — Com Contexto Completo

Agora execute com o template completo:

```bash
claude "Contexto: Python 3.11, pandas 2.1. Script processa um CSV de transações financeiras e agrega valores por cliente.

Erro que recebo:
TypeError: unsupported operand type(s) for +=: 'float' and 'str'
  File 'process_csv.py', linha 10, em calcular_total_por_cliente
    resultado[cliente] += valor

Código (linhas 1-14):
import pandas as pd

def calcular_total_por_cliente(arquivo_csv: str) -> dict:
    df = pd.read_csv(arquivo_csv)
    resultado = {}
    for _, row in df.iterrows():
        cliente = row['cliente_id']
        valor = row['valor']  
        if cliente in resultado:
            resultado[cliente] += valor
        else:
            resultado[cliente] = valor
    return resultado

CSV de entrada (dados.csv):
cliente_id,valor,data
101,150.50,2024-01-15
102,200,2024-01-15
101,75.25,2024-01-16

Qual é a raiz do problema? Como corrigir mantendo a lógica de agregação por cliente?"
```

**Saída Esperada** (simulada):
```
## Diagnóstico

O problema é que `pd.read_csv` leu a coluna `valor` como `object` (string) em vez de `float`. 

No CSV, você tem:
- 150.50 (string após read_csv)
- 200 (string após read_csv)
- 75.25 (string após read_csv)

Na linha `resultado[cliente] += valor`, você está tentando somar:
- `resultado[101] = 150.50` (float armazenado inicialmente)
- `+= 200` (string na próxima iteração)

## Solução 1 (Rápida)

Converter a coluna após read_csv:
```python
def calcular_total_por_cliente(arquivo_csv: str) -> dict:
    df = pd.read_csv(arquivo_csv)
    df['valor'] = pd.to_numeric(df['valor'])  # converter string → float
    resultado = {}
    for _, row in df.iterrows():
        cliente = row['cliente_id']
        valor = row['valor']
        if cliente in resultado:
            resultado[cliente] += valor
        else:
            resultado[cliente] = valor
    return resultado
```

## Solução 2 (Pythônica — Recomendada)

Usar groupby do pandas em vez de loop manual:
```python
def calcular_total_por_cliente(arquivo_csv: str) -> dict:
    df = pd.read_csv(arquivo_csv)
    df['valor'] = pd.to_numeric(df['valor'])
    return df.groupby('cliente_id')['valor'].sum().to_dict()
```

A Solução 2 é 100x mais rápida em arquivos grandes.
```

**O que observar**: Porque você forneceu a mensagem de erro exata + linha + CSV + código, Claude identificou a raiz (tipo de dados) em vez de apenas a sintaxe. Você também recebeu 2 soluções: a rápida (mínima mudança) e a correta (pythônica).

#### Conceito Reforçado

Checklist "Por que funciona" (do Exemplo 1 de `03-EXEMPLOS-REAIS.md`):

| Elemento | Eliminado qual adivinhação? |
|---|---|
| Python version + pandas version | Qual é a behavior de `read_csv`? |
| Mensagem de erro exata | Qual é o tipo que falha? (float vs str) |
| Código completo + linhas | Qual é a sequência de operações? |
| CSV de entrada | Qual é o formato que `read_csv` vê? |
| Objetivo ("manter a lógica de agregação") | Qual é a intenção semântica? (agrupar por cliente) |

---

### 3.2 — Few-Shot para Convenção de Nomenclatura

**Arquivo de Referência**: `03-EXEMPLOS-REAIS.md` (Exemplo 2: Refatorar Código Repetitivo) + `02-PADROES-DE-PROMPT.md` (Padrão 2: Few-Shot)  
**Conceito**: 3 exemplos Few-Shot ensinam um padrão exato que Claude extrapolará para casos desconhecidos.  
**Dificuldade**: Médio | **Tempo**: ~5 min

Neste exercício você verá como Few-Shot transfere um padrão de nomenclatura sem precisar especificar cada função.

#### Setup

Crie um arquivo `api_endpoints.py` com nomenclatura inconsistente:

```bash
cat > api_endpoints.py << 'EOF'
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{id}")
def GetUser(id: int): 
    """Retorna um usuário específico"""
    pass

@app.post("/users")
def create_user_record(data): 
    """Cria um novo usuário"""
    pass

@app.delete("/users/{id}")
def removeUser(id: int):
    """Remove um usuário existente"""
    pass

@app.get("/products")
def fetch_all_products_from_db():
    """Retorna lista de produtos"""
    pass

@app.put("/products/{id}")
def UpdateProductInfo(id: int, data):
    """Atualiza informações de produto"""
    pass
EOF
```

As funções têm nomes inconsistentes: `GetUser` (PascalCase), `create_user_record` (snake_case verbal), `removeUser` (camelCase), `fetch_all_products_from_db` (snake_case verbose), `UpdateProductInfo` (PascalCase).

#### Passo 1 — Sem Few-Shot

Execute um prompt genérico de padronização:

```bash
claude "Padronize os nomes das funções em api_endpoints.py"
```

**Saída Esperada** (simulada):
```python
@app.get("/users/{id}")
def get_user(id: int):  # snake_case, inglês
    pass

@app.post("/users")
def create_user(data):  # snake_case, inglês
    pass

@app.delete("/users/{id}")
def delete_user(id: int):  # snake_case, inglês
    pass

@app.get("/products")
def get_products():  # snake_case, inglês
    pass

@app.put("/products/{id}")
def update_product(id: int, data):  # snake_case, inglês
    pass
```

**O que observar**: Claude escolheu snake_case em inglês (genérico). Mas o projeto pode ter uma convenção diferente (português, verbos diferentes, prefixos).

#### Passo 2 — Com Few-Shot

Agora forneça 3 exemplos do padrão correto:

```bash
claude "Padronize os nomes das funções em api_endpoints.py. Seu projeto segue uma convenção específica de nomenclatura. Aqui estão 3 exemplos do padrão correto:

Exemplo 1: GET /users/{id} → obter_usuario(usuario_id)
Exemplo 2: POST /users → criar_usuario(dados)
Exemplo 3: DELETE /users/{id} → remover_usuario(usuario_id)

Agora aplique este padrão (PT-BR, snake_case, verbo ativo) a TODAS as 5 funções do arquivo, incluindo os endpoints de /products."
```

**Saída Esperada**:
```python
@app.get("/users/{id}")
def obter_usuario(usuario_id: int):  # PT-BR, snake_case, verbo ativo
    """Retorna um usuário específico"""
    pass

@app.post("/users")
def criar_usuario(dados):  # PT-BR, snake_case, verbo ativo
    """Cria um novo usuário"""
    pass

@app.delete("/users/{id}")
def remover_usuario(usuario_id: int):  # PT-BR, snake_case, verbo ativo
    """Remove um usuário existente"""
    pass

@app.get("/products")
def listar_produtos():  # PT-BR, snake_case, verbo ativo
    """Retorna lista de produtos"""
    pass

@app.put("/products/{id}")
def atualizar_produto(produto_id: int, dados):  # PT-BR, snake_case, verbo ativo
    """Atualiza informações de produto"""
    pass
```

**O que observar**: Com apenas 3 exemplos (GET/POST/DELETE na rota `/users`), Claude extrapolou para `/products` usando o mesmo padrão (PT-BR, snake_case, verbo ativo). Few-Shot *transfere* o padrão, não requer especificação per-funcão.

#### Conceito Reforçado

Zero-Shot vs Few-Shot:

| Critério | Zero-Shot (genérico) | Few-Shot (3 exemplos) |
|---|---|---|
| Nomes gerados | `get_user` (inglês) | `obter_usuario` (PT-BR) |
| Padrão | Genérico industry-standard | Específico do projeto |
| Funciona para casos novos? | Sim (genérico) | Sim (extrapolação) |
| Tempo até padronização global | Requer N prompts | 1 prompt com 3 exemplos |
| Precisão em 5/5 funções | Depende da sorte | 100% — padrão foi demonstrado |

---

### 3.3 — Combinando Role + CoT + Structured Output

**Arquivo de Referência**: `03-EXEMPLOS-REAIS.md` (Exemplo 10: Otimização Avançada) + `02-PADROES-DE-PROMPT.md` (Seção "Combinação de Padrões")  
**Conceito**: Combinar 3 padrões (Role + CoT + Structured Output) produz análise especializada, raciocínio verificável e saída processável — o "prompt final boss".  
**Dificuldade**: Difícil | **Tempo**: ~7 min

Neste exercício você vai ver como 3 padrões trabalham juntos para amplificar um ao outro.

#### Setup

Crie um arquivo `produto_endpoint.py` — uma versão realista e mais completa:

```bash
cat > produto_endpoint.py << 'EOF'
from fastapi import FastAPI
import psycopg2

app = FastAPI()

@app.get("/produtos")
def listar_produtos(categoria: str = None, preco_max: float = None):
    conn = psycopg2.connect("postgresql://localhost/loja")
    cursor = conn.cursor()
    
    todos = cursor.execute("SELECT * FROM produtos").fetchall()
    
    resultado = []
    for produto in todos:
        if categoria and produto[3] != categoria:
            continue
        if preco_max and produto[2] > preco_max:
            continue
        
        pedidos = cursor.execute(
            f"SELECT COUNT(*) FROM pedidos WHERE produto_id = {produto[0]}"
        ).fetchone()[0]
        
        resultado.append({
            'id': produto[0], 'nome': produto[1], 'preco': produto[2],
            'categoria': produto[3], 'total_pedidos': pedidos
        })
    
    return sorted(resultado, key=lambda x: x['total_pedidos'], reverse=True)[:20]
EOF
```

Este endpoint tem: N+1 query (para cada produto), SQL injection (f-string), full table scan, sem limit/offset, sem índices.

#### Comando

Execute um prompt único que combina os 3 padrões:

```bash
claude "Você é um especialista em performance de APIs Python com expertise em PostgreSQL query optimization e FastAPI concurrency patterns. Você tem 8 anos de experiência otimizando backends que servem 100k+ requisições/dia.

Analise produto_endpoint.py passo a passo:

1. Identifique cada operação de banco de dados (SELECT, loop) e sua complexidade Big-O
2. Para cada problema encontrado, explique como ele degrada com crescimento de dados (100k produtos vs 10M produtos)
3. Rastreie o impacto cascata: se há N+1, quantas queries extras são executadas para 100k resultados?
4. Proponha a solução otimizada com SQL correto e índices necessários

Retorne um JSON com esta estrutura exata:
{
  \"diagnostico\": {
    \"complexidade_atual\": \"string Big-O\",
    \"problemas\": [
      {\"categoria\": \"string\", \"linha\": número, \"impacto_escala\": \"string\", \"severidade\": \"critica|alta|media\"}
    ]
  },
  \"solucao\": {
    \"endpoint_otimizado\": \"string com código Python completo\",
    \"indices_necessarios\": [\"string com CREATE INDEX\"],
    \"complexidade_resultante\": \"string Big-O\",
    \"ganho_estimado_100k_produtos\": \"string com tempo antes/depois\"
  }
}"
```

#### Saída Esperada

```json
{
  "diagnostico": {
    "complexidade_atual": "O(n²) — select inicial de todos os produtos (1 query) + loop de N produtos executando 1 query cada",
    "problemas": [
      {
        "categoria": "N+1 Query Pattern",
        "linha": 16,
        "impacto_escala": "100k produtos = 100.001 queries (1 inicial + 100k no loop). Com 1 QPS limite, isso demora 27 horas em vez de 1 segundo com JOIN",
        "severidade": "critica"
      },
      {
        "categoria": "SQL Injection via F-String",
        "linha": 17,
        "impacto_escala": "produto[0] interpolado sem parameterization. Attacker pode executar queries arbitrárias. Exemplo: produto[0] = '1; DROP TABLE produtos; --' ",
        "severidade": "critica"
      },
      {
        "categoria": "Full Table Scan sem Índices",
        "linha": 12,
        "impacto_escala": "100k produtos sem filtro carrega tudo na memória. Com 10M produtos, memory exhaustion e timeout. Nenhum índice aproveitado.",
        "severidade": "alta"
      },
      {
        "categoria": "Sem Pagination/LIMIT Eficiente",
        "linha": 26,
        "impacto_escala": "Retorna apenas 20 items, mas lê toda a tabela. Em 10M produtos, descartar 9.999.980 linhas é custoso.",
        "severidade": "alta"
      }
    ]
  },
  "solucao": {
    "endpoint_otimizado": "from fastapi import FastAPI\nfrom sqlalchemy import create_engine, select, func\nfrom sqlalchemy.orm import sessionmaker\nfrom models import Produto\n\nengine = create_engine('postgresql://localhost/loja')\nSession = sessionmaker(bind=engine)\n\napp = FastAPI()\n\n@app.get('/produtos')\nasync def listar_produtos(categoria: str = None, preco_max: float = None, offset: int = 0, limit: int = 20):\n    \"\"\"Retorna produtos com agregação de pedidos via single JOIN query.\"\"\"\n    session = Session()\n    \n    query = select(\n        Produto.id, Produto.nome, Produto.preco, Produto.categoria,\n        func.count(Pedido.id).label('total_pedidos')\n    ).outerjoin(Pedido).group_by(Produto.id)\n    \n    if categoria:\n        query = query.where(Produto.categoria == categoria)\n    if preco_max:\n        query = query.where(Produto.preco <= preco_max)\n    \n    query = query.order_by(func.count(Pedido.id).desc()).limit(limit).offset(offset)\n    \n    resultado = session.execute(query).fetchall()\n    session.close()\n    \n    return [{'id': r.id, 'nome': r.nome, 'preco': r.preco, 'categoria': r.categoria, 'total_pedidos': r.total_pedidos} for r in resultado]",
    "indices_necessarios": [
      "CREATE INDEX CONCURRENTLY idx_produtos_categoria ON produtos(categoria);",
      "CREATE INDEX CONCURRENTLY idx_produtos_preco ON produtos(preco);",
      "CREATE INDEX CONCURRENTLY idx_pedidos_produto_id ON pedidos(produto_id);"
    ],
    "complexidade_resultante": "O(1 query) — single optimized LEFT JOIN com filtros aplicados na query, não em Python",
    "ganho_estimado_100k_produtos": "ANTES: 100.001 queries (~27 horas com rate limit 1 QPS). DEPOIS: 1 query (~50ms com índices). Ganho: 1.944.000x mais rápido (de 27h para 50ms)"
  }
}
```

**O que observar**: 

- **Role** (especialista em performance): O JSON menciona "N+1 pattern", "sequential scan", "memory exhaustion", "rate limit" — vocabulário técnico que um generalista não usaria.
- **CoT** (passo a passo): A seção "impacto_escala" mostra o raciocínio (100k produtos = 100k queries, 27 horas com 1 QPS), deixando você verificar a matemática.
- **Structured Output** (JSON): O código otimizado é um string dentro do JSON; você pode extrair e usar diretamente em um CI/CD pipeline. O `ganho_estimado` é preciso porque foi estruturado (antes/depois em tempo absoluto).

#### Conceito Reforçado

Contribuição de cada padrão na combinação:

| Padrão | Contribuição | Evidência |
|---|---|---|
| Role (especialista performance) | Vocabulário técnico correto | "N+1 pattern", "sequential scan", "JOIN eficiente" |
| CoT (passo a passo) | Raciocínio verificável | "100k produtos = 100.001 queries... 27 horas com 1 QPS" |
| Structured Output (JSON) | Pronto para automação | String Python no JSON + 3 CREATE INDEX exatos + número 1.944.000x |

Nenhum padrão sozinho produziria este resultado completo. Juntos, amplifique um ao outro.

---

## Checklist de Conclusão

- [ ] **1.1**: Observei concretamente como cada componente do template elimina uma adivinação do Claude
- [ ] **1.2**: Usei o template de 4 componentes para gerar um endpoint FastAPI production-ready
- [ ] **1.3**: Identifiquei os 4 anti-padrões em um prompt real e corrigi cada um separadamente
- [ ] **2.1**: Vi Chain-of-Thought revelando a raiz do bug passo a passo (não apenas o sintoma)
- [ ] **2.2**: Observei como Role Prompting muda a profundidade e frame da análise (2 itens → 5 itens estruturados)
- [ ] **2.3**: Recebi um JSON válido e parseable em vez de texto ambíguo
- [ ] **2.4**: Usei Claude para melhorar meu próprio prompt (Meta-Prompting como coach de prompts)
- [ ] **3.1**: Apliquei o template completo de debugging e eliminei rodadas de clarificação
- [ ] **3.2**: Três Few-Shot examples foram suficientes para Claude extrapolação para 2 casos desconhecidos
- [ ] **3.3**: Combinei Role + CoT + Structured Output e observei a contribuição sinérgica de cada padrão

---

## Próximos Passos

Parabéns! Você completou o **Laboratório Prático de Comandos e Sintaxe de Prompt**. Agora você domina os fundamentos de prompting (4 componentes), 10 padrões avançados, e técnicas de combinação para máxima efetividade.

- **Próximo módulo**: Leia [`04-PADROES-USO/01-ITERACAO-RAPIDA.md`](../04-PADROES-USO/01-ITERACAO-RAPIDA.md) para aprender técnicas de iteração rápida com Claude Code em ciclos reais de desenvolvimento
- **Revisão rápida**: Use o [`CHEAT-SHEET.md`](./CHEAT-SHEET.md) como referência diária para escolher o padrão certo para cada situação de codificação
- **Aprofundamento**: Nos próximos projetos, pratique combinar 2–3 padrões em um único prompt e observe como a qualidade da saída melhora exponencialmente

---

**Criado em**: 2026-05-23 | **Tempo total de prática**: ~50 minutos (trilha completa), ~15 minutos (trilha iniciante)
