"""Testes para o módulo de roteamento do AI Route."""

import pytest

from ai_route.router import classify, AGENTS


class TestClassify:
    """Testes da função classify."""

    def test_shell_command_routes_to_copilot(self):
        """Shell commands devem rotear para copilot."""
        best, _ = classify("como listar todos os arquivos .py?")
        assert best == "copilot"

    def test_architecture_routes_to_claude(self):
        """Queries de arquitetura devem rotear para claude."""
        best, _ = classify("desenhe a arquitetura para um sistema de microserviços")
        assert best == "claude"

    def test_quick_fix_routes_to_aider_groq(self):
        """Quick fixes devem rotear para aider-groq."""
        best, _ = classify("corrige o bug de import no arquivo main.py")
        assert best == "aider-groq"

    def test_complex_refactor_routes_to_aider_or(self):
        """Refatoração complexa deve rotear para aider-or."""
        best, _ = classify("refatora todo o código para usar TypeScript strict")
        assert best == "aider-or"

    def test_explanation_routes_to_gemini(self):
        """Explicações devem rotear para gemini."""
        best, _ = classify("explique como funciona o algoritmo de ordenação")
        assert best == "gemini"

    def test_scaffolding_routes_to_codex(self):
        """Scaffolding deve rotear para codex."""
        best, _ = classify("cria um boilerplate para projeto React + Vite")
        assert best == "codex"

    def test_offline_routes_to_ollama(self):
        """Queries offline devem rotear para ollama."""
        best, _ = classify("analise este código sensível (sem internet)")
        assert best == "ollama"

    def test_short_query_boosts_copilot(self):
        """Queries muito curtas devem favorecer copilot."""
        best, ranked = classify("listar arquivos")
        # copilot deve ter pontuação alta
        copilot_score = next((score for name, score, _ in ranked if name == "copilot"), 0)
        assert copilot_score >= 10

    def test_long_query_boosts_claude(self):
        """Queries muito longas devem favorecer claude."""
        long_query = " ".join(["palavra"] * 35)
        best, ranked = classify(long_query)
        # claude deve ter pontuação alta
        claude_score = next((score for name, score, _ in ranked if name == "claude"), 0)
        assert claude_score >= 10

    def test_file_reference_boosts_aider(self):
        """Referências a arquivos devem favorecer aider-groq."""
        best, ranked = classify("corrige o bug no arquivo main.py")
        # aider-groq deve ter pontuação alta
        aider_score = next((score for name, score, _ in ranked if name == "aider-groq"), 0)
        assert aider_score >= 15

    def test_ranked_list_is_sorted(self):
        """A lista rankeada deve estar ordenada por score decrescente."""
        _, ranked = classify("qualquer query")
        scores = [score for _, score, _ in ranked]
        assert scores == sorted(scores, reverse=True)

    def test_all_agents_in_registry(self):
        """Todos os agents devem estar no registry."""
        expected_agents = {
            "claude", "aider-groq", "aider-or", "opencode",
            "gemini", "codex", "copilot", "ollama"
        }
        assert set(AGENTS.keys()) == expected_agents


class TestAgents:
    """Testes do registry de agents."""

    def test_agents_have_required_fields(self):
        """Todos os agents devem ter os campos obrigatórios."""
        required_fields = {"cmd", "binary", "tier", "cost", "speed", "strengths", "desc"}
        for name, agent in AGENTS.items():
            for field in required_fields:
                assert field in agent, f"Agent {name} missing field: {field}"

    def test_agent_costs_are_valid(self):
        """Os custos devem ser um dos valores válidos."""
        valid_costs = {"$", "$$", "$$$", "0"}
        for name, agent in AGENTS.items():
            assert agent["cost"] in valid_costs, f"Agent {name} has invalid cost: {agent['cost']}"

    def test_agent_speeds_are_valid(self):
        """As velocidades devem ser um dos valores válidos."""
        valid_speeds = {"instant", "fast", "medium", "slow"}
        for name, agent in AGENTS.items():
            assert agent["speed"] in valid_speeds, f"Agent {name} has invalid speed: {agent['speed']}"


class TestGetAgent:
    """Testes da função get_agent."""

    def test_get_existing_agent(self):
        """Deve retornar configuração de agent existente."""
        agent = get_agent("claude")
        assert agent["binary"] == "claude"
        assert agent["cost"] == "$$$"

    def test_get_nonexistent_agent_raises(self):
        """Deve levantar KeyError para agent inexistente."""
        with pytest.raises(KeyError):
            get_agent("nonexistent")
