# O que é Claude Code?

> **Para quem é este tópico:** qualquer pessoa que queira entender o que o Claude Code faz — não exige saber programar.
>
> **Ao terminar você será capaz de:**
> - Explicar o que é Claude Code em uma frase
> - Diferenciar Claude Code, Chat Web e API Anthropic
> - Decidir se Claude Code resolve o seu caso

> 💡 *Imagine um colega que lê seus arquivos, edita código, roda comandos no terminal e explica o que fez — sem você precisar copiar e colar nada. Esse é o Claude Code.*

## Definição

Claude Code é uma **ferramenta CLI e IDE extension** desenvolvida pela Anthropic que integra o modelo Claude diretamente no fluxo de trabalho do desenvolvedor. Diferente do chat web tradicional, Claude Code foi otimizado para **leitura e manipulação de código**, com suporte a tool use integrado.

> 📖 **Glossário rápido:**
> - **CLI** = Command Line Interface — a interface por linha de comando (o "terminal preto").
> - **IDE extension** = plugin que roda dentro do editor (VS Code, JetBrains, etc.).
> - **Tool use** = ver o glossário na seção "Componentes Principais" abaixo.

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

> 📖 *Tool Use = capacidade do modelo de executar ações reais (ler arquivo, editar, rodar comando) e não só devolver texto. É o que torna o Claude Code útil dentro do projeto.*

Claude Code pode:
- 📖 Ler arquivos (`Read`)
- ✏️ Editar arquivos (`Edit`)
- 🔍 Buscar padrões (`Bash` com grep)
- ⚙️ Executar comandos (`Bash`)
- 🌐 Buscar na web (`WebSearch`, `WebFetch`)
- 📝 Escrever arquivos (`Write`)

### 3. **MCP Servers**

> 📖 *MCP = Model Context Protocol — uma espécie de "plugin" que conecta o Claude a sistemas externos (Gmail, Drive, banco de dados, APIs internas).*

Integração com servidores Model Context Protocol para expandir capacidades.

### 4. **Hooks**

> 📖 *Hook = script automático que dispara em resposta a um evento (antes de um commit, depois de uma resposta do Claude, ao parar a sessão).*

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

### Exemplo concreto

> **Você:** Corrija o bug de timezone em `src/dates.py`.
>
> **Claude Code:**
> 1. *(usa `Read` em `src/dates.py`)*
> 2. *(detecta `datetime.now()` sem timezone na linha 42)*
> 3. *(aplica `Edit` substituindo por `datetime.now(timezone.utc)`)*
>
> *"Encontrei e corrigi o bug na linha 42 — o `datetime.now()` estava sem timezone, o que causava horários inconsistentes entre servidores. Quer que eu rode os testes?"*

Repare em três coisas: você falou em linguagem natural; o Claude **escolheu sozinho** quais ferramentas usar (`Read` + `Edit`); e a resposta final explica o que mudou e propõe o próximo passo.

## Quando Usar Claude Code

- ✅ Debugging e investigação de código
- ✅ Refatoração de arquivos
- ✅ Geração de documentação
- ✅ Análise de performance
- ✅ Automação DevOps
- ✅ Processamento de dados

## Limitações Importantes

- ⚠️ **Context window limitado (~200k tokens com Sonnet 4.6)** — equivale a aproximadamente **150 mil palavras**, mais ou menos o tamanho de um livro técnico médio. Acima desse limite, o modelo começa a "esquecer" o início da conversa.
- ⚠️ **Sem memória entre sessões** — ao fechar o terminal, o contexto se perde. Use `CLAUDE.md` para gravar padrões, decisões e vocabulário que devem persistir entre sessões.
- ⚠️ **Não substitui revisão humana** — código gerado deve ser lido, testado e validado antes de ir para produção, principalmente em mudanças sensíveis (segurança, migrações de banco, deploys).
- ⚠️ **Custo por token** — uso intensivo pode chegar a alguns dólares por hora; para uso ocasional o impacto é desprezível, mas em times grandes ou pipelines automatizados vale monitorar.

---

**Próximo**: [Casos de Uso Práticos](02-CASOS-DE-USO.md)
