# Debugging com Claude Code

## Princípio: Forneça Evidência, Não Suposições

```
❌ "Meu código está bugado"
✅ "Esperado: 100, Recebido: null"

❌ "Não funciona"
✅ "Stack trace: [trace]
   Entrada: x=5, y=0
   Output: KeyError: 'result'"
```

---

## Passo 1: Reproduzir o Problema

### Erro Consistente
```
"Sempre falha quando:
- Input: usuario_id=999
- Esperado: levanta UserNotFound
- Atual: levanta KeyError
- Stack trace:
[colar stack trace inteiro]"
```

### Erro Intermitente (Flaky)
```
"Falha aleatoriamente (~30% do tempo)
- Passos: [listar exatos]
- Log de 3 execuções:
  [log execução 1 - sucesso]
  [log execução 2 - falha]
  [log execução 3 - sucesso]"
```

### Comportamento Errado
```
"Roda sem erro, mas resultado está errado
- Input: [dados específicos]
- Esperado: [resultado correto]
- Recebido: [resultado atual]
- Diferença: [o que está errado]"
```

---

## Passo 2: Forneça Contexto Mínimo

### Código Relevante
```
❌ "Aqui está projeto inteiro"
   [500 arquivos]

✅ "Aqui está arquivo com bug"
   [1 arquivo, 200 linhas máximo]

✅ "Aqui está função com bug"
   [50 linhas máximo]
```

### Arquivos Dependentes
```
"Bug está em payment_processor.py

Dependências:
- Usa User model (def [link])
- Usa StripeClient (def [link])
- Chama send_email (def [link])"
```

### Data Teste
```
"Para reproduzir preciso:
- Database com 1 usuário (user_id=1, status='active')
- Ou aqui está JSON mock: [dados]"
```

---

## Passo 3: Diagnóstico de Claude

### Claude Pode Fazer:
1. **Ler código**: Vê o que escreveu
2. **Análise estática**: Vê problemas lógicos
3. **Simulação**: Roda mentalmente o código
4. **Patterns**: Reconhece bugs comuns

### Claude NÃO Pode Fazer (sem sua ajuda):
1. **Ler stack traces incompletos**: "Arquivo removed" não ajuda
2. **Debugar sem contexto**: Precisa de input/output exatos
3. **Rodar em seu ambiente**: Só consegue com Bash tool

---

## Exemplo 1: Bug Simples

### Seu Relato
```
ERRO: TypeError: unsupported operand type(s) for +: 'str' and 'int'

Arquivo: utils.py, linha 42

Contexto: Função que soma dois números
```

### O que Fornecer
```
# utils.py (linhas 35-50)

def calculate_total(items: list) -> int:
    total = "0"  # AQUI?
    for item in items:
        total = total + item['price']  # ERRO AQUI (str + int)
    return total

# Teste
calculate_total([{'price': 10}, {'price': 20}])
# TypeError: unsupported...
```

### Diagnóstico Claude
```
Claude vê:
1. total = "0" (string, não int)
2. Tenta somar com inteiro (item['price'])
3. Causa TypeError

Fix: total = 0 (sem aspas)
```

---

## Exemplo 2: Bug Lógico

### Seu Relato
```
Função calcula desconto errado

Input: price=100, quantity=10, category='vip'
Esperado: 70 (desconto de 30%)
Recebido: 95 (desconto de 5%)
```

### O que Fornecer
```
def calculate_discount(price: float, quantity: int, category: str) -> float:
    discount = 0.05  # 5% base
    
    if category == 'vip':
        discount = 0.30
    
    # Bug está aqui?
    if quantity > 5:
        discount = discount + 0.10  # Adiciona 10%
    
    return price * (1 - discount)

# Teste
calculate_discount(100, 10, 'vip')
# Esperado: 70
# Recebido: 95 (price * 0.95 = 95)
```

