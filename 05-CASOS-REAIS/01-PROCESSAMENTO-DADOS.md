# Processamento de Dados com Claude Code

## Caso 1: ETL de CSV para JSON

### Situação
Arquivo CSV com 1M linhas. Precisa transformar em JSON, validar dados.

### Prompt
```
Contexto: Python 3.11, pandas para processing

Tarefa: Ler CSV grande, validar, exportar JSON

Arquivo: customers.csv (1M linhas)
Colunas: id, name, email, created_at

Validação:
- Email deve ser válido
- created_at formato ISO
- Remover duplicatas de email

Exportar: clientes_validos.json

Performance: deve rodar em <30 segundos
```

### Resultado
Claude cria script que:
1. Lê CSV em chunks (memory efficient)
2. Valida com regex/validators
3. Remove duplicatas (set de emails)
4. Escreve JSON
5. Log de erros rejeitados

---

## Caso 2: Parse de Log Estruturado

### Situação
Log de aplicação com milhões de linhas. Precisa extrair padrões.

### Prompt
```
Contexto: Python, análise de logs de produção

Tarefa: Parse de app.log e gerar relatório

Log format:
2026-05-23 10:30:15 [ERROR] User registration failed: email_exists

Preciso:
- Contar erros por tipo
- Extrair timings (latência de requisições)
- Identificar padrões de falha

Output: JSON com estatísticas
```

### Resultado
Claude cria parser que:
1. Regex para extrair campos
2. Agrupa por tipo de erro
3. Calcula médias/percentis
4. Gera JSON estruturado

---

## Caso 3: Transformação de Schema

### Situação
BD antiga em MySQL, migrar para PostgreSQL.

### Prompt
```
Contexto: MySQL → PostgreSQL migration

Tarefa: Exportar dados, adaptar para novo schema

Schema Antigo:
- users (id, name, email)
- posts (id, user_id, content)

Schema Novo:
- users (id, email, full_name, created_at)
- articles (id, author_id, title, body, published_at)

Requisitos:
- Mapear user_id → author_id
- Dividir 'content' em title + body
- Gerar created_at com timestamp atual
- Validar referências integridade

Output: SQL INSERT statements para PostgreSQL
```

### Resultado
Claude cria migration que:
1. Exporta dados do MySQL
2. Mapeia schemas
3. Valida FK constraints
4. Gera INSERT statement para PG

---

## Caso 4: Limpeza de Dados

### Situação
Dataset com muitos missing values, outliers.

### Prompt
```
Contexto: Python, análise de sales_data.csv

Tarefa: Limpar dados para ML training

Problemas:
- Colunas price têm valores negativos
- Date column tem "NULL" como string
- Nome tem espaços extras
- 5% dos dados faltam valores

Estratégia:
- Remover preço <0 (provavelmente erros)
- Converter date corretamente
- Trim whitespace em strings
- Imputar valores faltantes (média para numéricos)

Output: dataset_clean.csv
```

### Resultado
Claude cria script que:
1. Detecta tipo de coluna
2. Aplica transformações apropriadas
3. Imputação automática
4. Relatório de limpeza (quantas linhas removidas)

---

## Caso 5: Agregação e Resumo

### Situação
Tabela de transações, precisa gerar relatório executivo.

### Prompt
```
Contexto: PostgreSQL, dados de transações

Tarefa: Gerar relatório de vendas por período

Dados:
- transactions (id, date, amount, category, customer_id)
- 10M linhas

Gerar JSON:
{
  "total_revenue": 1000000,
  "by_category": { "A": 500000, "B": 300000 },
  "by_month": { "2026-01": 100000, "2026-02": 150000 },
  "top_10_customers": [...]
}

Performance: <5 segundos
```

### Resultado
Claude cria query + Python que:
1. Agrupa por categoria
2. Agrupa por período
3. Ranks de clientes
4. Retorna JSON estruturado

---

## Exemplo Prático: Caso Completo

### Problema
Temos CSV com vendas, precisa gerar KPI dashboard.

### Prompt Detalhado

```
Contexto:
- Python 3.11
- Arquivo: sales_2026.csv (500k linhas)
- Colunas: date, product_id, quantity, unit_price, region

Tarefa: Gerar KPI para dashboard

KPIs esperados:
1. Total revenue (sum de quantidade × preço)
2. Vendas por região (breakdown)
3. Top 10 produtos
4. Trend mensal (revenue crescendo ou reduzindo?)
5. Ticket médio (revenue / número de transações)

Output Format:
```json
{
  "total_revenue": 1000000,
  "metrics": {
    "by_region": { "North": ..., "South": ... },
    "top_products": [...],
    "monthly_trend": [...],
    "avg_ticket": 150.50
  }
}
```

Requisitos:
- Use pandas (performance)
- Type hints completos
- Docstring explicando cada KPI
- Trate valores inválidos
- Validação: total_revenue = sum(quantidade × preço)

Você fornece:
- Amostra de dados (primeiras 10 linhas)
```

### Resultado do Claude

```python
import pandas as pd
from typing import dict

def calculate_kpis(csv_file: str) -> dict:
    """Calculates KPI metrics from sales data"""
    
    # Lê em chunks para memoria eficiente
    df = pd.read_csv(csv_file)
    
    # Validação
    assert df['unit_price'].min() >= 0
    
    # Calcula revenue
    df['revenue'] = df['quantity'] * df['unit_price']
    
    total_revenue = df['revenue'].sum()
    
    # Agregações
    by_region = df.groupby('region')['revenue'].sum().to_dict()
    top_products = df.groupby('product_id')['revenue'].sum().nlargest(10)
    
    # Trend
    df['date'] = pd.to_datetime(df['date'])
    monthly_trend = df.groupby(df['date'].dt.to_period('M'))['revenue'].sum()
    
    # Ticket médio
    avg_ticket = total_revenue / len(df)
    
    return {
        "total_revenue": float(total_revenue),
        "metrics": {
            "by_region": by_region,
            "top_products": top_products.to_dict(),
            "monthly_trend": monthly_trend.to_dict(),
            "avg_ticket": float(avg_ticket)
        }
    }
```

---

## Padrões Comuns em Processamento

### Chunk Processing (Arquivos Grandes)
```python
for chunk in pd.read_csv('huge.csv', chunksize=10000):
    # Processa 10k linhas por vez (memory efficient)
    process(chunk)
```

### Validação em Pipe
```python
df = (
    pd.read_csv('data.csv')
    .loc[df['value'] > 0]  # Filtra
    .drop_duplicates()     # Remove duplicatas
    .fillna(df.mean())     # Imputa
)
```

### Erro Tracking
```python
errors = []
for row in data:
    try:
        process(row)
    except Exception as e:
        errors.append({
            'row': row,
            'error': str(e)
        })

# Relatório de erros
print(f"Processados: {len(data) - len(errors)}")
print(f"Erros: {len(errors)}")
```

---

## Benchmarks Típicos

| Operação | Tamanho | Tempo |
|---|---|---|
| Ler CSV | 1M linhas | 5-10s |
| Validar email | 100k linhas | 2-3s |
| Dedupe | 1M linhas | 3-5s |
| Agregação | 10M linhas | 5-10s |
| ML training | 100k features | 30-60s |

---

**Próximo**: [Geração de Código](02-GERACAO-CODIGO.md)
