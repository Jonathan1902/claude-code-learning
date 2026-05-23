# Laboratório Prático — Conceitos Fundamentais

Bem-vindo ao laboratório prático! Este guia oferece exercícios concretos para reforçar cada conceito aprendido nos 4 primeiros arquivos do módulo. Você irá **praticar interações reais** com Claude Code, observando Tool Use em ação, testando limitações, e validando a matriz de decisão.

## Pré-requisitos

- ✅ Claude Code instalado e funcional (teste com `claude --version`)
- ✅ Estar no diretório raiz do repositório (`cd ~/Documentos/Projetos/claude-code-learning`)
- ✅ ~55 minutos para a trilha completa, ou ~15 minutos para a trilha iniciante

---

## Sumário de Exercícios

| # | Conceito | Exercício | Dificuldade | Tempo |
|---|---|---|---|---|
| 1.1 | 01-O-QUE-E-CLAUDE-CODE | Primeiro Contato: Tool Use | Fácil | 3 min |
| 1.2 | 01-O-QUE-E-CLAUDE-CODE | CLAUDE.md na Prática | Médio | 5 min |
| 1.3 | 01-O-QUE-E-CLAUDE-CODE | Claude Code vs Chat Web | Médio | 5 min |
| 2.1 | 02-CASOS-DE-USO | Debugging: Encontrando um Bug | Fácil | 4 min |
| 2.2 | 02-CASOS-DE-USO | Documentação Automática | Médio | 5 min |
| 2.3 | 02-CASOS-DE-USO | Análise de Código Legado | Difícil | 6 min |
| 3.1 | 03-QUANDO-USAR | Testando a Matriz de Decisão | Fácil | 3 min |
| 3.2 | 03-QUANDO-USAR | Contexto de Projeto Importa | Médio | 5 min |
| 3.3 | 03-QUANDO-USAR | Identificando Quando NÃO Usar | Difícil | 4 min |
| 4.1 | 04-LIMITACOES | Limite de Contexto | Fácil | 4 min |
| 4.2 | 04-LIMITACOES | Sem Memória Entre Sessões | Médio | 6 min |
| 4.3 | 04-LIMITACOES | Erros Silenciosos | Difícil | 5 min |

---

## Trilhas de Aprendizado

### 🚀 Trilha Iniciante (~15 min)
Para quem quer uma visão geral prática sem aprofundamento:
- **1.1** → Primeiro Contato (Tool Use)
- **2.1** → Debugging
- **3.1** → Matriz de Decisão
- **4.1** → Contexto Window

**Objetivo**: Sentir como Claude Code funciona e quando é adequado usar.

### 📚 Trilha Completa (~55 min)
Para aprendizado total: execute todos os 12 exercícios em sequência (1.1 → 1.2 → 1.3 → 2.1 → ... → 4.3).

**Objetivo**: Dominar cada conceito e suas nuances, incluindo limitações e mitigações.

---

## Exercícios

### 1.1 — Primeiro Contato: Tool Use em Ação

**Arquivo de Referência**: `01-O-QUE-E-CLAUDE-CODE.md`  
**Conceito**: O Agente Claude decide usar ferramentas (Tool Use) automaticamente sem instrução explícita.  
**Dificuldade**: Fácil | **Tempo**: ~3 min

Você vai pedir ao Claude para ler e resumir um arquivo do repositório. Observe como Claude **automaticamente usa o tool `Read`** para acessar o arquivo.

#### Setup
Você está no diretório raiz do repositório. Nenhum arquivo precisa ser criado.

#### Comando

```bash
claude "Leia o arquivo 01-CONCEITOS-FUNDAMENTAIS/02-CASOS-DE-USO.md e me dê um resumo de 3 linhas de cada caso de uso"
```

#### Saída Esperada

Você verá algo como:

```
Reading 01-CONCEITOS-FUNDAMENTAIS/02-CASOS-DE-USO.md...

[Claude responde com um resumo de 3 linhas para cada um dos 10 casos de uso]
```

**O que observar**: A mensagem `Reading ...` antes da resposta prova que Claude usou o tool `Read` automaticamente. Você nunca pediu explicitamente para "usar o tool Read" — Claude **decidiu sozinho** que precisava ler o arquivo para responder sua pergunta.

#### Conceito Reforçado

Este é o fluxo fundamental do Claude Code:

```
Seu Prompt → Claude Agente → [Decide usar ferramentas] → Tool Use (Read) → Resultado → Resposta
```

À diferença do Chat Web, aqui Claude age como um agente que escolhe as ferramentas certas para o trabalho.

---

### 1.2 — CLAUDE.md na Prática: Contexto Persistente

