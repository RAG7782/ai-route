"""
AI Route - CLI Entry Point

Este módulo fornece a interface de linha de comando para o AI Route.
"""

import sys
import os
import re
from typing import List, Tuple

from .router import AGENTS, classify, show_list, show_cost, get_agent


def print_header() -> None:
    """Print the AI Route header."""
    print(f"\n  \033[36m{'━'*50}\033[0m")
    print(f"  \033[1mAI Route\033[0m — Roteador Inteligente de CLI Agents")
    print(f"  \033[36m{'━'*50}\033[0m\n")


def print_routing(best: str, ranked: List[Tuple[str, int, str]], dry: bool = False) -> None:
    """
    Print the routing decision with scoring details.

    Args:
        best: Best agent name
        ranked: Ranked list of (agent, score, reasons)
        dry: If True, show command without executing
    """
    agent = AGENTS[best]

    print(f"  \033[1mAI Route → \033[1;32m{best}\033[0m  {agent['cost']}  ({agent['speed']})")
    print(f"  \033[2m{agent['desc']}\033[0m")

    if len(ranked) > 1:
        print(f"\n  \033[2mScoring:\033[0m")
        for name, score, reason in ranked[:4]:
            marker = " \033[32m>\033[0m" if name == best else "  "
            print(f"  {marker} {name:<14} {score:>3}pts  \033[2m{reason}\033[0m")

    print(f"  \033[36m{'━'*50}\033[0m\n")

    if dry:
        cmd = " ".join(agent['cmd']) if isinstance(agent['cmd'], list) else agent['cmd']
        print(f"  \033[2mComando: {cmd} \"<query>\"\033[0m\n")


def execute_agent(best: str, query: str) -> None:
    """
    Execute the chosen agent with the query.

    Args:
        best: Best agent name
        query: Query string to pass to the agent
    """
    agent = AGENTS[best]

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


def main() -> None:
    """Main CLI entry point."""
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
    if not query:
        print("  \033[31mErro:\033[0m Por favor forneça uma query.")
        print("  Uso: ai-route \"sua pergunta ou tarefa\"")
        return

    best, ranked = classify(query)
    print_routing(best, ranked, dry=dry_run)

    if not dry_run:
        execute_agent(best, query)


if __name__ == "__main__":
    main()
