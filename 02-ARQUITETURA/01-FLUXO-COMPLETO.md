# Fluxo Completo do Claude Code

## Diagrama ASCII do Fluxo

```
┌─────────────────────────────────────────────────────────────────┐
│                      USUÁRIO DIGITA PROMPT                       │
│              "Refatore este arquivo para melhorar"               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  CLAUDE CODE PROCESSA ENTRADA                    │
│  - Carrega CLAUDE.md (contexto do projeto)                      │
│  - Identifica arquivo atual (context)                           │
│  - Prepara mensagem para Claude API                             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│               CLAUDE API (MODEL + TOOL USE)                      │
│  - Recebe prompt + contexto                                     │
│  - Analisa e decide ferramenta necessária                       │
│  - Retorna: "usar Read tool para arquivo"                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                    ▼                 ▼
        ┌──────────────────┐  ┌──────────────────┐
        │  LOOP DE TOOL USE │  │   TOOL CALL     │
        │                  │  │   (Read file)    │
        └────────┬─────────┘  └────────┬─────────┘
                 │                     │
                 └─────────┬───────────┘
                           │
                           ▼
        ┌──────────────────────────────────┐
        │ FERRAMENTA EXECUTA              │
        │ - Lê arquivo                     │
        │ - Retorna conteúdo               │
        └────────────────────┬─────────────┘
                             │
                             ▼
        ┌──────────────────────────────────┐
        │ RESULTADO INTEGRADO              │
        │ - Claude analisa código          │
        │ - Propõe refatoração             │
        │ - Decide: precisa Edit tool      │
        └────────────────────┬─────────────┘
                             │
        ┌────────────────────┴────────────────────┐
        │                                         │
        ▼                                         ▼
  ┌──────────────────┐              ┌──────────────────┐
  │   Edit Tool      │              │  Resposta        │
  │ (modifica arquivo)│              │  para Usuário    │
  └────────┬─────────┘              └────────┬─────────┘
           │                                  │
           └──────────────┬───────────────────┘
                          │
                          ▼
        ┌──────────────────────────────────┐
        │ ARQUIVO MODIFICADO + EXPLICAÇÃO  │
        │ - Alterações aplicadas           │
        │ - Explicação do porquê           │
        │ - Próximos passos sugeridos      │
        └──────────────────────────────────┘
```

---

## Fases Detalhadas

### 1. **Inicialização**
```
Usuário → Claude Code
↓
Carrega:
- Arquivo atual
- CLAUDE.md (se existir)
- Histórico de sessão (tokens usados)
- Modelo selecionado
```

### 2. **Processamento do Prompt**
```
Prompt em linguagem natural
    ↓
Parse de intenção
    ↓
Montagem de contexto (file content + CLAUDE.md)
    ↓
Chamada à API Anthropic
```

### 3. **Tool Use Loop**
Claude pode:
- **Read**: Ler arquivo
- **Edit**: Modificar arquivo
- **Write**: Criar novo arquivo
- **Bash**: Executar comando
- **WebSearch**: Buscar na internet
- **MCP Tools**: Ferramentas customizadas

Exemplo:
```
Claude quer debugar → precisa Read (arquivo) → analisar → propõe Edit
```

### 4. **Iteração Contínua**
```
Prompt 1 → Tool Use → Resultado 1
    ↓
Refina com feedback → Prompt 2
    ↓
Tool Use → Resultado 2
    ↓
... (até usuário estar satisfeito)
```

---

## Exemplo Passo a Passo

**Tarefa**: "Adicione testes para este função"

```
1. USUÁRIO DIGITA
   "Adicione testes para a função `calcular_juros`"
   (+ arquivo aberto: main.py)

2. CLAUDE CODE PROCESSA
   - Identifica arquivo atual
   - Carrega main.py
   - Monta contexto

3. CLAUDE API PENSA
   - "Preciso ler a função"
   - → Retorna: "usar Read tool"

4. TOOL USE: READ
   - Lê main.py
   - Extrai função `calcular_juros`
   - Retorna conteúdo

5. CLAUDE API ANALISA
   - Vê função (e.g., juro composto)
   - Pensa em casos de teste
   - Retorna: "usar Write tool para tests.py"

6. TOOL USE: WRITE
   - Cria tests.py com:
     - Teste caso normal
     - Teste juro zero
     - Teste taxa negativa
     - etc.

7. RESPOSTA AO USUÁRIO
   - "Criei 5 testes para sua função"
   - Mostra conteúdo de tests.py
   - Sugere: "Quer rodá-los?"

8. USUÁRIO: "Sim"
   - Claude usa Bash tool
   - Executa: pytest tests.py
   - Mostra resultado
```

---

## Ciclo de Feedback

```
┌─────────────────────┐
│   Usuário vê saída  │
│   Claude Code       │
└──────────┬──────────┘
           │
      ┌────▼────┐
      │ Feedback?│
      └─┬──────┬─┘
        │      │
      ❌ Não   ✅ Sim
        │        │
        │      ┌─▼─────────────────┐
        │      │ Refine: "Mas..."   │
        │      │ Novo prompt        │
        │      └────┬──────────────┘
        │           │
        │      Volta para Step 3
        │           │
        │      [Nova iteração]
        │
        └──────────┘
         Pronto!
```

---

## Context Management

Claude Code gerencia contexto para:
- **Reutilizar** informações já fornecidas
- **Evitar** repetição desnecessária
- **Economizar** tokens
- **Manter** coerência entre respostas

```
Sessão 1: Fornecer contexto (custoso em tokens)
Sessão 2: Reutilizar + novo contexto (mais barato)
Sessão 3+: Manter histórico em CLAUDE.md (persistente)
```

---

## Timing e Performance

| Ação | Tempo Típico |
|---|---|
| Inicialização | <1s |
| Processamento de prompt (pequeno) | 1-3s |
| Tool use simples (Read) | <500ms |
| API call | 5-15s |
| Tool use complexo (Bash) | 2-10s |
| Resposta ao usuário | Imediata |

---

**Próximo**: [Como Funciona Internamente](02-COMO-FUNCIONA-INTERNAMENTE.md)