**Arquivo de Referência**: `01-O-QUE-E-CLAUDE-CODE.md`  
**Conceito**: CLAUDE.md fornece contexto de projeto que persiste dentro da sessão, elimina repetição.  
**Dificuldade**: Médio | **Tempo**: ~5 min

Você vai fazer uma pergunta que **depende do CLAUDE.md** sem repetir o contexto manualmente. Claude lerá o arquivo automaticamente.

#### Setup
Você está no diretório raiz. O arquivo `CLAUDE.md` já existe no repositório.

#### Primeiro Comando

```bash
claude "Leia o CLAUDE.md deste projeto e me diga: qual é o público-alvo deste repositório e quais são os 6 módulos que ele contém?"
```

**Saída esperada**: Claude lista o público-alvo (desenvolvedores com 2+ anos de experiência) e os 6 módulos (01-CONCEITOS-FUNDAMENTAIS até 06-TROUBLESHOOTING).

#### Segundo Comando (mesma sessão)

Agora, **sem repetir nada do CLAUDE.md**, faça uma pergunta que depende dele:

```bash
"Baseado nas diretrizes de escopo do projeto, um arquivo sobre 'Boas Práticas de Testes em Python' deveria estar neste repositório? Por quê?"
```

**Saída esperada**: Claude responde consultando a seção "What Doesn't Belong" do CLAUDE.md: "Não, porque 'Boas Práticas de Testes em Python' é engenharia geral/conteúdo que já existe em milhares de lugares. O repositório focam em **Claude Code especificamente**."

#### Conceito Reforçado

Na segunda pergunta, Claude **já tinha o CLAUDE.md carregado** e conseguiu responder sem que você precisasse repetir o contexto do projeto. Este é o poder de CLAUDE.md:

- ✅ **Com CLAUDE.md**: Contexto persiste, sem repetição, decisões rápidas
- ❌ **Sem CLAUDE.md**: Você repeteria "Este repositório ensina Claude Code, modulo tal..." a cada pergunta

---

### 1.3 — Claude Code vs Chat Web: Diferença Concreta

**Arquivo de Referência**: `01-O-QUE-E-CLAUDE-CODE.md` (tabela de comparação)  
**Conceito**: Claude Code acessa diretamente arquivos; Chat Web exige copy-paste manual.  
**Dificuldade**: Médio | **Tempo**: ~5 min

Você vai fazer a **mesma pergunta de dois jeitos** para sentir a diferença concretamente.

#### Passo 1 — Simulando Chat Web (sem acesso a arquivos)

```bash
claude "Sem ler nenhum arquivo, apenas pelo seu conhecimento, quantos módulos tem este repositório de aprendizado sobre Claude Code e qual é o nome do primeiro arquivo de cada módulo?"
```

**Saída esperada**: Claude vai admitir que não sabe com precisão, ou vai chutar baseado em padrões genéricos. A resposta será vaga ou possivelmente incorreta.

**Tempo**: ~1 min. Anote a qualidade da resposta.

#### Passo 2 — Usando Claude Code Corretamente (com acesso a arquivos)

```bash
"Agora leia o README.md e o arquivo CLAUDE.md, depois responda com precisão: quantos módulos tem este repositório e qual é o nome do primeiro arquivo de cada?"
```

**Saída esperada**: Claude lê os arquivos, extrai a estrutura exata e responde:
- **6 módulos**: 01-CONCEITOS-FUNDAMENTAIS, 02-ARQUITETURA, 03-COMANDOS-SINTAXE, 04-PADROES-USO, 05-CASOS-REAIS, 06-TROUBLESHOOTING
- **Primeiro arquivo de cada**: 01-O-QUE-E-CLAUDE-CODE.md, 01-VISAO-GERAL.md, 01-PROMPT-BASICO.md, etc.

**Tempo**: ~2 min.

#### Conceito Reforçado

Compare as duas respostas:

| Aspecto | Passo 1 (Chat Web) | Passo 2 (Claude Code) |
|---|---|---|
| **Precisão** | Genérica, possivelmente errada | Exata, extraída diretamente |
| **Confiança** | "Acho que..."  | "Conforme o README.md..." |
| **Esforço** | Você não fez nada | Claude usou Tool Use automaticamente |

A linha da tabela de comparação "**Contexto de Código**: Acesso direto a arquivos vs Copy-paste manual" é agora uma experiência vivida, não apenas lida.

---

### 2.1 — Debugging: Encontrando um Bug

**Arquivo de Referência**: `02-CASOS-DE-USO.md` (Caso de Uso 1: Debugging e Investigação)  
**Conceito**: Claude Code lê arquivos e faz análise estática de código para identificar bugs.  
**Dificuldade**: Fácil | **Tempo**: ~4 min

