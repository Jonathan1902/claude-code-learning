# Laboratório Prático — Arquitetura do Claude Code

Bem-vindo ao laboratório de arquitetura! Este guia oferece exercícios concretos para reforçar os conceitos internos de como Claude Code funciona. Você irá **observar o fluxo completo**, entender o agent loop em ação, gerenciar tokens, e explorar as tecnologias subjacentes (modelos, hooks, CLAUDE.md avançado).

## Pré-requisitos

- ✅ Claude Code instalado e funcional (teste com `claude --version`)
- ✅ Estar no diretório raiz do repositório (`cd ~/Documentos/Projetos/claude-code-learning`)
- ✅ ~48 minutos para a trilha completa, ou ~15 minutos para a trilha iniciante

---

## Sumário de Exercícios

| # | Conceito | Exercício | Dificuldade | Tempo |
|---|---|---|---|---|
| 1.1 | 01-FLUXO-COMPLETO | Observar o Fluxo em Tempo Real | Fácil | 3 min |
| 1.2 | 01-FLUXO-COMPLETO | Rastrear as Fases de Inicialização | Médio | 5 min |
| 1.3 | 01-FLUXO-COMPLETO | Analisar o Ciclo de Feedback | Difícil | 6 min |
| 2.1 | 02-COMO-FUNCIONA-INTERNAMENTE | Visualizar o Agent Loop | Fácil | 4 min |
| 2.2 | 02-COMO-FUNCIONA-INTERNAMENTE | Inspecionar o Uso de Tokens | Médio | 5 min |
| 2.3 | 02-COMO-FUNCIONA-INTERNAMENTE | Testar a Compactação de Contexto | Difícil | 8 min |
| 3.1 | 03-TECNOLOGIAS-SUBJACENTES | Comparar Modelos na Prática | Fácil | 4 min |
| 3.2 | 03-TECNOLOGIAS-SUBJACENTES | Criar e Ativar um Hook | Médio | 6 min |
| 3.3 | 03-TECNOLOGIAS-SUBJACENTES | Estruturar um CLAUDE.md Avançado | Difícil | 7 min |

---

## Trilhas de Aprendizado

### 🚀 Trilha Iniciante (~15 min)
Para quem quer uma visão geral prática dos internals sem aprofundamento:
- **1.1** → Observar o Fluxo em Tempo Real
- **2.1** → Visualizar o Agent Loop
- **3.1** → Comparar Modelos na Prática

**Objetivo**: Sentir o funcionamento interno do Claude Code sem mergulhar em detalhes técnicos.

### 📚 Trilha Completa (~48 min)
Para aprendizado total: execute todos os 9 exercícios em sequência (1.1 → 1.2 → 1.3 → 2.1 → ... → 3.3).

**Objetivo**: Dominar a arquitetura interna, gerenciamento de contexto e tecnologias subjacentes.

---

## Exercícios

### 1.1 — Observar o Fluxo em Tempo Real

**Arquivo de Referência**: `01-FLUXO-COMPLETO.md`  
**Conceito**: O fluxo completo de uma interação passa por fases distintas (Inicialização → Processamento → Tool Use Loop → Resposta).  
**Dificuldade**: Fácil | **Tempo**: ~3 min

Você vai executar um comando simples e observar as fases do fluxo acontecendo em tempo real.

#### Setup
Você está no diretório raiz do repositório. Nenhum arquivo precisa ser criado.

#### Comando

```bash
claude "Liste os nomes dos 3 primeiros arquivos do diretório 02-ARQUITETURA/"
```

#### Saída Esperada

Você verá:

```
Reading 02-ARQUITETURA/...
[Claude lista os arquivos ou avisa que precisa usar Bash]
```

Se Claude usar `Bash` para listar os arquivos:

```
Executando: find 02-ARQUITETURA/ -maxdepth 1 -type f -name "*.md" | head -3

01-FLUXO-COMPLETO.md
02-COMO-FUNCIONA-INTERNAMENTE.md
03-TECNOLOGIAS-SUBJACENTES.md
```

**O que observar**: Você viu pelo menos 2 fases em ação:
1. **Inicialização**: Claude carregou o contexto (arquivo, CLAUDE.md, histórico)
2. **Tool Use Loop**: Claude executou uma ferramenta (Read ou Bash) para responder

#### Conceito Reforçado

Este é o fluxo básico descrito em `01-FLUXO-COMPLETO.md`:

```
Seu Prompt → Claude Agente → [Decide usar ferramenta] → Tool Use (Read/Bash) → Resultado → Resposta
```

