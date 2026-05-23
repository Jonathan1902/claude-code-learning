# Casos de Uso Práticos

## 1. Debugging e Investigação

### Cenário
Aplicação Python com erro em runtime.

### Como Usar Claude Code
```
"Tenho este stack trace. Qual é a raiz do problema?"
[fornecer stack trace + arquivo relevante]
```

**Resultado**: Claude lê o arquivo, analisa o stack trace e identifica o bug.

---

## 2. Refatoração de Código

### Cenário
Método muito longo que precisa ser dividido.

### Como Usar Claude Code
```
"Refatore este arquivo para melhorar legibilidade"
```

**Resultado**: Claude Code edita o arquivo automaticamente e explica as mudanças.

---

## 3. Geração de Documentação

### Cenário
Código sem docstrings ou README.

### Como Usar Claude Code
```
"Adicione docstrings em todos os métodos e escreva um README"
```

**Resultado**: Arquivos são atualizados com documentação completa.

---

## 4. Análise de Performance

### Cenário
Script Python rodando lentamente.

### Como Usar Claude Code
```
"Execute com profiling e me mostre onde está o bottleneck"
```

**Resultado**: 
- Claude roda profiler
- Identifica funções lentas
- Sugere otimizações específicas

---

## 5. Testes Automatizados

### Cenário
Novo módulo sem cobertura de testes.

### Como Usar Claude Code
```
"Escreva testes completos para este módulo"
```

**Resultado**: Suite de testes é gerada com múltiplos casos.

---

## 6. Automação DevOps

### Cenário
Deploy repetitivo e propenso a erro.

### Como Usar Claude Code
```
"Crie um script de deploy automatizado"
```

**Resultado**: Script shell ou Python é gerado e testado.

---

## 7. Processamento de Dados

### Cenário
CSV grande que precisa ser transformado.

### Como Usar Claude Code
```
"Leia este CSV e transforme conforme o padrão especificado"
```

**Resultado**: Script de ETL é gerado e executado.

---

## 8. Análise de Código Existente

### Cenário
Projeto legado que ninguém entende.

### Como Usar Claude Code
```
"Me explique como este fluxo de autenticação funciona"
```

**Resultado**: Explicação detalhada com diagramas ASCII.

---

## 9. Segurança

### Cenário
Verificar se há vulnerabilidades conhecidas.

### Como Usar Claude Code
```
"Analise este código para vulnerabilidades de segurança"
```

**Resultado**: Análise de OWASP Top 10, inputs validation, etc.

---

## 10. Migrações de Tecnologia

### Cenário
Atualizar Django 3.x para 4.x.

### Como Usar Claude Code
```
"Migre este projeto para Django 4.x respeitando as breaking changes"
```

**Resultado**: Código atualizado com compatibilidade.

---

**Próximo**: [Quando Usar Claude Code](03-QUANDO-USAR.md)
