# Política de Segurança

## Versão

Versão 1.0 - Última atualização: 2026-04-23

## Relatando Vulnerabilidades

Se você descobrir uma vulnerabilidade de segurança, por favor relate de forma responsável:

1. **Não** crie uma issue pública
2. Envie um email para: security@example.com
3. Inclua:
   - Descrição da vulnerabilidade
   - Passos para reproduzir
   - Impacto potencial
   - Sugestão de correção (se aplicável)

Nós responderemos dentro de 48 horas com:
   - Confirmação de recebimento
   - Plano de correção
   - Timeline estimado

## Versões Suportadas

| Versão | Status | Fim de Vida |
|---------|--------|------------|
| 0.1.x  | ✅ Suportado | 2026-10-23 |
| 0.0.x  | ❌ Não suportado | 2026-04-23 |

## Coleta de Dados

AI Route **não coleta dados** dos usuários. O script:
- Processa queries localmente
- Não faz chamadas de rede
- Não armazena histórico por padrão
- Não envia dados para servidores externos

## Dependências

AI Route depende apenas da biblioteca padrão do Python. Não há dependências externas que precisem de atualização de segurança.

## Boas Práticas

### Execução de Scripts

- Sempre revise scripts antes de executar
- Use `--dry` para preview de decisões
- Verifique a origem do script antes de instalar

### Permissões

- O script requer permissão de execução (`chmod +x`)
- Não requer permissões de root/admin
- Funciona com permissões de usuário normal

### PATH

- O script é instalado em `~/.local/bin`
- Verifique que este diretório está no seu PATH
- Evite instalar em diretórios do sistema (`/usr/local/bin`)

## Atualizações de Segurança

### Como Atualizar

```bash
# Via git
cd ~/ai-route
git pull origin main

# Via pip (quando disponível)
pip install --upgrade ai-route
```

### Verificar Integridade

```bash
# Verificar hash do script
sha256sum ~/.local/bin/ai-route

# Comparar com hash oficial
# (disponível em releases do GitHub)
```

## Divulgação Responsável

Se você encontrar uma vulnerabilidade e decidir divulgá-la publicamente antes de termos tempo para corrigir:

1. Forneça detalhes suficientes para que usuários possam se proteger
2. Não forneça código de exploração
3. Dê tempo razoável para correção (mínimo 30 dias)

## Agradecimentos

Agradecemos a todos que reportam vulnerabilidades de forma responsável e ajudam a manter o AI Route seguro.