Você vai criar um arquivo Python com um bug intencional e pedir ao Claude para diagnosticar.

#### Setup

Crie um arquivo chamado `bug_exemplo.py` no diretório raiz do repositório com este conteúdo:

```python
# bug_exemplo.py
def calcular_media(numeros):
    total = "0"  # BUG: string em vez de int
    for n in numeros:
        total = total + n  # Tentará somar string + int
    return total / len(numeros)

resultado = calcular_media([10, 20, 30])
print(f"Média: {resultado}")
```

Você pode criar o arquivo manualmente no editor ou via terminal:

```bash
cat > bug_exemplo.py << 'EOF'
# bug_exemplo.py
def calcular_media(numeros):
    total = "0"  # BUG: string em vez de int
    for n in numeros:
        total = total + n  # Tentará somar string + int
    return total / len(numeros)

resultado = calcular_media([10, 20, 30])
print(f"Média: {resultado}")
EOF
```

#### Comando

```bash
claude "Analise o arquivo bug_exemplo.py. Há um erro de tipo que causa TypeError. Identifique a linha exata do bug, explique por que causa o erro e proponha o fix correto."
```

#### Saída Esperada

Claude lê o arquivo e responde:

```
Analisando bug_exemplo.py...

**Linha 3**: `total = "0"` — inicializa total como string em vez de inteiro.

**Por que causa TypeError**: Na linha 6, o código tenta `total + n`, que é "0" + 10. 
Python não permite somar string com int diretamente, causando: 
  TypeError: can only concatenate str (not "int") to str

**Fix**: Mude a linha 3 para:
  total = 0

Com este fix, o código retorna 20.0 (a média correta de [10, 20, 30]).
```

#### Conceito Reforçado

Este é o **Caso de Uso 1**: Claude lê o arquivo Python, entende a lógica, detecta o problema estático e propõe a correção. Sem Claude Code, você teria que:
1. Copiar todo o código do arquivo
2. Colar no chat web
3. Esperar resposta
4. Copiar o código corrigido de volta

Com Claude Code, foi uma pergunta e pronto.

---

### 2.2 — Documentação Automática

**Arquivo de Referência**: `02-CASOS-DE-USO.md` (Caso de Uso 3: Geração de Documentação)  
**Conceito**: Claude Code edita arquivos in-place adicionando docstrings e type hints.  
**Dificuldade**: Médio | **Tempo**: ~5 min

Você vai criar um arquivo Python sem documentação e pedir ao Claude para adicionar docstrings Google-style e type hints.

#### Setup

Crie `sem_docs.py`:

```bash
cat > sem_docs.py << 'EOF'
# sem_docs.py
def processar_pedido(cliente_id, itens, desconto=0.0):
    if not itens:
        raise ValueError("Lista de itens vazia")
    subtotal = sum(item['preco'] * item['quantidade'] for item in itens)
    total = subtotal * (1 - desconto)
    return {"cliente": cliente_id, "subtotal": subtotal, "total": total}

def validar_email(email):
    return "@" in email and "." in email.split("@")[-1]
EOF
```

#### Comando

```bash
claude "Leia sem_docs.py e adicione: (1) docstrings Google-style para cada função com Args, Returns e Raises; (2) type hints nos parâmetros e retorno; (3) um comentário de módulo no topo explicando o propósito do arquivo."
```

#### Saída Esperada

Claude edita o arquivo **in-place** usando o tool `Edit`. Você verá mensagens como:

```
Editing sem_docs.py...
```

O arquivo `sem_docs.py` será modificado para incluir:

```python
"""Processamento de pedidos com validação de email."""

from typing import Any, Dict, List

def processar_pedido(cliente_id: int, itens: List[Dict[str, Any]], desconto: float = 0.0) -> Dict[str, float]:
    """Processa um pedido e calcula o total com desconto.
    
    Args:
        cliente_id: ID único do cliente.
        itens: Lista de dicionários com 'preco' e 'quantidade' de cada item.
        desconto: Percentual de desconto (0.0 a 1.0). Padrão: 0.0.
    
    Returns:
        Dicionário com chaves 'cliente', 'subtotal' e 'total'.
    
    Raises:
        ValueError: Se a lista de itens está vazia.
    """
    if not itens:
        raise ValueError("Lista de itens vazia")
    subtotal = sum(item['preco'] * item['quantidade'] for item in itens)
    total = subtotal * (1 - desconto)
    return {"cliente": cliente_id, "subtotal": subtotal, "total": total}

def validar_email(email: str) -> bool:
    """Valida se um email tem formato básico válido.
    
    Args:
        email: Endereço de email a validar.
    
    Returns:
        True se o email contém '@' e um '.' após o '@', False caso contrário.
    """
    return "@" in email and "." in email.split("@")[-1]
```

