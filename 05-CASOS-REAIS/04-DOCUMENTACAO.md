# Geração de Documentação

## Caso 1: Docstrings Automáticas

### Situação
Código Python sem documentação.

### Prompt
```
Contexto: Django project, type hints presentes

Adicione docstrings Google-style a este arquivo:

[fornecer arquivo inteiro]

Requisitos:
- Docstring para cada classe, função, método
- Format: Google (### Args, Returns, Raises)
- Exemplo de uso onde apropriado
- Mencione raises/exceptions
- Não documente óbvio (type hints já dizem)
```

### Resultado
```python
def calculate_discount(price: float, quantity: int) -> float:
    """Calculate discount based on quantity threshold.
    
    Args:
        price: Base price per item (must be positive)
        quantity: Number of items (must be >= 1)
    
    Returns:
        Discounted total price
    
    Raises:
        ValueError: If price < 0 or quantity < 1
    
    Example:
        >>> calculate_discount(100, 5)
        450.0
    """
```

---

## Caso 2: README Completo

### Situação
Novo projeto sem documentação inicial.

### Prompt
```
Contexto: Django REST API project

Crie README.md que cover:
1. Descrição do projeto
2. Tech stack (Python 3.11, Django 4.2, PostgreSQL)
3. Setup/instalação (venv, pip, migrations)
4. Como rodar localmente
5. Endpoints principais (lista breve)
6. Testing (como rodar testes)
7. Deployment (instruções)
8. Estrutura de pastas
9. Como contribuir

Tone: Profissional mas amigável
Target audience: Novos devs no projeto
```

### Resultado
Markdown bem estruturado com:
- Badges (build status, version)
- Table of contents com links
- Code examples
- Instruções passo-a-passo
- Troubleshooting section

---

## Caso 3: API Documentation

### Situação
FastAPI endpoints sem documentação.

### Prompt
```
Contexto: FastAPI app com 20+ endpoints

Gere documentation.md que cover:

Para cada endpoint:
- HTTP verb + path
- Descrição breve
- Request body schema (exemplo JSON)
- Response schema (exemplo JSON)
- Status codes (200, 400, 401, 404, etc)
- Exemplo de curl command
- Rate limits (se houver)

Estruture por resource:
- /users
- /orders
- /products
etc

[fornecer código dos endpoints]
```

### Resultado
Markdown com documentação clara:
```markdown
## GET /api/users/:id

Retrieve user by ID.

### Response (200)
\`\`\`json
{
  "id": "uuid",
  "email": "user@example.com",
  "created_at": "2026-05-23T..."
}
\`\`\`

### cURL
\`\`\`bash
curl https://api.example.com/api/users/123
\`\`\`
```

---

## Caso 4: Architecture Decision Record (ADR)

### Situação
Decisões técnicas espalhadas, sem documentação.

### Prompt
```
Contexto: Decisão de usar Redis para cache vs Memcached

Crie ADR (Architecture Decision Record) que cover:

1. Context: Por que precisava decidir?
2. Decision: Escolhemos Redis
3. Rationale: Por quê? Trade-offs?
4. Consequences: Impacto positivo/negativo
5. Alternatives considered: Memcached, in-memory, etc
6. Related decisions: Outras decisões que dependem desta

Format: Markdown, conciso
```

### Resultado
```markdown
# ADR-001: Use Redis for Session Caching

## Context
App needs fast session cache. Current in-memory grows 
unbounded and doesn't work with multi-process.

## Decision
Use Redis for session cache with automatic TTL.

## Rationale
- Redis is stateful, persistent (snapshots)
- Better than Memcached for our use case (TTL control)
- Simpler than building custom solution

## Consequences
+ Reliable session persistence
+ Horizontal scaling (shared Redis)
- Added dependency
- Redis downtime affects sessions
```

---

## Caso 5: Setup Guide

### Situação
Novo dev não consegue fazer setup local.

### Prompt
```
Contexto: Python project com PostgreSQL, Redis, external APIs

Crie SETUP.md que guide novo dev:

Passos:
1. Prerequisites (o que precisa instalar)
2. Clone repo
3. Virtual env setup
4. Dependências (.env, API keys)
5. Database setup (migrations, seed data)
6. Rodando localmente
7. Troubleshooting (erros comuns)
8. Como saber que deu certo (test suite)

Assuma: Dev é experiente mas novo no projeto
```

### Resultado
Markdown passo-a-passo com:
- Commands exatos
- Error outputs comuns + soluções
- Links para dependências
- Video tutorial (se relevante)
- Contato para suporte

---

## Padrão: Auto-gerar docs em CI

### Conceito
Documentação fica sempre atualizada automaticamente.

### Exemplo
```bash
# CI/CD pipeline (GitHub Actions, etc)
- name: Generate docs
  run: |
    claude-code "Gere README.md baseado em package.json e estrutura"
    # Commits se houver mudanças
```

---

## Tipos de Documentação

| Tipo | Para Quem | Exemplo |
|---|---|---|
| README | Novo usuário/dev | "Como usar este projeto" |
| API Docs | Consumidor da API | "Endpoints disponíveis" |
| Architecture | Tech lead | "Por que estruturado assim" |
| Runbook | DevOps/SRE | "Como deployar, troubleshoot" |
| Changelog | Usuários | "O que mudou em v2.0" |
| ADR | Time técnica | "Decisões importantes" |

---

## Ferramenta de Documentação Recomendada

| Ferramenta | Linguagem | Uso |
|---|---|---|
| MkDocs | Markdown | Site de docs com busca |
| Sphinx | reStructuredText | Docs profissionais (Python) |
| Swagger/OpenAPI | YAML/JSON | API documentation |
| Notion/Confluence | Web | Documentação colaborativa |
| GitHub Pages | Markdown | Site estático |

---

**Próximo**: [Automação DevOps](05-AUTOMACAO-DEVOPS.md)
