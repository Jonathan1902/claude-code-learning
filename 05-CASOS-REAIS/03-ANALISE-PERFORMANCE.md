# Análise de Performance

## Caso 1: Profiling de Python

### Problema
Script de processamento de dados roda em 5 minutos. Target: 1 minuto.

### Prompt
```
Contexto: Python 3.11, pandas, processing dataset 100MB

Script atual demora 5 minutos.
Target: <1 minuto (5x mais rápido)

Código:
[fornecer script completo]

Por favor:
1. Identifique funções lentas (profile)
2. Explique porquê (complexidade, I/O, etc)
3. Sugira otimizações (específicas)
4. Estime speedup esperado
```

### Resultado
Claude:
1. Identifica loops aninhados (O(n²))
2. Vê queries redundantes em loop
3. Sugere:
   - Índices para lookup
   - Vetorização com numpy
   - Caching de resultados
4. Estima 5-10x mais rápido

---

## Caso 2: Query SQL Lenta

### Problema
Endpoint de dashboard timeout (>5s).

### Prompt
```
Contexto: Django ORM, PostgreSQL 14, 100k+ usuários

Endpoint tarda >5s (timeout=5s, é limite)

Query atual (ORM):
[fornecer views.py]

SQL gerado (se souber):
[fornecer EXPLAIN output]

Por favor:
1. Que índices faltam?
2. Há N+1 problem?
3. Pode ser denormalizado?
4. Há cache estratégico?

Target: <500ms
```

### Resultado
Claude sugere:
1. Índices compostos necessários
2. select_related() / prefetch_related()
3. Caching com Redis
4. Query desnormalizada (se relevante)

---

## Caso 3: Memory Leak

### Problema
Aplicação crescendo em memória continuamente.

### Prompt
```
Contexto: Python Flask app, running 24/7

Observação:
- Inicia: 100MB
- Depois 1h: 200MB
- Depois 2h: 300MB
- Stays até restart

Suspeita: Memory leak em handler de requisição

Código relevante:
[fornecer views/handlers]

Como debugar:
1. Qual ferramenta usar?
2. Como identificar leak?
3. Como corrigir?

Não finalizando objetos? Ciclos referência?
```

### Resultado
Claude sugere:
1. Usar `memory_profiler` ou `tracemalloc`
2. Identifica objetos não coletados
3. Propõe fixes (finalizers, circular refs)

---

## Caso 4: Database Performance

### Problema
Dashboard query de analytics roda em 30s.

### Prompt
```
Contexto: 50M transaction records, PostgreSQL

Query atual demora 30s (deve ser <5s)

Query:
[SQL ou ORM]

Índices atuais:
- PK em id
- FK em user_id
- Nenhum outro

Preciso de:
1. Que índices criar?
2. Qual será ganho estimado?
3. Há agregação que possa ser pré-computada?
4. Particionamento ajudaria?

Dados históricos (2+ anos) que crescem 1M/dia
```

### Resultado
Claude sugere:
1. Índices compostos: (user_id, date, amount)
2. Pré-agregação (table `daily_summary`)
3. Particionamento por data (ranges)
4. Estima: 30s → 100-200ms

---

## Caso 5: Frontend Performance

### Problema
Website carrega lentamente (>3s).

### Prompt
```
Contexto: React 18, TypeScript

Performance:
- Lighthouse: 45/100
- Time to interactive: 4s
- Large JS bundle (2MB)

Componentes:
[listar principais]

Por favor:
1. Identifique overhead
2. Code splitting estratégia
3. Lazy loading recomendado
4. Bundle otimização

Estou usando:
- Too many dependencies?
- Renders desnecessários?
```

### Resultado
Claude sugere:
1. Code splitting por rota
2. Lazy load heavy components
3. Tree-shake unused code
4. Imagem optimization
5. Estima: 4s → 1.2s

---

## Metodologia: Performance Audit Completo

### Step 1: Baseline
```
Medir:
- Tempo atual (10s)
- Métrica (requisições/segundo)
- P95 latência
- CPU/Memória usage
```

### Step 2: Profile
```
Com ferramentas:
- Python: cProfile, memory_profiler
- JS: Chrome DevTools, Lighthouse
- DB: EXPLAIN, pg_stat_statements
- Sys: perf, htop
```

### Step 3: Análise
```
Claude analisa output do profile:
- Qual função usa 50%+ tempo?
- Há padrão (I/O, CPU, memory)?
- Isto é otimizável?
```

### Step 4: Otimizações
```
Prioridade:
1. 80/20 (maiores ganhos)
2. Risco/reward (rápido de implementar)
3. Documentado (claro why)
```

### Step 5: Validação
```
Medir novamente:
- Nova baseline
- Comparar com target
- Aceitável?
```

---

## Exemplo Real: 10x Mais Rápido

### Antes
```python
def process_users():
    for user in User.objects.all():  # N queries
        orders = user.orders.all()   # N queries (N+1)
        for order in orders:
            items = order.items.all()  # N*M queries
            total = sum(item.price for item in items)
            order.total = total
            order.save()  # N*M saves
```

Tempo: ~30 segundos para 1k usuários

### Depois
```python
def process_users():
    # 1 query só
    orders = Order.objects.select_related(
        'user'
    ).prefetch_related(
        'items'
    ).all()
    
    # Em memória
    for order in orders:
        total = sum(item.price for item in order.items.all())
        order.total = total
    
    # 1 bulk update
    Order.objects.bulk_update(orders, ['total'], batch_size=1000)
```

Tempo: ~2 segundos (15x mais rápido)

---

## Ferramentas por Linguagem

| Linguagem | Tool | O que mede |
|---|---|---|
| Python | cProfile | CPU time por função |
| Python | memory_profiler | Memory linha por linha |
| JavaScript | Chrome DevTools | CPU, memory, rendering |
| JavaScript | Lighthouse | Web vitals |
| PostgreSQL | EXPLAIN ANALYZE | Query execution plan |
| PostgreSQL | pg_stat_statements | Queries mais caras |

---

**Próximo**: [Documentação](04-DOCUMENTACAO.md)
