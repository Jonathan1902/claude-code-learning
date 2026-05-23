# Claude Code Learning Repository 📚

Repositório de aprendizado completo das funcionalidades do **Claude Code** de maneira incremental e progressiva, do básico ao avançado, com exemplos práticos.

---

## 📖 O que é Claude Code?

Claude Code é uma ferramenta CLI e IDE extension da Anthropic que integra o modelo Claude diretamente no fluxo de trabalho do desenvolvedor, com suporte a tool use integrado para leitura, edição e execução de comandos.

**Este repositório documenta:**
- ✅ Conceitos fundamentais
- ✅ Arquitetura e como funciona
- ✅ Padrões e técnicas de prompting
- ✅ Uso efetivo e iterativo
- ✅ Casos de uso reais (10+ exemplos)
- ✅ Troubleshooting e debugging

---

## 📂 Estrutura do Repositório

```
📁 01-CONCEITOS-FUNDAMENTAIS/        (Introdução ao Claude Code)
├─ 01-O-QUE-E-CLAUDE-CODE.md         → Definição, propósito, CLI vs API
├─ 02-CASOS-DE-USO.md                → Debugging, refatoração, geração, análise
├─ 03-QUANDO-USAR.md                 → Critérios e matriz de decisão
├─ 04-LIMITACOES.md                  → Context window, custo, segurança
└─ 05-HANDS-ON.md                    → 🧪 Laboratório prático com 12 exercícios

📁 02-ARQUITETURA/                    (Como funciona internamente)
├─ 01-FLUXO-COMPLETO.md              → Diagrama ASCII do fluxo end-to-end
├─ 02-COMO-FUNCIONA-INTERNAMENTE.md  → Agent loop, tool use, token management
├─ 03-TECNOLOGIAS-SUBJACENTES.md     → Modelos, API Anthropic, MCP, hooks, CLAUDE.md
└─ diagrama-fluxo.png.md             → Placeholder para diagrama visual

📁 03-COMANDOS-SINTAXE/               (Como fazer prompts efetivos)
├─ 01-PROMPT-BASICO.md               → Estrutura, componentes, exemplos
├─ 02-PADROES-DE-PROMPT.md           → Chain-of-thought, few-shot, role, etc
├─ 03-EXEMPLOS-REAIS.md              → 10 exemplos práticos comentados
└─ CHEAT-SHEET.md                    → Referência rápida, atalhos, flags

📁 04-PADROES-USO/                    (Técnicas e estratégias)
├─ 01-ITERACAO-RAPIDA.md             → Ciclo prompt-teste-refine
├─ 02-ESPECIFICACOES-DETALHADAS.md   → Quando fornecer contexto completo
├─ 03-DEBUGGING.md                   → Técnicas de debugging colaborativo
└─ 04-ANALISE.md                     → Análise de segurança, performance, etc

📁 05-CASOS-REAIS/                    (Exemplos end-to-end)
├─ 01-PROCESSAMENTO-DADOS.md         → ETL, CSV, transformação de schema
├─ 02-GERACAO-CODIGO.md              → REST API, testes, deploy scripts, CLI
├─ 03-ANALISE-PERFORMANCE.md         → Profiling, otimização, benchmarks
├─ 04-DOCUMENTACAO.md                → Docstrings, README, API docs, ADR
└─ 05-AUTOMACAO-DEVOPS.md            → CI/CD, Infrastructure as Code, monitoring

📁 06-TROUBLESHOOTING/                (Problemas e soluções)
├─ 01-ERROS-COMUNS.md                → 10 erros comuns com soluções
├─ 02-COMO-DEBUGAR.md                → Estratégias de debugging
└─ 03-SOLUCOES-RAPIDAS.md            → Lookup table problema → solução

└─ README.md                          → Este arquivo
```

---

## 🚀 Guia de Estudo Recomendado

### Semana 1: Fundamentos
```
Dia 1-2:  01-CONCEITOS-FUNDAMENTAIS/
  ├─ O-QUE-E-CLAUDE-CODE.md (30 min)
  ├─ CASOS-DE-USO.md (30 min)
  ├─ QUANDO-USAR.md (20 min)
  └─ LIMITACOES.md (20 min)

Dia 3:    01-CONCEITOS-FUNDAMENTAIS/05-HANDS-ON.md
  └─ Laboratório Prático (trilha iniciante: 15 min, completa: 55 min)

Dia 4:    02-ARQUITETURA/01-FLUXO-COMPLETO.md (45 min)

Dia 5:    03-COMANDOS-SINTAXE/01-PROMPT-BASICO.md (1h)
```

