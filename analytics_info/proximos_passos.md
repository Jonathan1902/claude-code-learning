# FP&A Analytics — Próximos Passos e Roadmap de Evolução

> **Documento:** Visão estratégica e técnica para evolução do sistema de analytics  
> **Perspectivas:** CFO · Especialista em Dados & Analytics  
> **Contexto:** Pós-validação da POC com estruturas-piloto

---

## Como ler este documento

Cada seção apresenta a mesma frente de evolução por dois ângulos:

- **👔 CFO** — impacto no negócio, risco, governança, decisão
- **🛠 Dados** — arquitetura, implementação, esforço técnico

As fases são sequenciais mas não rígidas — algumas evoluções de Fase 2 podem ser antecipadas dependendo da maturidade da organização.

---

## Fase 0 — POC (onde você está agora)

**Objetivo:** Validar o conceito com 3 estruturas-piloto antes de investir em escala.

| O que testar | Critério de sucesso |
|---|---|
| O prompt gera análises confiáveis? | Gestor das 3 áreas considera os insights relevantes |
| Os números batem com o ERP? | Reconciliação manual confirma zero divergência |
| O tempo de geração é viável? | Relatório pronto em menos de 5 minutos por área |
| O perfil YAML captura o contexto real? | Análise diferencia o que é anomalia do que é sazonalidade |

**Entregável de saída da POC:** Documento de lições aprendidas + decisão de escalar (go / no-go)

---

## Fase 1 — Consolidação (1–3 meses pós-POC)

### 👔 Perspectiva CFO

**O que priorizar:**

**1. Governança de dados antes de escala**  
O maior risco neste momento não é técnico — é de credibilidade. Um relatório com número errado para 100 estruturas é pior do que nenhum relatório. Antes de escalar, estabeleça formalmente: quem é o dono do dado de cada estrutura? Quem aprova o orçamento que entra no sistema? Qual o SLA de atualização após o fechamento contábil?

**2. Patrocínio dos gestores**  
O sistema só funciona se os gestores das estruturas alimentarem e validarem os perfis YAML. Isso exige um processo de onboarding — não é técnico, é de mudança cultural. Cada gestor precisa entender que o perfil é o contrato deles com o sistema.

**3. Definição do ciclo de vida do relatório**  
Quando o relatório é gerado? Quem recebe? O que acontece se o gestor discordar do insight? Estabeleça o rito antes de automatizar. Relatório sem rito de consumo vira ruído.

**4. Métricas de sucesso do próprio sistema**  
Como você vai saber se o sistema está funcionando? Defina agora: redução no tempo de fechamento? Aumento na acurácia do forecast? Redução de estouros não antecipados? Sem isso, a ferramenta não tem ROI mensurável.

---

### 🛠 Perspectiva de Dados

**O que construir:**

**1. Pipeline de ingestão automatizado**  
Substituir o CSV manual por conexão direta com o ERP (SAP, TOTVS, Oracle). Meta: dados do fechamento mensal disponíveis automaticamente até D+2 após o fechamento. Prioridade: leitura antes de escrita — não modifique o ERP, apenas consuma.

**2. Repositório de perfis versionado**  
Os arquivos YAML precisam de controle de versão (Git ou equivalente). Quando um gestor muda a tolerância de desvio de uma rubrica, o sistema precisa saber qual versão do perfil foi usada para gerar cada relatório. Sem isso, relatórios históricos se tornam irrastreáveis.

**3. Testes automatizados de reconciliação**  
Antes de qualquer relatório ser gerado, um job de validação precisa confirmar: soma das coordenações = gerência, soma das gerências = diretoria, soma das diretorias = consolidado. Qualquer divergência bloqueia a geração e notifica o responsável pelo dado.

**4. Log de execução centralizado**  
Cada geração de relatório deve registrar: estrutura, período, snapshot dos dados, versão do perfil, detectores disparados, tempo de geração, erros. Isso alimenta a auditoria e permite reprocessar relatórios quando os dados são corrigidos.

**5. Separação de ambientes**  
POC roda em local ou notebook. A partir daqui: ambiente de desenvolvimento, homologação e produção separados. Dado financeiro em produção não pode estar misturado com experimentos.

---

## Fase 2 — Escala e Qualidade (3–6 meses)

### 👔 Perspectiva CFO

