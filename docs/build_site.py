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
            display: flex;
            min-height: 100vh;
        }}

        .sidebar {{
            width: 280px;
            background: white;
            border-right: 1px solid #e2e8f0;
            padding: 20px;
            overflow-y: auto;
            box-shadow: 2px 0 8px rgba(0,0,0,0.05);
            position: fixed;
            left: 0;
            top: 0;
            height: 100vh;
        }}

        .sidebar-header {{
            font-size: 0.85em;
            font-weight: 600;
            color: #718096;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 15px;
            padding: 10px 0;
            border-bottom: 1px solid #e2e8f0;
        }}

        .sidebar-section {{
            margin-bottom: 25px;
        }}

        .sidebar-section-title {{
            font-size: 0.9em;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 10px;
            padding: 8px 10px;
            background: #f7fafc;
            border-radius: 4px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .sidebar-section-title .emoji {{
            font-size: 1.1em;
        }}

        .sidebar-links {{
            list-style: none;
        }}

        .sidebar-links li {{
            margin-bottom: 6px;
        }}

        .sidebar-links a {{
            display: block;
            padding: 8px 12px;
            color: #4a5568;
            text-decoration: none;
            border-radius: 6px;
            font-size: 0.9em;
            transition: all 0.2s;
            border-left: 3px solid transparent;
        }}

        .sidebar-links a:hover {{
            background: #edf2f7;
            color: #2d3748;
            border-left-color: #3182ce;
            padding-left: 15px;
        }}

        .sidebar-links a.active {{
            background: #3182ce;
            color: white;
            font-weight: 500;
            border-left-color: #2c5aa0;
        }}

        .sidebar-home {{
            padding: 12px;
            margin-top: 20px;
            border-top: 1px solid #e2e8f0;
            padding-top: 20px;
        }}

        .sidebar-home a {{
            display: block;
            text-align: center;
            padding: 10px;
            background: #3182ce;
            color: white;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.2s;
        }}

        .sidebar-home a:hover {{
            background: #2c5aa0;
        }}

        .sidebar-toggle {{
            display: none;
            position: fixed;
            top: 15px;
            left: 15px;
            z-index: 1000;
            background: white;
            border: 1px solid #e2e8f0;
            padding: 10px;
            border-radius: 6px;
            cursor: pointer;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        main {{
            margin-left: 280px;
            flex: 1;
            display: flex;
            flex-direction: column;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            width: 100%;
        }}

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
        .nav a {{
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
        .nav a.disabled {{
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
            body {{ flex-direction: column; }}
            .sidebar {{
                width: 100%;
                height: auto;
                position: static;
                max-height: 0;
                overflow: hidden;
                transition: max-height 0.3s ease;
                border-right: none;
                border-bottom: 1px solid #e2e8f0;
            }}
            .sidebar.open {{
                max-height: 500px;
            }}
            .sidebar-toggle {{
                display: block;
            }}
            main {{
                margin-left: 0;
            }}
            .container {{ padding: 20px; }}
            .nav {{ flex-direction: column; }}
            header h1 {{ font-size: 1.5em; }}
        }}
    </style>
</head>
<body>
    <button class="sidebar-toggle" id="sidebar-toggle">☰ Menu</button>

    <aside class="sidebar" id="sidebar">
        <div class="sidebar-header">Navegação</div>

        <div class="sidebar-section">
            <div class="sidebar-section-title">
                <span class="emoji">📚</span> Conceitos
            </div>
            <ul class="sidebar-links" id="module-01"></ul>
        </div>

        <div class="sidebar-section">
            <div class="sidebar-section-title">
                <span class="emoji">⚙️</span> Arquitetura
            </div>
            <ul class="sidebar-links" id="module-02"></ul>
        </div>

        <div class="sidebar-section">
            <div class="sidebar-section-title">
                <span class="emoji">💬</span> Comandos
            </div>
            <ul class="sidebar-links" id="module-03"></ul>
        </div>

        <div class="sidebar-section">
            <div class="sidebar-section-title">
                <span class="emoji">🎯</span> Padrões
            </div>
            <ul class="sidebar-links" id="module-04"></ul>
        </div>

        <div class="sidebar-section">
            <div class="sidebar-section-title">
                <span class="emoji">🔧</span> Casos Reais
            </div>
            <ul class="sidebar-links" id="module-05"></ul>
        </div>

        <div class="sidebar-section">
            <div class="sidebar-section-title">
                <span class="emoji">🐛</span> Troubleshooting
            </div>
            <ul class="sidebar-links" id="module-06"></ul>
        </div>

        <div class="sidebar-home">
            <a href="../index.html">← Voltar ao Menu</a>
        </div>
    </aside>

    <main>
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
    </main>

    <script>
        const topics = {topics_json};
        let current = parseInt(new URLSearchParams(window.location.search).get('topic') || '1');
        const total = {count};
        const currentModule = '{num}';

        const allModules = {{
            '01': ['Conceitos Fundamentais', 5],
            '02': ['Arquitetura', 5],
            '03': ['Comandos & Sintaxe', 5],
            '04': ['Padrões de Uso', 5],
            '05': ['Casos Reais', 4],
            '06': ['Troubleshooting', 4],
        }};

        const moduleFiles = {{
            '01': '01-conceitos-fundamentais',
            '02': '02-arquitetura',
            '03': '03-comandos--sintaxe',
            '04': '04-padrões-de-uso',
            '05': '05-casos-reais',
            '06': '06-troubleshooting',
        }};

        function buildSidebar() {{
            Object.entries(allModules).forEach(([modNum, [modName, topicCount]]) => {{
                const container = document.getElementById(`module-${{modNum}}`);
                for (let i = 1; i <= topicCount; i++) {{
                    const link = document.createElement('a');
                    link.href = `${{moduleFiles[modNum]}}.html?topic=${{i}}`;
                    link.textContent = `Tópico ${{i}}`;
                    if (modNum === currentModule && i === current) {{
                        link.classList.add('active');
                    }}
                    container.appendChild(document.createElement('li')).appendChild(link);
                }}
            }});
        }}

        function render(n) {{
            if (!topics[n]) return;
            document.getElementById('content').innerHTML = topics[n].html;
            document.getElementById('prev-btn').href = current > 1 ? `?topic=${{current - 1}}` : '#';
            document.getElementById('prev-btn').classList.toggle('disabled', current === 1);
            document.getElementById('next-btn').href = current < total ? `?topic=${{current + 1}}` : '#';
            document.getElementById('next-btn').classList.toggle('disabled', current === total);
            window.history.replaceState({{}}, '', `?topic=${{current}}`);

            // Update active link in sidebar
            document.querySelectorAll('.sidebar-links a').forEach(a => {{
                a.classList.remove('active');
            }});
            const currentLink = document.querySelector(`.sidebar-links a[href="${{moduleFiles[currentModule]}}.html?topic=${{current}}"]`);
            if (currentLink) currentLink.classList.add('active');
        }}

        document.getElementById('prev-btn').addEventListener('click', (e) => {{
            if (current > 1) {{ current--; render(current); }}
            e.preventDefault();
        }});

        document.getElementById('next-btn').addEventListener('click', (e) => {{
            if (current < total) {{ current++; render(current); }}
            e.preventDefault();
        }});

        document.getElementById('sidebar-toggle').addEventListener('click', () => {{
            document.getElementById('sidebar').classList.toggle('open');
        }});

        // Close sidebar on link click (mobile)
        document.querySelectorAll('.sidebar-links a').forEach(link => {{
            link.addEventListener('click', () => {{
                document.getElementById('sidebar').classList.remove('open');
            }});
        }});

        buildSidebar();
        render(current);
    </script>
</body>
</html>"""

if __name__ == '__main__':
    build_site()
