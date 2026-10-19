"""Router behaviour with mocked model calls (no quota used)."""
import pytest

from src.tools import llm
from src.utils import config


@pytest.fixture(autouse=True)
def isolated(monkeypatch, tmp_path):
    monkeypatch.setattr(llm, "_USAGE_FILE", tmp_path / "usage.json")
    monkeypatch.setattr(config, "GEMINI_MODELS", ["m1", "m2", "m3"])
    monkeypatch.setattr(config, "LLM_PROVIDER", "gemini")
    monkeypatch.setattr(llm.time, "sleep", lambda s: None)


def test_old_format_usage_file_is_ignored(monkeypatch):
    llm._USAGE_FILE.write_text('{"date": "%s", "gemini": 3, "ollama": 0}' % llm._quota_day())
    assert llm.usage_summary()["calls"] == {}


def test_uses_first_model(monkeypatch):
    seen = []
    monkeypatch.setattr(llm, "_gemini", lambda model, prompt: (seen.append(model), "ok")[1])
    assert llm.complete("p") == "ok" and seen == ["m1"]


def test_rotates_on_daily_quota_and_remembers(monkeypatch):
    def fake(model, prompt):
        if model == "m1":
            raise RuntimeError("429 RESOURCE_EXHAUSTED GenerateRequestsPerDayPerProjectPerModel-FreeTier")
        return model
    monkeypatch.setattr(llm, "_gemini", fake)
    assert llm.complete("p") == "m2"
    assert "m1" in llm.usage_summary()["exhausted"]
    assert llm.complete("p") == "m2"  # m1 is skipped without being retried


def test_transient_error_falls_through_without_marking_exhausted(monkeypatch):
    def fake(model, prompt):
        if model == "m1":
            raise RuntimeError("503 UNAVAILABLE")
        return model
    monkeypatch.setattr(llm, "_gemini", fake)
    assert llm.complete("p") == "m2"
    assert llm.usage_summary()["exhausted"] == []


def test_per_minute_limit_waits_and_retries_same_model(monkeypatch):
    n = {"c": 0}

    def fake(model, prompt):
        n["c"] += 1
        if n["c"] == 1:
            raise RuntimeError("429 RESOURCE_EXHAUSTED GenerateRequestsPerMinutePerProjectPerModel retry in 3s")
        return model
    monkeypatch.setattr(llm, "_gemini", fake)
    assert llm.complete("p") == "m1"


def test_all_models_spent_raises_quota_exhausted(monkeypatch):
    def fake(model, prompt):
        raise RuntimeError("429 PerDay")
    monkeypatch.setattr(llm, "_gemini", fake)
    with pytest.raises(llm.QuotaExhausted):
        llm.complete("p")