Você pode verificar a mudança:

```bash
cat sem_docs.py
```

#### Conceito Reforçado

Este é o **Caso de Uso 3**: Documentação automática. O arquivo foi modificado in-place sem copy-paste. Na prática real, Claude Code é especialmente útil para:
- Gerar docstrings em projetos legados sem documentação
- Adicionar type hints a código dinâmico
- Padronizar estilo de documentação

---

### 2.3 — Análise de Código Legado

**Arquivo de Referência**: `02-CASOS-DE-USO.md` (Caso de Uso 8: Análise de Código Legado)  
**Conceito**: Claude Code pode explicar código desconhecido, identificar padrões, apontar problemas de segurança.  
**Dificuldade**: Difícil | **Tempo**: ~6 min

Você vai criar um arquivo com código legado (nomes obscuros, sem documentação) e pedir análise completa.

#### Setup

Crie `legado.py`:

```bash
cat > legado.py << 'EOF'
import hashlib, time

_cache = {}

def p(u, s):
    k = hashlib.md5(f"{u}{s}".encode()).hexdigest()
    if k in _cache and time.time() - _cache[k][1] < 300:
        return _cache[k][0]
    r = u == "admin" and len(s) >= 8
    _cache[k] = (r, time.time())
    return r

def c(d):
    return {k: v for k, v in d.items() if v is not None and v != ""}

def m(u, pw, pl):
    if not p(u, pw):
        return None
    return c(pl)
EOF
```

#### Comando

```bash
claude "Leia legado.py e faça uma análise completa: (1) explique em português o que cada função faz; (2) identifique qual é o fluxo de autenticação; (3) aponte 2 problemas de segurança neste código; (4) sugira nomes melhores para as funções e variáveis."
```

#### Saída Esperada

Claude fornece análise estruturada:

```
Analisando legado.py...

## Funções

**p(u, s)**: Função de autenticação com cache de 5 minutos usando MD5.
- u: nome de usuário
- s: senha
- Retorna: True se usuario é "admin" E senha tem 8+ caracteres, com cache

**c(d)**: Limpa um dicionário removendo valores None e strings vazias.
- d: dicionário a limpar
- Retorna: novo dicionário sem valores falsos

**m(u, pw, pl)**: Função main que autentica e limpa payload.
- u: usuário
- pw: senha
- pl: payload
- Retorna: payload limpo ou None se falha na autenticação

## Fluxo de Autenticação
1. m() chama p() para autenticar usuário e senha
2. Se falha, retorna None
3. Se sucede, retorna o payload limpo

## Problemas de Segurança

1. **MD5 inadequado para senhas**: O código usa `hashlib.md5(f"{u}{s}".encode())` 
   - MD5 não é adequado para hash de senhas (collision-prone, não é uma função de derivação de chave)
   - Deveria usar bcrypt, scrypt ou argon2

2. **Hardcoding de credencial**: `u == "admin"` hardcoda a credencial
   - Não há verificação real de senha com hash armazenado
   - Qualquer um que vê o código sabe a credencial correta é "admin"

## Nomes Melhores

- `p()` → `autenticar_usuario()`
- `c()` → `limpar_payload_vazio()`
- `m()` → `processar_login()`
- `u` → `usuario`
- `s` → `senha`
- `k` → `hash_chave`
- `r` → `autenticado`
- `pl` → `payload`
```

#### Conceito Reforçado

Este é o **Caso de Uso 8**: Claude Code como "explicador de código legado". A análise em um bloco coeso inclui fluxo, segurança e refatoração — o tipo de trabalho que humanos fazem horas, Claude entrega em segundos.

---

### 3.1 — Testando a Matriz de Decisão

**Arquivo de Referência**: `03-QUANDO-USAR.md` (Tabela de decisão)  
**Conceito**: Reconhecer quando Claude Code é a ferramenta certa vs quando evitar.  
**Dificuldade**: Fácil | **Tempo**: ~3 min

Você vai fazer dois prompts contrastantes e observar as respostas para validar os critérios de decisão.

#### Passo 1 — ✅ Problema Adequado (com código concreto)

```bash
claude "Este script leva 45 segundos para rodar. Otimize com processamento paralelo usando ThreadPoolExecutor:

def processar_lista(itens):
    resultados = []
    for item in itens:
        import time
        time.sleep(0.1)  # Simula operação lenta
        resultados.append(item * 2)
    return resultados"
```

**Saída esperada**: Claude produz código otimizado usando `ThreadPoolExecutor`, reduzindo o tempo teórico de 45s para ~0.5s (paralelismo). Exemplo:

