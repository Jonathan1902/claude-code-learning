# Exemplos Reais de Prompts

## Exemplo 1: Debugar Erro TypeError

### Situação
Script Python com erro: `TypeError: unsupported operand type(s)`

### Prompt Efetivo

```
Contexto: Script Python 3.11, usando pandas para processar CSV

Erro que recebo:
TypeError: unsupported operand type(s) for +: 'str' and 'int'
  File "process.py", line 42, in calculate_total

Aqui está o código (linhas 35-50):
[colar código do arquivo]

Qual é a raiz do problema? Como corrigir?
```

### Por que funciona
✅ Fornece contexto (Python 3.11, pandas)
✅ Mostra erro exato + local
✅ Fornece código relevante
✅ Pergunta clara

### Resultado Esperado
Claude vai:
1. Identificar linha 42
2. Ver que está somando string + int
3. Propor conversão com int() ou casting

---

## Exemplo 2: Refatorar Código Repetitivo

### Situação
3 métodos com lógica muito parecida

### Prompt Efetivo

```
Contexto: Django project, Python 3.11, type hints required

Tenho 3 métodos com lógica repetida. Quero extrair em uma função comum.

Aqui estão os 3 métodos:
[colar código dos 3 métodos]

Como fazer DRY (Don't Repeat Yourself)?
Requisitos:
- Usar type hints
- Manter compatibilidade com views existentes
- Adicionar docstring
```

### Por que funciona
✅ Mostra código duplicado
✅ Define objetivo (DRY)
✅ Lista requisitos
✅ Contexto claro

### Resultado Esperado
Claude vai:
1. Identificar padrão comum
2. Criar função base
3. Refatorar 3 métodos para usar função
4. Adicionar types e docstrings

---

## Exemplo 3: Análise de Performance

### Situação
Script que processa 1M linhas de dados, lento

### Prompt Efetivo

```
Contexto: Python 3.11, processing large CSV (1M rows)

Script está muito lento (~5 min para processar).
Quero entender onde está o bottleneck.

Código:
[colar arquivo completo ou função principal]

Por favor:
1. Identifique operações O(n²) ou piores
2. Me mostre timing esperado
3. Sugira otimizações (sem mudar lógica)
4. Estime quanto mais rápido ficaria

Depois vou rodá-las para confirmar.
```

### Por que funciona
✅ Define problema (lentidão)
✅ Fornece código completo
✅ Pede análise específica (complexidade)
✅ Pede estimativa
✅ Oferece feedback futura

### Resultado Esperado
Claude vai:
1. Analisar loops aninhados
2. Propor índices/dicts
3. Sugerir pandas operations
4. Estimar 10-50x mais rápido

---

## Exemplo 4: Teste Automatizado

### Situação
Função complexa sem testes

### Prompt Efetivo

```
Contexto: Django 4.2, pytest, testing should cover edge cases

Preciso de testes para esta função:

def calculate_discount(price: float, quantity: int, vip: bool) -> float:
    [código complexo com várias condições]
    return discounted_price

Casos de teste esperados:
- Quantidade normal com desconto
- VIP com desconto extra
- Quantidade 0 (edge case)
- Preço negativo (erro esperado)
- Desconto >100% (error handling)

Crie testes pytest cobrindo todos os casos.
```

### Por que funciona
✅ Fornece função exata
✅ Define casos esperados
✅ Menciona edge cases
✅ Especifica framework (pytest)

### Resultado Esperado
Claude vai:
1. Criar file test_calculate_discount.py
2. Testar casos normais
3. Testar edge cases
4. Testar error cases
5. Coverage >90%

---

## Exemplo 5: Gerar Documentação

### Situação
Código sem docstrings ou README

### Prompt Efetivo

```
Contexto: Python project, using type hints, Google-style docstrings

Adicione documentação a este arquivo:

[colar arquivo inteiro]

Requisitos:
- Docstring Google-style para cada função/classe
- Incluir Args, Returns, Raises
- Adicionar docstring de módulo no topo
- Manter comentários onde lógica não é óbvia
```

### Por que funciona
✅ Fornece arquivo completo
✅ Especifica estilo (Google)
✅ Define o que documentar
✅ Contexto claro

### Resultado Esperado
Claude vai:
1. Adicionar docstring do módulo
2. Documentar cada função
3. Incluir tipos de return
4. Notar exceptions

---

## Exemplo 6: Implementar Feature Nova

### Situação
Precisa adicionar autenticação a API

### Prompt Efetivo

```
Contexto:
- FastAPI project, Python 3.11
- PostgreSQL banco de dados
- Use Pydantic v2 para models
- No external auth libraries (implement ourselves)

Feature: Adicionar autenticação com JWT

Requisitos:
1. Endpoint /auth/register (username, password)
2. Endpoint /auth/login (username, password) → retorna JWT
3. Endpoint /auth/refresh (refresh_token) → novo JWT
4. Middleware para validar JWT em endpoints protegidos

DB schema já tem table 'users' com id, username, hashed_password

Defina:
- User model (Pydantic)
- Auth endpoints
- JWT token manager
- Middleware

Não use libraries prontas, quero entender a implementação.
```

