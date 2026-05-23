# Padrões de Análise com Claude Code

## Quando Usar Análise

Análise é **não-executável**: Claude lê e opina, sem rodar código.

```
✅ Análise: "Este código é seguro?"
✅ Análise: "Qual é a complexidade O()?"
✅ Análise: "Há memory leaks?"

❌ Não é análise: "Rode este código"
❌ Não é análise: "Crie função X"
```

---

## 1. Análise de Segurança

### O Que Procurar
- SQL injection
- XSS (Cross-site scripting)
- CSRF (Cross-site request forgery)
- Broken authentication
- Sensitive data exposure
- Missing input validation
- Hardcoded secrets

### Prompt
```
Contexto: Web app Django com autenticação

Analise este código para vulnerabilidades OWASP Top 10:

[fornecer views.py ou models.py]

Foque em:
- Input validation
- Secret management
- Query safety

Levante problemas encontrados.
```

### Exemplo
```python
def login(request):
    username = request.POST['username']  # ❌ Sem validation
    password = request.POST['password']
    
    # ❌ SQL injection risk
    user = User.objects.raw(
        f"SELECT * FROM users WHERE username='{username}'"
    )
    
    # ❌ Senha em plaintext (devia ser hash)
    if user.password == password:
        return redirect('home')
```

Claude identifica:
1. Sem validation de entrada
2. SQL injection na query raw
3. Senha não hasheada

---

## 2. Análise de Performance

### O Que Procurar
- O(n²) ou pior loops
- Queries repetidas (N+1 problem)
- Memory usage excessivo
- Operações bloqueantes desnecessárias
- Cache não utilizado

### Prompt
```
Contexto: Django API, 100k+ usuários, chamada 1000x/min

Analise performance deste endpoint:

[fornecer views.py]

Problemas esperados:
- Loops aninhados
- Queries não otimizadas
- Falta de índices

Estime impacto (quanto mais lento).
```

### Exemplo
```python
def get_user_posts(request, user_id):
    user = User.objects.get(id=user_id)
    
    # ❌ N+1 problem: query por post, comment por comment
    posts = user.posts.all()
    for post in posts:
        # Isso executa query para cada post
        comments = post.comments.all()
        for comment in comments:
            # Mais uma query por comment
            comment.author.name
    
    return render(request, 'posts.html', {'posts': posts})
```

Claude identifica:
1. N queries para posts
2. N queries para comments
3. N*M queries para authors
Total: O(n²) queries

---

## 3. Análise de Qualidade de Código

### O Que Procurar
- Variáveis não usadas
- Código morto
- Duplicação
- Funções muito longas
- Nomes ruins
- Falta de types
- Falta de documentação

### Prompt
```
Contexto: Python project, type hints required, 80%+ test coverage

Faça code review deste arquivo:

[fornecer arquivo]

Critérios:
- Type hints completude
- Docstrings adequadas
- Nomes claros
- DRY (Don't Repeat Yourself)
- SOLID principles

Sugira melhorias.
```

### Exemplo
```python
def process_data(x):  # ❌ Nome ruim, sem type
    y = []  # ❌ Nome ruim
    for i in x:  # ❌ Sem type
        if i > 5:
            z = i * 2  # ❌ Sem docstring explicando
            y.append(z)
    return y

def process_data_2(a, b):  # ❌ Duplicado (similar)
    result = []
    for item in a:
        if item > b:
            result.append(item * 2)
    return result
```

Claude identifica:
1. Nomes obscuros
2. Sem type hints
3. Sem docstrings
4. Duplicação de lógica
5. Função muito curta (ok) mas impenetrável

---

## 4. Análise de Arquitetura

### O Que Procurar
- Separação de responsabilidades
- Acoplamento alto
- Dependências circulares
- Padrões não seguidos
- Escalabilidade

### Prompt
```
Contexto: Microservices, FastAPI, event-driven

Analise a arquitetura deste service:

[fornecer estrutura de pastas + principais módulos]

Questões:
- Está bem separado (concerns)?
- Há acoplamento desnecessário?
- Escalaria bem (10x usuários)?

Sugira refatoração se necessário.
```

---

## 5. Análise de Decisões Técnicas

### O Que Procurar
- Trade-offs claros?
- Alternativas consideradas?
- Documentadas as razões?

### Prompt
```
Contexto: Sistema de autenticação nova

Quero validar minha decisão de usar:
- JWT com refresh tokens (não sessions)
- Redis para cache (não memória)
- PostgreSQL FTS (não Elasticsearch)

São boas decisões? Trade-offs?
Existe melhor alternativa?
```

Claude oferece:
1. Prós/contras de cada
2. Quando falham
3. Alternativas
4. Recomendação

---

## 6. Análise de Escalabilidade

### O Que Procurar
- Gargalos óbvios
- Estruturas de dados ineficientes
- Falta de caching
- Índices de BD
- Particionamento

### Prompt
```
Contexto: Sistema de recomendação, 100M+ usuários

Código atual processa recomendações real-time.
Hoje: <2s por requisição (aceitável)
Meta: <500ms para 10x usuários (desafiador)

Como escalar sem major refactor?

[fornecer código + queries]
```

Claude sugere:
1. Índices específicos
2. Pré-computação
3. Caching agressivo
4. Arquitetura distribuída
5. Estimativa de ganho

---

## 7. Análise Comparativa

### O Que Procurar
- Qual abordagem é melhor
- Para meu contexto específico

### Prompt
```
Contexto: Django projeto, 50k usuários

Preciso armazenar sessões. Opções:

1. Banco de dados (default Django)
2. Redis (mais rápido)
3. Memcached (simples)
4. JWT (stateless)

Qual escolho? Prós/contras?
```

Claude compara:
| Opção | Velocidade | Escalabilidade | Complexidade |
|---|---|---|---|
| DB | 🟡 | 🟡 | 🟢 |
| Redis | 🟢 | 🟢 | 🟡 |
| JWT | 🟢 | 🟢 | 🟡 |

---

## Prompt Template para Análise

```
Contexto:
- [Tecnologias]
- [Escala: N usuários, X requisições/min]
- [Constraints: latência, custo, etc]

Código:
[fornecer arquivo ou trecho]

Tipo de Análise:
- [ ] Segurança
- [ ] Performance
- [ ] Qualidade
- [ ] Arquitetura

Foco:
- [O que é mais importante]

Questão:
- [O que quer saber]
```

---

## Exemplo Completo: Análise Multi-Critério

```
Contexto:
- Django 4.2
- 50k usuários ativos
- 500 requisições/segundo pico
- 99.99% uptime SLA
- PCI compliance (dados de pagamento)

Código (user_auth.py):
[80 linhas]

Analise em relação a:
1. Segurança (PCI compliance)
2. Performance (<100ms SLA)
3. Escalabilidade (10x crescimento)
4. Qualidade (manutenibilidade)

Resultado:
- Vulnerabilidades descobertas
- Problemas de performance
- Como refatorar
- Prioridade de fixes
```

---

## Quando Análise Falha

### ❌ Não consegue sem contexto extra:
```
"Este código é bom?"
(Muito vago, é bom para quê?)

"Quanto vai custar?"
(Não sabe escala, infra, etc)
```

### ✅ Corrija fornecendo contexto:
```
"Este código é bom para Dashboard real-time
com 100k usuários? Performance é crítica."

"Quanto vai custar em AWS?
1. Isso roda 10 horas/dia
2. API chama 100x/min
3. Dados crescem 1GB/mês"
```

---

**Voltar**: [Padrões de Uso](01-ITERACAO-RAPIDA.md)
