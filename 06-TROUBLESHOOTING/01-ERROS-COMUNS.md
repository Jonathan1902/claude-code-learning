# Erros Comuns e Soluções

## 1. "Context Too Long"

### Problema
```
Error: Total tokens exceed context window limit (200k)
```

### Por Quê
Forneceu muito contexto:
- Projeto inteiro (~500 arquivos)
- Histórico de 50+ mensagens
- Código desnecessário

### Solução
```
❌ Errado:
"Aqui está meu projeto inteiro"
[todo o projeto]

✅ Certo:
"Debugue este erro em app/views.py"
[apenas views.py, ~200 linhas]

✅ Melhor ainda:
"Debugue erro nesta função"
[apenas função relevante, ~30 linhas]
```

---

## 2. "Command Not Found"

### Problema
```
bash: pytest: command not found
```

### Por Quê
Claude rodou `pytest` mas:
- Não instalado no ambiente
- Não no PATH
- Wrong Python environment

### Solução
```
❌ Não roda:
pytest tests/

✅ Roda:
python -m pytest tests/

✅ Ou instale primeiro:
pip install pytest
python -m pytest tests/
```

---

## 3. "Permission Denied"

### Problema
```
PermissionError: [Errno 13] Permission denied: 'file.py'
```

### Por Quê
Claude tentou:
- Editar arquivo protegido
- Executar script sem permissão
- Acessar diretório privado

### Solução
```bash
# Ver permissões
ls -la file.py

# Dar permissão
chmod +x file.py

# Ou usar sudo (cuidado!)
sudo nano file.py
```

---

## 4. "Resposta Truncada"

### Problema
```
[resposta parece incompleta]
... (truncated due to length)
```

### Por Quê
Resposta é muito longa (saída grande, muitos erros).

### Solução
```
✅ Peça resumo:
"Mas em resumo, qual era o erro?"

✅ Peça por partes:
"Mostre apenas os 10 primeiros erros"

✅ Redirecione output:
python script.py > output.txt
# Depois: "Leia output.txt e me mostre os erros"
```

---

## 5. "Claude Não Lembrou"

### Problema
```
Você: "Agora refatore views.py"
Claude: "Qual é views.py?"
(Você já forneceu na mensagem anterior)
```

### Por Quê
Contexto é preservado na mesma sessão, mas:
- Se forneceu em prompt 1, prompt 2 é ambíguo
- Histórico foi limpado (você usou /clear)
- Contexto foi compactado (muitas mensagens)

### Solução
```
❌ Ambíguo:
"Refatore views.py"

✅ Claro:
"Refatore views.py (que você acabou de ler)"
[ou forneça novamente]

✅ Use CLAUDE.md para contexto persistente:
"Contexto está em CLAUDE.md"
```

---

## 6. "Erro Ao Editar Arquivo"

### Problema
```
Edit failed: old_string not found
```

### Por Quê
Claude tentou Edit tool mas:
- Código mudou entre leitura e edição
- String exata não encontrada
- Indentação diferente

### Solução
```
✅ Forneça contexto maior:
"Leia views.py novamente (pode ter mudado)"

✅ Use novo prompt:
"Edite views.py: remova função X"
(Claude relê primeiro)

✅ Use Write em vez de Edit (para reescrever):
"Reescreva views.py com..."
```

---

## 7. "Teste Falhando"

### Problema
```
FAILED test_auth.py::test_login - AssertionError
```

### Por Quê
Claude gerou código mas:
- Edge case não coberto
- Mock de BD incorreto
- Lógica não testa o que acha

### Solução
```
✅ Fornecedor teste falhando:
"Teste falha com este erro: [error]
[forneça função testada]
O que está errado?"

✅ Peça para validar manualmente:
"Rode pytest test_auth.py -vv"
[Claude vê erro completo]
```

---

## 8. "API Rate Limit Atingido"

### Problema
```
Error: Rate limit exceeded (429)
```

### Por Quê
Muitas chamadas à API Anthropic:
- Trocas rápidas demais
- Contexto grande repetido

### Solução
```
✅ Aguarde:
"Aguarde 60 segundos e tente novamente"

✅ Use Haiku (mais barato):
"/model haiku"
Depois continue

✅ Combine prompts:
"Passo 1 + 2 + 3 em um prompt"
(1 chamada em vez de 3)
```

---

## 9. "Código Gerado Não Funciona"

### Problema
```
Código de Claude rodou mas lógica está errada
```

### Por Quê
Claude:
- Não entendeu requisito
- Suposição errada
- Não viu edge case

### Solução
```
✅ Forneça evidência:
"Esperado: X, Recebido: Y
Input que quebrou: Z"

✅ Mostre erro específico:
"Rodi e recebei: [traceback]"

✅ Corrija iterativamente:
"Mas preciso também..."
[refinamento]
```

---

## 10. "Módulo Python Não Encontrado"

### Problema
```
ModuleNotFoundError: No module named 'requests'
```

### Por Quê
Código usa módulo mas:
- Não está instalado
- Venv não ativado
- Wrong Python version

### Solução
```bash
✅ Instale dependência:
pip install requests

✅ Ou use venv:
source venv/bin/activate
pip install -r requirements.txt

✅ Verifique Python:
python --version
```

---

## Tabela de Troubleshooting Rápida

| Erro | Causa | Fix |
|---|---|---|
| Context too long | Contexto grande | Remova código não-relevante |
| Command not found | Módulo não instalado | pip install / use Python path |
| Permission denied | Arquivo protegido | chmod +x ou sudo |
| Edit failed | String não found | Releia arquivo, use Write |
| Test failing | Lógica errada | Fornecedor teste output |
| Rate limited | Muitas requisições | Aguarde ou use Haiku |
| Response truncated | Output muito grande | Peça resumo ou split |
| Claude não lembrou | Contexto perdido | Forneça novamente |
| Module not found | Não instalado | pip install |
| Weird behavior | Suposição errada | Refine requisito |

---

## Checklist: Antes de Pedir Help

- [ ] Erro exato (copie stack trace completo)?
- [ ] Já tentei isso sozinho? (como?)
- [ ] Contexto fornecido (arquivo relevante)?
- [ ] Código está visível (pode Claude ver)?
- [ ] Input/output esperado vs recebido?
- [ ] Ambiente (Python version, packages)?

Se sim em 5+: pronto para pedir help a Claude

---

**Próximo**: [Como Debugar](02-COMO-DEBUGAR.md)
