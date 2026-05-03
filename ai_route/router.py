"""
AI Route - Módulo de Roteamento

Contém a lógica principal de classificação e roteamento de queries
para CLI agents.
"""

from __future__ import annotations

import re
import shutil
import urllib.request
from pathlib import Path

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
        "strengths": ["explore codebase", "understand code", "free tier"],
        "desc": "OpenCode — free tier, exploração de código",
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
    "aider-omni": {
        "cmd": ["bash", "~/.aiox/scripts/aider-omniroute.sh", "--message"],
        "binary": "aider",
        "tier": "free",
        "cost": "$",
        "speed": "fast",
        "strengths": ["358 models", "fallback", "any model", "omniroute"],
        "desc": "Aider via OmniRoute — 358 modelos, fallback automático",
    },
    "symbiont": {
        "cmd": ["python3", str(Path.home() / ".aiox/tools/a2a_symbiont.py"), "--send", "route"],
        "binary": "python3",
        "tier": "premium",
        "cost": "$$$",
        "speed": "medium",
        "strengths": ["meta-orchestration", "multi-agent", "a2a-protocol", "routing", "escalation"],
        "desc": "SYMBIONT via A2A — meta-orquestrador, roteamento inteligente multi-agente",
    },
}


OMNIROUTE_URL = "http://localhost:20128"


def check_omniroute_health() -> dict | None:
    """Check OmniRoute availability and return model count, or None if down."""
    try:
        req = urllib.request.Request(
            f"{OMNIROUTE_URL}/v1/models",
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=2) as resp:
            if resp.status == 200:
                import json
                data = json.loads(resp.read())
                models = data.get("data", [])
                return {"status": "ok", "model_count": len(models)}
    except Exception:
        pass
    return None

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
    (r"\b(refator|refactor).*\b(comple[xt]|inteiro|entire|total|full|all|todo|toda|m[oó]dulo|module|m[uú]ltiplos? arquivos?|multiple files?)\b", "aider-or", 25, "complex refactor"),
    (r"\b(migra|migrar|migration|migrate).*\b(m[oó]dulo|module|auth|autentica[cç][aã]o|database|banco|api)\b", "aider-or", 25, "module migration"),
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

    # Offline / SYMBIONT — meta-orquestração, multi-agente, A2A
    (r"\b(symbiont|a2a.protocol)\b", "symbiont", 45, "meta-orchestration task"),
    (r"meta.?orquestra", "symbiont", 45, "meta-orchestration keyword"),
    (r"meta.?orchestrat", "symbiont", 45, "meta-orchestration keyword"),
    (r"\b(melhor agente|best agent|qual agente|which agent|auto.?dispatch)\b", "symbiont", 35, "routing decision"),
    (r"\b(paralelo|simultane|concomitant).*(agent|agente|model|modelo|revis)\b", "symbiont", 30, "parallel agent task"),
    (r"\b(escal[ae]|handoff|transfer).*(agente|agent|claude|codex|aider)\b", "symbiont", 30, "agent escalation"),
    (r"\b(orquestra[cç]|orchestrat).*(agente|agent|multi|modelo|model|revis)\b", "symbiont", 35, "agent orchestration"),
    (r"\b\d+\s*(agentes?|agents?)\b", "symbiont", 35, "multi-agent task"),
    (r"\borquestra[r]?\b.*\bagentes?\b", "symbiont", 35, "orchestrate agents"),
    (r"\bconsensus\b.*(arquitetura|architect|design|decisão|decision|tecnologi)", "symbiont", 40, "consensus on architecture"),
    (r"\b(consenso|consensus)\b.*(modelo|model|agent|agente|multi)", "symbiont", 40, "consensus multi-model"),
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SCORING ENGINE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def classify(query: str) -> tuple[str, list[tuple[str, int, str]]]:
    """
    Score each agent and return (best_agent, [(agent, score, reasons)])

    Args:
        query: A query string to classify

    Returns:
        Tuple of (best_agent_name, ranked_list)
        ranked_list contains tuples of (agent_name, score, reasons)
    """
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

    # OmniRoute boost: prefer aider-omni for complex tasks only (aider-or score > 0 signals
    # complexity; quick fixes stay with aider-groq for speed).
    omniroute_status = check_omniroute_health()
    if omniroute_status and scores.get("aider-or", 0) > 0:
        scores["aider-omni"] = max(scores.get("aider-omni", 0), scores["aider-or"] + 5)
        reasons["aider-omni"] = reasons.get("aider-or", []) + [
            f"OmniRoute available ({omniroute_status['model_count']} models, fallback)"
        ]

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


def show_list() -> None:
    """Display all available agents with their status."""
    print("\n  AI Route — Agents Disponíveis\n")
    for name, info in AGENTS.items():
        available = "ok" if shutil.which(info["binary"]) else "N/A"
        status = f"[{available}]"
        print(f"  {info['cost']:>4}  {name:<14} {status:<6}  {info['desc']}")
    print()


def show_cost() -> None:
    """Display cost comparison for all agents."""
    print("\n  AI Route — Custo por Agent\n")
    print(f"  {'Agent':<14} {'Tier':<8} {'Cost':<6} {'Speed':<8}")
    print(f"  {'─'*14} {'─'*8} {'─'*6} {'─'*8}")
    for name, info in sorted(AGENTS.items(), key=lambda x: x[1]["cost"]):
        print(f"  {name:<14} {info['tier']:<8} {info['cost']:<6} {info['speed']:<8}")
    print()


def get_agent(name: str) -> dict:
    """
    Get agent configuration by name.

    Args:
        name: Agent name

    Returns:
        Agent configuration dict

    Raises:
        KeyError: If agent name is not found
    """
    if name not in AGENTS:
        raise KeyError(f"Agent '{name}' not found. Available: {list(AGENTS.keys())}")
    return AGENTS[name]
