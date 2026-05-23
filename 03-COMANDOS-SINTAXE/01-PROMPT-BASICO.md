# Estrutura de um Bom Prompt

## Componentes Essenciais

### 1. Contexto
"Você está em um projeto Django"

### 2. Tarefa Específica
"Quero adicionar autenticação via OAuth"

### 3. Restrições
"Sem modificar modelos existentes"

### 4. Formato Esperado
"Código pronto para produção com tipos"

---

## Exemplo 1: Prompt Ruim ❌

```
"Faça um script"
```

**Problemas**:
- Vago demais
- Sem contexto
- Sem restrições
- Claude vai chutar

---

## Exemplo 2: Prompt Melhor ✅

```
"Preciso de um script Python que:
- Leia um CSV com dados de usuários
- Valide emails
- Exporte resultado em JSON
- Trate erros de I/O
- Rode em Python 3.11+"
```

**Melhorias**:
- Específico
- Linguagem clara
- Restrições explícitas
- Formato definido

---

## Exemplo 3: Prompt Excelente ⭐

```
"Contexto: Projeto Django 4.2, PostgreSQL, use type hints

Tarefa: Criar comando manage.py que migre usuários de Auth0 para DB local

Restrições:
- Sem modificar tabela existente de permissions
- Validar email antes de inserir
- Logar erros em migration_errors.log
- Reversível (allow rollback)

Formato: 
- Código com docstrings
- Tests com pytest >80% coverage
- Instrução de uso em docstring

Forneço:
- Auth0 export.json (anexo)
- current User model (posso carregar)
"
```

**Por que funciona**:
- ✅ Contexto completo do projeto
- ✅ Tarefa ultra-específica
- ✅ Restrições claras
- ✅ Formato esperado definido
- ✅ Oferece informação necessária

---

## Estrutura Template

```
[Contexto do Projeto]
"Estou em um projeto [linguagem/framework], usando [tecnologias]"

[Tarefa Principal]
"Preciso de [O QUÊ EXATAMENTE]"

[Restrições e Requisitos]
"Importante:
- [Restrição 1]
- [Restrição 2]
- [Requisito 1]"

[Formato e Qualidade]
"Quero:
- [Formato código: with types, with tests, etc]
- [Documentação: docstrings, comments]
- [Padrão: seguir convenção do projeto]"

[Contexto Adicional]
"Para referência:
- [Arquivo relevante]
- [Exemplo similar]
- [Especificação de negócio]"
```

---

## Erros Comuns

### ❌ Muito Vago
```
"Refatore o código"
```
✅ Melhor:
```
"Refatore app/views.py para:
- Extrair lógica repetida em 3 métodos
- Adicionar type hints
- Remover variáveis não usadas"
```

### ❌ Assumir conhecimento
```
"Implemente como no projeto X"
```
✅ Melhor:
```
"Implemente seguindo padrão do projeto
(ver CLAUDE.md para convenções)"
```

### ❌ Pedir múltiplas coisas ao mesmo tempo
```
"Refatore, adicione testes, documente e otimize"
```
✅ Melhor:
```
"Passo 1: Refatore app/views.py
(Depois pedimos testes)"
```

### ❌ Fornecer contexto irrelevante
```
"Aqui está todo o projeto de 500 arquivos"
```
✅ Melhor:
```
"Aqui está apenas app/models.py (relevante)
Ver CLAUDE.md para contexto geral"
```

---

## Dicas de Ouro

### 📍 Ser Específico
```
❌ "Debugue este erro"
✅ "Debugue: TypeError in line 42 of auth.py"
```

### 📍 Fornecedorização Progressiva
```
Primeiro prompt: "Crie módulo de autenticação"
Claude: "Preciso entender suas requirements"

Segundo prompt: "OAuth2, 3 providers (Google, GitHub, Microsoft)"
Claude: "Entendido, preciso template de BD?"

Terceiro prompt: "Aqui está User model, usa PostgreSQL"
Claude: "Ótimo, agora consigo criar"
```

### 📍 Reutilizar Contexto
```
Prompt 1: "Aqui está projeto Django"
Prompt 2: "Agora refatore views.py"
(Não repete contexto)

Prompt 3: "Agora testes"
(Continua com contexto da sessão)
```

### 📍 Indicar Prioridades
```
"Prioridade:
1. Funcionar corretamente (essencial)
2. Performante (importante)
3. Código bonito (nice-to-have)"
```

---

## Exercício

Escreva prompts para:

1. Adicionar logging a um arquivo Python
2. Criar API REST em FastAPI
3. Debugar query SQL lenta

**Soluções no** [Exemplos Reais](03-EXEMPLOS-REAIS.md)

---

**Próximo**: [Padrões de Prompt](02-PADROES-DE-PROMPT.md)