A latência que você observou (segundos entre o prompt e a resposta) inclui:
- Carregamento de contexto (<1s)
- Chamada à API Claude (5-15s)
- Execução da ferramenta (<1s)

---

### 1.2 — Rastrear as Fases de Inicialização

**Arquivo de Referência**: `01-FLUXO-COMPLETO.md` (Fase 1: Inicialização)  
**Conceito**: Na fase de Inicialização, Claude Code carrega o arquivo atual, CLAUDE.md, histórico e modelo.  
**Dificuldade**: Médio | **Tempo**: ~5 min

Você vai criar um CLAUDE.md mínimo e observar como Claude o carrega automaticamente.

#### Setup

Crie um arquivo `CLAUDE_test.md` no diretório raiz com este conteúdo:

```bash
cat > CLAUDE_test.md << 'EOF'
# Projeto de Teste

Stack: Python 3.12, FastAPI
Padrão: snake_case em nomes de função
Restrição: Todas as funções devem ter type hints

## Decisões Arquiteturais
- Usar async/await por padrão
- Validar input em handlers HTTP
EOF
```

(Usamos `CLAUDE_test.md` para não sobrescrever o CLAUDE.md real do repositório.)

#### Comando — Sessão 1

Rode um prompt que dependa do contexto do arquivo de teste:

```bash
claude "Leia o arquivo CLAUDE_test.md. Baseado nas convenções ali definidas, crie uma função para buscar um usuário do banco de dados."
```

**Saída esperada**: Claude lê o arquivo automaticamente e gera uma função com type hints, snake_case e async/await:

```python
async def obter_usuario(usuario_id: int) -> dict[str, Any]:
    """Busca um usuário do banco de dados."""
    usuario = await db.fetch("SELECT * FROM usuarios WHERE id = ?", usuario_id)
    return usuario
```

#### Conceito Reforçado

Observe que na **Fase 1 (Inicialização)**:
- Claude leu `CLAUDE_test.md` automaticamente
- Você **nunca pediu explicitamente** para "ler o arquivo"
- Claude extraiu as restrições (type hints, async/await) e as aplicou

Este é o poder da Inicialização: contexto persiste e é reutilizado sem repetição manual.

---

### 1.3 — Analisar o Ciclo de Feedback

**Arquivo de Referência**: `01-FLUXO-COMPLETO.md` (Ciclo de Feedback)  
**Conceito**: O Ciclo de Feedback permite iteração: o usuário refina com novos prompts, contexto acumula, respostas melhoram.  
**Dificuldade**: Difícil | **Tempo**: ~6 min

Você vai fazer 3 prompts encadeados para observar como o contexto se acumula e refina.

#### Sequência de 3 Prompts (mesma sessão)

**Prompt 1**:

```bash
claude "Descreva brevemente o que é o Agent Loop segundo 02-COMO-FUNCIONA-INTERNAMENTE.md"
```

**Saída esperada**: Claude descreve o loop while-not-done que executa ferramentas iterativamente.

**Prompt 2** (sem repetir contexto):

```bash
"Agora dê um exemplo de código Python que simule este loop com 3 iterações."
```

**Saída esperada**: Claude gera pseudocódigo do loop, baseado no conceito anterior (contexto acumulou).

**Prompt 3** (refinamento):

```bash
"Adicione comentários explicando cada etapa do loop e identifique onde ocorre a 'parada' (termination condition)."
```

**Saída esperada**: Claude refina o código anterior adicionando comentários, sem você precisar repetir o contexto.

#### Conceito Reforçado

| Aspecto | Resultado |
|---|---|
| **Prompt 1** | Claude entendeu o conceito isolado |
| **Prompt 2** | Claude reutilizou a resposta anterior (contexto acumulou) |
| **Prompt 3** | Claude refinou a resposta, mantendo coesão |

O **Ciclo de Feedback** é a ferramenta principal para iteração. Você não precisa "reiniciar" o contexto — ele cresce com cada prompt.

---

### 2.1 — Visualizar o Agent Loop

**Arquivo de Referência**: `02-COMO-FUNCIONA-INTERNAMENTE.md` (Agent Loop)  
**Conceito**: O Agent Loop é o while-not-done que executa ferramentas repetidamente até não haver mais tool calls.  
**Dificuldade**: Fácil | **Tempo**: ~4 min

Você vai forçar múltiplas tool calls em sequência para observar o loop em ação.

#### Setup

Crie um arquivo `arquitetura_test.py` no diretório raiz:

```bash
cat > arquitetura_test.py << 'EOF'
def saudacao(nome):
    return f"Ola {nome}"

def calcular_dobro(numero):
    return numero * 2
EOF
```

