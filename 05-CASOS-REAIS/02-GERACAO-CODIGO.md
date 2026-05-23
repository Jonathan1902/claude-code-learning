# Geração de Código com Claude Code

## Caso 1: REST API Completa

### Situação
Precisa de API CRUD para entidade de BD.

### Prompt
```
Contexto: FastAPI, PostgreSQL, Python 3.11

Tarefa: Criar API CRUD completa para Produto

Requisitos:
- GET /products (listar paginado)
- GET /products/{id} (detalhe)
- POST /products (criar)
- PUT /products/{id} (atualizar)
- DELETE /products/{id} (remover)

Schema Produto:
- id (UUID)
- name (string)
- price (decimal)
- stock (int)
- created_at (datetime)

Implementar:
- Pydantic models (request/response)
- SQLAlchemy ORM models
- Error handling (404, 422, etc)
- Type hints completos
- Docstrings

Estrutura:
- models.py (DB schema)
- schemas.py (Pydantic)
- main.py (endpoints)
```

### Resultado
Claude gera:
1. SQLAlchemy Product model
2. Pydantic ProductCreate, ProductResponse
3. Todos os 5 endpoints
4. Validações apropriadas
5. Error handling

---

## Caso 2: Testes Automatizados

### Situação
Função complexa sem testes. Gerar suite completa.

### Prompt
```
Contexto: Pytest, Django, >80% coverage

Função para testar:
def calculate_discount(price: float, user_type: str, quantity: int) -> float:
    [código complexo com múltiplas condições]

Casos de teste:
1. Normal user, 1 item → 0% discount
2. Premium user, 1 item → 10% discount
3. Bulk (10+ items) → 5% discount
4. Premium + Bulk → 15% discount
5. Negative price → ValueError
6. Invalid user_type → ValueError

Gerar test_discount.py com:
- Fixtures necessárias
- Parametrized tests
- Edge cases
- Assertions claras
```

### Resultado
Claude gera:
```python
import pytest
from discount import calculate_discount

@pytest.mark.parametrize("price,user_type,qty,expected", [
    (100, "normal", 1, 100),
    (100, "premium", 1, 90),
    (100, "normal", 10, 95),
    (100, "premium", 10, 85),
])
def test_calculate_discount(price, user_type, qty, expected):
    assert calculate_discount(price, user_type, qty) == expected

def test_invalid_price():
    with pytest.raises(ValueError):
        calculate_discount(-100, "normal", 1)

def test_invalid_user_type():
    with pytest.raises(ValueError):
        calculate_discount(100, "invalid", 1)
```

---

## Caso 3: Deploy Script Automatizado

### Situação
Deploy manual é propenso a erro. Gerar script robusto.

### Prompt
```
Contexto: Python/Django app, PostgreSQL, Nginx reverse proxy

Tarefa: Deploy script que:
1. Faz backup do banco
2. Puxa latest git
3. Instala dependências
4. Roda migrations
5. Coleta static files
6. Restarts gunicorn
7. Testa health check
8. Rollback se falhar

Requisitos:
- Logging em arquivo
- Email alert se falhar
- Dry-run mode
- Rollback automático
- Testar depois que app está up

Argumentos:
deploy.py --env production --no-backup (skip backup)
deploy.py --rollback (volta para anterior)
```

### Resultado
Claude gera script que:
1. Validações pré-deploy
2. Backup com timestamp
3. Execução passo-a-passo
4. Logging detalhado
5. Health check
6. Rollback em caso de erro

---

## Caso 4: CLI Tool

### Situação
Precisa de ferramenta de linha de comando para tarefas repetitivas.

### Prompt
```
Contexto: Python Click library, PostgreSQL

CLI Tool: user-manager

Comandos:
1. user create --email X --name Y
2. user list [--status active|inactive]
3. user reset-password --email X
4. user delete --email X [--confirm]
5. user import --file users.csv
6. user export --format json|csv

Requisitos:
- Validação de input
- Confirmação para operações destruidoras
- Feedback claro (sucesso/erro)
- Progress bar para bulk ops
- Connection pool para DB
```

### Resultado
Claude gera CLI tool com:
1. Click app structure
2. Subcomandos para cada operação
3. Validações apropriadas
4. Confirmação interativa
5. Pretty-print output
6. Error handling robusto

---

## Caso 5: Micro-frontend Component

### Situação
Precisa de React component reutilizável.

### Prompt
```
Contexto: React 18, TypeScript, TailwindCSS

Componente: Modal Dialog

Props:
- isOpen: boolean
- title: string
- content: ReactNode
- onClose: () => void
- onConfirm: () => void
- confirmLabel?: string (default: "Confirmar")
- cancelLabel?: string (default: "Cancelar")

Requisitos:
- Acessibilidade (keyboard escape close)
- Animation smooth (fade in/out)
- Backdrop click fecha
- Focus trap dentro modal
- TypeScript types
```

### Resultado
Claude gera:
```typescript
interface ModalProps {
  isOpen: boolean;
  title: string;
  content: React.ReactNode;
  onClose: () => void;
  onConfirm: () => void;
  confirmLabel?: string;
  cancelLabel?: string;
}

export function Modal({ isOpen, title, ... }: ModalProps) {
  // Implementação com acessibilidade, animações, etc
}
```

---

## Padrão: Geração com TDD

### 1. Teste Primeiro
```
Claude: "Qual é seu código de teste?"
Você: [fornece test_feature.py]
```

### 2. Claude Implementa
```
Claude vê que testes precisam de Feature class
e gera implementação que passa nos testes
```

### 3. Valida Cobertura
```
Claude roda pytest --cov
Garante >80% coverage
```

---

## Benchmarks

| Tipo | Tempo |
|---|---|
| API CRUD 5 endpoints | 1-2 min |
| Test suite 10 casos | 2-3 min |
| Deploy script robusto | 5-10 min |
| CLI tool 5 comandos | 5-10 min |
| React component avançado | 3-5 min |

---

**Próximo**: [Análise de Performance](03-ANALISE-PERFORMANCE.md)