```python
from concurrent.futures import ThreadPoolExecutor
import time

def processar_lista(itens):
    def processar_item(item):
        time.sleep(0.1)
        return item * 2
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        resultados = list(executor.map(processar_item, itens))
    return resultados
```

**Por que é adequado**: Há código concreto para analisar e otimizar. A solução é técnica e iterativa.

#### Passo 2 — ❌ Problema Inadequado (decisão arquitetural)

```bash
"Devo usar microsserviços ou monolítico para meu novo projeto de e-commerce que tem 3 desenvolvedores e aproximadamente 1000 usuários por dia?"
```

**Saída esperada**: Claude responde algo como:

```
Esta é uma decisão arquitetural que não posso responder sozinho, porque depende de fatores 
de negócio e organização que você entende melhor do que eu:

- Recursos do time (3 devs é uma restrição real)
- Complexidade do escopo futuro
- Orçamento para DevOps/infraestrutura
- Riscos de falha

Recomendação: Discuta com seu time e considere:
- Se vai crescer rápido → microsserviços depois
- Se quer simplicidade inicial → monolítico agora
```

Claude não produz uma "resposta certa", porque não há — a decisão depende de contexto que humanos devem discutir.

#### Conceito Reforçado

A matriz de decisão em ação:

| Aspecto | Passo 1 (✅) | Passo 2 (❌) |
|---|---|---|
| **Tem código?** | Sim | Não |
| **Iteração técnica?** | Sim (otimizar) | Não (decisão pura) |
| **Resposta única certa?** | Sim (código mais rápido) | Não (depende de contexto) |

Leia novamente `03-QUANDO-USAR.md` — a linha **✅ USE: Tem código a analisar** vs **❌ EVITE: Decisão arquitetural pura** acabou de se tornar intuitiva.

---

### 3.2 — Contexto de Projeto Importa

**Arquivo de Referência**: `03-QUANDO-USAR.md` (Critério ✅ 5: Contexto de projeto importa)  
**Conceito**: A presença do CLAUDE.md transforma fundamentalmente a qualidade e adequação da resposta.  
**Dificuldade**: Médio | **Tempo**: ~5 min

Você vai fazer a mesma tarefa **duas vezes**, uma sem contexto de projeto e outra com, e comparar as respostas.

#### Passo 1 — Sem Contexto de Projeto

```bash
claude "Crie uma função Python para validar um formulário de cadastro com campos nome, email e idade. Inclua validações básicas."
```

**Saída esperada**: Claude gera uma função genérica, funcional mas sem conhecimento do contexto educacional:

```python
import re

def validar_cadastro(nome, email, idade):
    if not nome or len(nome) < 3:
        raise ValueError("Nome deve ter pelo menos 3 caracteres")
    
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        raise ValueError("Email inválido")
    
    if not isinstance(idade, int) or idade < 18:
        raise ValueError("Idade deve ser >= 18")
    
    return True
```

**Aspecto**: Código correto, mas genérico, sem estilo educacional.

#### Passo 2 — Com Contexto de Projeto (CLAUDE.md)

Primeira, leia o CLAUDE.md para carregar contexto:

```bash
claude "Leia o CLAUDE.md deste projeto educacional sobre Claude Code. Agora, considerando este contexto, crie um exemplo de função Python para validar um formulário de cadastro que seria adequado como material didático neste repositório — seguindo padrões de estilo, comentários explicativos e propósito educacional."
```

**Saída esperada**: Claude gera uma função mais educacional:

```python
"""Validação de formulário de cadastro — exemplo educacional para Claude Code."""

import re
from typing import Tuple

def validar_cadastro(nome: str, email: str, idade: int) -> Tuple[bool, str]:
    """Valida dados de cadastro e retorna resultado com mensagem.
    
    Demonstra:
    - Type hints (bom para documentação em Claude Code)
    - Mensagens de erro claras (ajuda usuários a entender o que está errado)
    - Return tuple (padrão simples vs exceção)
    
    Args:
        nome: Nome completo do usuário.
        email: Endereço de email.
        idade: Idade em anos.
    
    Returns:
        Tupla (válido: bool, mensagem: str)
    """
    # Validação 1: Nome deve ter pelo menos 3 caracteres
    if not nome or len(nome) < 3:
        return False, "Nome deve ter pelo menos 3 caracteres"
    
    # Validação 2: Email básico (regex simples para fins didáticos)
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return False, "Email inválido"
    
    # Validação 3: Idade deve ser >= 18
    if not isinstance(idade, int) or idade < 18:
        return False, "Deve ter 18 anos ou mais"
    
    return True, "Cadastro válido"

# Exemplo de uso
if __name__ == "__main__":
    valido, mensagem = validar_cadastro("João Silva", "joao@example.com", 25)
    print(f"Resultado: {valido} — {mensagem}")
```

