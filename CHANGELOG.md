# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Adicionado
- README completo com manual de operação
- Guia de instalação detalhado
- Exemplos de uso por categoria
- Configuração de exemplo YAML
- Contributing guidelines
- LICENSE MIT

### Planejado
- Suporte a configuração via YAML
- Histórico de decisões de roteamento
- Sistema de feedback e aprendizado
- Integração com fzf para seleção interativa
- Testes automatizados
- Publicação no PyPI
- Publicação no Homebrew

## [0.1.0] - 2026-04-23

### Adicionado
- Sistema de roteamento baseado em regex scoring
- Suporte a 8 CLI agents (claude, aider-groq, aider-or, opencode, gemini, codex, copilot, ollama)
- Modo dry-run para preview de decisões
- Comando `--list` para listar agents disponíveis
- Comando `--cost` para comparar custos
- Heurísticas de scoring (query curta/longa, referências a arquivos)
- Bilingue (português e inglês)
- Zero configuração necessária

### Agentes Suportados
- **claude** — Claude Code (Opus) — arquitetura, multi-arquivo, raciocínio profundo
- **aider-groq** — Aider + Groq (554 t/s) — code rápido, grátis
- **aider-or** — Aider + OpenRouter (DeepSeek) — refatoração complexa barata
- **opencode** — OpenCode — free tier, exploração de código
- **gemini** — Gemini CLI — contexto grande, explicações, grátis
- **codex** — OpenAI Codex — scaffolding, protótipos rápidos
- **copilot** — GitHub Copilot — sugere comandos shell
- **ollama** — Ollama local — 100% offline, privado

### Padrões de Roteamento
- Shell / CLI commands → copilot
- Arquitetura / complex → claude
- Fixes rápidos → aider-groq
- Refatoração complexa → aider-or
- Explicações / documentação → gemini
- Scaffolding / protótipos → codex
- Offline / privado → ollama

### Documentação
- Docstrings completas no script
- Help inline (`ai-route --help`)
- Exemplos de uso em docstring

---

## [0.0.1] - 2026-04-22

### Adicionado
- Versão inicial do script
- Registry básico de agents
- Sistema de scoring simples
- Execução direta de agents escolhidos
