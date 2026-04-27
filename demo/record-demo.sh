#!/bin/bash
# AI Route — Demo recording script for asciinema
# Run: asciinema rec demo.cast -c "bash demo/record-demo.sh"
# Then: agg demo.cast demo.gif (or upload to asciinema.org)

set -e

# Colors
CYAN='\033[36m'
GREEN='\033[32m'
RESET='\033[0m'

type_slow() {
    local text="$1"
    for ((i=0; i<${#text}; i++)); do
        printf '%s' "${text:$i:1}"
        sleep 0.04
    done
    echo
}

pause() { sleep "${1:-1.5}"; }

clear
echo -e "${GREEN}AI Route${RESET} — The missing router for your AI coding agents"
echo ""
pause 2

# Query 1: Shell → Copilot
echo -e "${CYAN}# Query 1: Shell command${RESET}"
type_slow 'ai-route --dry "how to kill process on port 8080"'
ai-route --dry "how to kill process on port 8080"
pause 2

# Query 2: Architecture → Claude
echo -e "${CYAN}# Query 2: Architecture task${RESET}"
type_slow 'ai-route --dry "redesign the auth system to use OAuth2 with PKCE"'
ai-route --dry "redesign the auth system to use OAuth2 with PKCE"
pause 2

# Query 3: Quick fix → Aider
echo -e "${CYAN}# Query 3: Quick code fix${RESET}"
type_slow 'ai-route --dry "fix the typo in config.py line 42"'
ai-route --dry "fix the typo in config.py line 42"
pause 2

# Query 4: Explanation → Gemini
echo -e "${CYAN}# Query 4: Explanation${RESET}"
type_slow 'ai-route --dry "explain how this codebase handles authentication"'
ai-route --dry "explain how this codebase handles authentication"
pause 2

# Query 5: Legal (domain-specific) → Claude
echo -e "${CYAN}# Query 5: Domain-specific (legal)${RESET}"
type_slow 'ai-route --dry "análise ICMS-ST conforme ADI 5469 do STF"'
ai-route --dry "análise ICMS-ST conforme ADI 5469 do STF"
pause 2

# Stats
echo -e "${CYAN}# Learning stats${RESET}"
type_slow 'ai-route --stats'
ai-route --stats
pause 2

echo ""
echo -e "${GREEN}pip install ai-route${RESET}  |  github.com/RAG7782/ai-route"
echo ""
pause 3
