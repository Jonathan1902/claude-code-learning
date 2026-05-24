#!/usr/bin/env python3
"""
Build script to convert markdown docs to HTML with fluid navigation.
Generates static site for GitHub Pages with smooth transitions between topics.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Module mapping
MODULES = {
    "01": {"name": "Conceitos Fundamentais", "emoji": "📚", "topics": 5},
    "02": {"name": "Arquitetura", "emoji": "⚙️", "topics": 5},
    "03": {"name": "Comandos & Sintaxe", "emoji": "💬", "topics": 5},
    "04": {"name": "Padrões de Uso", "emoji": "🎯", "topics": 5},
    "05": {"name": "Casos Reais", "emoji": "🔧", "topics": 4},
    "06": {"name": "Troubleshooting", "emoji": "🐛", "topics": 4},
}

def markdown_to_html(md_content: str) -> str:
    """Convert basic markdown to HTML."""
    html = md_content

    # Code blocks
    html = re.sub(r'```(\w+)?\n(.*?)\n```', lambda m: f'<pre><code>{m.group(2)}</code></pre>', html, flags=re.DOTALL)

    # Headings
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

    # Bold and italics
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)

    # Links
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)

    # Lists
    html = re.sub(r'- (.*?)(?=\n|$)', r'<li>\1</li>', html)
    html = re.sub(r'(<li>.*?</li>)', lambda m: f'<ul>{m.group(1)}</ul>' if m.group(1).count('<li>') == 1 else m.group(1), html, flags=re.DOTALL)

    # Blockquotes
    html = re.sub(r'^> (.*?)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)

    # Paragraphs
    html = re.sub(r'\n\n+', '</p><p>', html)
    html = f'<p>{html}</p>'

    return html

def generate_module_page(module_num: str, module_info: Dict, output_dir: str) -> None:
    """Generate HTML page for a module with all its topics."""

    module_dir = Path(f"../{module_num}-*/")
    files = sorted(Path(".").glob(f"../{module_num}-*/*.md"))

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{module_info['name']} — Claude Code</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.7;
            color: #333;
            background: #f5f7fa;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
        }}

        header {{
            background: white;
            padding: 40px;
            border-radius: 12px;
            margin-bottom: 40px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
        }}

        header h1 {{
            font-size: 2em;
            color: #2d3748;
            margin-bottom: 10px;
        }}

        header p {{
            color: #666;
            font-size: 1.1em;
        }}

        .content {{
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 40px;
            animation: fadeIn 0.3s ease-in;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}

        h2, h3 {{
            color: #2d3748;
            margin-top: 30px;
            margin-bottom: 15px;
        }}

        h2 {{
            border-bottom: 2px solid #3182ce;
            padding-bottom: 10px;
        }}

        a {{
            color: #3182ce;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        pre {{
            background: #f7fafc;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 15px 0;
            border-left: 4px solid #3182ce;
        }}

        blockquote {{
            border-left: 4px solid #3182ce;
            padding-left: 15px;
            margin: 15px 0;
            color: #666;
            font-style: italic;
        }}

        ul {{
            margin-left: 20px;
            margin-bottom: 15px;
        }}

        li {{
            margin-bottom: 8px;
        }}

        .nav {{
            display: flex;
            justify-content: space-between;
            gap: 20px;
            margin-top: 40px;
            flex-wrap: wrap;
        }}

        .nav a {{
            flex: 1;
            min-width: 200px;
            padding: 15px 20px;
            background: #3182ce;
            color: white;
            border-radius: 8px;
            text-align: center;
            transition: all 0.3s;
        }}

        .nav a:hover {{
            background: #2c5aa0;
            transform: translateY(-2px);
            text-decoration: none;
            box-shadow: 0 4px 12px rgba(49, 130, 206, 0.3);
        }}

        .nav a.disabled {{
            background: #cbd5e0;
            cursor: not-allowed;
        }}

        .nav a.disabled:hover {{
            background: #cbd5e0;
            transform: none;
        }}

        .breadcrumb {{
            margin-bottom: 30px;
            font-size: 0.9em;
            color: #666;
        }}

        .breadcrumb a {{
            color: #3182ce;
        }}

        footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
        }}

        footer a {{
            color: #3182ce;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
            }}

            header h1 {{
                font-size: 1.5em;
            }}

            .nav {{
                flex-direction: column;
            }}

            .nav a {{
                min-width: auto;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="breadcrumb">
            <a href="../index.html">← Início</a> > {module_info['name']}
        </div>

        <header>
            <h1>{module_info['emoji']} {module_info['name']}</h1>
            <p>Tópicos deste módulo</p>
        </header>

        <div class="content" id="content">
            <p>Carregando...</p>
        </div>

        <div class="nav">
            <a href="#" id="prev-btn" class="disabled">← Anterior</a>
            <a href="../index.html" style="flex: 0.5; background: #718096;">↑ Menu</a>
            <a href="#" id="next-btn">Próximo →</a>
        </div>

        <footer>
            <p>Claude Code Learning | <a href="https://github.com" target="_blank">GitHub</a></p>
        </footer>
    </div>

    <script>
        const TOPICS = {TOPICS_JSON};
        const MODULE = "{module_num}";
        let currentTopic = parseInt(new URLSearchParams(window.location.search).get('topic') || '1');

        function loadTopic(topic) {{
            const topicData = TOPICS[topic];
            if (!topicData) return;

            document.getElementById('content').innerHTML = topicData.html;

            // Update navigation buttons
            const prevBtn = document.getElementById('prev-btn');
            const nextBtn = document.getElementById('next-btn');

            if (topic === 1) {{
                prevBtn.classList.add('disabled');
                prevBtn.href = '#';
            }} else {{
                prevBtn.classList.remove('disabled');
                prevBtn.href = `?topic=${{topic - 1}}`;
            }}

            if (topic === {topics_count}) {{
                nextBtn.classList.add('disabled');
                nextBtn.href = '#';
            }} else {{
                nextBtn.classList.remove('disabled');
                nextBtn.href = `?topic=${{topic + 1}}`;
            }}

            window.history.replaceState({{}}, '', `?topic=${{topic}}`);
        }}

        document.getElementById('prev-btn').addEventListener('click', (e) => {{
            if (currentTopic > 1) {{
                currentTopic--;
                loadTopic(currentTopic);
                e.preventDefault();
            }}
        }});

        document.getElementById('next-btn').addEventListener('click', (e) => {{
            if (currentTopic < {topics_count}) {{
                currentTopic++;
                loadTopic(currentTopic);
                e.preventDefault();
            }}
        }});

        loadTopic(currentTopic);
    </script>
</body>
</html>
"""

    # Parse topics and build JSON
    topics_data = {}
    md_files = sorted([f for f in Path(f"../{module_num}-*").glob("*.md") if not f.name.startswith("REVISAO")])

    for idx, md_file in enumerate(md_files[:module_info['topics']], 1):
        try:
            content = md_file.read_text(encoding='utf-8')
            html = markdown_to_html(content)
            topics_data[idx] = {"html": html.replace('"', '\\"')}
        except:
            topics_data[idx] = {"html": f"<p>Erro ao carregar {md_file.name}</p>"}

    topics_json = str(topics_data).replace("'", '"')
    html_content = html_content.replace('{TOPICS_JSON}', topics_json)
    html_content = html_content.replace('{topics_count}', str(module_info['topics']))

    output_file = Path(output_dir) / f"{module_num.lower()}-{module_info['name'].lower().replace(' ', '-').replace('&', '')}.html"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(html_content)

    print(f"✓ Generated: {output_file}")

if __name__ == "__main__":
    output_dir = Path("./modules")
    output_dir.mkdir(exist_ok=True)

    for module_num, module_info in MODULES.items():
        generate_module_page(module_num, module_info, output_dir)

    print("\n✓ Build complete! Open ./index.html to view")
