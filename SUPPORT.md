# Suporte

## Como Obter Ajuda

### Documentação

- [README.md](README.md) — Manual completo
- [INSTALL.md](INSTALL.md) — Guia de instalação
- [EXAMPLES.md](EXAMPLES.md) — Exemplos de uso
- [FAQ.md](FAQ.md) — Perguntas frequentes

### Comandos de Ajuda

```bash
# Ajuda inline
ai-route --help

# Listar agents disponíveis
ai-route --list

# Comparar custos
ai-route --cost
```

### Relatar Problemas

Se você encontrar um bug ou tiver uma sugestão:

1. Verifique o [FAQ.md](FAQ.md) — sua pergunta pode já ter resposta
2. Busque [issues existentes](https://github.com/seu-usuario/ai-route/issues)
3. Se não encontrar, crie uma nova issue usando os templates:
   - [Bug Report](https://github.com/seu-usuario/ai-route/issues/new?template=bug_report.md)
   - [Feature Request](https://github.com/seu-usuario/ai-route/issues/new?template=feature_request.md)

### Comunidade

- [GitHub Discussions](https://github.com/seu-usuario/ai-route/discussions) — Perguntas e discussões
- [Discord](https://discord.gg/example) — Chat em tempo real (quando disponível)

## Níveis de Suporte

| Nível | Descrição | Tempo de Resposta |
|-------|-----------|-------------------|
| 📖 Documentação | Leitura de docs e FAQs | Imediato |
| 💬 Comunidade | Perguntas em GitHub Discussions | 1-3 dias |
| 🐛 Bugs | Reportar bugs via Issues | 1-7 dias |
| ✨ Features | Sugerir novas funcionalidades | 1-14 dias |
| 🔒 Segurança | Vulnerabilidades de segurança | 24-48 horas |

## Antes de Pedir Ajuda

### Verifique o Básico

1. **Versão do Python**
   ```bash
   python --version  # Deve ser 3.10+
   ```

2. **Instalação do AI Route**
   ```bash
   which ai-route  # Deve mostrar ~/.local/bin/ai-route
   ```

3. **Permissões**
   ```bash
   ls -la ~/.local/bin/ai-route  # Deve ter permissão -rwxr-xr-x
   ```

4. **PATH**
   ```bash
   echo $PATH | grep -q "$HOME/.local/bin" && echo "OK" || echo "NÃO está no PATH"
   ```

### Cole Informações Relevantes

Ao reportar um problema, inclua:

- Sistema operacional e versão
- Versão do Python (`python --version`)
- Versão do AI Route (`ai-route --version` quando disponível)
- Comando executado
- Output esperado vs output obtido
- Passos para reproduzir
- Screenshots se aplicável

## Contribuindo

Se você quer contribuir com código:

1. Leia [CONTRIBUTING.md](CONTRIBUTING.md)
2. Fork o repositório
3. Crie uma branch para sua feature
4. Faça commit das suas mudanças
5. Abra um Pull Request

## Suporte Comercial

Atualmente, o AI Route é um projeto de código aberto mantido por voluntários. Não há suporte comercial disponível.

Se você precisa de suporte comercial ou SLA garantido, considere:
- Contratar os mantenedores diretamente
- Forkar o projeto e manter sua própria versão
- Usar o AI Route como base para um produto comercial

## Agradecimentos

Agradecemos a todos que contribuem com:
- Reportando bugs
- Sugerindo melhorias
- Contribuindo código
- Ajudando outros usuários na comunidade
