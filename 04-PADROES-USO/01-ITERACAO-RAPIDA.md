# Iteração Rápida com Claude Code

## O Ciclo Prompt-Teste-Refine

```
┌─────────────────┐
│  1. Prompt      │ Seu pedido inicial
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│  2. Claude Responde + Code  │ Implementação
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  3. Teste Resultado         │ Valida output
└────────┬────────────────────┘
         │
    ┌────┴────────┐
    │ Funciona?   │
    └────┬────┬───┘
    ✅ Sim   ❌ Não
      │      │
      │      ▼
      │    ┌──────────────────────┐
      │    │ 4. Refine            │ Feedback
      │    │ "Mas precisa..."      │
      │    └────────┬─────────────┘
      │             │
      │        [Volta ao 2]
      │
      ▼
   PRONTO!
```

---

## Passo 1: Primeiro Prompt

### Seja Direto
```
"Crie uma função que calcula desconto em compras
- Recebe: preço, quantidade, categoria
- Retorna: preço com desconto
- Use type hints"
```

### O que fornecer
- ✅ Linguagem (Python, Go, JS?)
- ✅ Contexto (Django? FastAPI? standalone?)
- ✅ Requisitos (types? testes? docs?)
- ❌ Muito código (deixa Claude decidir implementação)

---

## Passo 2: Claude Responde

Claude pode:
- Gerar código
- Fazer perguntas esclarecedoras
- Pedir mais contexto

### Se pedir contexto
```
Claude: "Qual é a tabela de desconto? Fixa ou por categoria?"

Você: "Desconto fixo:
- Normal: 5%
- VIP: 15%
- Corporate: 25%"

Claude: "Perfeito, vou implementar"
```

---

## Passo 3: Teste o Resultado

### Automaticamente
```
Claude código já com:
- Type hints
- Docstring
- Exemplos de uso

Você pode copiar e rodar:
python -c "print(calculate_discount(100, 5, 'vip'))"
```

### Se forneceu arquivo
```
Claude usa Bash tool:
pytest test_discount.py -v

Resultado mostra tudo passar
```

---

## Passo 4: Refine com Feedback

### Sem Funcionar Bem
```
Você: "Desconto está errado para múltiplas quantidades.
Deveria ser progressivo:
- 1-5 unidades: 5%
- 6-10 unidades: 10%
- 11+: 15%"

Claude: "Ah entendi, vou corrigir"
[nova implementação]
```

### Performance Ruim
```
Você: "Funciona mas lento. Pode otimizar?"

Claude: "Que tipo de otimização?
Caching? Índices? Algoritmo diferente?"

Você: "Caching de cálculos"

Claude: [implementa com cache]
```

### Não Segue Padrão do Projeto
```
Você: "Funciona mas não segue nosso padrão.
Ver CLAUDE.md para detalhes"

Claude: [relê CLAUDE.md]
"Ah, precisa de [...]. Vou ajustar"
```

---

## Exemplo Completo: 3 Iterações

### Iteração 1: Básico
```
VOCÊ: "Função para calcular juros compostos
Recebe: principal, taxa anual, anos
Retorna: valor final com juros"

CLAUDE: [Implementa fórmula básica]

RESULTADO: Funciona, muito simples
```

### Iteração 2: Refine
```
VOCÊ: "Precisa validar:
- principal > 0
- taxa entre 0 e 100%
- anos >= 1
Levantar ValueError se inválido"

CLAUDE: [Adiciona validação]

RESULTADO: Melhor, com error handling
```

### Iteração 3: Otimize
```
VOCÊ: "Suporte para capitalização mensal/diária
(não só anual)"

CLAUDE: [Generaliza para qualquer período]

RESULTADO: Produção ready
```

---

## Quando Parar de Iterar

### ✅ Está Pronto Quando:

1. **Funciona corretamente**
   - Testes passam
   - Edge cases cobertos
   - Output correto

2. **Segue padrões do projeto**
   - Type hints presentes
   - Naming conventions ok
   - Docstrings adicionadas

3. **Performance aceitável**
   - Roda em tempo esperado
   - Sem memory leaks
   - Escalável se necessário

4. **Você está satisfeito**
   - Nenhuma dúvida remanescente
   - Entende o código gerado
   - Confiante em usar produção

### ❌ Sinais que Precisa Mais Iteração:

- [ ] Teste falhando
- [ ] Código não legível
- [ ] Performance ruim
- [ ] Não segue padrão
- [ ] Error handling inadequado
- [ ] Você não entende o código

---

## Técnicas para Iteração Eficiente

### 1. Feedback Específico
```
❌ Ruim: "Não gosto do código"
✅ Bom: "Remove os imports não usados na linha 5-7"
```

### 2. Exemplo Concreto
```
❌ Ruim: "Não funciona bem"
✅ Bom: "Testa input=(100, 0.05, 2), esperado=110.25, recebido=105"
```

### 3. Uma Mudança por Iteração
```
❌ Ruim: "Adicione tipos, docstrings, testes, otimize"
✅ Bom: "Adicione type hints" [depois pede testes]
```

### 4. Contexto Reutilizado
```
Prompt 1: "Crie função X com [contexto]"
Prompt 2: "Adicione validação" (não repete contexto)
Prompt 3: "Otimize performance" (contexto ainda ativo)
```

---

## Decisão de Implementação

### Simples (< 30 min)
```
Iteração direta:
1. Descrever
2. Testar
3. Pronto
```

### Médio (30 min - 2h)
```
Iteração com 2-3 refinamentos:
1. Descrever
2. Testar + refine 1x
3. Testar + refine 2x
4. Pronto
```

### Complexo (> 2h)
```
Decompor em passos:
1. Descrever passo 1
2. Implementar passo 1
3. Testar passo 1
[repete para passo 2, 3, etc]
```

---

## Exemplo: Feature Completa em 5 Iterações

**Objetivo**: Adicionar sistema de notificações por email

### Iteração 1: Estrutura
```
"Crie classe EmailNotification com método send()
Tipos: tipo_notificação, destinatários, assunto, corpo"
```

### Iteração 2: SMTP Integration
```
"Integre com SMTP real usando smtplib
Credentials vêm de environment variables"
```

### Iteração 3: Validation
```
"Valide emails, trate erro de conexão,
retry com backoff exponencial"
```

### Iteração 4: Testes
```
"Crie testes com mock de SMTP
Casos: sucesso, erro de conexão, email inválido"
```

### Iteração 5: Documentação
```
"Docstrings completas, exemplo de uso,
instrução de setup"
```

**Total**: ~2 horas de trabalho bem organizado

---

## Context Preservation

Claude mantém contexto durante iterações:

```
Iteração 1: Fornece arquivo A (5k tokens)
Iteração 2: Não repete arquivo A (Claude lembra)
Iteração 3: Pode referenciar "a função de A" sem fornecer
```

**Dica**: Use `CLAUDE.md` para contexto que dura múltiplas sessões.

---

**Próximo**: [Especificações Detalhadas](02-ESPECIFICACOES-DETALHADAS.md)
