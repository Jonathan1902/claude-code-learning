# Cheat Sheet - Referência Rápida

## Claude Code Slash Commands

| Comando | O que faz | Exemplo |
|---|---|---|
| `/help` | Mostra ajuda | `/help` |
| `/clear` | Limpa conversa | `/clear` |
| `/model <name>` | Troca modelo | `/model sonnet` |
| `/fast` | Toggle fast mode | `/fast` |
| `/code` | Abre editor | `/code` |
| `/terminal` | Abre terminal | `/terminal` |
| `/share` | Cria link compartilhável | `/share` |
| `/ultrareview` | Review em Cloud | `/ultrareview` |
| `/loop [interval]` | Loop de tarefa | `/loop 5m` |
| `/schedule` | Agenda remote agent | `/schedule` |

---

## Tool Use Rápido

### Read (Ler arquivo)
```
"Leia app/views.py"
Claude usa: Read tool
Resultado: Arquivo inteiro na conversa
```

### Edit (Editar arquivo)
```
"Adicione type hints neste método"
Claude usa: Edit tool (mudança cirúrgica)
Resultado: Arquivo modificado
```

### Write (Criar arquivo)
```
"Crie test_auth.py com testes para..."
Claude usa: Write tool
Resultado: Novo arquivo criado
```

### Bash (Executar comando)
```
"Rode pytest para validar"
Claude usa: Bash tool
Resultado: Output do comando
```

### WebSearch / WebFetch
```
"Busque documentação recente de FastAPI"
Claude usa: WebSearch
Resultado: Links + resumo relevante
```

---

## Atalhos de Teclado

| Shortcut | Ação |
|---|---|
| `Ctrl+Enter` | Enviar prompt |
| `Shift+Enter` | Nova linha no prompt |
| `Ctrl+L` | Limpar conversa |
| `Tab` | Autocomplete (em alguns contextos) |
| `Ctrl+Shift+P` | Paleta de comandos |
| `Ctrl+/` | Toggle sidebar |

---

## Padrões de Prompt Rápidos

### Debugging Rápido
```
"Por que [função] retorna [valor inesperado]?
Aqui: [arquivo]"
```

### Refatoração Rápida
```
"Refatore [arquivo] para ser mais legível
Requisitos: [type hints, docstrings, etc]"
```

### Teste Rápido
```
"Testes para [função]
Edge cases: [lista]"
```

### Documento Rápido
```
"Docstrings para [arquivo]
Estilo: [Google/NumPy/etc]"
```

---

## Flags Importantes

### Model Selection
```bash
claude-code -m sonnet   # Sonnet 4.6 (default)
claude-code -m opus     # Opus 4.7
claude-code -m haiku    # Haiku 4.5
```

### Configuration
```bash
claude-code --config     # Ver settings
claude-code --api-key    # Set API key
```

---

## Contexto Mínimo (Template Rápido)

```
[Contexto]: [Tech stack]
[Tarefa]: [O que fazer]
[Arquivo]: [Colar código]
[Quer]: [Resultado esperado]
```

**Exemplo**:
```
Django 4.2 + PostgreSQL
Debugue método que retorna None quando devia retornar User
[colar models.py]
Quer: Identificar bug + fix
```

---

## Token Budgets (Aproximado)

| Tipo | Tokens |
|---|---|
| Arquivo Python 100 linhas | ~500 tokens |
| Arquivo Python 1000 linhas | ~5k tokens |
| CLAUDE.md típico | ~500 tokens |
| Conversa de 10 trocas | ~10k tokens |
| Contexto total típico | ~20k tokens |

---

## Ordem de Ação Recomendada

### Novo Projeto
1. Criar CLAUDE.md (contexto, padrões, decisões)
2. Fornecer arquivo relevante
3. Fazer primeiro prompt

### Debugging
1. Fornecer error + stack trace
2. Fornecer arquivo onde erro ocorre
3. Perguntar "qual é a raiz?"

### Feature Nova
1. Descrever requisito
2. Fornecer arquivo onde vai plugar
3. Pedir implementação passo-a-passo

### Otimização
1. Descrever performance target
2. Fornecer código atual
3. Pedir análise + sugestão

---

## Checklist Pre-Prompt

- [ ] Contexto claro (tech, version)?
- [ ] Tarefa específica?
- [ ] Arquivo fornecido (se relevante)?
- [ ] Restrições mencionadas?
- [ ] Formato esperado definido?
- [ ] Exemplos (se zero-shot)?

---

## Status Line Info

```
tanjiro@host ~/path | Claude Sonnet 4.6 | ████░░░░░░░░░░░░░░░░ 20%

         user@host       current dir      model name      tokens used
```

---

## Common Issues + Quick Fix

| Problema | Fix |
|---|---|
| "Context too long" | Remova arquivo não-relevante |
| "Command not found" | Prefixe com path absoluto |
| "Permission denied" | Grant permission (settings) |
| "API rate limit" | Aguarde 60s ou use Haiku |
| "Resposta truncada" | Peça resumo ou split em 2 prompts |
| "Claude não lembrou" | Forneça contexto novamente ou use CLAUDE.md |

---

## Settings.json Essencial

```json
{
  "model": "claude-sonnet-4-6",
  "permissions": {
    "bash": "allow-read-only",
    "git": "allow"
  },
  "displayTokenUsage": true
}
```

---

**Voltar**: [Padrões de Prompt](02-PADROES-DE-PROMPT.md)