### Por que funciona
✅ Contexto técnico completo
✅ Requirements numerados e claros
✅ Escopo bem definido
✅ Restrições explícitas (no libraries)
✅ Schema de BD informado

### Resultado Esperado
Claude vai:
1. Criar Pydantic models
2. Implementar token generation/validation
3. Criar endpoints
4. Criar middleware
5. Com type hints e docstrings

---

## Exemplo 7: Comparação de Abordagens

### Situação
Dúvida entre SQL raw vs ORM

### Prompt Efetivo

```
Contexto: Django ORM, PostgreSQL, performance-critical dashboard

Minha query busca usuários com filtros complexos.
Tenho 2 abordagens:

Abordagem 1: Django ORM (nested filters)
[mostrar código ORM complexo]

Abordagem 2: Raw SQL
[mostrar query SQL)

Para meu caso (50k usuários, dashboard):
- Qual é mais rápido?
- Qual é mais maintível?
- Qual escolho? Por quê?

Context: Dashboard carrega a cada 30 segundos
```

### Por que funciona
✅ Mostra ambas abordagens
✅ Define contexto (performance)
✅ Pede comparação
✅ Oferece parâmetros de decisão

### Resultado Esperado
Claude vai:
1. Comparar velocidade
2. Comparar manutenibilidade
3. Recomendar uma
4. Explicar reasoning

---

## Exemplo 8: Code Review

### Situação
Pull request que quer review

### Prompt Efetivo

```
Contexto: Python project, security-sensitive (payment processing)

Criei PR que adiciona payment processing. 
Quero verificar:

1. Segurança (OWASP top 10 relevantes)
2. Performance
3. Error handling
4. Code quality

Código da função principal:
[colar PR changes]

Levante problemas ou aprove?
```

### Por que funciona
✅ Contexto importante (payment = segurança crítica)
✅ Critérios específicos de review
✅ Código fornecido

### Resultado Esperado
Claude vai:
1. Verificar input validation
2. Verificar secret management
3. Sugerir error handling
4. Apontar issues ou aprovar

---

## Exemplo 9: Troubleshooting

### Situação
Teste falhando aleatoriamente (flaky)

### Prompt Efetivo

```
Contexto: Pytest, Django test database, tests são flaky (50% falham)

Teste falha aleatoriamente:

def test_user_creation():
    user = User.objects.create(username="test")
    time.sleep(0.1)  # Hack para "fix"
    assert User.objects.filter(username="test").count() == 1

Falha: AssertionError: 1 != 0

Pista: Funciona se adiciono time.sleep() antes do assert
Isso indica problema de timing/async

Diagnóstico: O que é o real problema?
Como "fix" corretamente?
```

### Por que funciona
✅ Mostra sintoma (flaky test)
✅ Fornece código exato
✅ Oferece pista (sleep "fix")
✅ Pergunta diagnóstico

### Resultado Esperado
Claude vai:
1. Identificar race condition ou
2. Problema de transação de BD
3. Propor fix correto (fixtures, teardown)
4. Explicar por que sleep "funciona"

---

## Exemplo 10: Otimização Avançada

### Situação
API endpoint lento, causa timeout

### Prompt Efetivo

```
Contexto:
- FastAPI, PostgreSQL, 100k+ produtos
- Endpoint /products?category=X&price=Y (usado 1000x/min)
- Atualmente: ~500ms (TIMEOUT = 5s, OK mas perto do limite)
- Quer: <100ms idealmente

Código do endpoint:
[colar endpoint code]

Query database:
[colar SQL ou ORM query]

Índices atuais:
- id (PK)
- category (index)

Performance profile (se tiver): [colar]

Como posso otimizar para <100ms?
```

### Por que funciona
✅ Contexto técnico completo
✅ Problema quantificado (500ms → 100ms)
✅ Usa real (1000x/min)
✅ Índices atuais informados
✅ Convida profile se tiver

### Resultado Esperado
Claude vai:
1. Propor índices adicionais (compound index)
2. Sugerir query optimization
3. Propor caching
4. Estimar ganho de performance

---

## Template Geral

```
**Contexto:**
[Tecnologias, versões, constraints]

**Problema:**
[O que está acontecendo]

**Código:**
[Arquivo relevante ou snippet]

**Objetivo:**
[O que quer conseguir]

**Restrições:**
[Não fazer X, manter Y]

**Extras:**
[Performance profile, dados adicionais, hints]

**Pergunta:**
[O que quer saber/fazer]
```

---

**Próximo**: [Cheat Sheet](CHEAT-SHEET.md)