### Semana 2: Técnica
```
Dia 1:    03-COMANDOS-SINTAXE/
  ├─ PADROES-DE-PROMPT.md (1h)
  └─ CHEAT-SHEET.md (30 min reference)

Dia 2-3:  04-PADROES-USO/01-ITERACAO-RAPIDA.md (1.5h)

Dia 4:    04-PADROES-USO/03-DEBUGGING.md (1h)

Dia 5:    Pratique! Use Claude Code para 2-3 tarefas reais
```

### Semana 3-4: Avançado
```
Segunda:  05-CASOS-REAIS/01-PROCESSAMENTO-DADOS.md (1h)
Terça:    05-CASOS-REAIS/02-GERACAO-CODIGO.md (1.5h)
Quarta:   05-CASOS-REAIS/03-ANALISE-PERFORMANCE.md (1h)
Quinta:   Escolha 1 caso real do seu projeto, aplique
```

### Ongoing: Reference
```
- CHEAT-SHEET.md → bookmarked
- SOLUCOES-RAPIDAS.md → quando der erro
- QUANDO-USAR.md → para decisões
```

---

## ⏱️ Tempo Total Estimado

| Módulo | Leitura | Prática | Total |
|---|---|---|---|
| Conceitos | 2h | 1h | **3h** |
| Arquitetura | 1.5h | 0.5h | **2h** |
| Prompting | 2h | 2h | **4h** |
| Padrões | 2h | 3h | **5h** |
| Casos Reais | 3h | 5h | **8h** |
| Troubleshooting | 1h | 1h | **2h** |
| **TOTAL** | **11.5h** | **12.5h** | **~24h** |

---

## 🎯 Objetivos de Aprendizado

Após completar este repositório, você será capaz de:

### Conceitual
- [ ] Explicar o que é Claude Code e como funciona
- [ ] Decidir quando usar Claude Code vs chat web vs API
- [ ] Entender limitações (context window, custo, etc)

### Prático
- [ ] Escrever prompts efetivos que produzem código correto
- [ ] Iterar rapidamente com feedback estruturado
- [ ] Debugar problemas em colaboração com Claude
- [ ] Aplicar padrões (few-shot, chain-of-thought, etc)

### Avançado
- [ ] Gerar código complexo (APIs, testes, deploy scripts)
- [ ] Analisar performance e propor otimizações
- [ ] Documentar código e decisões arquiteturais
- [ ] Resolver problemas reais em produção

---

## 💡 Exemplo Rápido

### Seu Primeiro Prompt

```
Contexto: Python 3.11 project

Crie função que valida email:
- Recebe string (email)
- Retorna boolean
- Use regex simples
- Inclua docstring
- Type hints
```

**Resultado**: Claude Code gera função pronta, com testes, sem você ter que especificar cada detalhe.

---

## 🔗 Links Úteis

- [Claude Code Documentation](https://github.com/anthropics/claude-code)
- [Claude API Docs](https://docs.anthropic.com/claude)
- [Anthropic Models](https://www.anthropic.com/pricing)
- [GitHub](https://github.com)

---

## 🤝 Como Contribuir

Quer adicionar conteúdo?

1. Fork repositório
2. Crie branch `feature/seu-topico`
3. Adicione markdown seguindo estrutura
4. Abra PR com descrição

Tópicos bem-vindos:
- Novos casos de uso
- Erros que encontrou + solução
- Padrões específicos de linguagem (Go, Rust, etc)
- Integrações com ferramentas (GitHub, GitLab, etc)

---

## 📋 Checklist: Primeiro Uso

- [ ] Instalou Claude Code? (`claude-code --version`)
- [ ] Tem API key? (`export ANTHROPIC_API_KEY=sk-ant-...`)
- [ ] Completou leitura de 01-CONCEITOS-FUNDAMENTAIS?
- [ ] Testou primeiro prompt do CHEAT-SHEET?
- [ ] Debugou um erro real com Claude?
- [ ] Completou 1 caso de uso de 05-CASOS-REAIS?

---

## 📧 Feedback

Encontrou erro? Tem sugestão?

- Abra issue no GitHub
- Mencione qual arquivo + linha
- Descreva problema/sugestão

---

## 📄 Licença

Apache License 2.0

---

## 🎓 Nível por Seção

```
Iniciante   ████████░░ 01 + 02 (Conceitos e Arquitetura)
Intermediário ████████░░ 03 + 04 (Prompting e Padrões)
Avançado    ████░░░░░░ 05 + 06 (Casos Reais e Troubleshooting)
```

---

**Comece com**: [01-CONCEITOS-FUNDAMENTAIS/01-O-QUE-E-CLAUDE-CODE.md](./01-CONCEITOS-FUNDAMENTAIS/01-O-QUE-E-CLAUDE-CODE.md)

**Última atualização**: 2026-05-23
