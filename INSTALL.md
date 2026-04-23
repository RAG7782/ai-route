# Guia de Instalação Detalhado

## Pré-requisitos

- Python 3.10 ou superior
- Acesso ao terminal
- Permissão para instalar scripts no seu PATH

## Instalação

### Método 1: Clone do Repositório (Recomendado)

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/ai-route.git
cd ai-route

# 2. Torne o script executável
chmod +x ai-route.py

# 3. Crie um link simbólico no seu PATH
ln -s $(pwd)/ai-route.py ~/.local/bin/ai-route

# 4. Verifique se ~/.local/bin está no seu PATH
echo $PATH | grep -q "$HOME/.local/bin" || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc

# 5. Recarregue seu shell
source ~/.zshrc

# 6. Teste a instalação
ai-route --list
```

### Método 2: Download Direto

```bash
# 1. Baixe o script
curl -o ~/.local/bin/ai-route https://raw.githubusercontent.com/seu-usuario/ai-route/main/ai-route.py

# 2. Torne executável
chmod +x ~/.local/bin/ai-route

# 3. Teste
ai-route --list
```

### Método 3: Via pip (Futuro)

```bash
pip install ai-route
```

## Configuração

### Verificar Agents Disponíveis

```bash
ai-route --list
```

Saída esperada:
```
  AI Route — Agents Disponíveis

  $$$   claude          [ok]    Claude Code (Opus) — arquitetura, multi-arquivo, raciocínio profundo
  $     aider-groq     [ok]    Aider + Groq (554 t/s) — code rápido, grátis
  $$    aider-or        [ok]    Aider + OpenRouter (DeepSeek) — refatoração complexa barata
  ...
```

Se um agent mostrar `[N/A]`, significa que o binário não está instalado.

### Instalar Agents Opcionais

#### Claude Code
```bash
# Via Homebrew
brew install claude-code

# Ou via npm
npm install -g @anthropic-ai/claude-code
```

#### Aider
```bash
pip install aider-chat

# Configurar aliases no ~/.zshrc
alias aider-groq='aider --model groq/llama-3.3-70b-versatile'
alias aider-or='aider --model openrouter/deepseek/deepseek-r1'
```

#### OpenCode
```bash
npm install -g opencode
```

#### Gemini CLI
```bash
npm install -g @google/generative-ai-cli
```

#### Codex
```bash
npm install -g openai-codex-cli
```

#### GitHub Copilot CLI
```bash
# Instalar gh CLI primeiro
brew install gh

# Instalar extensão copilot
gh extension install github/gh-copilot
```

#### Ollama
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Baixar modelo
ollama pull gemma4:26b
```

## Verificação

Teste cada modo de operação:

```bash
# 1. Listagem
ai-route --list

# 2. Custo
ai-route --cost

# 3. Dry-run
ai-route --dry "como listar arquivos?"

# 4. Execução real
ai-route "como matar processo na porta 8080?"
```

## Troubleshooting

### "command not found: ai-route"

**Causa:** `~/.local/bin` não está no seu PATH.

**Solução:**
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### "Permission denied"

**Causa:** Script não tem permissão de execução.

**Solução:**
```bash
chmod +x ~/.local/bin/ai-route
```

### Agent mostra [N/A]

**Causa:** Binário do agent não está instalado.

**Solução:** Instale o agent conforme instruções acima.

### Python 3 não encontrado

**Causa:** Python 3 não está no PATH.

**Solução:**
```bash
# macOS
brew install python@3.10

# Linux
sudo apt install python3.10
```

## Desinstalação

```bash
# Remover script
rm ~/.local/bin/ai-route

# Remover repositório clonado (se aplicável)
rm -rf ~/ai-route
```

## Próximos Passos

- Leia o [README.md](README.md) para o manual completo
- Veja [CONTRIBUTING.md](CONTRIBUTING.md) para contribuir
- Experimente diferentes queries para ver o roteamento em ação
