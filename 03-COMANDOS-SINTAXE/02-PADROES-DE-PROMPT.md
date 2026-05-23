# Padrões de Prompt Avançados

## 1. Chain-of-Thought (Cadeia de Pensamento)

Pede ao Claude para **raciocinar passo a passo**.

### Exemplo

```
❌ Sem CoT:
"Por que este código é lento?"

✅ Com CoT:
"Analise este código e:
1. Identifique loops aninhados
2. Conte operações O(n²)
3. Explique complexidade
4. Sugira otimização
Mostre passo a passo"
```

### Benefício
- Melhor raciocínio
- Menos erros
- Mais confiável para problemas complexos

---

## 2. Few-Shot Prompting

Fornecer exemplos do resultado esperado.

### Exemplo

```
"Converta variáveis Python para camelCase.

Exemplos:
- user_name → userName
- is_active → isActive
- total_amount → totalAmount

Agora converta estas variáveis:
- customer_id
- product_price
- order_status"
```

### Benefício
- Formato exato é claro
- Menos ambiguidade
- Claude entende padrão

---

## 3. Zero-Shot Prompting

Nenhum exemplo, só instruções.

### Exemplo

```
"Converta variáveis em camelCase"
```

### Benefício
- Mais rápido
- Menos tokens
- Se tarefa é óbvia

### Quando usar
- Tarefas simples (renomear, formatar)
- Claude já tem expertise
- Resultado óbvio

---

## 4. Role Prompting

Atribuir um "papel" ao Claude.

### Exemplo

```
❌ Sem role:
"Revise este código"

✅ Com role:
"Você é um especialista em performance Python.
Revise este código e identifique bottlenecks.
Foque em O(n²) loops e cálculos repetidos."
```

### Variações
```
"Você é um especialista em segurança"
"Você é DevOps experiente em AWS"
"Você é especialista em UX"
```

### Benefício
- Claude adota perspectiva apropriada
- Qualidade de análise melhora

---

## 5. Structured Output

Solicitar saída em formato estruturado.

### Exemplo

```
"Analise este código e retorne JSON:
{
  \"complexity\": \"O(n²)\",
  \"issues\": [\"issue1\", \"issue2\"],
  \"fix_priority\": \"high\",
  \"estimated_speedup\": \"3-5x\"
}"
```

### Benefício
- Parseable por máquina
- Sem ambiguidade
- Fácil de processar

---

## 6. Decomposição

Quebrar tarefa grande em passos.

### Exemplo

```
❌ Tudo de uma vez:
"Faça um sistema de autenticação completo"

✅ Decomposto:
"Passo 1: Criar modelo User com type hints
Passo 2: Hash de password com bcrypt
Passo 3: Endpoint de registro
Passo 4: Endpoint de login
Passo 5: Token JWT
Passo 6: Middleware de autenticação
Passo 7: Testes

Comece pelo Passo 1"
```

### Benefício
- Menos erro
- Feedback contínuo
- Controle granular

---

## 7. Adversarial Prompting

Pedir para Claude **questionar premissas**.

### Exemplo

```
"Quero usar GraphQL em vez de REST.
Levante 3 argumentos CONTRA esta decisão
(para eu considerar)"
```

### Benefício
- Força criativa de Claude
- Questiona suposições
- Mais pensamento crítico

---

## 8. Meta-Prompting

Pedir para Claude melhorar seu próprio prompt.

### Exemplo

```
"Meu prompt é muito vago. 
Aqui está:
'Otimize este código'

Reescreva o prompt para ser mais claro e efetivo"
```

### Benefício
- Aprender a fazer melhores prompts
- Iteração rápida
- Claude como coach

---

## 9. Comparação e Contraste

Pedir para comparar abordagens.

### Exemplo

```
"Compare estas 3 formas de autenticar:
1. Sessions (tradicionais)
2. JWT (stateless)
3. OAuth2 (delegado)

Para cada: prós, contras, quando usar"
```

### Benefício
- Visão holística
- Entendimento profundo
- Informado na decisão

---

## 10. Conditional Prompting

Pedir para Claude responder diferente conforme situação.

### Exemplo

```
"Analise este código:
- Se tem erro: explique + corrija
- Se performance ruin: perfil + otimize
- Se bem escrito: sugira melhorias avançadas"
```

### Benefício
- Flexibilidade
- Adapta-se ao contexto
- Eficiente

---

## Combinação de Padrões

Os padrões podem ser combinados:

```
[Role Prompting]
"Você é especialista em performance"

[Structured Output]
"Retorne como JSON"

[Chain of Thought]
"Passo a passo"

[Few-Shot]
"Exemplos: ..."

Resultado: Análise profunda e estruturada
```

---

## Quando Usar Cada Um

| Padrão | Cenário |
|---|---|
| **Chain-of-Thought** | Problemas complexos, análise profunda |
| **Few-Shot** | Formato específico, tarefas de transformação |
| **Zero-Shot** | Tarefas simples, prompts rápidos |
| **Role** | Análise com perspectiva específica |
| **Structured** | Output precisa ser processada |
| **Decomposição** | Tarefas muito grandes |
| **Adversarial** | Validar decisões, questionar |
| **Meta** | Melhorar seus próprios prompts |
| **Comparação** | Entender alternativas |
| **Conditional** | Comportamento adaptativo |

---

**Próximo**: [Exemplos Reais](03-EXEMPLOS-REAIS.md)
