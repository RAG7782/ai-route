# Perguntas Frequentes (FAQ)

## Geral

### O que é AI Route?

AI Route é um roteador inteligente de CLI agents. Ele analisa sua tarefa e automaticamente escolhe o melhor CLI agent para executá-la, eliminando a necessidade de pensar qual ferramenta usar.

### Por que preciso disso?

Se você tem múltiplos CLI agents instalados (Claude, Aider, Gemini, etc.), toda vez que precisa de ajuda com código, você precisa parar e decidir qual usar. AI Route automatiza essa decisão.

### É gratuito?

Sim! AI Route é 100% gratuito e open-source (MIT License).

## Instalação

### Como instalo?

Veja o [Guia de Instalação](INSTALL.md) para instruções detalhadas. O método mais simples é:

```bash
git clone https://github.com/seu-usuario/ai-route.git
cd ai-route
cp ai-route.py ~/.local/bin/ai-route
chmod +x ~/.local/bin/ai-route
```

### Funciona no Windows?

Sim! O script é Python e funciona em qualquer sistema com Python 3.10+. No Windows, você pode precisar ajustar o PATH.

### Preciso de todos os agents?

Não! AI Route funciona com qualquer agent que você tenha instalado. Agents não instalados mostrarão `[N/A]` na listagem.

## Uso

### Como uso?

```bash
ai-route "sua pergunta ou tarefa"
```

AI Route analisa sua query e escolhe o melhor agent automaticamente.

### O que é modo dry-run?

Modo dry-run (`--dry`) mostra qual agent seria usado sem executar:

```bash
ai-route --dry "sua query"
```

### Posso forçar um agent específico?

Sim! Se você discordar da escolha do AI Route, use o agent diretamente:

```bash
# AI Route escolheria aider-groq
$ ai-route "corrige o bug"

# Mas você quer usar Claude
$ claude -p "corrige o bug"
```

### Como vejo quais agents estão disponíveis?

```bash
ai-route --list
```

### Como comparo custos?

```bash
ai-route --cost
```

## Funcionamento

### Como o AI Route escolhe o agent?

AI Route usa um sistema de **regex scoring**:
1. Sua query é normalizada (lowercase)
2. Cada regex pattern é testado contra a query
3. Para cada match, o agent correspondente ganha pontos
4. O agent com maior score é escolhido

### É sempre preciso?

Não é perfeito. É baseado em regex patterns, então pode haver falsos positivos/negativos. Se a escolha for errada, use o agent diretamente.

### Posso adicionar meus próprios patterns?

Sim! Edite o script `ai-route.py` e adicione suas regras ao `RULES`:

```python
RULES = [
    # ... regras existentes
    (r"\b(minha palavra chave)\b", "meu-agent", 25, "minha razão"),
]
```

### Posso adicionar novos agents?

Sim! Adicione ao `AGENTS` registry:

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

## Troubleshooting

### "command not found: ai-route"

`~/.local/bin` não está no seu PATH. Adicione ao `~/.zshrc`:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Agent mostra [N/A]

O binário do agent não está instalado. Instale o agent conforme instruções no [Guia de Instalação](INSTALL.md).

### O AI Route não está escolhendo o agent certo

O sistema de regex scoring não é perfeito. Você pode:
1. Usar o agent diretamente
2. Adicionar seus próprios patterns ao script
3. Contribuir com melhorias ao projeto

### Python 3 não encontrado

Instale Python 3.10+:

```bash
# macOS
brew install python@3.10

# Linux
sudo apt install python3.10
```

## Contribuindo

### Como posso contribuir?

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes. Áreas para contribuir:
- Adicionar novos agents
- Melhorar o scoring (NLP em vez de regex)
- Adicionar configuração via YAML
- Implementar histórico e feedback
- Adicionar testes

### Preciso de Python skills?

Para contribuir com código, sim. Mas você também pode contribuir com:
- Documentação
- Exemplos de uso
- Reportando bugs
- Sugerindo features
- Traduções

## Futuro

### O que está planejado?

Veja [CHANGELOG.md](CHANGELOG.md) para o que está planejado:
- Configuração via YAML
- Histórico de decisões
- Sistema de feedback e aprendizado
- Integração com fzf
- Publicação no PyPI e Homebrew

### Quando terá suporte a NLP?

Está planejado para v0.2.0. Substituir regex por NLP melhorará significativamente a precisão.

## Outros

### Posso usar em scripts automatizados?

Sim! AI Route é perfeito para scripts que precisam escolher o agent certo dinamicamente.

### Funciona com pipe?

Sim! Você pode fazer:

```bash
echo "sua query" | ai-route
```

### Tem suporte a outras línguas?

Atualmente suporta português e inglês. Outras línguas podem ser adicionadas contribuindo patterns.

### É seguro?

Sim! AI Route apenas roteia sua query para o agent escolhido. Não coleta dados nem faz chamadas de rede.

## Mais Perguntas

Se você tem outras perguntas não respondidas aqui:
- Abra uma [issue](https://github.com/seu-usuario/ai-route/issues)
- Leia o [README.md](README.md) completo
- Veja os [EXAMPLES.md](EXAMPLES.md) para casos de uso
