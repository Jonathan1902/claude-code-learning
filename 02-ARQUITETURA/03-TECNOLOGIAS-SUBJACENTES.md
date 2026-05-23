# Tecnologias Subjacentes

## Modelos Claude Disponíveis

### Sonnet 4.6 (Padrão)
- **Velocidade**: Rápido (~2-3s response)
- **Precisão**: 90% de Opus, 70% mais rápido
- **Custo**: Médio
- **Caso de uso**: Iteração rápida, debugging, refatoração
- **Context window**: 200k tokens
- **Token pricing**: $3/$15 por 1M tokens

### Opus 4.7
- **Velocidade**: Lento (~10-15s response)
- **Precisão**: Melhor para análise profunda
- **Custo**: Mais alto
- **Caso de uso**: Arquitetura, análise de segurança, decisões críticas
- **Context window**: 200k tokens
- **Token pricing**: $15/$60 por 1M tokens

### Haiku 4.5
- **Velocidade**: Muito rápido (~500ms response)
- **Precisão**: Adequado para tarefas simples
- **Custo**: Mais baixo
- **Caso de uso**: Bugfix rápido, edição simples
- **Context window**: 100k tokens
- **Token pricing**: $0.80/$4 por 1M tokens

---

## API Anthropic

Claude Code usa a **Anthropic API** sob o capô.

### Fluxo
```
Claude Code (interface)
    ↓
API Anthropic (autenticação + billing)
    ↓
Modelo Claude (processamento)
    ↓
Resposta (volta pelo mesmo caminho)
```

### Autenticação
```bash
# Variável de ambiente
export ANTHROPIC_API_KEY="sk-ant-..."

# Claude Code carrega automaticamente
# Armazenado em ~/.claude/api_key
```

### Billing
```
Cobrado por:
- Tokens de entrada (mais barato)
- Tokens de saída (mais caro)

Não cobrado por:
- Chamadas falhadas (de sua culpa)
- Leitura de arquivo local
- Execução de comando bash
```

---

## Model Context Protocol (MCP)

Protocolo que expande capabilities de Claude Code.

### Arquitetura MCP

```
Claude Code
    ↓
MCP Client (built-in)
    ↓
MCP Server (customizado ou oficial)
    ↓
Recurso externo (DB, API, etc)
```

### Exemplo: PostgreSQL via MCP

```
Usuário: "Quantos usuários ativos temos?"

Claude Code:
1. Reconhece query de BD
2. Usa MCP PostgreSQL server
3. Server executa: SELECT COUNT(*) FROM users...
4. Resultado integrado na resposta
```

### Servidores MCP Oficiais
- **Filesystem**: acesso a arquivos
- **PostgreSQL**: queries de BD
- **GitHub**: integração com repos
- **Google Drive**: acesso a documentos

---

## Hook System

Sistema de automação baseado em eventos.

### Hooks Disponíveis

| Hook | Quando Dispara | Exemplo |
|---|---|---|
| `before-prompt` | Antes de enviar prompt | Validação de código |
| `before-response` | Antes de mostrar resposta | Formatação automática |
| `after-tool-execution` | Após ferramenta executar | Auto-commit git |
| `before-git-push` | Antes de push | Lint checklist |

### Exemplo Hook: Auto-format antes de resposta

```bash
#!/bin/bash
# ~/.claude/hooks/before-response.sh
# Formata Python automaticamente

if [[ "$FILE" == *.py ]]; then
  black "$FILE"
  isort "$FILE"
fi
```

Configuração em settings.json:
```json
{
  "hooks": {
    "before-response": "~/.claude/hooks/before-response.sh"
  }
}
```

---

## CLAUDE.md

Arquivo especial de configuração de projeto (não execute, apenas documente).

### Estrutura Recomendada

```markdown
# Projeto: Nome

## Contexto
- Linguagem: Python
- Framework: Django 4.2
- DB: PostgreSQL 14

## Padrões
- Type hints sempre
- Docstrings em tudo
- Black + Isort para formatação
- Pytest para testes

## Decisões Arquiteturais
- Monolítico por simplicidade
- ORM Django (não raw SQL)
- Cache Redis (não memória)

## Convenções
- Variáveis em snake_case
- Classes em PascalCase
- Constantes em SCREAMING_SNAKE_CASE

## Restrições
- Não fazer queryset em loop (N+1 problem)
- Sempre validar entrada de usuário
- Testes precisam >80% coverage

## Ferramentas
- Black: formatação Python
- Pytest: testes
- Ruff: linter
```

### Por que é importante

```
Sem CLAUDE.md:
Claude: "Devo usar Django ORM ou raw SQL?"
Você: "ORM"
Claude: "Ok, mas acho que raw SQL é mais claro aqui"
Você: "SEGUE O PADRÃO!"

Com CLAUDE.md:
Claude lê: "Use Django ORM, nunca raw SQL"
Claude: "Usando ORM como padrão do projeto"
✅ Eficiente, sem discussão
```

---

## Token Counting e Pricing

### Exemplo Real

**Operação**: Refatorar arquivo com 2k linhas

```
Entrada:
- Seu prompt: 100 tokens
- Arquivo lido: 2,000 tokens
- CLAUDE.md: 500 tokens
- Tool result (read): 2,000 tokens
Total entrada: ~4,600 tokens

Saída:
- Resposta Claude: 300 tokens
- Código refatorado: 2,100 tokens
Total saída: ~2,400 tokens

Custo:
- Entrada: 4,600 × $0.003 / 1,000 = $0.0138
- Saída: 2,400 × $0.015 / 1,000 = $0.036
- Total operação: $0.05 (aproximado)
```

### Como Monitorar

```bash
# Ver uso de tokens (em settings.json)
"displayTokenUsage": true

# Claude Code mostra após cada resposta:
"Tokens: 4,600 input | 2,400 output | Total: 7,000"
```

---

## Compactação de Prompt (Prompt Caching)

Claude usa **cache de prompts** para economizar tokens e tempo.

### Como funciona

```
Primeira chamada (SEM cache):
- Arquivo: 10k tokens
- Prompt: 500 tokens
- TOTAL: 10,500 tokens × $0.003 = $0.0315

Chamadas próximas (COM cache):
- Arquivo (cacheado): 10k tokens (custo reduzido 90%)
- Prompt novo: 500 tokens
- Cache setup: 1,200 tokens (setup adicional)
- TOTAL: ~3k tokens novos × $0.003 = $0.009

Economia: 65% de tokens se contextoreusar
```

### Quando cache é útil

```
✅ Útil:
- Iteração sobre mesmo arquivo
- Sessão longa com mesmo contexto
- Múltiplos prompts sobre mesmo documento

❌ Não útil:
- Arquivo muda a cada prompt
- Contexto completamente novo
- Sessão única de prompt
```

---

## Segurança e Privacidade

### Como Claude Code protege dados

1. **API Call criptografada** (HTTPS)
2. **Sem persistência de arquivo** (não salvo em cache Anthropic)
3. **Sem análise de dados** (Anthropic não treina em seus dados)
4. **Controle local** (settings.json define o que compartilhar)

### O que Claude Code pode acessar

```
Vê:
- Arquivo aberto no editor
- Arquivo que você fornecer
- Output de comandos que você rodou

Não vê:
- Outros arquivos do projeto (a menos que você forneça)
- Variáveis de ambiente (a menos que output mostre)
- Senhas em .env (a menos que você paste)

Nunca compartilha com Anthropic:
- Seu código em cache permanente
- Histórico de sessão anterior
```

---

**Voltar**: [Arquitetura](01-FLUXO-COMPLETO.md)
