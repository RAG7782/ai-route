# Contributing to AI Route

Obrigado pelo interesse em contribuir com o AI Route! 🎉

## Como Contribuir

### Reporting Bugs

Antes de reportar um bug, verifique se já existe uma [issue](https://github.com/seu-usuario/ai-route/issues) aberta.

Ao reportar, inclua:
- Versão do Python (`python --version`)
- Sistema operacional
- Comando executado
- Output esperado vs output obtido
- Passos para reproduzir

### Sugerindo Features

Use o template de issue para sugerir novas features. Ideias bem-vindas:
- Novos agents CLI
- Melhorias no scoring
- Novos modos de operação
- Melhorias na UX

### Pull Requests

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Add nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

### Código de Conduta

- Seja respeitoso e construtivo
- Aceite feedback construtivo
- Foque no que é melhor para a comunidade
- Mostre empatia com outros usuários

## Áreas para Contribuir

### 1. Mais Agents

Adicione suporte para novos CLI agents:

```python
AGENTS = {
    "novoAgent": {
        "cmd": ["novo-agent", "--arg"],
        "binary": "novo-agent",
        "tier": "free",
        "cost": "$",
        "speed": "fast",
        "strengths": ["especialidade1", "especialidade2"],
        "desc": "Descrição do novo agent",
    },
}
```

### 2. Melhor Scoring

Substitua regex por NLP:

```python
# Atual: regex
(r"\b(arquitetura|architecture)\b", "claude", 30, "architecture")

# Futuro: NLP
from transformers import pipeline
classifier = pipeline("zero-shot-classification")
result = classifier(query, candidate_labels=["architecture", "code", "shell"])
```

### 3. Configuração via YAML

Permitir customização via arquivo:

```yaml
# ~/.config/ai-route/config.yaml
agents:
  claude:
    enabled: true
    priority: 10
  aider-groq:
    enabled: true
    priority: 5
```

### 4. Histórico e Feedback

Guardar histórico de decisões e permitir correção:

```python
# Guardar decisão
history.append({
    "query": query,
    "chosen": best,
    "timestamp": datetime.now(),
})

# Permitir correção
ai-route --correct "query anterior" --use "claude"
```

## Setup de Desenvolvimento

```bash
# Clone o repo
git clone https://github.com/seu-usuario/ai-route.git
cd ai-route

# Teste local
python3 ai-route.py "sua query"

# Modo dry-run
python3 ai-route.py --dry "sua query"

# Lista agents
python3 ai-route.py --list
```

## Testes

```bash
# Rodar testes (quando implementados)
python3 -m pytest tests/

# Teste específico
python3 -m pytest tests/test_scoring.py
```

## Style Guide

- Python 3.10+
- Seguir PEP 8
- Docstrings para funções públicas
- Type hints onde apropriado
- Comentários em português ou inglês (consistente)

## Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a MIT License.
