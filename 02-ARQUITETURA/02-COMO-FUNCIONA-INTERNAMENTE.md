# Como Claude Code Funciona Internamente

## Arquitetura Interna

```
┌──────────────────────────────────────────────────────┐
│            CLAUDE CODE HARNESS (Controle)            │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │  Input Parser (prompt do usuário)            │  │
│  └────────────────┬─────────────────────────────┘  │
│                   │                                │
│  ┌────────────────▼──────────────────────────────┐ │
│  │  Context Manager                              │ │
│  │  - Arquivo atual                              │ │
│  │  - CLAUDE.md                                  │ │
│  │  - Token counter                              │ │
│  │  - History                                    │ │
│  └────────────────┬──────────────────────────────┘ │
│                   │                                │
│  ┌────────────────▼──────────────────────────────┐ │
│  │  Claude Model (via API)                       │ │
│  │  - Recebe contexto + prompt                   │ │
│  │  - Processa (internamente: LLM)               │ │
│  │  - Retorna: resposta + tool calls             │ │
│  └────────────────┬──────────────────────────────┘ │
│                   │                                │
│  ┌────────────────▼──────────────────────────────┐ │
│  │  Tool Execution Engine                        │ │
│  │  - Executa Read, Edit, Write                  │ │
│  │  - Executa Bash, WebSearch                    │ │
│  │  - Aplica resultados                          │ │
│  └────────────────┬──────────────────────────────┘ │
│                   │                                │
│  ┌────────────────▼──────────────────────────────┐ │
│  │  Output Formatter (resposta ao usuário)       │ │
│  │  - Markdown formatting                        │ │
│  │  - Syntax highlighting                        │ │
│  │  - Tool results display                       │ │
│  └──────────────────────────────────────────────┘ │
│                                                   │
└──────────────────────────────────────────────────────┘
```

---

## Agent Loop (Loop de Agente)

```
while not done:
    # 1. Claude pensa: precisa de ferramenta?
    if model_response.contains_tool_call():
        # 2. Executa ferramenta
        tool_result = execute_tool(model_response.tool_call)
        
        # 3. Integra resultado
        context.add(tool_result)
        
        # 4. Chama modelo novamente com resultado
        model_response = call_api(context)
    else:
        # 5. Sem mais ferramentas, responde usuário
        display_response(model_response)
        done = True
```

---

## Exemplo Real: Debugging

**Entrada**: "Não estou vendo output do print"

```
1️⃣ Claude pensa:
   "Preciso ler o arquivo para ver o código"
   → Tool: Read(app.py)

2️⃣ Ferramenta executa:
   Arquivo lido, conteúdo retornado

3️⃣ Claude analisa:
   "Vi o problema! Print está fora de escopo"
   → Tool: Edit(mudar indentação)

4️⃣ Ferramenta executa:
   Arquivo editado

5️⃣ Claude oferece:
   "Para testar, quer que eu rode?"
   → Aguardando feedback usuário

6️⃣ Usuário: "Sim"

7️⃣ Claude executa:
   → Tool: Bash(python app.py)

8️⃣ Resultado:
   Output aparece, problema resolvido

9️⃣ Claude responde:
   "Visto! Precisava de indentação correta."
```

---

## Token Management

### Como tokens são contados

```
Entrada:
- Seu prompt: N tokens
- Arquivo carregado: M tokens
- CLAUDE.md: K tokens
- Histórico: H tokens
Total Input = N + M + K + H

Saída:
- Resposta Claude: R tokens
Total Output = R

Custo sessão = (Input × $0.003) + (Output × $0.015) / 1000
```

### Otimização de Tokens

```
❌ Ineficiente
- Fornecer projeto inteiro
- Histórico de 50 mensagens
- Código irrelevante

✅ Eficiente
- Apenas arquivo necessário
- Histórico essencial
- Contexto focado em CLAUDE.md
```

---

## Context Window (200k tokens)

Sonnet 4.6 pode processar até 200k tokens de entrada.

```
Exemplo de distribuição:
- Seu prompt: 500 tokens (0.25%)
- Arquivo grande: 50k tokens (25%)
- CLAUDE.md: 5k tokens (2.5%)
- Histórico: 10k tokens (5%)
- Disponível para nova resposta: 134.5k tokens (67.25%)
```

**Quando cabe tudo**: Use tudo!
**Quando não cabe**: Seja seletivo (focar em relevante)

---

## Compactação de Contexto

Claude Code pode "resumir" conversas antigas para fazer espaço para novas.

```
Conversação longa:
M1 (editor) → R1 (Claude)
M2 (usuário refina) → R2 (Claude)
M3 (novo bug) → R3 (Claude)
... (50 mensagens)

Quando atinge ~80% tokens:
[Sistema resume conversas antigas]

Novo espaço disponível para continuar
```

---

## Settings.json e Hooks

### settings.json
Arquivo de configuração em `~/.claude/settings.json`:

```json
{
  "model": "claude-sonnet-4-6",
  "permissions": {
    "bash": "allow-read-only"
  },
  "hooks": {
    "before-response": "linter.sh"
  }
}
```

### Hooks
Scripts que executam automaticamente:

```
before-prompt: valida entrada antes de enviar
before-response: processa antes de mostrar ao usuário
after-tool: executa após ferramenta (e.g., auto-format)
```

---

## CLAUDE.md (Persistência)

Arquivo especial que Claude Code lê automaticamente:

```markdown
# Projeto: API Django

## Padrões
- Use type hints em tudo
- Django ORM, nunca SQL raw
- Testes com pytest

## Decisões
- Python 3.11+
- PostgreSQL 14+

## Estrutura
- `api/` - código principal
- `tests/` - testes
```

Claude integra isso automaticamente em cada contexto.

---

## Fluxo de Edição (Edit Tool)

```
Usuário pede mudança:
"Adicione import no topo"

Claude:
1. Lê arquivo (Read)
2. Identifica local preciso
3. Calcula mudança mínima
4. Usa Edit tool com:
   - old_string: texto exato a trocar
   - new_string: novo texto
5. Valida mudança
6. Aplica com sucesso
```

Edit é preciso porque:
- ✅ Alvo exato (não quebra indentação)
- ✅ Rápido (não reescreve arquivo inteiro)
- ✅ Reversível (mudança mínima)

---

## MCP Servers

Model Context Protocol - extensão de ferramentas:

```
Ferramentas padrão (built-in):
- Read, Edit, Write
- Bash
- WebSearch, WebFetch

MCP Servers (customizáveis):
- Banco de dados (ex: PostgreSQL query)
- APIs específicas (ex: GitHub API)
- Ferramentas de negócio (ex: Jira)
```

Usuário pode adicionar MCP servers em settings.json.

---

**Próximo**: [Tecnologias Subjacentes](03-TECNOLOGIAS-SUBJACENTES.md)
