# Quando Usar Claude Code

## Critérios de Decisão

### ✅ USE Claude Code quando:

#### 1. Você tem código para analisar
- Arquivo aberto no editor
- Erro específico com stack trace
- Precisa entender fluxo complexo

**Exemplo**: "Por que este teste está falhando?" + arquivo de teste

---

#### 2. Tarefa requer iteração
- Não é um prompt único
- Você vai refinar e testar várias vezes
- Feedback contínuo é necessário

**Exemplo**: Refatoração com testes depois

---

#### 3. Código precisa ser modificado
- Editar múltiplos arquivos
- Aplicar padrão em vários locais
- Atualizar automaticamente

**Exemplo**: Adicionar logging em 20 funções

---

#### 4. Automação de tarefas repetitivas
- Deploy scripts
- Data processing
- Batch operations

**Exemplo**: ETL que precisa rodar toda semana

---

#### 5. Contexto de projeto importa
- Arquivos relacionados
- Convenções específicas
- Histórico de decisões

**Exemplo**: "Refatore seguindo o padrão do projeto"

---

### ❌ EVITE Claude Code quando:

#### 1. Decisão arquitetural pura
- Qual framework escolher?
- SQL vs NoSQL?
- Monolítico vs microsserviços?

**Por quê**: Requer visão de negócio, não código. Use discussão com time.

---

#### 2. Conhecimento específico de domínio
- "Qual é a melhor prática para MRI?"
- "Como regulamentar criptografia?"

**Por quê**: Claude não substitui expertise humana.

---

#### 3. Criatividade pura
- Conceito de produto novo
- Design de interface inovador

**Por quê**: Criatividade requer direção humana clara.

---

#### 4. Contexto muito grande (>100k tokens)
- Projeto inteiro
- Base de dados enorme
- Muitos arquivos relacionados

**Por quê**: Context window é limitado; prefira exploração seletiva.

---

#### 5. Modificação de dados críticos
- Banco de dados em produção
- Deletar arquivos permanentemente
- Operações financeiras

**Por quê**: Sempre requer aprovação manual explícita.

---

## Matriz de Decisão

| Tipo de Tarefa | Claude Code | Chat Web | Humano |
|---|---|---|---|
| Debugar erro específico | ✅ | ⚠️ | ⚠️ |
| Refatorar código | ✅ | ⚠️ | ⚠️ |
| Gerar testes | ✅ | ✅ | ⚠️ |
| Escolher arquitetura | ⚠️ | ⚠️ | ✅ |
| Escrever documentação | ✅ | ✅ | ⚠️ |
| Análise de segurança | ✅ | ✅ | ✅ |
| Deploy automatizado | ✅ | ⚠️ | ⚠️ |
| Decisão de negócio | ❌ | ⚠️ | ✅ |

---

## Exemplo de Fluxo

**Caso**: Preciso otimizar um script Python lento

1. **Vou usar Claude Code porque**:
   - ✅ Tenho código para analisar
   - ✅ Requer iteração (profile → fix → test)
   - ✅ Contexto específico importa

2. **Como**:
   ```
   "Execute este script com profiler e identifique bottlenecks"
   [fornecer arquivo]
   ```

3. **Então**:
   - Claude roda profiler
   - Explica resultado
   - Sugere otimizações específicas
   - Você aprova ou refina

---

**Próximo**: [Limitações](04-LIMITACOES.md)
