"""CLI for AI Route.

The package entrypoint lives here so `ai-route`, `python -m ai_route`, and tests
exercise the same implementation.
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .router import AGENTS, classify, show_cost, show_list


HELP = """AI Route — Roteador Inteligente de CLI Agents

Uso:
  ai-route "sua pergunta ou tarefa"
  ai-route --dry "query"
  ai-route --smart "query"
  ai-route --local "query"
  ai-route --list
  ai-route --cost
  ai-route --feedback good [--query "q"]
  ai-route --feedback bad [--query "q"]
  ai-route --train
  ai-route --stats
"""

_LOCAL_MODEL = os.environ.get("AI_ROUTE_LOCAL_MODEL", "qwen3:8b")
_SMART_TIMEOUT = float(os.environ.get("AI_ROUTE_SMART_TIMEOUT", "3"))
_LOCAL_TIMEOUT = float(os.environ.get("AI_ROUTE_LOCAL_TIMEOUT", "5"))
_DEFAULT_DATA_DIR = Path(os.environ.get("AI_ROUTE_DATA_DIR", "~/.aiox/ai-route")).expanduser()
_FEEDBACK_LOG = _DEFAULT_DATA_DIR / "feedback.jsonl"
_ROUTING_LOG = _DEFAULT_DATA_DIR / "routing_history.jsonl"
_TRAINING_DATA = _DEFAULT_DATA_DIR / "training_data.jsonl"
_CLASSIFIER_PROMPT = Path(__file__).with_name("classifier_prompt.txt")


def _load_classifier_prompt() -> str:
    if _CLASSIFIER_PROMPT.exists():
        return _CLASSIFIER_PROMPT.read_text(encoding="utf-8").strip()
    return (
        "You are an AI CLI agent router. Given a developer query, choose the "
        f"best agent from: {', '.join(AGENTS)}. Reply with ONLY the agent name."
    )


def _append_jsonl(path: Path, entry: dict) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return True
    except OSError:
        return False


def _iter_jsonl(path: Path) -> Iterable[dict]:
    try:
        with path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue
    except OSError:
        return


def _log_routing(query: str, agent: str, method: str) -> None:
    _append_jsonl(_ROUTING_LOG, {
        "ts": datetime.now(timezone.utc).isoformat(),
        "query": query,
        "agent": agent,
        "method": method,
    })


def record_feedback(quality: str, query: str | None = None, agent: str | None = None) -> None:
    quality = quality.strip().lower()
    if quality not in {"good", "bad"}:
        print("  Feedback deve ser 'good' ou 'bad'.")
        return

    if query is None:
        last = None
        for entry in _iter_jsonl(_ROUTING_LOG):
            last = entry
        if last:
            query = last.get("query")
            agent = agent or last.get("agent")

    if not query:
        print("  No routing history found. Use --query to specify.")
        return

    ok = _append_jsonl(_FEEDBACK_LOG, {
        "ts": datetime.now(timezone.utc).isoformat(),
        "query": query,
        "agent": agent or "unknown",
        "quality": quality,
    })
    if ok:
        print(f"  Feedback recorded: {quality} for {agent or 'last'}")
    else:
        print("  Feedback not recorded: data directory is not writable.")


def _build_feedback_context() -> str:
    good_agents: dict[str, list[str]] = {}
    bad_agents: dict[str, list[str]] = {}

    for entry in _iter_jsonl(_FEEDBACK_LOG):
        agent = entry.get("agent", "")
        query = entry.get("query", "")[:80]
        if entry.get("quality") == "good":
            good_agents.setdefault(agent, []).append(query)
        elif entry.get("quality") == "bad":
            bad_agents.setdefault(agent, []).append(query)

    if not good_agents and not bad_agents:
        return ""

    parts = ["\n\nLearned routing preferences from user feedback:"]
    for agent, queries in good_agents.items():
        parts.append(f"  GOOD for {agent}: {'; '.join(queries[-3:])}")
    for agent, queries in bad_agents.items():
        parts.append(f"  BAD for {agent} (avoid for similar): {'; '.join(queries[-3:])}")
    return "\n".join(parts)


def _classify_with_openai_compatible(
    query: str,
    *,
    base_url: str,
    api_key: str,
    model: str,
    reason: str,
    timeout: float,
) -> tuple[str, list[tuple[str, int, str]]]:
    try:
        from openai import OpenAI
    except ImportError:
        return classify(query)

    try:
        prompt = _load_classifier_prompt() + _build_feedback_context()
        client = OpenAI(base_url=base_url, api_key=api_key, timeout=timeout)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": query},
            ],
            max_tokens=20,
            temperature=0,
        )
        raw = response.choices[0].message.content or ""
        agent = _parse_agent_name(raw)
        if agent in AGENTS:
            override = _policy_override(query, agent)
            if override and override != agent:
                return override, [
                    (override, 100, "policy override"),
                    (agent, 80, reason),
                ]
            return agent, [(agent, 100, reason)]
    except Exception:
        pass
    return classify(query)


def _parse_agent_name(raw: str) -> str:
    """Extract one valid agent name from a model response."""
    text = re.sub(r"<think>.*?</think>", "", raw, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"</?think[^>]*>", "", text, flags=re.IGNORECASE)
    text = text.strip().lower()
    text = re.sub(r"^`+|`+$", "", text).strip()
    if text in AGENTS:
        return text

    tokens = re.findall(r"[a-z]+(?:-[a-z]+)?", text)
    matches = [token for token in tokens if token in AGENTS]
    return matches[0] if len(matches) == 1 else ""


def _policy_override(query: str, agent: str) -> str:
    """Keep high-confidence local rules above the LLM classifier."""
    regex_agent, ranked = classify(query)
    top_score = ranked[0][1] if ranked else 0
    if top_score >= 25 and regex_agent in {"copilot", "ollama", "aider-or", "claude"}:
        return regex_agent
    return agent


def classify_with_llm(query: str) -> tuple[str, list[tuple[str, int, str]]]:
    return _classify_with_openai_compatible(
        query,
        base_url=os.environ.get("AI_ROUTE_SMART_BASE_URL", "http://localhost:20128/v1"),
        api_key=os.environ.get("AI_ROUTE_SMART_API_KEY", "x"),
        model=os.environ.get("AI_ROUTE_SMART_MODEL", "groq/qwen/qwen3-32b"),
        reason="LLM classification",
        timeout=_SMART_TIMEOUT,
    )


def classify_with_local(query: str) -> tuple[str, list[tuple[str, int, str]]]:
    return _classify_with_openai_compatible(
        query,
        base_url=os.environ.get("AI_ROUTE_LOCAL_BASE_URL", "http://localhost:11434/v1"),
        api_key=os.environ.get("AI_ROUTE_LOCAL_API_KEY", "ollama"),
        model=_LOCAL_MODEL,
        reason="local classification",
        timeout=_LOCAL_TIMEOUT,
    )


def export_training_data() -> None:
    good_pairs: dict[str, str] = {}
    for entry in _iter_jsonl(_FEEDBACK_LOG):
        if entry.get("quality") == "good" and entry.get("query") and entry.get("agent"):
            good_pairs[entry["query"]] = entry["agent"]

    if not good_pairs:
        print("  No positive feedback found. Route some queries and use --feedback good first.")
        return

    prompt = _load_classifier_prompt()
    try:
        _TRAINING_DATA.parent.mkdir(parents=True, exist_ok=True)
        with _TRAINING_DATA.open("w", encoding="utf-8") as f:
            for query, agent in good_pairs.items():
                f.write(json.dumps({
                    "messages": [
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": query},
                        {"role": "assistant", "content": agent},
                    ]
                }, ensure_ascii=False) + "\n")
    except OSError:
        print("  Training data not exported: data directory is not writable.")
        return

    print(f"  Exported {len(good_pairs)} training examples to {_TRAINING_DATA}")


def show_stats() -> None:
    print("\n  AI Route — Routing Statistics\n")

    methods: dict[str, int] = {}
    agents: dict[str, int] = {}
    total = 0
    for entry in _iter_jsonl(_ROUTING_LOG):
        methods[entry.get("method", "?")] = methods.get(entry.get("method", "?"), 0) + 1
        agents[entry.get("agent", "?")] = agents.get(entry.get("agent", "?"), 0) + 1
        total += 1

    if total:
        print(f"  Total routings: {total}")
        print("  By method:")
        for method, count in sorted(methods.items(), key=lambda item: -item[1]):
            print(f"    {method:<20} {count:>5} ({count / total * 100:.0f}%)")
        print("  By agent:")
        for agent, count in sorted(agents.items(), key=lambda item: -item[1]):
            print(f"    {agent:<20} {count:>5} ({count / total * 100:.0f}%)")
    else:
        print("  No routing history yet.")

    good = bad = 0
    for entry in _iter_jsonl(_FEEDBACK_LOG):
        if entry.get("quality") == "good":
            good += 1
        elif entry.get("quality") == "bad":
            bad += 1
    total_feedback = good + bad
    if total_feedback:
        print(f"\n  Feedback: {good} good, {bad} bad ({good / total_feedback * 100:.0f}% positive)")
    else:
        print("\n  No feedback yet.")
    print()


def print_routing(best: str, ranked: list[tuple[str, int, str]], dry: bool = False, query: str = "") -> None:
    agent = AGENTS[best]
    print(f"\n  \033[36m{'━' * 50}\033[0m")
    print(f"  \033[1mAI Route\033[0m → \033[1;32m{best}\033[0m  {agent['cost']}  ({agent['speed']})")
    print(f"  \033[2m{agent['desc']}\033[0m")

    if len(ranked) > 1:
        print("\n  \033[2mScoring:\033[0m")
        for name, score, reason in ranked[:4]:
            marker = " \033[32m>\033[0m" if name == best else "  "
            print(f"  {marker} {name:<14} {score:>3}pts  \033[2m{reason}\033[0m")
    print(f"  \033[36m{'━' * 50}\033[0m\n")

    if dry:
        cmd = " ".join(agent["cmd"]) if isinstance(agent["cmd"], list) else str(agent["cmd"])
        print(f"  \033[2mComando: {cmd} \"{query or '<query>'}\"\033[0m\n")


def _prompt_feedback(query: str, agent: str) -> None:
    """Ask user for feedback on the last routing decision (non-blocking)."""
    try:
        if not sys.stdin.isatty():
            return
        answer = input(f"  \033[2mFeedback: roteamento para '{agent}' foi bom? [y/n/skip] \033[0m").strip().lower()
        if answer in {"y", "yes", "s", "sim"}:
            record_feedback("good", query=query, agent=agent)
        elif answer in {"n", "no", "nao", "não"}:
            record_feedback("bad", query=query, agent=agent)
    except (EOFError, KeyboardInterrupt):
        pass


def execute_agent(best: str, query: str) -> None:
    agent = AGENTS[best]
    if best == "copilot":
        os.execvp("gh", ["gh", "copilot", "suggest", "-t", "shell", query])
    if best == "claude":
        os.execvp("claude", ["claude", "-p", query])
    if best.startswith("aider"):
        script = "aider-groq" if best == "aider-groq" else "aider-or"
        files = re.findall(r"\b(\S+\.(?:py|js|ts|tsx|jsx|rs|go|java|rb|cpp|c|h))\b", query)
        if files:
            cmd = f"source ~/.zshrc 2>/dev/null; {script} {' '.join(files)} --message \"{query}\""
        else:
            print("  \033[33mDica:\033[0m Aider funciona melhor com arquivos. Exemplo:")
            print(f"  ai-route \"refatora {best} arquivo.py\"\n")
            cmd = f"source ~/.zshrc 2>/dev/null; {script} --message \"{query}\""
        os.execvp("bash", ["bash", "-c", cmd])
    if best == "opencode":
        os.execvp("opencode", ["opencode"])
    if best == "gemini":
        os.execvp("gemini", ["gemini", query])
    if best == "codex":
        os.execvp("codex", ["codex", query])
    if best == "ollama":
        os.execvp("ollama", ["ollama", "run", "gemma4:26b", query])
    raise SystemExit(f"Unknown agent: {best}")


def main(argv: list[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)

    if not args or args[0] in {"-h", "--help"}:
        print(HELP)
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
            index = args.index("--query")
            query_override = args[index + 1] if index + 1 < len(args) else None
        record_feedback(quality, query=query_override)
        return

    dry_run = False
    smart = False
    local = False
    while args and args[0].startswith("--"):
        flag = args.pop(0)
        if flag == "--dry":
            dry_run = True
        elif flag == "--smart":
            smart = True
        elif flag == "--local":
            local = True
        else:
            print(f"  Unknown option: {flag}")
            print(HELP)
            return

    query = " ".join(args)
    if not query:
        print("  Erro: por favor forneça uma query.")
        print('  Uso: ai-route "sua pergunta ou tarefa"')
        return

    if local:
        best, ranked = classify_with_local(query)
        method = "local"
    elif smart:
        best, ranked = classify_with_llm(query)
        method = "smart"
    else:
        best, ranked = classify(query)
        method = "regex"

    _log_routing(query, best, method)
    print_routing(best, ranked, dry=dry_run, query=query)

    if dry_run:
        _prompt_feedback(query, best)
    else:
        execute_agent(best, query)