### Diagnóstico Claude
```
Claude vê:
1. VIP = 0.30 (correto)
2. Quantity > 5 → adiciona 0.10
   Deveria ser: 0.30 + 0.10 = 0.40
   Mas está calculando: 0.30 + 0.10 = 0.40
   Desconto: 1 - 0.40 = 0.60
   Resultado: 100 * 0.60 = 60

   ESPERA, está retornando 95?
   Deixe Claude ver o código executando:
   
   discount = 0.05
   category == 'vip' → discount = 0.30
   quantity > 5 → discount = 0.30 + 0.10 = 0.40
   price * (1 - 0.40) = 100 * 0.60 = 60

   Mas você diz que retorna 95?
   Seu código com os ifs está certo?
   [Pede rever código]
```

---

## Exemplo 3: Race Condition / Async Bug

### Seu Relato
```
Teste falha aleatoriamente (flaky test)

test_user_creation
  - Cria usuário
  - Espera 0.1s
  - Assertion falha ~50% do tempo

from_selenium:
  - User.objects.create(...) returns
  - Imediatamente tenta User.objects.get(...)
  - KeyError: usuário não existe!
  - Se adiciono time.sleep(0.5) funciona
```

### O que Fornecer
```
def test_user_creation():
    user = User.objects.create(username="testuser")
    # Fail aqui ~50% do tempo
    assert User.objects.filter(username="testuser").count() == 1

# No código real:
user = User.objects.create(...)  # Async cache
response = self.client.get(f'/users/{user.id}/')  # Sometimes not found
```

### Diagnóstico Claude
```
Claude vê:
1. time.sleep() "fix" indica timing issue
2. Create() retorna, mas objeto não está visível
3. Possível causa: cache ou transaction isolation

Diagnóstico:
- Django ORM: create() deveria ser síncrono
- Mas cache pode não ser atualizado
- Ou transação não commited

Sugestões:
- Usar transaction.atomic() explícito
- Ou refresh_from_db()
- Ou verificar se há signal handlers async
```

---

## Passo 4: Testar Fix

### Código Fixado
```
VOCÊ: "Aqui está meu fix

[código antes]
→ [código depois]

Testei com:
[comandos de teste]

Resultado:
[output do teste]

Funciona?"
```

### Validação Claude
```
Claude:
1. Vê fix
2. Valida logicamente
3. Verifica se trata root cause
4. Aprova ou sugere melhor forma
```

---

## Padrão: Minimal Reproduction (Minrep)

Criar exemplo mínimo que reproduz bug:

### Antes (Muita Informação)
```
"Meu app de 500 arquivos tem um bug
Arquivo payment_processor.py falha
Quer que veja tudo?"
```

### Depois (Mínimo)
```
# bug_example.py (10 linhas)

def process_payment(amount: float, currency: str) -> dict:
    result = amount * currency  # ❌ Bug aqui
    return {"amount": result}

# Erro
try:
    process_payment(100, "USD")
except TypeError as e:
    print(f"BUG: {e}")
    # TypeError: can't multiply float by str
```

### Benefício
- ✅ Claude foca no problema
- ✅ Sem ruído
- ✅ Rápido de entender

---

## Checklist: Relato de Bug Bom

- [ ] Erro exato (stack trace ou resultado errado)
- [ ] Input específico que causa erro
- [ ] Código relevante (máximo 100 linhas)
- [ ] Dependências claras (que outros arquivos usa)
- [ ] Já tentei o quê (para não repetir)
- [ ] Qual é o comportamento esperado

Se OK em 5+: Bug report é bom

---

## Debugging Colaborativo

### Você Observa
```
"Saída é diferente do esperado"
```

### Claude Analisa
```
"Vejo possível causa:
1. [possibilidade]
2. [possibilidade]

Qual é mais provável? Ou deixo testar?"
```

### Você Testa
```
"Testei possibilidade 1: não é
Testei possibilidade 2: ERA!"
```

### Claude Confirma
```
"Ótimo, então o bug é [X]
Fix é [Y]"
```

---

**Próximo**: [Análise](04-ANALISE.md)