#### Comando

```bash
claude "Leia o arquivo arquitetura_test.py e me diga: (1) quantas funções tem, (2) o que cada uma faz, (3) execute uma chamada de teste de cada função em Python."
```

#### Saída Esperada

Claude vai:

```
Lendo arquitetura_test.py...

[Análise do arquivo]

[Resultado da análise: 2 funções]

[Execução de testes]
```

Você verá mensagens como:
- `Reading arquitetura_test.py` (Tool: Read)
- `Executando: python -c "..."` (Tool: Bash)

#### Conceito Reforçado

O Agent Loop em ação:

```
Iteração 1: Read arquivo → resultado integrado
Iteração 2: Bash executa teste → resultado integrado
Iteração 3: Claude sintetiza resposta final
while not done
```

Cada iteração do loop recebe o resultado da anterior e o integra ao contexto automaticamente.

---

### 2.2 — Inspecionar o Uso de Tokens

**Arquivo de Referência**: `02-COMO-FUNCIONA-INTERNAMENTE.md` (Token Management)  
**Conceito**: Cada interação consome tokens; é importante monitorar a distribuição (prompt / arquivo / histórico).  
**Dificuldade**: Médio | **Tempo**: ~5 min

Você vai ativar o monitoramento de tokens e observar a distribuição.

#### Setup

Ative a exibição de tokens na configuração:

```bash
claude "/config"
```

Procure por `displayTokenUsage` e defina como `true`. (Se não encontrar, tudo bem — continue com o exercício.)

#### Comando

```bash
claude "Analise todo o arquivo 02-COMO-FUNCIONA-INTERNAMENTE.md e responda: qual é a fórmula de custo apresentada e qual é o exemplo real de refatoração com seu custo estimado?"
```

#### Saída Esperada

Se o `displayTokenUsage` estiver ativado, você verá algo como:

```
Analisando 02-COMO-FUNCIONA-INTERNAMENTE.md...

[Resposta]

--- Token Usage ---
Input tokens: 4500
Output tokens: 1200
Total: 5700 tokens
Custo estimado: (~$0.017)
```

Decomposição esperada de input tokens:
- ~200 tokens: seu prompt
- ~2500 tokens: conteúdo do arquivo
- ~1800 tokens: histórico/contexto

#### Conceito Reforçado

Cada componente do contexto consome tokens:

| Componente | Proporção Típica |
|---|---|
| Seu prompt | 5-10% |
| Arquivo(s) | 40-60% |
| CLAUDE.md | 2-5% |
| Histórico | 10-30% |
| Disponível (buffer) | ~10% |

Monitorar tokens ajuda a otimizar prompts e evitar truncagem em sessões longas.

---

### 2.3 — Testar a Compactação de Contexto

**Arquivo de Referência**: `02-COMO-FUNCIONA-INTERNAMENTE.md` (Compactação de Contexto)  
**Conceito**: Quando o contexto atinge ~80% dos tokens, o sistema resume conversas antigas para liberar espaço.  
**Dificuldade**: Difícil | **Tempo**: ~8 min

Você vai fazer uma sessão longa com ~10 prompts para pressionar o context window e observar a compactação.

#### Setup

Abra um editor ou terminal para monitorar. Você vai fazer 10 prompts curtos em sequência.

#### Sequência de Prompts

Execute cada um após o outro **na mesma sessão** (não feche Claude entre eles):

1. `"O que é o context window em Claude Code?"`
2. `"Qual é o tamanho do context window do Sonnet 4.6?"`
3. `"Quais são os 3 principais componentes que consomem tokens?"`
4. `"Como a compactação de contexto funciona quando se atinge 80%?"`
5. `"Que tipos de resumos o sistema faz durante compactação?"`
6. `"Qual é a diferença entre compactação automática e manual?"`
7. `"Dê um exemplo de como uma conversa longa é resumida."`
8. `"Qual é o impacto da compactação na qualidade da resposta?"`
9. `"Como posso evitar atingir o limite de contexto em sessões longas?"`
10. `"Resuma tudo que discutimos sobre contexto nesta sessão."`

#### Saída Esperada (Prompts 1-5)

Claude responde normalmente com latência de 5-15s por prompt.

#### Saída Esperada (Prompts 6-10)

Se o contexto começar a ficar cheio, você pode observar:
- Mensagens explícitas como `[Context compacted to save space]` (alguns ambientes mostram)
- Respostas mais curtas (Claude resumiu para economizar espaço)
- Possível latência ligeiramente maior (processamento do resumo)

#### Conceito Reforçado

A **Compactação de Contexto** é automática:

