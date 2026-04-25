"""CLI tests for AI Route."""

from __future__ import annotations

import json

from ai_route.cli import main


def test_entrypoint_help(capsys):
    main(["--help"])
    out = capsys.readouterr().out
    assert "AI Route" in out
    assert "--smart" in out


def test_dry_run_does_not_require_writable_home(tmp_path, monkeypatch, capsys):
    not_a_dir = tmp_path / "not-a-dir"
    not_a_dir.write_text("blocks mkdir", encoding="utf-8")
    monkeypatch.setattr("ai_route.cli._ROUTING_LOG", not_a_dir / "routing_history.jsonl")

    main(["--dry", "desenhe arquitetura de microserviços"])

    out = capsys.readouterr().out
    assert "AI Route" in out
    assert "claude" in out


def test_feedback_and_stats_use_data_dir(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr("ai_route.cli._FEEDBACK_LOG", tmp_path / "feedback.jsonl")
    monkeypatch.setattr("ai_route.cli._ROUTING_LOG", tmp_path / "routing_history.jsonl")

    main(["--dry", "corrige o bug no arquivo main.py"])
    main(["--feedback", "good"])
    main(["--stats"])

    out = capsys.readouterr().out
    assert "Feedback recorded" in out
    assert "Routing Statistics" in out

    feedback = [json.loads(line) for line in (tmp_path / "feedback.jsonl").read_text().splitlines()]
    assert feedback[0]["quality"] == "good"
    assert feedback[0]["agent"] == "aider-groq"


def test_smart_falls_back_without_openai(monkeypatch, capsys):
    def fail_import(name, *args, **kwargs):
        if name == "openai":
            raise ImportError("no openai")
        return original_import(name, *args, **kwargs)

    original_import = __import__
    monkeypatch.setattr("builtins.__import__", fail_import)

    main(["--smart", "--dry", "explique como funciona o algoritmo"])

    out = capsys.readouterr().out
    assert "gemini" in out
