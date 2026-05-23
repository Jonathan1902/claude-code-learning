# Diagrama de Fluxo Completo

## 📋 Nota

Este arquivo é um **placeholder** para um diagrama visual do fluxo completo de Claude Code.

### Para adicionar diagrama:

Você pode criar um diagrama em um dos seguintes formatos:

1. **SVG** (recomendado para repositórios)
   - Texto puro, versionável no git
   - Renomear arquivo para `diagrama-fluxo.svg`
   - Pode ser editado com Inkscape ou editor de texto

2. **PNG** (mais visual)
   - Usar ferramentas como:
     - Mermaid (mermaid-js.github.io)
     - Draw.io (draw.io)
     - Lucidchart

3. **ASCII Art** (já incluído)
   - Ver arquivo `01-FLUXO-COMPLETO.md` para diagrama ASCII completo

### Sugestão de Conteúdo

O diagrama deve mostrar:

```
┌─────────────────┐
│  Usuário Digita │
└────────┬────────┘
         │
         ▼
┌──────────────────────┐
│ Claude Code Processa │
└────────┬─────────────┘
         │
         ▼
┌────────────────────────┐
│ API Anthropic          │
│ (Claude Model)         │
└────────┬───────────────┘
         │
    ┌────┴────┐
    │ Tool?   │
    ├─────────┤
    │ Sim │Não│
    └────┬──┬─┘
    │  │
    ▼  ▼
Tool   Resposta
Use    Usuário
```

---

**Próximo**: [Tecnologias Subjacentes](03-TECNOLOGIAS-SUBJACENTES.md)