```
Tokens usados < 80% do limite
  ↓ (continue normalmente)
Tokens usados ≥ 80% do limite
  ↓ (acionar compactação)
Sistema resume conversas antigas
  ↓
Libera ~20-30% de espaço
  ↓
Continua aceitando novos prompts
```

Você vivenciou isto: sessão longa com 10 prompts funciona porque o sistema compacta automaticamente.

---

### 3.1 — Comparar Modelos na Prática

**Arquivo de Referência**: `03-TECNOLOGIAS-SUBJACENTES.md` (Modelos Disponíveis)  
**Conceito**: Diferentes modelos têm tradeoffs: Haiku é rápido/barato, Sonnet é equilibrado, Opus é potente/caro.  
**Dificuldade**: Fácil | **Tempo**: ~4 min

Você vai executar o mesmo prompt com 2 modelos diferentes e comparar.

#### Comando 1 — Haiku (rápido)

```bash
claude --model claude-haiku-4-5 "Explique em 3 linhas o que é o Agent Loop em Claude Code."
```

**Tempo observado**: ~1-2 segundos  
**Saída esperada**: Explicação concisa de 3 linhas.

#### Comando 2 — Opus (potente)

```bash
claude --model claude-opus-4-7 "Explique em 3 linhas o que é o Agent Loop em Claude Code."
```

**Tempo observado**: ~10-15 segundos  
**Saída esperada**: Explicação mais detalhada e elaborada.

#### Conceito Reforçado

Comparação prática:

| Aspecto | Haiku 4.5 | Opus 4.7 |
|---|---|---|
| **Velocidade** | ~500ms | ~10-15s |
| **Profundidade** | Superficial | Profundo |
| **Custo estimado** | $0.80 por 1M | $15 por 1M |
| **Melhor para** | Bugfix rápido | Análise pesada |

**Regra prática**: Use Haiku para iteração rápida, Opus para decisões críticas.

---

### 3.2 — Criar e Ativar um Hook

**Arquivo de Referência**: `03-TECNOLOGIAS-SUBJACENTES.md` (Hook System)  
**Conceito**: Hooks são scripts que executam antes/depois de eventos (prompts, tools, respostas).  
**Dificuldade**: Médio | **Tempo**: ~6 min

Você vai criar um hook simples que imprime um símbolo após cada execução de ferramenta.

#### Setup

Crie um script de hook:

```bash
mkdir -p ~/.claude/hooks
cat > ~/.claude/hooks/after-tool.sh << 'EOF'
#!/bin/bash
echo "✓ Ferramenta executada"
EOF
chmod +x ~/.claude/hooks/after-tool.sh
```

Agora registre o hook no `~/.claude/settings.json` ou `~/.claude/settings.local.json`:

Procure pela seção `hooks` e adicione (ou crie se não existir):

```json
{
  "hooks": {
    "after-tool-execution": "~/.claude/hooks/after-tool.sh"
  }
}
```

#### Comando

```bash
claude "Leia o arquivo README.md deste repositório e conte quantos arquivos .md tem na raiz."
```

#### Saída Esperada

Você verá:

```
Reading README.md...
✓ Ferramenta executada

[Claude fornece o resultado]
```

O símbolo `✓` aparece após Claude executar o tool `Read`, confirmando que o hook foi acionado.

#### Conceito Reforçado

Hooks permitem automação:

```
Tool executada → Hook `after-tool-execution` dispara → Script roda → Log, validação, etc.
```

Casos de uso comuns:
- Auto-commit git após edições
- Linting após mudanças de código
- Logging de operações críticas

---

### 3.3 — Estruturar um CLAUDE.md Avançado

**Arquivo de Referência**: `03-TECNOLOGIAS-SUBJACENTES.md` (CLAUDE.md Avançado)  
**Conceito**: Um CLAUDE.md bem estruturado com 6 seções define o contexto completo do projeto.  
**Dificuldade**: Difícil | **Tempo**: ~7 min

Você vai criar um CLAUDE.md completo seguindo o padrão recomendado.

#### Setup

Crie um arquivo `CLAUDE_advanced.md` (não sobrescrevemos o real):