**Aspecto**: Mesmo código base, mas com:
- Docstring explicativa sobre **por que** cada padrão é usado
- Comentários educacionais
- Example de uso no main
- Type hints visíveis
- Estrutura pensada para aprendizado

#### Conceito Reforçado

O **CLAUDE.md fez diferença radical**:

| Aspecto | Passo 1 | Passo 2 |
|---|---|---|
| **Estilo** | Genérico, eficiente | Educacional, comentado |
| **Público** | Qualquer projeto | Desenvolvedores aprendendo |
| **Docstring** | Mínima | Explicativa |
| **Comentários** | Nenhum | Instrucionais |

Critério ✅ 5 de "Quando Usar Claude Code": **Contexto de projeto importa**. Sem CLAUDE.md, Claude não sabe que está criando material educacional.

---

### 3.3 — Identificando Quando NÃO Usar

**Arquivo de Referência**: `03-QUANDO-USAR.md` (Critério ❌ 5: Modificação de dados críticos)  
**Conceito**: Claude Code se recusa ou avisa de forma muito clara quando a tarefa é destrutiva em produção.  
**Dificuldade**: Difícil | **Tempo**: ~4 min

Você vai pedir uma operação destrutiva de dados críticos e observar como Claude se comporta.

#### Comando

```bash
claude "Temos uma tabela PostgreSQL com 50.000 usuários em produção. Execute o seguinte SQL diretamente: DELETE FROM users WHERE last_login < '2024-01-01';"
```

#### Saída Esperada

Claude **não executa** e fornece um aviso firme:

```
⚠️ AVISO DE SEGURANÇA

Não vou executar este DELETE em produção sem aprovação explícita e proteção.
Dados críticos exigem workflow seguro:

1. **Backup primeiro**
   pg_dump -Fc proddb > backup_$(date +%Y%m%d_%H%M%S).sql

2. **Verificar impacto**
   SELECT COUNT(*) FROM users WHERE last_login < '2024-01-01';
   → Resultado: ~X usuários serão deletados

3. **Testar em staging**
   Rode o DELETE em ambiente de staging e verifique impacto

4. **Aprovação humana**
   Obtenha autorização de um DBA ou arquiteto antes de produção

5. **Documentar**
   Log: "DELETE 2024-01-30: removidos usuários inativos pré-2024"

Comando sugerido para staging (NÃO PRODUÇÃO):
SELECT COUNT(*) FROM users WHERE last_login < '2024-01-01';
-- Verifique o número acima
-- DELETE FROM users WHERE last_login < '2024-01-01';
-- (comentado por segurança)
```

Claude reconhece o risco e recusa até ter aprovação explícita.

#### Conceito Reforçado

Critério ❌ 5 da matriz: **"Modificação de dados críticos — sempre requer aprovação manual"**.

Claude Code não é um "botão de executar SQL". É uma ferramenta que ajuda você a **pensar** antes de executar — especialmente em produção. A recusa é uma feature, não um bug.

---

### 4.1 — Limite de Contexto: Veja o Problema e a Solução

**Arquivo de Referência**: `04-LIMITACOES.md` (Limitação 1: Context Window)  
**Conceito**: Context window tem limite; a solução é focar em arquivos específicos, não tentar processar tudo.  
**Dificuldade**: Fácil | **Tempo**: ~4 min

Você vai fazer **dois pedidos** para comparar: um amplo (que sofre com limite de contexto) e um focado.

#### Passo 1 — ❌ Amplo Demais

```bash
claude "Analise completamente todos os arquivos deste repositório e me dê um resumo detalhado de cada um."
```

**Saída esperada**: Claude vai tentar mas possivelmente vai truncar, resumir demais, ou pedir para você delimitar o escopo. A qualidade será genérica porque não consegue processar ~20k palavras simultaneamente.

**Tempo**: ~2-3 min. Anote o resultado.

#### Passo 2 — ✅ Focado

```bash
claude "Analise apenas os arquivos dentro de 01-CONCEITOS-FUNDAMENTAIS/ e me dê um resumo de 2-3 linhas de cada arquivo."
```

**Saída esperada**: Claude fornece resumo preciso e completo dos 4 (agora 5 com o novo 05-HANDS-ON.md) arquivos do módulo:

```
## 01-O-QUE-E-CLAUDE-CODE.md
Define Claude Code como ferramenta CLI/IDE, compara com Chat Web e API, apresenta 5 componentes principais (Agente, Tool Use, MCP, Hooks, CLAUDE.md) e descreve o fluxo básico de interação.

## 02-CASOS-DE-USO.md
Lista 10 casos de uso práticos (debugging, refatoração, documentação, análise de performance, testes, DevOps, ETL, código legado, segurança, migrações) com cenários e prompts de exemplo.

[continua...]
```

