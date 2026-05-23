# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 📚 Project Overview

This is a **comprehensive learning repository** documenting Claude Code - a CLI tool and IDE extension by Anthropic that integrates Claude AI directly into the developer workflow. The repository provides:

- Progressive learning from fundamentals to advanced topics
- 25+ markdown documents organized in 6 learning modules
- Real-world use case examples
- Troubleshooting and best practices guide

**Target Audience**: Developers learning how to effectively use Claude Code in their daily workflow.

**Repository Type**: Educational documentation (not a software project with build/test cycles).

---

## 📂 Repository Structure & Architecture

### Top-Level Organization

The repository follows a **progressive learning path** structured in 6 modules:

```
01-CONCEITOS-FUNDAMENTAIS/     Intro to Claude Code: what it is, use cases, when to use
02-ARQUITETURA/                How it works internally: flow, architecture, tech stack
03-COMANDOS-SINTAXE/           How to write effective prompts: syntax, patterns, examples
04-PADROES-USO/                Techniques and strategies: iteration, debugging, analysis
05-CASOS-REAIS/                End-to-end examples: data processing, code generation, DevOps
06-TROUBLESHOOTING/            Common errors, debugging strategies, quick solutions
```

### Content Organization Pattern

Each module follows a progression:
1. **Foundational**: What/Why/When concepts (Modules 01-02)
2. **Practical**: How-to guides and patterns (Modules 03-04)
3. **Applied**: Real examples and troubleshooting (Modules 05-06)

Within each module, files are ordered (01-XYZ, 02-XYZ, etc.) to guide learning sequence. Cross-references between modules use markdown links.

### Key Navigation

- **README.md**: Study guide, learning paths, and learning outcomes
- **03-COMANDOS-SINTAXE/CHEAT-SHEET.md**: Quick reference (bookmark this)
- **06-TROUBLESHOOTING/03-SOLUCOES-RAPIDAS.md**: Problem → Solution lookup table

---

## 🛠️ Common Development Tasks

### Viewing/Navigating Content

```bash
# View the learning guide and study path
cat README.md

# Quick lookup for common Claude Code patterns
cat 03-COMANDOS-SINTAXE/CHEAT-SHEET.md

# Find quick solutions to common problems
cat 06-TROUBLESHOOTING/03-SOLUCOES-RAPIDAS.md

# Browse by learning difficulty
# Beginner: 01-CONCEITOS-FUNDAMENTAIS/ + 02-ARQUITETURA/
# Intermediate: 03-COMANDOS-SINTAXE/ + 04-PADROES-USO/
# Advanced: 05-CASOS-REAIS/ + 06-TROUBLESHOOTING/
```

### Validating Documentation

```bash
# Check for broken internal markdown links
grep -r "\[.*\](.*\.md)" . --include="*.md" | grep -v "^Binary"

# Find all markdown files and their line count (for content review)
find . -name "*.md" -exec wc -l {} + | sort -n

# List all sections with file count
for dir in */; do echo "$dir: $(ls $dir/*.md 2>/dev/null | wc -l) files"; done
```

### Adding New Content

```bash
# Count current files to maintain naming convention
ls 01-CONCEITOS-FUNDAMENTAIS/ | grep -c "^[0-9]"

# Create new file following the convention: NN-DESCRIPTION.md
# where NN is the next sequential number in that module
touch 01-CONCEITOS-FUNDAMENTAIS/05-NEW-TOPIC.md
```

### Checking Repository Stats

```bash
# Total markdown content size
du -sh $(find . -name "*.md" -type f)

# Word count across all documentation
find . -name "*.md" -type f -exec wc -w {} + | tail -1

# List files by last modification
find . -name "*.md" -type f -printf '%T@ %p\n' | sort -nr | head -10
```

---

## 📋 Contribution Guidelines

### Before Adding Content

1. **Check the Learning Path**: Determine which module (01-06) is most appropriate
2. **Review Existing Files**: Scan the module to understand depth and style
3. **Identify Position**: New content should follow the module's learning progression
4. **Cross-Reference**: Link from related files to maintain navigation

### Content Standards

