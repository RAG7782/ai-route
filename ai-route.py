#!/usr/bin/env python3
"""
AI Route — Roteador Inteligente de CLI Agents
Classifica a query e roteia para o CLI agent mais adequado.

Uso:
  ai-route "sua pergunta ou tarefa"
  ai-route --dry "query"          # mostra qual agent usaria sem executar
  ai-route --list                 # lista agents disponíveis
  ai-route --cost                 # mostra custo estimado por agent
"""

import sys
import os
import re
import subprocess
import shutil

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# AGENT REGISTRY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AGENTS = {
    "claude": {
        "cmd": ["claude", "-p"],
        "binary": "claude",
        "tier": "premium",
        "cost": "$$$",
        "speed": "medium",
        "strengths": ["architecture", "multi-file", "complex reasoning", "MCPs", "memory"],
        "desc": "Claude Code (Opus) — arquitetura, multi-arquivo, raciocínio profundo",
    },
    "aider-groq": {
        "cmd": ["bash", "-c", "source ~/.zshrc 2>/dev/null; aider-groq --message"],
        "binary": "aider",
        "tier": "free",
        "cost": "$",
        "speed": "fast",
        "strengths": ["quick code", "refactor simple", "single file", "git commits"],
        "desc": "Aider + Groq (554 t/s) — code rápido, grátis",
    },
    "aider-or": {
        "cmd": ["bash", "-c", "source ~/.zshrc 2>/dev/null; aider-or --message"],
        "binary": "aider",
        "tier": "cheap",
        "cost": "$$",
        "speed": "medium",
        "strengths": ["complex refactor", "multi-file refactor", "deep code"],
        "desc": "Aider + OpenRouter (DeepSeek) — refatoração complexa barata",
    },
    "opencode": {
        "cmd": ["opencode"],
        "binary": "opencode",
        "tier": "free",
        "cost": "$",
        "speed": "medium",
        "strengths": ["explore codebase", "understand code", "free tier", "multi-model", "auto-routing", "code generation", "refactor"],
        "desc": "OpenCode — 358+ modelos via OmniRoute/Nvidia/Ollama, auto-routing por query",
    },
    "gemini": {
        "cmd": ["gemini"],
        "binary": "gemini",
        "tier": "free",
        "cost": "$",
        "speed": "fast",
        "strengths": ["large context", "explanation", "docs", "free tier"],
        "desc": "Gemini CLI — contexto grande, explicações, grátis",
    },
    "codex": {
        "cmd": ["codex"],
        "binary": "codex",
        "tier": "cheap",
        "cost": "$$",
        "speed": "fast",
        "strengths": ["scaffolding", "prototype", "quick app"],
        "desc": "OpenAI Codex — scaffolding, protótipos rápidos",
    },
    "copilot": {
        "cmd": ["gh", "copilot", "suggest", "-t", "shell"],
        "binary": "gh",
        "tier": "free",
        "cost": "$",
        "speed": "instant",
        "strengths": ["shell commands", "one-liners", "cli help"],
        "desc": "GitHub Copilot — sugere comandos shell",
    },
    "ollama": {
        "cmd": ["ollama", "run", "gemma4:26b"],
        "binary": "ollama",
        "tier": "free",
        "cost": "0",
        "speed": "medium",
        "strengths": ["offline", "private", "general chat", "no internet"],
        "desc": "Ollama local — 100% offline, privado",
    },
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLASSIFICATION RULES (scored, not keyword-only)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RULES = [
    # (pattern, agent, score_boost, reason)
    # Shell / CLI commands
    (r"\b(como|how|comando|command|shell|terminal|bash|zsh)\b.*\b(listar|deletar|copiar|mover|encontrar|parar|matar|kill|list|delete|copy|move|find|stop)\b", "copilot", 30, "shell command question"),
    (r"\b(docker|kubectl|git|npm|pip|brew|apt|curl|wget|ssh|scp|rsync|tar|chmod|chown)\b", "copilot", 25, "CLI tool usage"),

    # Architecture / complex
    (r"\b(arquitetura|architecture|design|system|microservi[cç]|pipeline|orquest|orchestrat)\b", "claude", 30, "architecture/design task"),
    (r"\b(multi.?file|multi.?arquivo|refator.*comple|migra[cç]|migration)\b", "claude", 25, "multi-file complex task"),
    (r"\b(MCP|memory|IMI|ClawVault|Qdrant|Supabase|n8n)\b", "claude", 35, "needs MCP tools"),
    (r"\b(analise cr[ií]tica|racioc[ií]nio|reason|think.*step|chain.?of.?thought)\b", "claude", 20, "deep reasoning"),
    (r"\b(jurid|tribut|CARF|STF|STJ|jurisprud|OAB|penal|civil|trabalhist|ICMS|ISS|IPVA|ADI|ementa|ac[oó]rd[aã]o)\b", "claude", 40, "legal domain (needs context)"),

    # Quick code changes
    (r"\b(fix|corrig|bug|error|typo|ajust|ajeit)\b", "aider-groq", 20, "quick fix"),
    (r"\b(adicionar?|add|criar?|create|implementar?|implement)\b.*\b(fun[cç][aã]o|function|method|endpoint|route|component)\b", "aider-groq", 20, "add single function"),
    (r"\b(renomear?|rename|extrair?|extract|mover?|move)\b.*\b(fun[cç]|class|method|vari[aá]vel|variable)\b", "aider-groq", 15, "simple refactor"),

    # Complex refactor
    (r"\b(refator|refactor).*\b(comple[xt]|inteiro|entire|total|full|all)\b", "aider-or", 25, "complex refactor"),
    (r"\b(reescrev|rewrite|reestrutur|restructure)\b", "aider-or", 20, "rewrite/restructure"),

    # Exploration / understanding
    (r"\b(expli[cq]|explain|entend|understand|como funciona|how.*work|what.*does)\b", "gemini", 20, "explanation/understanding"),
    (r"\b(document|doc|README|comentar|comment)\b", "gemini", 15, "documentation"),
    (r"\b(explor|naveg|navigate|browse|find.*in.*code)\b", "opencode", 15, "code exploration"),

    # Scaffolding
    (r"\b(scaffold|boilerplate|starter|template|bootstrap|novo projeto|new project|criar app|create app)\b", "codex", 25, "scaffolding/prototype"),
    (r"\b(protot[ií]p|prototype|MVP|poc|proof.?of.?concept)\b", "codex", 20, "prototyping"),

    # Offline / privacy
    (r"\b(offline|sem internet|privado|private|local|confidencial|confidential|sensivel|sensitive)\b", "ollama", 30, "offline/privacy required"),
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SCORING ENGINE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def classify(query: str) -> tuple[str, list[tuple[str, int, str]]]:
    """Score each agent and return (best_agent, [(agent, score, reasons)])"""
    query_lower = query.lower()
    scores: dict[str, int] = {name: 0 for name in AGENTS}
    reasons: dict[str, list[str]] = {name: [] for name in AGENTS}

    for pattern, agent, boost, reason in RULES:
        if re.search(pattern, query_lower, re.IGNORECASE):
            scores[agent] += boost
            reasons[agent].append(reason)

    # Length heuristic: very short queries → copilot or aider-groq
    if len(query.split()) <= 5:
        scores["copilot"] += 10
        reasons["copilot"].append("short query")

    # Length heuristic: very long queries → claude (complex)
    if len(query.split()) > 30:
        scores["claude"] += 10
        reasons["claude"].append("long/complex query")

    # File references → aider
    if re.search(r"\b\w+\.(py|js|ts|tsx|jsx|rs|go|java|rb|cpp|c|h)\b", query):
        scores["aider-groq"] += 15
        reasons["aider-groq"].append("file reference detected")

    # Default: if no strong signal, use aider-groq (fast, free, good enough)
    max_score = max(scores.values())
    if max_score == 0:
        scores["aider-groq"] += 5
        reasons["aider-groq"].append("default (no strong signal)")

    # Filter to available agents only
    available = {k: v for k, v in scores.items() if shutil.which(AGENTS[k]["binary"])}
    if not available:
        available = scores  # fallback to all

    best = max(available, key=available.get)
    ranked = sorted(
        [(name, scores[name], ", ".join(reasons[name]) if reasons[name] else "-")
         for name in scores if scores[name] > 0],
        key=lambda x: -x[1]
    )

    return best, ranked


def show_list():
    print("\n  AI Route — Agents Disponíveis\n")
    for name, info in AGENTS.items():
        available = "ok" if shutil.which(info["binary"]) else "N/A"
        status = f"[{available}]"
        print(f"  {info['cost']:>4}  {name:<14} {status:<6}  {info['desc']}")
    print()


def show_cost():
    print("\n  AI Route — Custo por Agent\n")
    print(f"  {'Agent':<14} {'Tier':<8} {'Cost':<6} {'Speed':<8}")
    print(f"  {'─'*14} {'─'*8} {'─'*6} {'─'*8}")
    for name, info in sorted(AGENTS.items(), key=lambda x: x[1]["cost"]):
        print(f"  {name:<14} {info['tier']:<8} {info['cost']:<6} {info['speed']:<8}")
    print()


def main():
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return

    if args[0] == "--list":
        show_list()
        return

    if args[0] == "--cost":
        show_cost()
        return

    dry_run = False
    if args[0] == "--dry":
        dry_run = True
        args = args[1:]

    query = " ".join(args)
    best, ranked = classify(query)
    agent = AGENTS[best]

    # Display routing decision
    print(f"\n  \033[36m{'━'*50}\033[0m")
    print(f"  \033[1mAI Route\033[0m → \033[1;32m{best}\033[0m  {agent['cost']}  ({agent['speed']})")
    print(f"  \033[2m{agent['desc']}\033[0m")

    if len(ranked) > 1:
        print(f"\n  \033[2mScoring:\033[0m")
        for name, score, reason in ranked[:4]:
            marker = " \033[32m>\033[0m" if name == best else "  "
            print(f"  {marker} {name:<14} {score:>3}pts  \033[2m{reason}\033[0m")

    print(f"  \033[36m{'━'*50}\033[0m\n")

    if dry_run:
        print(f"  \033[2mComando: {' '.join(agent['cmd'])} \"{query}\"\033[0m\n")
        return

    # Execute the agent
    if best == "copilot":
        os.execvp("gh", ["gh", "copilot", "suggest", "-t", "shell", query])
    elif best == "claude":
        os.execvp("claude", ["claude", "-p", query])
    elif best.startswith("aider"):
        script = "aider-groq" if best == "aider-groq" else "aider-or"
        # aider needs files — just print suggestion if no files referenced
        files = re.findall(r"\b(\S+\.(?:py|js|ts|tsx|jsx|rs|go|java|rb|cpp|c|h))\b", query)
        if files:
            cmd = f"source ~/.zshrc 2>/dev/null; {script} {' '.join(files)} --message \"{query}\""
        else:
            print(f"  \033[33mDica:\033[0m Aider funciona melhor com arquivos. Exemplo:")
            print(f"  ai-route \"refatora {best} arquivo.py\"\n")
            cmd = f"source ~/.zshrc 2>/dev/null; {script} --message \"{query}\""
        os.execvp("bash", ["bash", "-c", cmd])
    elif best == "opencode":
        os.execvp("opencode", ["opencode"])
    elif best == "gemini":
        os.execvp("gemini", ["gemini", query])
    elif best == "codex":
        os.execvp("codex", ["codex", query])
    elif best == "ollama":
        model = "gemma4:26b"
        os.execvp("ollama", ["ollama", "run", model, query])


if __name__ == "__main__":
    main()
