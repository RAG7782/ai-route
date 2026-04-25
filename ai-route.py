#!/usr/bin/env python3
"""
AI Route — Roteador Inteligente de CLI Agents
Classifica a query e roteia para o CLI agent mais adequado.

Uso:
  ai-route "sua pergunta ou tarefa"
  ai-route --dry "query"                  # mostra qual agent usaria sem executar
  ai-route --smart "query"                # usa LLM (Groq) para classificar
  ai-route --smart --dry "query"          # combina smart + dry run
  ai-route --local "query"                # usa classificador local (Ollama) v3
  ai-route --list                         # lista agents disponíveis
  ai-route --cost                         # mostra custo estimado por agent
  ai-route --feedback good [--query "q"]  # registra feedback para learning loop (v2)
  ai-route --feedback bad [--query "q"]   # registra feedback negativo
  ai-route --train                        # exporta training data para fine-tune (v3)
  ai-route --stats                        # mostra estatísticas de routing
"""

import sys
import os
import re
import json
import subprocess
import shutil
from pathlib import Path
from datetime import datetime, timezone
from openai import OpenAI

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


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FEEDBACK & LEARNING (v2)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_DATA_DIR = Path(os.path.expanduser("~/.aiox/ai-route"))
_FEEDBACK_LOG = _DATA_DIR / "feedback.jsonl"
_ROUTING_LOG = _DATA_DIR / "routing_history.jsonl"
_CLASSIFIER_PROMPT = Path(__file__).parent / "classifier_prompt.txt"


def _load_classifier_prompt() -> str:
    """Load classifier prompt from file, with fallback to inline default."""
    if _CLASSIFIER_PROMPT.exists():
        return _CLASSIFIER_PROMPT.read_text().strip()
    return (
        f"You are an AI CLI agent router. Given a developer query, "
        f"choose the best agent from: {list(AGENTS.keys())}. "
        f"Reply with ONLY the agent name, nothing else."
    )


def _log_routing(query: str, agent: str, method: str) -> None:
    """Log every routing decision for learning loop."""
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "query": query,
        "agent": agent,
        "method": method,
    }
    with open(_ROUTING_LOG, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def record_feedback(quality: str, query: str = None, agent: str = None) -> None:
    """Record feedback (good/bad) for the most recent or specified routing.

    Args:
        quality: "good" or "bad"
        query: Optional query to match (if None, uses last routing)
        agent: Optional agent override (if None, uses the routed agent)
    """
    _DATA_DIR.mkdir(parents=True, exist_ok=True)

    # If no query specified, find the last routing
    if query is None and _ROUTING_LOG.exists():
        last_line = None
        with open(_ROUTING_LOG) as f:
            for line in f:
                if line.strip():
                    last_line = line.strip()
        if last_line:
            last = json.loads(last_line)
            query = last["query"]
            agent = agent or last["agent"]

    if not query:
        print("  No routing history found. Use --query to specify.")
        return

    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "query": query,
        "agent": agent or "unknown",
        "quality": quality,
    }
    with open(_FEEDBACK_LOG, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"  Feedback recorded: {quality} for {agent or 'last'}")


def _build_feedback_context() -> str:
    """Build feedback context string for LLM prompt augmentation."""
    if not _FEEDBACK_LOG.exists():
        return ""

    good_agents: dict[str, list[str]] = {}
    bad_agents: dict[str, list[str]] = {}

    with open(_FEEDBACK_LOG) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
                agent = d.get("agent", "")
                query = d.get("query", "")[:80]
                if d.get("quality") == "good":
                    good_agents.setdefault(agent, []).append(query)
                elif d.get("quality") == "bad":
                    bad_agents.setdefault(agent, []).append(query)
            except json.JSONDecodeError:
                continue

    if not good_agents and not bad_agents:
        return ""

    parts = ["\n\nLearned routing preferences from user feedback:"]
    for agent, queries in good_agents.items():
        samples = queries[-3:]  # last 3
        parts.append(f"  GOOD for {agent}: {'; '.join(samples)}")
    for agent, queries in bad_agents.items():
        samples = queries[-3:]
        parts.append(f"  BAD for {agent} (avoid for similar): {'; '.join(samples)}")

    return "\n".join(parts)


def classify_with_llm(query: str) -> tuple[str, list[tuple[str, int, str]]]:
    """Classifica query via LLM leve (v2: with feedback context)."""
    try:
        client = OpenAI(base_url="http://localhost:20128/v1", api_key="x")
        prompt = _load_classifier_prompt()
        feedback_ctx = _build_feedback_context()
        if feedback_ctx:
            prompt += feedback_ctx

        response = client.chat.completions.create(
            model="groq/qwen/qwen3-32b",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": query},
            ],
            max_tokens=20,
            temperature=0,
        )
        raw = response.choices[0].message.content.strip().lower()
        # Strip thinking tags if present (Qwen3 sometimes wraps in <think>)
        agent = re.sub(r"</?think[^>]*>", "", raw).strip()
        if agent in AGENTS:
            return agent, [(agent, 100, "LLM classification (v2)")]
        # Try partial match
        for name in AGENTS:
            if name in agent:
                return name, [(name, 100, "LLM classification (v2, partial)")]
        # Fallback to regex scoring
        return classify(query)
    except Exception:
        return classify(query)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOCAL CLASSIFIER (v3)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_LOCAL_MODEL = os.environ.get("AI_ROUTE_LOCAL_MODEL", "qwen3:8b")
