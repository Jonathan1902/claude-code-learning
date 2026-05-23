# Quando Fornecer Especificações Detalhadas

## O Dilema

Quanto contexto fornecer?

```
❌ Pouco: Claude chuта, muitas iterações
✅ Certo: Contexto relevante, solução em 1-2 iterações
❌ Muito: Tokens desperdiçados, resposta lenta
```

---

## Framework de Decisão

### Use Especificação Detalhada Quando:

#### 1. Requisitos são Complexos
```
❌ Simples: "Crie validador de email"
(Claude sabe o padrão de regex)

✅ Complexo: "Validador de email que:
- Rejeita + dispos
- Aceita subdomínios profundos
- Bloqueia domínios conhecidos de tempmail
- Retorna score de confiança 0-1"

Precisa de especificação
```

#### 2. Decisões Importantes Já Foram Tomadas
```
"Vamos usar:
- Django ORM (não raw SQL)
- PostgreSQL (não SQLite)
- Caching com Redis (não memória)
- Pydantic (não dict)"

CLAUDE.md lista essas decisões
```

#### 3. Há Integrações com Código Existente
```
"Novo endpoint deve:
- Usar View existente em views.py
- Reaprovitar Serializer de User
- Seguir middleware de autenticação"

Forneça código existente
```

#### 4. Performance ou Segurança são Críticas
```
"Este endpoint é chamado 10k vezes/min.
Deve responder em <50ms.
Dados incluem info de pagamento (PCI compliance)"

Especifique requisitos não-funcionais
```

---

## O que Fornecer em CLAUDE.md

CLAUDE.md é o lugar perfeito para contexto duradouro.

### Exemplo Completo

```markdown
# Projeto: E-commerce API

## Contexto Técnico
- Framework: Django 4.2
- Database: PostgreSQL 14
- Cache: Redis
- Broker: Celery
- Python: 3.11+

## Decisões Arquiteturais Fundamentais
1. ORM: Django ORM only (nunca raw SQL)
2. Auth: JWT + refresh tokens (não sessions)
3. Async: Celery para tasks (não asyncio)
4. Search: PostgreSQL FTS (não Elasticsearch)
5. Storage: S3 (não filesystem)

## Padrões de Código
- Type hints: OBRIGATÓRIO
- Docstrings: Google-style para tudo
- Formatação: Black + Isort
- Linting: Ruff com config.toml
- Testing: Pytest com >80% coverage

## Convenções de Naming
- Classes: PascalCase (User, OrderItem)
- Functions: snake_case (get_user, create_order)
- Constants: SCREAMING_SNAKE_CASE (MAX_RETRIES)
- Private: _leading_underscore (_internal_helper)

## Padrões de View/Serializer
```python
# Todas as Views herdam de GenericViewSet
# Todos os Serializers usam Meta class com fields explícitos
# Validação: sempre usar validators no Serializer
```

## Database Schema Patterns
- Timestampado: created_at, updated_at em tudo
- Soft delete: deleted_at field (nunca DELETE)
- Foreign keys: on_delete=CASCADE ou PROTECT explícito

## API Response Format
```json
{
  "success": true,
  "data": {...},
  "error": null,
  "timestamp": "2026-05-23T10:30:00Z"
}
```

## Error Handling
- Valide entrada em Views
- Não exponha stack traces (log internamente)
- Sempre retorne status code apropriado

## Performance SLAs
- Endpoint padrão: <200ms (P95)
- Endpoint crítico: <50ms (P95)
- Background task: <5 min (P95)
- Cache key: invalidar com versão

## Restrições Importantes
- ❌ Nunca modificar User.is_active (usa soft delete)
- ❌ Nunca DELETE (usar soft delete)
- ❌ Nunca transaction sem necessidade (overhead)
- ✅ Sempre logar änderungen de estado

## Ferramentas e Versões
- Django: 4.2.x (LTS)
- DRF: 3.14.x
- Celery: 5.3.x
- Redis: 7.0+
- PostgreSQL: 14.0+
```

### Benefício
```
Novo prompt sem CLAUDE.md:
"Crie endpoint que tira 10 linhas explicando padrões"

Com CLAUDE.md:
"Crie endpoint /api/users/:id/orders"
Claude já sabe tudo: types, docstrings, formato resposta, etc
```

