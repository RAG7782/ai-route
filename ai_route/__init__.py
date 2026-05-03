"""
AI Route — Roteador Inteligente de CLI Agents

Este pacote fornece funcionalidade para rotear automaticamente
queries de desenvolvimento para o CLI agent mais adequado.
"""

__version__ = "0.1.0"
__author__ = "AI Route Contributors"
__license__ = "MIT"

from .cli import main
from .router import classify, show_cost, show_list

__all__ = ["classify", "main", "show_list", "show_cost", "__version__"]