_TRAINING_DATA = _DATA_DIR / "training_data.jsonl"


def classify_with_local(query: str) -> tuple[str, list[tuple[str, int, str]]]:
    """Classify using local Ollama model (v3: fine-tuned or prompted)."""
    try:
        client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
        prompt = _load_classifier_prompt()
        feedback_ctx = _build_feedback_context()
        if feedback_ctx:
            prompt += feedback_ctx

        response = client.chat.completions.create(
            model=_LOCAL_MODEL,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": query},
            ],
            max_tokens=20,
            temperature=0,
        )
        raw = response.choices[0].message.content.strip().lower()
        agent = re.sub(r"</?think[^>]*>", "", raw).strip()
        if agent in AGENTS:
            return agent, [(agent, 100, "local classification (v3)")]
        for name in AGENTS:
            if name in agent:
                return name, [(name, 100, "local classification (v3, partial)")]
        return classify(query)
    except Exception:
        return classify(query)


def export_training_data() -> None:
    """Export feedback + routing history as training data for fine-tuning.

    Format: JSONL with {"messages": [{"role": "system", ...}, {"role": "user", ...}, {"role": "assistant", ...}]}
    Only includes entries with positive feedback.
    """
    _DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Build set of (query, agent) pairs with good feedback
    good_pairs: dict[str, str] = {}
    if _FEEDBACK_LOG.exists():
        with open(_FEEDBACK_LOG) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                    if d.get("quality") == "good":
                        good_pairs[d["query"]] = d["agent"]
                except json.JSONDecodeError:
                    continue

    if not good_pairs:
        print("  No positive feedback found. Route some queries and use --feedback good first.")
        return

    prompt = _load_classifier_prompt()
    count = 0

    with open(_TRAINING_DATA, "w") as f:
        for query, agent in good_pairs.items():
            entry = {
                "messages": [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": query},
                    {"role": "assistant", "content": agent},
                ]
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            count += 1

    print(f"  Exported {count} training examples to {_TRAINING_DATA}")
    print(f"  Fine-tune with: ollama create ai-route-classifier -f Modelfile")
    print(f"  Modelfile example:")
    print(f'    FROM {_LOCAL_MODEL}')
    print(f'    ADAPTER {_TRAINING_DATA}')


def show_stats() -> None:
    """Show routing statistics from history and feedback."""
    print("\n  AI Route — Routing Statistics\n")

    # Routing history stats
    if _ROUTING_LOG.exists():
        methods: dict[str, int] = {}
        agents: dict[str, int] = {}
        total = 0
        with open(_ROUTING_LOG) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                    methods[d.get("method", "?")] = methods.get(d.get("method", "?"), 0) + 1
                    agents[d.get("agent", "?")] = agents.get(d.get("agent", "?"), 0) + 1
                    total += 1
                except json.JSONDecodeError:
                    continue

        print(f"  Total routings: {total}")
        print(f"  By method:")
        for m, c in sorted(methods.items(), key=lambda x: -x[1]):
            print(f"    {m:<20} {c:>5} ({c/total*100:.0f}%)")
        print(f"  By agent:")
        for a, c in sorted(agents.items(), key=lambda x: -x[1]):
            print(f"    {a:<20} {c:>5} ({c/total*100:.0f}%)")
    else:
        print("  No routing history yet.")

    # Feedback stats
    if _FEEDBACK_LOG.exists():
        good = bad = 0
        with open(_FEEDBACK_LOG) as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    d = json.loads(line.strip())
                    if d.get("quality") == "good":
                        good += 1
                    elif d.get("quality") == "bad":
                        bad += 1
                except json.JSONDecodeError:
                    continue
        total_fb = good + bad
        print(f"\n  Feedback: {good} good, {bad} bad ({good/total_fb*100:.0f}% positive)" if total_fb else "\n  No feedback yet.")
    else:
        print("\n  No feedback yet.")
    print()


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

    if args[0] == "--stats":
        show_stats()
        return

    if args[0] == "--train":
        export_training_data()
        return

    if args[0] == "--feedback":
        quality = args[1] if len(args) > 1 else "good"
        query_override = None
        if "--query" in args:
            qi = args.index("--query")
            query_override = args[qi + 1] if qi + 1 < len(args) else None
        record_feedback(quality, query=query_override)
        return

    dry_run = False
    smart = False
    local = False
    while args and args[0].startswith("--"):
        if args[0] == "--dry":
            dry_run = True
            args = args[1:]
        elif args[0] == "--smart":
            smart = True
            args = args[1:]
        elif args[0] == "--local":
            local = True
            args = args[1:]
        else:
            break

    query = " ".join(args)

    if local:
        best, ranked = classify_with_local(query)
        method = "local"
    elif smart:
        best, ranked = classify_with_llm(query)
        method = "smart"
    else:
        best, ranked = classify(query)
        method = "regex"

    # Log routing decision for learning loop
    _log_routing(query, best, method)
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