```bash
cat > CLAUDE_advanced.md << 'EOF'
# CLAUDE.md — Projeto de Exemplo

## 1. Contexto

Projeto educacional em Python 3.12 que ensina arquitetura de sistemas.
Framework: FastAPI para API REST
Database: PostgreSQL 15
Objetivo: Demonstrar padrões de arquitetura limpa

## 2. Padrões

- **Linguagem**: Portuguese para documentação, English para código
- **Type hints**: Obrigatórios em todos os parâmetros e retornos
- **Docstrings**: Google-style com Args, Returns, Raises
- **Nomenclatura**: snake_case para variáveis/funções, PascalCase para classes
- **Async**: async/await por padrão em handlers HTTP

## 3. Decisões Arquiteturais

- Usar camadas: rotas → serviços → repositório → banco
- Validação de entrada em handlers HTTP (not in services)
- Logging centralizado com structlog
- Tratamento de erros com exceções customizadas

## 4. Convenções

- Arquivos de testes nomeados `test_*.py`
- Imports organizados: stdlib, 3rd-party, local
- Máximo 100 caracteres por linha
- Blank line após imports, entre functions

## 5. Restrições

- Sem N+1 queries (sempre usar joins ou bulk operations)
- Cobertura de testes > 80%
- Validação de entrada em todos os endpoints
- Nunca expor erros internos ao cliente

## 6. Ferramentas

- Testing: pytest + pytest-cov
- Linting: ruff, mypy
- Formatting: black
- CI: GitHub Actions
EOF
```

#### Comando

```bash
claude "Leia o arquivo CLAUDE_advanced.md e crie uma função async para obter um usuário por ID que siga TODAS as convenções e restrições definidas."
```

#### Saída Esperada

Claude gera uma função que respeita **todas as 6 seções** do CLAUDE.md:

```python
async def obter_usuario_por_id(usuario_id: int) -> dict[str, Any]:
    """Obtém um usuário do banco de dados por ID.
    
    Args:
        usuario_id: ID único do usuário.
    
    Returns:
        Dicionário com dados do usuário.
    
    Raises:
        UsuarioNaoEncontrado: Se o usuário não existir.
    """
    usuario = await db.fetch(
        "SELECT id, nome, email FROM usuarios WHERE id = ?", usuario_id
    )
    if not usuario:
        raise UsuarioNaoEncontrado(f"Usuário {usuario_id} não encontrado")
    return usuario
```

**Observe**:
- Type hints (`async`, `int`, `dict[str, Any]`)
- Docstring Google-style
- snake_case `obter_usuario_por_id`
- Validação e erro customizado
- Comentário mínimo (apenas quando necessário explicar WHY)

#### Conceito Reforçado

Um CLAUDE.md bem estruturado transforma a qualidade do código:

| Sem CLAUDE.md | Com CLAUDE.md |
|---|---|
| Inconsistência entre respostas | Consistência garantida |
| Sem padrões claros | Padrões implícitos em todo código |
| Repetição de contexto em cada prompt | Contexto carregado uma vez |
| Qualidade depende do prompt | Qualidade é basal (mesmo em prompts curtos) |

---

## Checklist de Conclusão

Depois de executar os exercícios, marque os itens abaixo para confirmar que você dominou cada conceito:

- [ ] **1.1**: Observei o fluxo completo (Inicialização → Tool Use → Resposta)
- [ ] **1.2**: Entendi que CLAUDE.md é carregado automaticamente na Inicialização
- [ ] **1.3**: Vivenciei o Ciclo de Feedback com 3 prompts encadeados
- [ ] **2.1**: Vi o Agent Loop executar múltiplas tool calls em sequência
- [ ] **2.2**: Inspecionei a distribuição de tokens (prompt / arquivo / histórico)
- [ ] **2.3**: Pressionar o context window e observar a compactação automática
- [ ] **3.1**: Comparei Haiku (rápido) vs Opus (potente) na prática
- [ ] **3.2**: Criei e ativei um hook em `~/.claude/settings.json`
- [ ] **3.3**: Estruturei um CLAUDE.md com todas as 6 seções

---

## Próximos Passos

Parabéns! Você completou o **Laboratório Prático de Arquitetura**. Agora está pronto para aprender técnicas avançadas de prompting:

- **Próximo módulo**: Leia [`03-COMANDOS-SINTAXE/01-PROMPT-BASICO.md`](../03-COMANDOS-SINTAXE/01-PROMPT-BASICO.md) para aprender sintaxe e padrões de prompts efetivos
- **Padrões de uso**: Depois explore [`04-PADROES-USO/01-ITERACAO-RAPIDA.md`](../04-PADROES-USO/01-ITERACAO-RAPIDA.md) para técnicas de iteração avançadas
- **Aprofundamento**: Se quiser entender melhor token management e compactação, releia [`02-COMO-FUNCIONA-INTERNAMENTE.md`](./02-COMO-FUNCIONA-INTERNAMENTE.md)

---

**Criado em**: 2026-05-23  
**Tempo total de prática**: ~48 minutos (trilha completa) ou ~15 minutos (trilha iniciante)
