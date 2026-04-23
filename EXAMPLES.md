# Exemplos de Uso do AI Route

Este documento mostra exemplos reais de como usar o AI Route no dia-a-dia.

## Exemplos por Categoria

### Shell / CLI Commands → Copilot

```bash
# Listar arquivos
$ ai-route "como listar todos os arquivos .py no diretório atual?"
  AI Route → copilot  $  (instant)
  GitHub Copilot — sugere comandos shell

# Docker
$ ai-route "como parar todos os containers docker?"
  AI Route → copilot  $  (instant)
  GitHub Copilot — sugere comandos shell

# Git
$ ai-route "como fazer commit com mensagem customizada?"
  AI Route → copilot  $  (instant)
  GitHub Copilot — sugere comandos shell

# Processos
$ ai-route "como matar o processo na porta 8080?"
  AI Route → copilot  $  (instant)
  GitHub Copilot — sugere comandos shell
```

### Arquitetura / Design → Claude

```bash
# Arquitetura de sistema
$ ai-route "desenhe a arquitetura para um sistema de microserviços de pagamentos"
  AI Route → claude  $$$  (medium)
  Claude Code (Opus) — arquitetura, multi-arquivo, raciocínio profundo

# Design de API
$ ai-route "como estruturar uma API RESTful para usuários e autenticação?"
  AI Route → claude  $$$  (medium)
  Claude Code (Opus) — arquitetura, multi-arquivo, raciocínio profundo

# Análise crítica
$ ai-route "analise criticamente o design deste sistema de cache"
  AI Route → claude  $$$  (medium)
  Claude Code (Opus) — arquitetura, multi-arquivo, raciocínio profundo

# Integração complexa
$ ai-route "como integrar MCP com Qdrant e Supabase para RAG?"
  AI Route → claude  $$$  (medium)
  Claude Code (Opus) — arquitetura, multi-arquivo, raciocínio profundo
```

### Fixes Rápidos → Aider-Groq

```bash
# Corrigir bug
$ ai-route "corrige o bug de import no arquivo main.py"
  AI Route → aider-groq  $  (fast)
  Aider + Groq (554 t/s) — code rápido, grátis

# Adicionar funcionalidade simples
$ ai-route "adiciona validação de email no formulário de registro"
  AI Route → aider-groq  $  (fast)
  Aider + Groq (554 t/s) — code rápido, grátis

# Ajuste de UI
$ ai-route "ajusta o padding do botão de submit"
  AI Route → aider-groq  $  (fast)
  Aider + Groq (554 t/s) — code rápido, grátis

# Renomear variável
$ ai-route "renomeia a variável 'temp' para 'temperature' no arquivo sensor.py"
  AI Route → aider-groq  $  (fast)
  Aider + Groq (554 t/s) — code rápido, grátis
```

### Refatoração Complexa → Aider-OR

```bash
# Refatoração completa
$ ai-route "refatora todo o código para usar TypeScript strict"
  AI Route → aider-or  $$  (medium)
  Aider + OpenRouter (DeepSeek) — refatoração complexa barata

# Reescrever módulo
$ ai-route "reescreva o módulo de autenticação usando OAuth2"
  AI Route → aider-or  $$  (medium)
  Aider + OpenRouter (DeepSeek) — refatoração complexa barata

# Migração
$ ai-route "migra o banco de dados de SQLite para PostgreSQL"
  AI Route → aider-or  $$  (medium)
  Aider + OpenRouter (DeepSeek) — refatoração complexa barata

# Reestruturação
$ ai-route "reestrutura o projeto para seguir clean architecture"
  AI Route → aider-or  $$  (medium)
  Aider + OpenRouter (DeepSeek) — refatoração complexa barata
```

### Explicações / Documentação → Gemini

```bash
# Explicar código
$ ai-route "explique como funciona o algoritmo de ordenação quicksort"
  AI Route → gemini  $  (fast)
  Gemini CLI — contexto grande, explicações, grátis

# Documentar API
$ ai-route "documente a API de usuários com OpenAPI spec"
  AI Route → gemini  $  (fast)
  Gemini CLI — contexto grande, explicações, grátis

# Entender código complexo
$ ai-route "o que esse código de machine learning faz exatamente?"
  AI Route → gemini  $  (fast)
  Gemini CLI — contexto grande, explicações, grátis

# Gerar README
$ ai-route "gera um README para este projeto"
  AI Route → gemini  $  (fast)
  Gemini CLI — contexto grande, explicações, grátis
```

### Scaffolding / Protótipos → Codex

