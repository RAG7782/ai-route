<div align="center">

# 🤖 AI Route

### Roteador Inteligente de CLI Agents — Nunca mais escolha qual ferramenta usar

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776ab.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)

**AI Route** analisa sua tarefa e automaticamente escolhe o melhor CLI agent para executá-la. Sem mais pensar "devo usar Claude, Aider, ou outro?"

[Quick Start](#quick-start) · [Manual de Operação](#manual-de-operao) · [Como Funciona](#como-funciona) · [Contributing](#contributing)

---

</div>

<div align="center">
  <img src="https://img.shields.io/badge/agents-8-blue?style=for-the-badge" alt="8 agents">
  <img src="https://img.shields.io/badge/scoring-regex-green?style=for-the-badge" alt="Regex scoring">
  <img src="https://img.shields.io/badge/language-PT/EN-orange?style=for-the-badge" alt="Bilingual">
</div>

## 🎯 O Problema que Resolve

Você tem **8+ CLI agents** instalados no seu sistema:
- `claude` — Claude Code (Opus)
- `aider-groq` — Aider + Groq
- `aider-or` — Aider + OpenRouter
- `opencode` — OpenCode
- `gemini` — Google Gemini CLI
- `codex` — OpenAI Codex
- `copilot` — GitHub Copilot CLI
- `ollama` — Local LLM

**A dor:** toda vez que você precisa de ajuda com código, você precisa parar e pensar:
- "Essa tarefa é complexa o suficiente para o Claude?"
- "É só um fix rápido, posso usar o Aider-Groq?"
- "Preciso de contexto grande, talvez Gemini?"
- "É só um comando shell, Copilot resolve?"

**AI Route resolve isso:** você digita a tarefa, ele escolhe a ferramenta certa.

---

## ✨ Features

| Feature | Descrição |
|---------|-----------|
| **Classificação Automática** | Analisa sua query e escolhe o melhor agent |
| **Scoring por Regex** | Sistema de pontuação baseado em padrões da tarefa |
| **8 Agents Suportados** | claude, aider-groq, aider-or, opencode, gemini, codex, copilot, ollama |
| **Modo Dry-Run** | Veja qual agent seria usado sem executar |
| **Listagem de Agents** | `ai-route --list` mostra todos disponíveis |
| **Custo por Agent** | `ai-route --cost` compara custos |
| **Bilingue** | Entende português e inglês |
| **Zero Configuração** | Funciona imediatamente após instalação |

---

## 🚀 Quick Start

### 1. Instalação

```bash
# Clone o repo
git clone https://github.com/seu-usuario/ai-route.git
cd ai-route

# Copie o script para seu PATH
cp ai-route ~/.local/bin/
chmod +x ~/.local/bin/ai-route

# Adicione ~/.local/bin ao seu PATH se ainda não estiver
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 2. Uso Básico

```bash
# AI Route analisa e roteia automaticamente
ai-route "como listar todos os arquivos .py no diretório atual?"

# Modo dry-run — mostra qual agent usaria sem executar
ai-route --dry "refatora essa função para usar async/await"

# Lista todos os agents disponíveis
ai-route --list

# Compara custo por agent
ai-route --cost
```

---

## 📖 Manual de Operação

### Quando usar cada Agent

| Agent | Custo | Velocidade | Melhor Para | Exemplo |
|-------|-------|------------|-------------|---------|
| **claude** | $$$ | Média | Arquitetura, multi-arquivo, raciocínio profundo | "Redesenhe a arquitetura do sistema de pagamentos" |
| **aider-groq** | $ | Rápida (554 t/s) | Fixes rápidos, código simples | "Corrige o bug na linha 42" |
| **aider-or** | $$ | Média | Refatoração complexa, multi-arquivo | "Refatora todo o módulo de auth para usar JWT" |
| **opencode** | $ | Média | Exploração de código, free tier | "Como funciona o pipeline de CI/CD?" |
| **gemini** | $ | Rápida | Explicações, contexto grande, docs | "Explique o que esse código faz" |
| **codex** | $$ | Rápida | Scaffolding, protótipos | "Cria um boilerplate para API FastAPI" |
| **copilot** | $ | Instantânea | Comandos shell, one-liners | "Como deletar todos os arquivos .log?" |
| **ollama** | 0 | Média | Offline, privado, sem internet | "Analise este código sensível (offline)" |

### Padrões de Roteamento

AI Route usa **regex scoring** para classificar sua tarefa:

#### Shell / CLI Commands → Copilot
```bash
ai-route "como matar o processo que está na porta 8080?"
ai-route "listar todos os containers docker rodando"
ai-route "como fazer commit no git com mensagem customizada?"
```

#### Arquitetura / Complex → Claude
```bash
ai-route "desenhe a arquitetura para um sistema de microserviços"
ai-route "analise criticamente o design deste sistema"
ai-route "como integrar MCP com Qdrant e Supabase?"
```

#### Fixes Rápidos → Aider-Groq
```bash
ai-route "corrige o bug de import no arquivo main.py"
ai-route "adiciona validação de email no formulário"
ai-route "ajusta o padding do botão de submit"
```

#### Refatoração Complexa → Aider-OR
```bash
ai-route "refatora todo o código para usar TypeScript strict"
ai-route "reescreva o módulo de autenticação usando OAuth2"
ai-route "migra o banco de dados para PostgreSQL"
```

#### Explicações / Documentação → Gemini
```bash
ai-route "explique como funciona o algoritmo de ordenação"
ai-route "documente a API de usuários"
ai-route "o que esse código faz exatamente?"
```

#### Scaffolding / Protótipos → Codex
```bash
ai-route "cria um boilerplate para projeto React + Vite"
ai-route "gera um protótipo de dashboard com gráficos"
ai-route "scaffolding para API REST com FastAPI"
```

#### Offline / Privado → Ollama
```bash
ai-route "analise este código sensível (sem internet)"
ai-route "gera documentação para código confidencial"
```

### Modo Dry-Run

Use `--dry` para ver qual agent seria usado sem executar:

```bash
$ ai-route --dry "como listar arquivos .py?"

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  AI Route → copilot  $  (instant)

  GitHub Copilot — sugere comandos shell

  Scoring:
  > copilot          35pts  shell command question
    aider-groq      15pts  file reference detected

  Comando: gh copilot suggest -t shell "como listar arquivos .py?"
```

### Listagem de Agents

```bash
$ ai-route --list

  AI Route — Agents Disponíveis

  $$$   claude          [ok]    Claude Code (Opus) — arquitetura, multi-arquivo, raciocínio profundo
  $     aider-groq     [ok]    Aider + Groq (554 t/s) — code rápido, grátis
  $$    aider-or        [ok]    Aider + OpenRouter (DeepSeek) — refatoração complexa barata
  $     opencode        [ok]    OpenCode — free tier, exploração de código
  $     gemini          [ok]    Gemini CLI — contexto grande, explicações, grátis
  $$    codex           [ok]    OpenAI Codex — scaffolding, protótipos rápidos
  $     copilot         [ok]    GitHub Copilot — sugere comandos shell
  0     ollama          [ok]    Ollama local — 100% offline, privado
```

### Comparação de Custo

```bash
$ ai-route --cost

  AI Route — Custo por Agent

  Agent           Tier     Cost    Speed
  ─────────────────────────────────────────
  ollama          free     0       medium
  aider-groq      free     $       fast
  opencode        free     $       medium
  gemini          free     $       fast
  copilot         free     $       instant
  aider-or        cheap    $$      medium
  codex           cheap    $$      fast
  claude          premium  $$$     medium
```

---

## 🔧 Como Funciona

### Arquitetura

```
┌─────────────────┐
│  Sua Query      │
│  "refatora X"   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│  AI Route (Python Script)       │
│                                 │
│  1. Normaliza query (lower)    │
│  2. Aplica regex patterns      │
│  3. Calcula score por agent     │
│  4. Escolhe melhor score       │
│  5. Executa agent escolhido     │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Agent Escolhido                │
│  (claude / aider / gemini / ...) │
└─────────────────────────────────┘
```

### Sistema de Scoring

Cada agent começa com score 0. Para cada regex que bate, adiciona pontos:

```python
# Exemplo de regra
(r"\b(arquitetura|architecture|design|system)\b", "claude", 30, "architecture/design task")

# Se a query contém "arquitetura":
# claude += 30 pontos
```

Heurísticas adicionais:
- Queries muito curtas (≤5 palavras) → +10 para copilot
- Queries muito longas (>30 palavras) → +10 para claude
- Referências a arquivos (.py, .js, etc.) → +15 para aider-groq
- Sem sinal forte → default para aider-groq

### Registry de Agents

```python
AGENTS = {
    "claude": {
        "cmd": ["claude", "-p"],
        "binary": "claude",
        "tier": "premium",
        "cost": "$$$",
        "speed": "medium",
        "strengths": ["architecture", "multi-file", "complex reasoning"],
        "desc": "Claude Code (Opus) — arquitetura, multi-arquivo, raciocínio profundo",
    },
    # ... outros agents
}
```

---

## 🛠️ Customização

### Adicionar Novo Agent

Edite o script `ai-route` e adicione ao `AGENTS`:

```python
AGENTS = {
    # ... agents existentes
    "meu-agent": {
        "cmd": ["meu-agent", "--arg"],
        "binary": "meu-agent",
        "tier": "free",
        "cost": "$",
        "speed": "fast",
        "strengths": ["minha especialidade"],
        "desc": "Descrição do meu agent",
    },
}
```

### Adicionar Nova Regra

Adicione ao `RULES`:

```python
RULES = [
    # ... regras existentes
    (r"\b(minha palavra chave|pattern)\b", "meu-agent", 25, "minha razão"),
]
```

---

## 📦 Instalação Avançada

### Via Homebrew (futuro)

```bash
brew tap seu-usuario/ai-route
brew install ai-route
```

### Via pip (futuro)

```bash
pip install ai-route
```

---

## 🤝 Contributing

Contribuições são bem-vindas! Áreas para melhorar:

1. **Mais agents** — Adicione suporte para novos CLI agents
2. **Melhor scoring** — Use NLP em vez de regex para classificação
3. **Configuração** — Permitir customização via arquivo YAML
4. **Histórico** — Guardar histórico de decisões de roteamento
5. **Feedback** — Permitir corrigir escolha errada e aprender

### Setup de Desenvolvimento

```bash
git clone https://github.com/seu-usuario/ai-route.git
cd ai-route

# Teste local
python3 ai-route "sua query aqui"

# Modo dry-run
python3 ai-route --dry "sua query aqui"
```

---

## 📄 License

MIT License — veja [LICENSE](LICENSE) para detalhes.

---

## 🙏 Agradecimentos

- Inspirado pela necessidade de simplificar o uso de múltiplos CLI agents
- Regex patterns baseados em experiência real de desenvolvimento
- Comunidade de AI/ML por feedback e sugestões

---

<div align="center">

**Feito com ❤️ para desenvolvedores que usam muitas ferramentas**

[⭐ Star no GitHub](https://github.com/seu-usuario/ai-route) · [🐛 Reportar Bug](https://github.com/seu-usuario/ai-route/issues) · [💡 Sugerir Feature](https://github.com/seu-usuario/ai-route/issues)

</div>
