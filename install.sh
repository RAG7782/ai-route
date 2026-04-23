#!/bin/bash
# AI Route - Script de Instalação Automática
# Este script instala o AI Route no seu sistema

set -e

echo "🤖 AI Route - Instalação"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Detectar sistema operacional
OS="$(uname -s)"
case "$OS" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    CYGWIN*)    MACHINE=Cygwin;;
    MINGW*)     MACHINE=MinGW;;
    *)          MACHINE="UNKNOWN:$OS"
esac

echo "📦 Sistema detectado: $MACHINE"
echo ""

# Criar diretório de instalação se não existir
INSTALL_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"

echo "📁 Diretório de instalação: $INSTALL_DIR"
echo ""

# Copiar script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "📂 Diretório do script: $SCRIPT_DIR"
echo ""

if [ -f "$SCRIPT_DIR/ai-route.py" ]; then
    cp "$SCRIPT_DIR/ai-route.py" "$INSTALL_DIR/ai-route"
    echo "✅ Script copiado para: $INSTALL_DIR/ai-route"
else
    echo "❌ Erro: ai-route.py não encontrado em $SCRIPT_DIR"
    exit 1
fi

# Tornar executável
chmod +x "$INSTALL_DIR/ai-route"
echo "✅ Permissão de execução concedida"
echo ""

# Verificar se ~/.local/bin está no PATH
if echo "$PATH" | grep -q "$HOME/.local/bin"; then
    echo "✅ $HOME/.local/bin já está no PATH"
else
    echo "⚠️  $HOME/.local/bin NÃO está no PATH"
    echo ""
    echo "Adicionando ao ~/.zshrc..."
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
    echo "✅ Adicionado ao ~/.zshrc"
    echo ""
    echo "⚠️  Execute: source ~/.zshrc"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Instalação concluída!"
echo ""
echo "🚀 Para usar, execute:"
echo "   source ~/.zshrc  # se necessário"
echo "   ai-route --list"
echo ""
echo "📖 Para mais informações, veja README.md"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