Comparar com o Passo 1: muito mais claro, completo e útil.

#### Conceito Reforçado

A **Limitação 1** em ação:

| Aspecto | Passo 1 (amplo) | Passo 2 (focado) |
|---|---|---|
| **Escopo** | ~20k palavras | ~3k palavras |
| **Qualidade** | Genérica, truncada | Precisa, completa |
| **Tempo** | Longo | Rápido |
| **Confiabilidade** | Média | Alta |

**Solução**: Delimite o escopo. Use "apenas este diretório", "apenas este arquivo", "apenas essas 3 funções". Foco é a chave.

---

### 4.2 — Sem Memória Entre Sessões: O Problema e a Solução

**Arquivo de Referência**: `04-LIMITACOES.md` (Limitação 2: Sem Memória Entre Sessões)  
**Conceito**: Claude não lembra entre sessões; CLAUDE.md é a solução.  
**Dificuldade**: Médio | **Tempo**: ~6 min

Você vai demonstrar o problema **e** a solução de forma prática.

#### Parte 1 — Demonstrando o Problema

**Sessão 1** (execute este comando):

```bash
claude "Para contexto deste projeto: estamos usando FastAPI com Python 3.12, PostgreSQL 15 e convenção de naming snake_case estrita com type hints obrigatórios. Crie uma função que retorna a versão da API."
```

**Saída esperada**: Claude cria uma função FastAPI corretamente:

```python
from fastapi import FastAPI

app = FastAPI()

async def obter_versao_api() -> dict[str, str]:
    """Retorna a versão atual da API."""
    return {"versao": "1.0.0"}
```

Anote que Claude entendeu o stack (FastAPI, Python 3.12, type hints).

**Sessão 2** (feche o Claude com Ctrl+C ou `/clear` para simular nova sessão):

```bash
claude "Continue o trabalho anterior e crie agora uma função para listar usuários."
```

**Saída esperada**: Claude **não lembra** do stack anterior. Pode gerar:
- Código sem type hints
- Em estilo genérico
- Ou perguntar "qual é o stack?"

**Tempo total da Parte 1**: ~3 min.

#### Parte 2 — Demonstrando a Solução (CLAUDE.md)

Crie um arquivo `CLAUDE.md` no diretório raiz (se ainda não existe um local para testes) ou use um específico para este exercício. Por brevidade, vamos criar um em `test_claude.md`:

```bash
cat > CLAUDE.md << 'EOF'
# Context

Projeto: API de Exemplo
Stack: FastAPI, Python 3.12, PostgreSQL 15
Convenções: 
- snake_case obrigatório
- type hints em todos os parâmetros e retornos
- docstrings Google-style
- async/await por padrão
EOF
```

Agora, **nova sessão**:

```bash
claude "Crie uma função para listar usuários da API."
```

**Saída esperada**: Desta vez, Claude lê automaticamente o CLAUDE.md e gera:

```python
async def listar_usuarios() -> list[dict[str, Any]]:
    """Lista todos os usuários da API.
    
    Returns:
        Lista de dicionários com dados dos usuários.
    """
    # Conexão com PostgreSQL...
    usuarios = await db.fetch("SELECT * FROM usuarios")
    return usuarios
```

O código já segue convenções de FastAPI, Python 3.12, snake_case e type hints — tudo porque o CLAUDE.md estava ali.

#### Conceito Reforçado

**Problema**: Cada nova sessão, Claude é um "agente novo" sem memória.  
**Solução**: CLAUDE.md persiste o contexto entre sessões automaticamente.

| Sem CLAUDE.md | Com CLAUDE.md |
|---|---|
| Repetir stack a cada sessão | Stack carregado automaticamente |
| Inconsistência entre respostas | Consistência garantida |
| Mais linhas no prompt | Prompt mais conciso |

Este é o motivo pelo qual todos os repositórios profissionais têm CLAUDE.md.

---

### 4.3 — Erros Silenciosos: Peça Premissas Explícitas

**Arquivo de Referência**: `04-LIMITACOES.md` (Limitação 6: Erros Silenciosos)  
**Conceito**: Prompts ambíguos podem levar Claude a assumir coisas erradas silenciosamente; peça suposições explícitas.  
**Dificuldade**: Difícil | **Tempo**: ~5 min

Você vai fazer um prompt ambíguo, ver as suposições perigosas que Claude faz, e depois usar a técnica defensiva.

#### Passo 1 — Prompt Ambíguo (Demonstrando o Risco)

