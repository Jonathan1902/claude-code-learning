# Automação DevOps

## Caso 1: CI/CD Pipeline

### Situação
Deploy manual, sujeito a erro.

### Prompt
```
Contexto: GitHub Actions, Python/Django, PostgreSQL

Crie workflow de CI/CD que:

Push to main → Automaticamente:
1. Run linters (black, isort, flake8)
2. Run testes (pytest)
3. Coverage report (>80% required)
4. Build Docker image
5. Push to registry
6. Deploy to staging
7. Run smoke tests
8. If all ok → deploy to production

Requisitos:
- Matriz: Python 3.10, 3.11, 3.12
- Cache dependencies
- Slack notification on failure
- Manual approval antes de prod
```

### Resultado
Claude gera `.github/workflows/deploy.yml` com:
1. Multi-stage pipeline
2. Conditional steps (só deploy se tests passam)
3. Artifact storage
4. Notifications
5. Rollback strategy

---

## Caso 2: Infrastructure as Code

### Situação
Servidores configurados manualmente. Difícil reproduzir.

### Prompt
```
Contexto: Terraform, AWS, Django app

Crie Terraform que provisiona:
1. VPC com subnets
2. RDS PostgreSQL (multi-AZ)
3. ElastiCache Redis
4. ECS cluster com ALB
5. Route53 DNS
6. CloudWatch logs

Requisitos:
- Staging e Production (different sizes)
- Backup automático (RDS)
- Auto-scaling para EC2
- Security groups restrictivos
- SSL certificate (ACM)

[fornecer current setup se tiver]
```

### Resultado
Terraform modules que:
1. Reproducible
2. Version controlled
3. Testable (terraform plan)
4. Documentado

---

## Caso 3: Monitoring e Alerting

### Situação
Produção muda, ninguém sabe que algo quebrou.

### Prompt
```
Contexto: Prometheus + Grafana, Django app

Crie alertas para:
1. Erro rate >1% (5min average)
2. Response time P95 >500ms
3. Database connections >80% max
4. Disk usage >90%
5. Memory usage >85%
6. Deployment failed
7. SSL certificate expiring soon

Métricas customizadas:
- User login failures
- Payment processing errors
- API rate limit exceeded

Notificações:
- Slack para warnings
- PagerDuty para crítico
- Email para infra issues
```

### Resultado
Prometheus rules + Grafana dashboards que:
1. Alertam proativamente
2. Contextualizam bem
3. Actionable (não spam)

---

## Caso 4: Backup e Disaster Recovery

### Situação
BD cai, sem backup recente.

### Prompt
```
Contexto: PostgreSQL, S3 buckets

Crie estratégia de backup:
1. Daily full backup (S3)
2. Hourly incremental (S3)
3. Point-in-time recovery (30 days)
4. Cross-region replication (disaster recovery)
5. Automated restore test (1x/week)

Requisitos:
- Backup encryption
- Versioning em S3
- Retenção policy (30 dias full, 90 dias incrementais)
- Script de restore (documentado)
- Health check (backups working?)

Automação:
- Cron job ou Lambda trigger
- Logging em CloudWatch
- Alert se backup falhar
```

### Resultado
Backup automation que:
1. Robusto (redundância)
2. Testado (restore automation)
3. Documentado (how to restore)
4. Monitorado (alerts)

---

## Caso 5: Scaling Automático

### Situação
Peak traffic causa timeout, node cai.

### Prompt
```
Contexto: Kubernetes, Docker, auto-scaling

Setup auto-scaling que:
1. Horizontal pod autoscaling (CPU >70% → scale up)
2. Vertical scaling (memory >80%)
3. Database scaling (read replicas quando querys lentas)
4. Cache scaling (Redis cluster)
5. Load balancing (round-robin)

Requisitos:
- Min replicas: 2 (availability)
- Max replicas: 10 (cost)
- Scaledown delay: 5 min (avoid thrashing)
- Metrics to watch: CPU, Memory, Custom (requests/sec)

Health checks:
- Liveness probe (is pod alive?)
- Readiness probe (can accept traffic?)
```

### Resultado
Kubernetes manifests que:
1. Auto-scale baseado em métricas
2. High availability
3. Cost optimized

---

## Padrão: Infraestrutura Robusta

```
┌──────────────────────────────────┐
│  Source Control (Git)            │
│  - Código                        │
│  - Infraestrutura (Terraform)    │
│  - Configuração (YAML)           │
└────────────┬─────────────────────┘
             │
             ▼
┌──────────────────────────────────┐
│  CI/CD Pipeline                  │
│  - Lint, test, build             │
│  - Deploy to staging             │
│  - Smoke tests                   │
│  - Deploy to prod                │
└────────────┬─────────────────────┘
             │
             ▼
┌──────────────────────────────────┐
│  Production                      │
│  - Monitored (Prometheus)        │
│  - Logged (ELK)                  │
│  - Backed up (S3)                │
│  - Auto-healing                  │
└──────────────────────────────────┘
```

---

## Exemplo Prático: Deploy Robusto

### Requisitos
- Django app em Kubernetes
- RDS PostgreSQL
- CloudFront CDN
- Route53 DNS

### Automação Claude Cria

1. **GitHub Actions workflow**
   - Run tests (pytest)
   - Build Docker image
   - Push to ECR
   - Deploy rolling (0 downtime)

2. **Terraform**
   - VPC, subnets, security groups
   - RDS with backups
   - CloudFront distribution
   - Route53 A record

3. **Kubernetes manifests**
   - Deployment with 3 replicas
   - Service (load balancer)
   - Horizontal autoscaler
   - Health checks

4. **Monitoring**
   - Prometheus scraping metrics
   - Grafana dashboard
   - Alerts for errors/latency

5. **Scripts**
   - Backup script (daily)
   - Rollback script (1-click)
   - Health check script

---

## Ferramentas DevOps Populares

| Ferramenta | O que faz |
|---|---|
| Terraform | Infrastructure as Code |
| Ansible | Configuration management |
| Docker | Containerization |
| Kubernetes | Orchestration |
| GitHub Actions | CI/CD |
| Jenkins | CI/CD (on-prem) |
| Prometheus | Monitoring |
| Grafana | Dashboards |
| ELK Stack | Logging |
| PagerDuty | On-call management |

---

**Voltar**: [Processamento de Dados](01-PROCESSAMENTO-DADOS.md)
