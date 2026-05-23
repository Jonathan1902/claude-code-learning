# Como Debugar com Claude Code

## Passo 1: Isolar o Problema

### Minimize
```
❌ Grande (500 linhas, vago):
"Meu código não funciona"

✅ Pequeno (10 linhas, específico):
"Função X retorna None quando devia retornar User
Input: user_id=999"
```

### Reproduzir Consistentemente
```
Anote:
- Input exato (números, strings)
- Output recebido
- Output esperado
- Frequência (sempre? aleatório?)
```

### Exemplo
```python
# Meu código
def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)

# Problema
get_user(999)
# Esperado: levanta User.DoesNotExist
# Recebido: levanta AttributeError (None.id)
# Frequência: sempre quando user_id não existe
```

---

## Passo 2: Forneça Evidência

### Stack Trace Completo
```python
# Isso:
TypeError: unsupported operand type(s)

# Não ajuda.

# Forneça completo:
Traceback (most recent call last):
  File "payment.py", line 42, in process_payment
    result = amount + currency
TypeError: unsupported operand type(s) for +: 'float' and 'str'
```

### Código Relevante
```python
# ❌ Grande demais:
[arquivo inteiro de 500 linhas]

# ✅ Focado:
def process_payment(amount: float, currency: str):
    result = amount + currency  # ❌ Aqui dá erro
    return result

# ✅ Com contexto:
process_payment(100, "USD")
# Erro: TypeError...
```

### Input/Output
```
❌ Vago:
"Erro ao processar"

✅ Específico:
Input: amount=100, currency="USD"
Expected: {"amount": 100, "currency": "USD"}
Received: TypeError at line 42
```

---

## Passo 3: Análise com Claude

### Claude Vê Código
Claude lê sua função e vê:
```python
result = amount + currency
# amount é float, currency é string
# Não dá somar float + string → TypeError
```

### Claude Propõe Hipóteses
```
1. Conversão de tipo faltando?
2. Suposição errada sobre tipo?
3. API mudou signature?
```

### Você Valida
```
"Sim, amount é float, currency é string.
Precisa converter currency para float antes?"
```

### Claude Confirma e Fixa
```python
# Fix:
amount_value = float(currency)  # Converte "USD" para número
# Mas... "USD" não é número!

# Verdadeiro fix:
# Talvez currency não devia ser string?
# Ou precisa lookup de taxa de câmbio?
```

---

## Estratégias de Debugging

### 1. Divide and Conquer (Divide para Conquistar)

Teste parte por parte:
```python
# Seu código:
def calculate_total(items: list) -> float:
    subtotal = sum(item['price'] * item['qty'] for item in items)
    tax = subtotal * 0.1
    discount = apply_discount(subtotal)
    return subtotal + tax - discount

# Teste cada parte:
item = {'price': 100, 'qty': 2}
subtotal_test = item['price'] * item['qty']  # Funciona?
tax_test = subtotal_test * 0.1  # Funciona?
discount_test = apply_discount(subtotal_test)  # Aqui quebra?
```

**Descoberta**: Erro está em `apply_discount()`

### 2. Print Debugging

```python
def calculate_total(items: list) -> float:
    subtotal = sum(item['price'] * item['qty'] for item in items)
    print(f"DEBUG: subtotal = {subtotal}")  # Vê valor intermediário
    
    tax = subtotal * 0.1
    print(f"DEBUG: tax = {tax}")
    
    discount = apply_discount(subtotal)
    print(f"DEBUG: discount = {discount}")
    
    return subtotal + tax - discount

# Output:
# DEBUG: subtotal = 200
# DEBUG: tax = 20
# DEBUG: discount = <None tipo aqui>  ← PROBLEMA
```

### 3. Breakpoint Debugging

Para Python:
```python
def calculate_total(items: list) -> float:
    subtotal = sum(...)
    breakpoint()  # Pausa aqui
    tax = ...
    return ...

# Claude executa e vê estado da memória
```

### 4. Type Checking

```python
def calculate_total(items: list) -> float:
    subtotal = sum(item['price'] * item['qty'] for item in items)
    
    # Valide tipos:
    assert isinstance(subtotal, (int, float)), f"subtotal must be number, got {type(subtotal)}"
    
    tax = subtotal * 0.1
    return subtotal + tax
```

---

## Exemplo: Debugging Real

### Seu Relato
```
Função `validate_email` retorna False para emails válidos.

Código:
def validate_email(email: str) -> bool:
    pattern = r"^[a-z]+@[a-z]+\.[a-z]+$"
    return bool(re.match(pattern, email))

Teste:
- validate_email("user@example.com") → True ✅
- validate_email("user.name@example.com") → False ❌ (deveria ser True)
- validate_email("user+tag@example.com") → False ❌ (deveria ser True)

Qual é o problema?
```

### Claude Vê Problema
```
Padrão regex: ^[a-z]+@[a-z]+\.[a-z]+$

Aceita: abc@def.com (✅)
Rejeita: user.name@example.com (❌ porque tem ponto em 'user.name')
Rejeita: user+tag@example.com (❌ porque tem + que não está no padrão)

O regex é muito restritivo!
```

### Claude Sugere
```python
# Melhor padrão:
pattern = r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}$"

# Ou use library:
from email_validator import validate_email, EmailNotValidError

def validate_email(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False
```

### Você Valida
```
Testei novo padrão:
- user@example.com ✅
- user.name@example.com ✅
- user+tag@example.com ✅
- invalid.email ❌

Funcionou!
```

---

## Ferramentas de Debug

### Python
```
- pdb: breakpoints e step through
- ipdb: versão melhor de pdb
- pudb: TUI debugger
- memory_profiler: memory leaks
- cProfile: performance profiling
```

### Bash
```
- set -x: mostra cada comando
- set -e: sai em qualquer erro
- echo statements: output intermediário
- shellcheck: lint para shell scripts
```

### Git
```
git log --all --oneline  # Ver histórico completo
git blame filename       # Quem mexeu em cada linha
git bisect              # Encontrar commit que quebrou
```

---

## Checklist de Debug

- [ ] Isolei o problema (função específica)?
- [ ] Reproduço consistentemente?
- [ ] Forneci stack trace completo?
- [ ] Forneci código relevante (~50 linhas max)?
- [ ] Forneci input/output esperado vs recebido?
- [ ] Já testei partes isoladamente?
- [ ] Removi print/debugging statements antes de pedir help?

Se OK em 6+: Pronto para debug com Claude

---

**Próximo**: [Soluções Rápidas](03-SOLUCOES-RAPIDAS.md)