```bash
# Criar boilerplate
$ ai-route "cria um boilerplate para projeto React + Vite + TypeScript"
  AI Route → codex  $$  (fast)
  OpenAI Codex — scaffolding, protótipos rápidos

# Protótipo de dashboard
$ ai-route "gera um protótipo de dashboard com gráficos usando Chart.js"
  AI Route → codex  $$  (fast)
  OpenAI Codex — scaffolding, protótipos rápidos

# API FastAPI
$ ai-route "scaffolding para API REST com FastAPI e SQLAlchemy"
  AI Route → codex  $$  (fast)
  OpenAI Codex — scaffolding, protótipos rápidos

# Componente React
$ ai-route "cria um componente de tabela com paginação e filtros"
  AI Route → codex  $$  (fast)
  OpenAI Codex — scaffolding, protótipos rápidos
```

### Offline / Privado → Ollama

```bash
# Código sensível
$ ai-route "analise este código sensível (sem internet)"
  AI Route → ollama  0  (medium)
  Ollama local — 100% offline, privado

# Documentação confidencial
$ ai-route "gera documentação para código confidencial (offline)"
  AI Route → ollama  0  (medium)
  Ollama local — 100% offline, privado

# Sem conexão
$ ai-route "ajuda com este código (estou sem internet)"
  AI Route → ollama  0  (medium)
  Ollama local — 100% offline, privado
```

## Modo Dry-Run

Use `--dry` para ver qual agent seria usado sem executar:

```bash
$ ai-route --dry "refatora o módulo de auth"

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  AI Route → aider-or  $$  (medium)

  Aider + OpenRouter (DeepSeek) — refatoração complexa barata

  Scoring:
  > aider-or         25pts  complex refactor
    claude           10pts  long/complex query
    aider-groq       15pts  file reference detected

  Comando: source ~/.zshrc 2>/dev/null; aider-or --message "refatora o módulo de auth"
```

## Casos de Uso Avançados

### 1. Forçar Agent Específico

Se você discordar da escolha do AI Route, pode usar o agent diretamente:

```bash
# AI Route escolheria aider-groq
$ ai-route "corrige o bug"

# Mas você quer usar Claude
$ claude -p "corrige o bug"
```

### 2. Combinar com Outras Ferramentas

```bash
# Usar AI Route + fzf para histórico
ai-route "$(cat ~/.bash_history | fzf)"

# Usar AI Route com pipe
echo "como listar processos?" | ai-route
```

### 3. Scripts Automatizados

```bash
#!/bin/bash
# deploy.sh

# Verificar configuração
ai-route --dry "verifica se a configuração de produção está correta"

# Deploy
ai-route "faz deploy da aplicação para produção"
```

## Dicas de Uso

### 1. Seja Específico

```bash
# ❌ Vago
$ ai-route "ajuda com código"

# ✅ Específico
$ ai-route "corrige o bug de import no arquivo main.py"
```

### 2. Inclua Contexto

```bash
# ❌ Sem contexto
$ ai-route "refatora"

# ✅ Com contexto
$ ai-route "refatora o módulo de auth para usar JWT"
```

### 3. Use Dry-Run para Aprender

```bash
# Veja qual agent seria usado
$ ai-route --dry "sua query"

# Aprenda os padrões de roteamento
$ ai-route --dry "como fazer X?"
$ ai-route --dry "refatora Y?"
$ ai-route --dry "explique Z?"
```

### 4. Combine com Aliases

```bash
# Alias no ~/.zshrc
alias ar="ai-route --dry"  # ar = ai-route dry-run

# Uso
$ ar "como listar arquivos?"
```

## Fluxo de Trabalho Recomendado

### Para Desenvolvimento Diário

1. **Quick fixes** → `ai-route "corrige X"`
2. **Refator simples** → `ai-route "refatora Y"`
3. **Comandos shell** → `ai-route "como fazer Z?"`
4. **Explicações** → `ai-route "explique W"`

### Para Tarefas Complexas

1. **Arquitetura** → `ai-route "desenhe arquitetura de X"`
2. **Multi-arquivo** → `ai-route "analise sistema Y"
3. **Integração** → `ai-route "como integrar Z com W?"

### Para Prototipagem

1. **Scaffolding** → `ai-route "cria boilerplate para X"`
2. **Protótipo** → `ai-route "gera protótipo de Y"
3. **MVP** → `ai-route "cria MVP de Z"

## Perguntas Frequentes

### Q: O AI Route sempre acerta?

A: Não é perfeito. É baseado em regex patterns. Se a escolha for errada, use o agent diretamente.

### Q: Posso adicionar meus próprios patterns?

A: Sim! Edite o script `ai-route.py` e adicione suas regras ao `RULES`.

### Q: O AI Route funciona com qualquer CLI agent?

A: Funciona com qualquer agent que tenha um binário no PATH. Adicione ao `AGENTS` registry.

### Q: O AI Route guarda histórico?

A: Não por padrão, mas você pode implementar facilmente adicionando logging ao script.

### Q: Posso usar o AI Route em scripts?

A: Sim! É perfeito para scripts automatizados que precisam escolher o agent certo.
