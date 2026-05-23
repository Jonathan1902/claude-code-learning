# Limitações do Claude Code

## 1. Context Window

### O Problema
Claude Sonnet 4.6 tem context window de **200k tokens** (~50k-100k linhas de código).

### Impacto
- Não consegue processar projeto inteiro simultaneamente
- Arquivos muito grandes podem ser truncados
- Resultado: análise incompleta

### Solução
```
# ✅ Certo: focar em arquivos específicos
"Analise apenas app/views.py para este bug"

# ❌ Errado: fornecer tudo
"Analise todo o projeto"
```

---

## 2. Sem Memória Entre Sessões

### O Problema
Cada sessão é independente. Claude não lembra de:
- Prompts anteriores
- Decisões tomadas
- Contexto de projeto

### Impacto
- Repetir contexto a cada sessão
- Inconsistência entre sessões
- Custo aumentado (repetir informação)

### Solução
```
Crie CLAUDE.md com:
- Padrões de código
- Decisões arquiteturais
- Convenções do projeto
- Instruções gerais
```

---

## 3. Não Substitui Revisão Humana

### O Problema
Claude pode gerar código:
- Sintaticamente correto mas semanticamente errado
- Que passa em testes mas não em produção
- Com trade-offs não óbvios

### Impacto
- Bugs passam despercebidos
- Decisões técnicas sem contexto
- Performance ruim

### Solução
```
# Sempre:
1. Revise o código gerado
2. Teste em ambiente não-produção
3. Faça code review com humano
4. Valide em produção gradualmente
```

---

## 4. Sem Acesso à Internet por Padrão

### O Problema
Claude Code não pode:
- Buscar informações atualizadas
- Verificar documentação online em tempo real
- Acessar APIs externas direto

### Impacto
- Conhecimento limitado a cutoff (Ago 2025)
- Não sabe última versão de libraries
- Não pode validar contra APIs em tempo real

### Solução
```
# Use WebSearch para informação recente
"Busque a documentação atual de FastAPI"

# Forneça manualmente versões
"Estou usando PostgreSQL 15.3"
```

---

## 5. Custo por Token

### O Problema
Cada prompt/resposta custa tokens:
- Input: ~$0.003 por 1K tokens
- Output: ~$0.015 por 1K tokens

### Impacto
- Iterações múltiplas = custo cumulativo
- Contexto grande = mais caro
- Uso produtivo requer estimativa

### Solução
```
# ✅ Eficiente
- Prompts focados e concisos
- Fornecer apenas código relevante
- Reutilizar contexto na sessão

# ❌ Ineficiente
- Contexto desnecessário
- Múltiplas sessões repetidas
- Falta de planejamento
```

---

## 6. Erros Silenciosos

### O Problema
Claude pode:
- Interpretar mal o que você quer
- Fazer suposição incorreta
- Não avisar quando tem dúvida

### Impacto
- Código errado é gerado
- Você não percebe o erro
- Bugs difíceis de rastrear

### Solução
```
# Sempre:
1. Revise saída de Claude
2. Teste código antes de produção
3. Use "Explique passo a passo"
4. Peça para Claude listar suposições
```

---

## 7. Limitações de Tool Use

### O Problema
Claude não pode:
- Interagir com sistemas interativos (requer input)
- Realizar operações de longa duração (timeout)
- Acessar alguns tipos de arquivos (binários)

### Impacto
- Alguns scripts requerem input manual
- Deploy pode timeout
- Imagens não podem ser lidas diretamente

### Solução
```
# Evite:
- Scripts interativos
- Operações que duram >5 min
- Binários complexos

# Prefira:
- Scripts automatizados
- Dividir tarefas longas
- Exportar dados como texto
```

---

## 8. Modelos Diferentes = Resultados Diferentes

### O Problema
- Sonnet 4.6: Fast, bom para iteração, menos preciso
- Opus 4.7: Lento, melhor para análise profunda
- Haiku 4.5: Rápido, menos capacidade

### Impacto
- Escolher modelo errado compromete resultado
- Trade-off entre velocidade e qualidade

### Solução
```
# Recomendação:
- Debugging rápido: Haiku
- Iteração normal: Sonnet (padrão)
- Análise complexa: Opus
```

---

## Checklist: Antes de Usar Claude Code

- [ ] Tenho código específico para analisar?
- [ ] Tarefa requer iteração?
- [ ] Contexto cabe em context window?
- [ ] Vou revisar output manualmente?
- [ ] Caso de uso apropriado?
- [ ] Documentei padrões em CLAUDE.md?

Se não a todas → considere alternativas.

---

**Voltar**: [O que é Claude Code?](01-O-QUE-E-CLAUDE-CODE.md)
