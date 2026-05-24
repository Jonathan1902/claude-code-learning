# GitHub Pages — Claude Code Learning

Site estático interativo publicado em GitHub Pages com navegação fluida entre tópicos.

## Estrutura

- `index.html` — Página inicial com cards dos módulos
- `modules/` — Páginas de módulos geradas dinamicamente
- `build_site.py` — Script que converte markdown em HTML

## Como funciona

1. **Geração**: O script `build_site.py` lê todos os arquivos `.md` dos módulos (01-06)
2. **Navegação**: Cada página de módulo usa JavaScript para carregar tópicos sem reload
3. **Transição**: CSS animado (`fadeIn`) entre tópicos
4. **Responsivo**: Design mobile-first com CSS Grid

## Rebuilding

Para atualizar o site após mudanças nos markdown:

```bash
python3 docs/build_site.py
```

Isso regenera os arquivos HTML em `docs/modules/`.

## Publicação

O branch `gh-pages` é servido automaticamente pelo GitHub Pages.

Para fazer push:

```bash
git add docs/
git commit -m "docs: update site pages"
git push origin gh-pages
```

Site disponível em: `https://seu-usuario.github.io/claude-code-learning/`

## Features

- ✅ Navegação entre tópicos sem reload
- ✅ Breadcrumb com volta ao menu
- ✅ Botões Anterior/Próximo com disable automático
- ✅ URL com parâmetro `?topic=N` para linkável
- ✅ Animação suave de transição (fadeIn)
- ✅ Totalmente responsivo
- ✅ Markdown simples (sem dependências externas)

## Customização

Edite `build_site.py` para:
- Ajustar CSS (estilos no template)
- Mudar converter markdown (função `markdown_to_html`)
- Adicionar novas seções

Os conteúdos markdown vêm diretamente dos arquivos da raiz (01-CONCEITOS-FUNDAMENTAIS/, etc).
