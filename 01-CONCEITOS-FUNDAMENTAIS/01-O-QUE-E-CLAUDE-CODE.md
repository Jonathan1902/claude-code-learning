# O que é Claude Code?

## Definição

Claude Code é uma **ferramenta CLI e IDE extension** desenvolvida pela Anthropic que integra o modelo Claude diretamente no fluxo de trabalho do desenvolvedor. Diferente do chat web tradicional, Claude Code foi otimizado para **leitura e manipulação de código**, com suporte a tool use integrado.

## Claude Code vs Chat Web

| Aspecto | Claude Code | Chat Web |
|---|---|---|
| **Interface** | CLI / IDE Extension / Web App | Browser |
| **Tool Use** | Nativo (lê, edita, executa comandos) | Limitado |
| **Contexto de Código** | Acesso direto a arquivos | Copy-paste manual |
| **Velocidade** | Iteração rápida | Mais lento |
| **Persistência** | Memória na sessão atual | Não persiste contexto |

## Claude Code vs API Anthropic

### Claude Code (Interface)
- ✅ Iteração interativa
- ✅ Acesso direto a arquivos
- ✅ Tool use automático
- ❌ Não é programático
- ❌ Modelo selecionável via interface

### Anthropic API (Programático)
- ✅ Integração em aplicações
- ✅ Controle total do programa
- ✅ Batch processing
- ❌ Requer código
- ❌ Sem interface visual

## Componentes Principais

### 1. **Agente Claude**
O modelo base que processa prompts e decide como usar ferramentas.

### 2. **Tool Use**
Claude Code pode:
- 📖 Ler arquivos (`Read`)
- ✏️ Editar arquivos (`Edit`)
- 🔍 Buscar padrões (`Bash` com grep)
- ⚙️ Executar comandos (`Bash`)
- 🌐 Buscar na web (`WebSearch`, `WebFetch`)
- 📝 Escrever arquivos (`Write`)

### 3. **MCP Servers**
Integração com servidores Model Context Protocol para expandir capacidades.

### 4. **Hooks**
Scripts executados automaticamente em eventos (pré-commit, pós-resposta, etc).

### 5. **CLAUDE.md**
Arquivo de configuração que documenta padrões, decisões e contexto do projeto.

## Fluxo Básico

```
Usuário → Prompt → Claude Code → Tool Use → Resultado → Resposta Iterativa
```

1. **Usuário** dá instrução em linguagem natural
2. **Claude Code** lê contexto (arquivos, projeto)
3. **Agente Claude** decide quais ferramentas usar
4. **Tool Use** executa (edita arquivo, roda teste, etc)
5. **Resultado** é processado e explicado ao usuário

## Quando Usar Claude Code

- ✅ Debugging e investigação de código
- ✅ Refatoração de arquivos
- ✅ Geração de documentação
- ✅ Análise de performance
- ✅ Automação DevOps
- ✅ Processamento de dados

## Limitações Importantes

- ⚠️ Context window limitado (~200k tokens com Sonnet 4.6)
- ⚠️ Sem memória entre sessões (use CLAUDE.md para persistência)
- ⚠️ Não substitui revisão humana
- ⚠️ Custo por token (considerar em uso produtivo)

---

**Próximo**: [Casos de Uso Práticos](02-CASOS-DE-USO.md)