**1. Rolling Forecast integrado**  
O relatório hoje olha para trás (realizado vs. orçado). O próximo passo é olhar para frente: o sistema deve incorporar o forecast revisado dos gestores e atualizar automaticamente as projeções de estouro. Isso transforma o relatório de documento histórico em ferramenta de decisão prospectiva.

**2. Alertas proativos, não apenas relatórios**  
Não espere o fechamento mensal para saber de um problema. O sistema deve emitir alertas em tempo real (ou semanal) quando uma estrutura cruza um threshold crítico — por exemplo, quando o comprometimento ultrapassa 85% com 3 meses restantes. O CFO deve saber do problema antes do gestor da área precisar reportar.

**3. Comparabilidade entre estruturas**  
Com 100 estruturas gerando métricas padronizadas, você pela primeira vez terá uma visão comparativa real: quais áreas têm maior acurácia de planejamento? Quais têm desvios sistêmicos? Isso permite uma conversa de calibração orçamentária baseada em evidência, não em negociação política.

**4. Integração com o ciclo de planejamento**  
O histórico de acurácia e viés sistemático gerado pelo sistema deve alimentar o próximo ciclo orçamentário. Área com viés de +15% por 3 ciclos consecutivos terá seu orçamento ajustado por um fator de correção automático — e o gestor precisará justificar para sair desse padrão.

**5. Auditoria e conformidade**  
Se a organização tem obrigações de compliance ou auditoria externa, o sistema precisa produzir trilha de auditoria: qual dado, de qual fonte, em qual versão, gerou qual análise, aprovada por quem. Construa isso agora, não depois que o auditor pedir.

---

### 🛠 Perspectiva de Dados

**1. Semantic layer formal**  
Com 100 estruturas consumindo métricas, a definição de "desvio orçamentário" não pode estar no prompt. Precisa existir em um lugar único e versionado — um semantic layer (dbt Semantic Layer, Cube, ou até views SQL documentadas). Qualquer mudança na fórmula propaga automaticamente para todos os relatórios.

**2. Orquestração do pipeline**  
Substitua execução manual por orquestrador (Airflow, Prefect, ou mesmo GitHub Actions para começar). O pipeline de fechamento — ingestão → validação → cálculo de métricas → geração de perfis → execução dos detectores → geração de relatórios → distribuição — precisa ser reproduzível, monitorado e com retry automático em caso de falha.

**3. Cache de resultados intermediários**  
Métricas calculadas não devem ser recalculadas a cada geração de relatório. Armazene os resultados intermediários (métricas por estrutura por período) em uma camada de serving — mais rápido, mais barato, e permite auditoria dos números sem reprocessar.

**4. Versionamento de snapshots de dados**  
Implemente snapshots imutáveis do dado no momento do fechamento. Quando o ERP corrige um lançamento retroativo, o sistema precisa saber: o relatório de outubro foi gerado com qual versão dos dados? Isso é fundamental para reconciliação e auditoria.

**5. Qualidade de dados como serviço**  
Implemente um dashboard de qualidade de dados: quais estruturas têm dados completos? Quais têm gaps de períodos? Quais têm inconsistências entre rubrica e grupo? Isso vira um contrato de SLA entre o time de dados e o time financeiro.

**6. Avaliação de qualidade dos insights gerados**  
Crie um mecanismo de feedback: após cada relatório, o gestor pode marcar cada insight como "relevante", "já sabia", "incorreto" ou "não aplicável". Esse feedback alimenta o ajuste dos detectores e dos thresholds — o sistema aprende com o uso.

---

## Fase 3 — Inteligência e Autonomia (6–18 meses)

### 👔 Perspectiva CFO

**1. Forecast preditivo por estrutura**  
Combinar o histórico de realizado, sazonalidade declarada nos perfis, e variáveis macroeconômicas relevantes (inflação, câmbio para áreas com exposição) para gerar um forecast estatístico por estrutura. O gestor parte de uma proposta fundamentada, não de uma planilha em branco.

**2. Simulador de cenários**  
"O que acontece com o orçamento da Diretoria de TI se o dólar subir 10%?" O sistema deve permitir simulações de sensibilidade que propagam automaticamente pela hierarquia. Hoje isso exige dias de trabalho manual de vários analistas.

**3. Realocação orçamentária inteligente**  
O sistema identifica automaticamente estruturas com folga real (potencial de realocação positivo) e estruturas em pressão de estouro, e sugere transferências orçamentárias com os valores e justificativas. O CFO aprova ou rejeita — mas não precisa mais descobrir a oportunidade manualmente.