- **Markdown Format**: GitHub-flavored markdown with proper heading hierarchy
- **Naming**: Use `NN-DESCRIPTION.md` where NN is sequential in the module
- **Headings**: Use `#` for title only, `##` for main sections, `###` for subsections
- **Examples**: Include practical, runnable examples where applicable
- **Audience**: Write for developers learning Claude Code (assume intermediate technical knowledge)
- **Length**: Aim for 5-15 min read time per file (1000-3000 words)

### File Types

- **Concept Files**: Define terms, explain "why" (modules 01-02)
- **Syntax Guides**: Show patterns and examples (modules 03-04)
- **Case Studies**: Real problems and solutions (modules 05)
- **Troubleshooting**: Error patterns and fixes (module 06)

### Maintenance Tasks

```bash
# After adding new content, update the README.md:
# 1. Add entry to structure diagram
# 2. Update file count if needed
# 3. Adjust time estimates if content is longer/shorter
# 4. Add to learning path if applicable

# Verify links from new file to related content
# Link to prerequisite concepts in earlier modules
# Link from later modules back to foundational material
```

---

## 🔄 Git Workflow

### Branch Naming

```bash
# Feature branch for new content
git checkout -b feature/topic-name

# Bug fix or clarification
git checkout -b fix/issue-description

# Examples:
git checkout -b feature/add-golang-patterns
git checkout -b fix/clarify-mcp-section
```

### Commit Messages

- **New Content**: `feat: add [topic] to [module]`
- **Updates**: `docs: update [topic] with [detail]`
- **Fixes**: `fix: [brief issue description]`

Examples:
```
feat: add real-world DevOps case study to 05-CASOS-REAIS
docs: clarify context window limits in 01-CONCEITOS-FUNDAMENTAIS
fix: correct broken link in 03-COMANDOS-SINTAXE
```

### Before Merging to Main

1. Verify all links are functional (no dead references)
2. Check markdown syntax is valid
3. Ensure new content follows naming conventions
4. Update README.md if structure changes
5. Get human review for accuracy and clarity

---

## 🎯 Content Scope & Policies

### What Belongs Here

✅ Claude Code concepts, features, and limitations  
✅ Effective prompting techniques and patterns  
✅ Real-world examples and case studies  
✅ Common errors and troubleshooting  
✅ Integration patterns (GitHub, Git, MCP, etc.)  

### What Doesn't Belong

❌ General software engineering (already covered elsewhere)  
❌ Unrelated tools or frameworks  
❌ Marketing or promotional content  
❌ Personal opinions without context  

### Accuracy Standards

- Information reflects Claude Code behavior as of the last commit date
- Examples are tested and reproducible
- API references link to official Anthropic documentation
- When referencing other tools, include their documentation links

---

## 📊 Repository Metrics

### Current State
- **Total Modules**: 6
- **Total Files**: 25+ markdown documents
- **Estimated Content**: ~20,000+ words
- **Learning Path**: ~23.5 hours (11h reading + 12.5h practice)

### Key Files to Update When Adding Content
1. `README.md` - Update structure diagram, learning path, time estimates
2. `.gitignore` - If adding non-markdown assets
3. Module index files - If changing file order

---

## 🔗 Important Links & Resources

- **Claude Code GitHub**: https://github.com/anthropics/claude-code
- **Claude Documentation**: https://docs.anthropic.com/claude
- **Anthropic Models**: https://www.anthropic.com/pricing
- **Learning Path**: Start with [01-CONCEITOS-FUNDAMENTAIS/01-O-QUE-E-CLAUDE-CODE.md](./01-CONCEITOS-FUNDAMENTAIS/01-O-QUE-E-CLAUDE-CODE.md)

---

## 📝 Notes for Future Contributors

- **Audience**: Developers with 2+ years experience (don't over-explain basics)
- **Depth**: Balance theory (architecture) with practice (examples)
- **Updates**: Keep examples current with Claude Code releases
- **Polish**: Edit for clarity; documentation is a product
- **Testing**: Before committing examples, verify they work

---

**Last Updated**: 2026-05-23  
**Maintainer**: Jonathan Costa (jonathancosta888@gmail.com)