```bash
claude "Crie um script para deletar arquivos antigos do servidor."
```

**Saída esperada**: Claude gera um script que **assume**:

```python
import os
import time

def deletar_antigos(diretorio="/tmp", dias=30):
    limite = time.time() - (dias * 86400)
    for arquivo in os.listdir(diretorio):
        caminho = os.path.join(diretorio, arquivo)
        if os.path.getmtime(caminho) < limite:
            os.remove(caminho)
            print(f"Deletado: {caminho}")
```

**O problema**: Quantas suposições perigosas Claude fez?

- Diretório alvo é `/tmp`?
- "Antigo" significa "modificado há 30 dias"?
- Deletar permanentemente?
- Sem confirmação?
- Sem logging de backup?

Se você executar este script, pode deletar arquivos importantes — **silenciosamente**.

#### Passo 2 — Técnica Defensiva (Pedir Suposições Explícitas)

```bash
claude "Antes de escrever qualquer código, liste todas as suposições que você está fazendo sobre este script de deleção de arquivos:
1. Qual é o diretório alvo exato?
2. O que significa 'antigo' (data de modificação? criação? acesso?)?
3. Quantos dias/meses constitui 'antigo'?
4. Vai mover para lixeira ou deletar permanentemente?
5. Precisa de confirmação do usuário?
6. Precisa fazer backup antes de deletar?
7. Precisa fazer logging das deleções?"
```

**Saída esperada**: Claude lista explicitamente todas as suposições:

```
Suposições que fiz:
1. **Diretório alvo**: /tmp (genérico, pode estar errado)
2. **Definição de antigo**: Modificado há 30 dias (pode não ser o certo)
3. **Deleção**: Permanente com os.remove() (sem lixeira)
4. **Confirmação**: Nenhuma (perigoso!)
5. **Backup**: Nenhum
6. **Logging**: Apenas print (não persiste)

Para código seguro em produção, você precisa especificar:
- Qual é exatamente o diretório que será afetado?
- Qual critério de tempo ("último acesso" ou "última modificação")?
- Criar um arquivo de log de deleções?
- Implementar modo "dry-run" para preview?
```

Agora você pode corrigir as suposições **antes** de rodar código perigoso.

#### Conceito Reforçado

**Limitação 6**: Claude pode gerar código que "parece certo" mas tem suposições silenciosas perigosas.

**Solução**: Sempre peça "liste suas suposições" antes de tarefas com impacto real (deleção, modificação de dados, infraestrutura).

---

## Checklist de Conclusão

Depois de executar os exercícios, marque os itens abaixo para confirmar que você dominou cada conceito:

- [ ] **1.1**: Observei Tool Use em ação (mensagem "Reading..." apareceu)
- [ ] **1.2**: Entendi como CLAUDE.md persiste contexto dentro da sessão
- [ ] **1.3**: Senti concretamente a diferença entre acesso direto vs copy-paste manual
- [ ] **2.1**: Debuguei código real com Claude identificando o erro de tipo
- [ ] **2.2**: Vi Claude editar um arquivo in-place adicionando documentação
- [ ] **2.3**: Li análise de segurança completa de código legado
- [ ] **3.1**: Distingui claramente quando Claude Code é adequado vs inadequado
- [ ] **3.2**: Observei como CLAUDE.md transformou a qualidade da resposta
- [ ] **3.3**: Entendi que Claude se recusa em tarefas destrutivas sem aprovação
- [ ] **4.1**: Experimentei o limite de contexto e a solução (foco seletivo)
- [ ] **4.2**: Demonstrei como CLAUDE.md substitui repetição entre sessões
- [ ] **4.3**: Aprendi a pedir suposições explícitas antes de código perigoso

---

## Próximos Passos

Parabéns! Você completou o **Laboratório Prático dos Conceitos Fundamentais**. Agora está pronto para aprender técnicas avançadas:

- **Próximo módulo**: Leia [`03-COMANDOS-SINTAXE/01-PROMPT-BASICO.md`](../03-COMANDOS-SINTAXE/01-PROMPT-BASICO.md) para aprender sintaxe e padrões de prompts efetivos
- **Padrões de uso**: Depois explore [`04-PADROES-USO/01-ITERACAO-RAPIDA.md`](../04-PADROES-USO/01-ITERACAO-RAPIDA.md) para técnicas de iteração e debugging com Claude Code
- **Casos reais**: Quando se sentir confortável, veja [`05-CASOS-REAIS/`](../05-CASOS-REAIS/) para exemplos end-to-end

---

**Criado em**: 2026-05-23  
**Tempo total de prática**: ~55 minutos (trilha completa) ou ~15 minutos (trilha iniciante)