**4. Benchmarking externo**  
Com o banco de dados de métricas históricas da organização consolidado, é possível comparar o comportamento financeiro das estruturas com benchmarks de mercado (quando disponíveis para o setor). Uma gerência de TI que gasta 3x a média do setor em manutenção de equipamentos tem um argumento de gestão muito mais forte (ou fraco) do que uma que apenas "estourou o orçamento".

**5. NLP para justificativas e comentários**  
Integrar as justificativas textuais que gestores registram no ERP ou em formulários de fechamento ao sistema de análise. Um desvio acompanhado de justificativa aprovada pelo nível superior tem tratamento diferente de um desvio sem explicação — o sistema deve saber disso.

---

### 🛠 Perspectiva de Dados

**1. Modelos de forecast estatístico por rubrica**  
Para rubricas com histórico suficiente (24+ meses), treinar modelos leves de série temporal (Prophet, ARIMA, ou regressão com sazonalidade) por estrutura e rubrica. O forecast resultante alimenta o campo `forecast_revisado` do pipeline, substituindo a entrada manual dos gestores como ponto de partida.

**2. Detecção de anomalias com ML**  
Substituir os detectores baseados em regras fixas por modelos de detecção de anomalia (Isolation Forest, DBSCAN sobre séries históricas). Vantagem: thresholds se adaptam automaticamente ao comportamento histórico de cada estrutura, reduzindo falsos positivos.

**3. Grafo de dependências entre estruturas**  
Modelar explicitamente as relações hierárquicas e laterais (ex: centro de custo compartilhado, rateio de custos indiretos) como um grafo. Permite análise de impacto: uma decisão na Coordenação A afeta como a Gerência B?

**4. Feature store de métricas financeiras**  
Centralizar todas as métricas calculadas historicamente em uma feature store. Isso habilita: treinar modelos com histórico completo, servir métricas em real-time para dashboards, e garantir que análises ad-hoc usem os mesmos cálculos que os relatórios automáticos.

**5. API de analytics**  
Expor as métricas e insights via API REST ou GraphQL. Isso permite que outros sistemas da organização (BI, ERP, intranet do gestor) consumam os mesmos dados sem duplicar lógica de cálculo. O relatório HTML vira apenas um dos clientes da API — não o único.

**6. Observabilidade do sistema como produto**  
Tratar o pipeline de analytics como produto de dados: SLA de disponibilidade, alertas de degradação, métricas de uso (quantos relatórios gerados, quais estruturas com mais acessos, quais insights mais marcados como relevantes). O time de dados precisa de visibilidade operacional como qualquer time de engenharia.

---

## Resumo executivo — O que decidir agora

| Decisão | Responsável | Prazo sugerido |
|---|---|---|
| Critério de go/no-go da POC | CFO + TI | Ao final da Fase 0 |
| Dono do dado por estrutura | Diretores de área | Antes da Fase 1 |
| Integração com ERP: leitura direta ou extração? | TI + Dados | Início da Fase 1 |
| Ferramenta de controle de versão dos perfis | Dados | Início da Fase 1 |
| Rito de consumo dos relatórios (quando, quem, como) | CFO + FP&A | Antes de escalar |
| Mecanismo de feedback dos gestores | FP&A + Dados | Fase 2 |
| Decisão de investir em modelos preditivos | CFO | Início da Fase 3 |

---

## Riscos a monitorar em todo o caminho

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Dado do ERP inconsistente bloqueia geração | Alta | Alto | Testes de reconciliação automáticos (Fase 1) |
| Gestores não atualizam os perfis YAML | Alta | Médio | Rito de revisão semestral + responsável nomeado |
| Insights irrelevantes geram desconfiança | Média | Alto | Loop de feedback + ajuste de thresholds (Fase 2) |
| LLM gera número incorreto na narrativa | Baixa | Muito alto | Guardrail: narrativa gerada, números calculados deterministicamente |
| Dependência de um único modelo de LLM | Baixa | Médio | Prompt agnóstico de modelo; testar com alternativas |
| Escala gera custo de API inesperado | Média | Médio | Estimativa de custo por estrutura antes de escalar |

---

*Documento gerado como parte da POC de FP&A Analytics · Versão 1.0*