---

## O que Fornecer no Prompt

### Arquivos do Projeto
```
SIM: Forneça arquivos existentes que:
- Definem estrutura (models.py, views.py)
- Contem código que vai integrar
- Mostram padrões do projeto

NÃO: Forneça tudo
- Só arquivos relevantes
- Máximo 3-4 arquivos por prompt
```

### Exemplos
```
SIM: "Aqui está User model para referência"

NÃO: "Aqui está código inteiro de 20 arquivos"
```

### Especificação de Requisitos
```
SIM: "Preciso que endpoint:
- Retorna lista paginada (50 itens por página)
- Filtrável por status
- Ordenável por data
- Requer autenticação
- Rate limit 1000/hora"

NÃO: "Crie um endpoint"
```

---

## Exemplo: Com vs Sem Especificação

### ❌ SEM Especificação (improdutivo)

```
VOCÊ: "Crie checkout"

CLAUDE: "Entendi, mas preciso esclarecer:
- Qual payment gateway? (Stripe? PayPal?)
- Precisa enviar email de confirmação?
- Qual validação de CVC?
- Divide pagamento em partes?
- Qual taxa de conversão para BRL?"

VOCÊ: "Stripe, sim email, CVC sim, não divide, 1 BRL = X USD"

CLAUDE: "Agora outro detalhe:
- Qual moeda principal?
- Refund automaticamente ou manual?
..."

[5-10 iterações para esclarecimentos]
```

### ✅ COM Especificação (produtivo)

```
VOCÊ: "Crie checkout:

Requisitos:
- Payment gateway: Stripe
- Moedas: BRL + USD (USD é default)
- Validação CVC obrigatória
- Sem split (pagamento único)
- Email de confirmação com recibo
- Refund manual (admin dashboard)
- Guarde transaction_id

Integração:
- Order model já existe (ver models.py)
- StripeClient já existe (ver stripe_handler.py)
- Email template: usar existing
- Error handling: usar nossa exception class

[forneça 2 arquivos relevantes]"

CLAUDE: "Entendido, vou criar. Terei [X] em 30 segundos"

[implementação exata, primeira tentativa]
```

---

## Template de Especificação Detalhada

```
# Feature: [Nome]

## Requisitos Funcionais
1. [O que deve fazer]
2. [Casos normais]
3. [Edge cases]

## Requisitos Não-Funcionais
- Performance: [SLA]
- Security: [level]
- Availability: [uptime]

## Restrições
- ❌ Não fazer X
- ✅ Deve usar Y

## Integração
- Arquivo A: [relação]
- Arquivo B: [relação]

## Formato Esperado
```json
{
  "type": "schema",
  "field": "type"
}
```

## Testing
- Casos a cobrir: [lista]
- Coverage mínimo: [%]

## Referências
- Documento: [link]
- Decisão ADR: [link]
```

---

## Quando Iteração é Melhor

### Use Iteração (Menos Contexto) Quando:

1. **Exploração**: Não sabe exatamente o que quer
   ```
   "Como posso autenticar usuários?"
   (Claude oferece opções, você escolhe)
   ```

2. **Prototipagem**: Teste de conceito
   ```
   "Teste rápido com mock data"
   (Não precisa de spec completa)
   ```

3. **Tarefa Simples**: Óbvia e direta
   ```
   "Refatore este método"
   (Não precisa spec detalhada)
   ```

4. **Budget de Tokens Baixo**: Contexto é caro
   ```
   (Forneça o mínimo, deixe Claude perguntar)
   ```

---

## Checklist: Especificação Adequada?

- [ ] Requisitos estão claros?
- [ ] Edge cases foram mapeados?
- [ ] Integração com código existente é clara?
- [ ] SLAs foram definidos (se crítico)?
- [ ] Formato de resposta está especificado?
- [ ] Padrões do projeto estão em CLAUDE.md?
- [ ] Arquivos relevantes foram fornecidos?

Se SIM em 5+: Especificação é adequada

---

**Próximo**: [Debugging](03-DEBUGGING.md)
