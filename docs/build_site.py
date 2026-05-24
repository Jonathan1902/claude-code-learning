#!/usr/bin/env python3
"""Generate static HTML site from markdown docs with fluid navigation."""

import json
import re
from pathlib import Path

def markdown_to_html(content: str) -> str:
    """Simple markdown to HTML converter."""
    lines = content.split('\n')
    html_lines = []
    in_code = False
    in_list = False

    for line in lines:
        # Code blocks
        if line.startswith('```'):
            if in_code:
                html_lines.append('</code></pre>')
                in_code = False
            else:
                html_lines.append('<pre><code>')
                in_code = True
            continue

        if in_code:
            html_lines.append(line)
            continue

        # Headings
        if line.startswith('### '):
            html_lines.append(f'<h3>{line[4:]}</h3>')
            continue
        if line.startswith('## '):
            html_lines.append(f'<h2>{line[3:]}</h2>')
            continue
        if line.startswith('# '):
            html_lines.append(f'<h1>{line[2:]}</h1>')
            continue

        # Bold, italic, links
        line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
        line = re.sub(r'\*(.*?)\*', r'<em>\1</em>', line)
        line = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', line)

        # Lists
        if line.startswith('- '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{line[2:]}</li>')
            continue
        elif in_list:
            html_lines.append('</ul>')
            in_list = False

        # Blockquotes
        if line.startswith('> '):
            html_lines.append(f'<blockquote>{line[2:]}</blockquote>')
            continue

        # Regular paragraphs
        if line.strip():
            html_lines.append(f'<p>{line}</p>')

    if in_list:
        html_lines.append('</ul>')
    if in_code:
        html_lines.append('</code></pre>')

    return '\n'.join(html_lines)

def build_site():
    """Build the complete site."""
    docs_dir = Path(__file__).parent
    repo_root = docs_dir.parent
    modules_dir = docs_dir / 'modules'
    modules_dir.mkdir(exist_ok=True)

    modules = [
        ('01', 'Conceitos Fundamentais', '📚'),
        ('02', 'Arquitetura', '⚙️'),
        ('03', 'Comandos & Sintaxe', '💬'),
        ('04', 'Padrões de Uso', '🎯'),
        ('05', 'Casos Reais', '🔧'),
        ('06', 'Troubleshooting', '🐛'),
    ]

    for num, name, emoji in modules:
        module_dir = repo_root / f"{num}-{name.upper().replace('&', '').replace(' ', '-')}"
        md_files = sorted([f for f in module_dir.glob('*.md') if not f.name.startswith('REVISAO')])

        topics_json = {}
        for idx, md_file in enumerate(md_files, 1):
            try:
                content = md_file.read_text(encoding='utf-8')
                html = markdown_to_html(content)
                topics_json[str(idx)] = {
                    'title': md_file.stem,
                    'html': html
                }
            except Exception as e:
                print(f"Warning: {md_file} - {e}")
                topics_json[str(idx)] = {'title': 'Error', 'html': f'<p>Erro ao carregar arquivo</p>'}

        # Generate module page
        module_file = f"{num.lower()}-{name.lower().replace(' ', '-').replace('&', '')}"
        html_template = generate_module_html(num, name, emoji, json.dumps(topics_json), len(md_files))

        (modules_dir / f"{module_file}.html").write_text(html_template)
        print(f"✓ {name}")

    print("\n✓ Build complete!")

def generate_module_html(num: str, name: str, emoji: str, topics_json: str, count: int) -> str:
    """Generate module HTML page."""
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} — Claude Code</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.7;
            color: #333;
            background: #f5f7fa;
        }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 40px 20px; }}
        header {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        header h1 {{ font-size: 2em; margin-bottom: 10px; }}
        .breadcrumb {{ color: #666; margin-bottom: 20px; }}
        .breadcrumb a {{ color: #3182ce; text-decoration: none; }}
        .breadcrumb a:hover {{ text-decoration: underline; }}
        .content {{
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            animation: fadeIn 0.3s ease;
        }}
        @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
        .content h1 {{ font-size: 1.8em; margin-bottom: 20px; border-bottom: 2px solid #3182ce; padding-bottom: 10px; }}
        .content h2 {{ font-size: 1.4em; margin-top: 25px; margin-bottom: 15px; color: #2d3748; }}
        .content h3 {{ font-size: 1.1em; margin-top: 20px; margin-bottom: 10px; color: #4a5568; }}
        .content p {{ margin: 15px 0; }}
        .content a {{ color: #3182ce; text-decoration: none; }}
        .content a:hover {{ text-decoration: underline; }}
        .content pre {{
            background: #f7fafc;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            border-left: 4px solid #3182ce;
            margin: 15px 0;
        }}
        .content blockquote {{
            border-left: 4px solid #3182ce;
            padding-left: 15px;
            margin: 15px 0;
            color: #666;
        }}
        .content ul {{ margin-left: 25px; margin-bottom: 15px; }}
        .content li {{ margin-bottom: 8px; }}
        .nav {{
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 40px;
        }}
        .nav a, .nav button {{
            padding: 12px 24px;
            border-radius: 6px;
            border: none;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s;
            text-decoration: none;
            color: white;
        }}
        .nav a {{
            background: #3182ce;
        }}
        .nav a:hover {{
            background: #2c5aa0;
            transform: translateY(-2px);
        }}
        .nav a.disabled, .nav button:disabled {{
            background: #cbd5e0;
            cursor: not-allowed;
            transform: none;
        }}
        .home-link {{
            background: #718096 !important;
        }}
        .home-link:hover {{
            background: #4a5568 !important;
        }}
        footer {{ text-align: center; padding: 20px; color: #666; font-size: 0.9em; }}
        footer a {{ color: #3182ce; text-decoration: none; }}
        @media (max-width: 768px) {{
            .container {{ padding: 20px; }}
            .nav {{ flex-direction: column; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="breadcrumb">
            <a href="../index.html">← Home</a> &gt; <strong>{name}</strong>
        </div>

        <header>
            <h1>{emoji} {name}</h1>
        </header>

        <div class="content" id="content">
            <p>Carregando...</p>
        </div>

        <div class="nav">
            <a href="#" id="prev-btn" class="disabled">← Anterior</a>
            <a href="../index.html" class="home-link">↑ Menu Principal</a>
            <a href="#" id="next-btn">Próximo →</a>
        </div>

        <footer>
            <p>Claude Code Learning Repository</p>
        </footer>
    </div>

    <script>
        const topics = {topics_json};
        let current = parseInt(new URLSearchParams(window.location.search).get('topic') || '1');
        const total = {count};

        function render(n) {{
            if (!topics[n]) return;
            document.getElementById('content').innerHTML = topics[n].html;
            document.getElementById('prev-btn').href = current > 1 ? `?topic=${{current - 1}}` : '#';
            document.getElementById('prev-btn').classList.toggle('disabled', current === 1);
            document.getElementById('next-btn').href = current < total ? `?topic=${{current + 1}}` : '#';
            document.getElementById('next-btn').classList.toggle('disabled', current === total);
            window.history.replaceState({{}}, '', `?topic=${{current}}`);
        }}

        document.getElementById('prev-btn').addEventListener('click', (e) => {{
            if (current > 1) {{ current--; render(current); }}
            e.preventDefault();
        }});
        document.getElementById('next-btn').addEventListener('click', (e) => {{
            if (current < total) {{ current++; render(current); }}
            e.preventDefault();
        }});

        render(current);
    </script>
</body>
</html>"""

if __name__ == '__main__':
    build_site()
