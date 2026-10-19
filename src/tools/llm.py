"""LLM router built around the Gemini free tier.

Free-tier quotas are per project AND per model, so `gemini_models` is an ordered pool: calls go to the
first model with budget left. When a model reports its daily quota is spent (429 ...PerDay) it is marked
exhausted until the next day and the router moves on. Per-minute 429s wait out the suggested delay.
Transient errors (503/500) fall through to the next model. Ollama is an optional extra provider
(provider: "ollama" or "hybrid"); it is parked by default.

Usage is persisted in results/logs/llm_usage.json so budgets survive restarts.
"""
import json
import re
import time
from datetime import datetime, timedelta, timezone

import requests
from google import genai
from google.genai import types

from src.prompts.system_prompts import CODE_GENERATOR_PROMPT
from src.utils import config
from src.utils.logger import get_logger

log = get_logger("llm")
_USAGE_FILE = config.ROOT / "results" / "logs" / "llm_usage.json"
_client = None


class QuotaExhausted(RuntimeError):
    """Every configured model is out of budget (or unavailable) right now."""


def _quota_day() -> str:
    """Gemini daily quotas reset at midnight Pacific time (approximated as UTC-8)."""
    return (datetime.now(timezone.utc) - timedelta(hours=8)).strftime("%Y-%m-%d")


def _usage() -> dict:
    try:
        u = json.loads(_USAGE_FILE.read_text())
        if u.get("date") == _quota_day() and "calls" in u and "exhausted" in u:  # ignore old-format files
            return u
    except (OSError, ValueError):
        pass
    return {"date": _quota_day(), "calls": {}, "exhausted": []}


def _save(u: dict) -> None:
    _USAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    _USAGE_FILE.write_text(json.dumps(u, indent=1))


def _record(provider_model: str) -> None:
    u = _usage()
    u["calls"][provider_model] = u["calls"].get(provider_model, 0) + 1
    _save(u)


def _mark_exhausted(model: str) -> None:
    u = _usage()
    if model not in u["exhausted"]:
        u["exhausted"].append(model)
    _save(u)


def usage_summary() -> dict:
    u = _usage()
    total = sum(u["calls"].values()) or 1
    ollama = sum(n for k, n in u["calls"].items() if k.startswith("ollama"))
    return {**u, "total_calls": sum(u["calls"].values()), "ollama_pct": round(100 * ollama / total),
            "models_left": [m for m in config.GEMINI_MODELS if m not in u["exhausted"]]}


def _gemini(model: str, prompt: str) -> str:
    global _client
    if not config.GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set")
    _client = _client or genai.Client(api_key=config.GEMINI_API_KEY)
    resp = _client.models.generate_content(
        model=model, contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=CODE_GENERATOR_PROMPT, temperature=config.TEMPERATURE,
            max_output_tokens=config.MAX_TOKENS,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)))
    if not resp.text:
        raise RuntimeError("empty response (token budget spent on reasoning?)")
    return resp.text


def _ollama(prompt: str) -> str:
    r = requests.post(f"{config.OLLAMA_URL}/api/chat", timeout=config.OLLAMA_TIMEOUT, json={
        "model": config.OLLAMA_MODEL, "stream": False,
        "messages": [{"role": "system", "content": CODE_GENERATOR_PROMPT}, {"role": "user", "content": prompt}],
        "options": {"temperature": config.TEMPERATURE, "num_predict": config.MAX_TOKENS}})
    r.raise_for_status()
    return r.json()["message"]["content"]


def _candidates(role: str) -> list[str]:
    """Ordered 'gemini:<model>' / 'ollama' targets for this call."""
    exhausted = _usage()["exhausted"]
    gem = [f"gemini:{m}" for m in config.GEMINI_MODELS if m not in exhausted]
    mode = config.LLM_PROVIDER
    if mode == "ollama":
        return ["ollama"]
    if mode == "gemini":
        return gem
    return (gem + ["ollama"]) if role in config.GEMINI_ROLES else (["ollama"] + gem)


def complete(prompt: str, role: str = "generate") -> str:
    last = None
    for target in _candidates(role):
        for attempt in range(3):  # retries only for per-minute rate limits
            try:
                text = _ollama(prompt) if target == "ollama" else _gemini(target.split(":", 1)[1], prompt)
                _record(target)
                log.info("llm role=%s target=%s", role, target)
                return text
            except Exception as e:
                last, msg = e, str(e)
                if target.startswith("gemini") and "429" in msg:
                    if "PerDay" in msg or "per_day" in msg.lower():
                        log.warning("%s daily quota spent; moving to next model", target)
                        _mark_exhausted(target.split(":", 1)[1])
                        break
                    m = re.search(r"retry in ([\d.]+)s", msg) or re.search(r"retryDelay': '(\d+)s", msg)
                    wait = min(float(m.group(1)) + 1, 90) if m else 30
                    log.warning("%s per-minute limit; waiting %.0fs", target, wait)
                    time.sleep(wait)
                    continue
                if "404" in msg:  # model retired/unknown: skip it for today
                    _mark_exhausted(target.split(":", 1)[1]) if target.startswith("gemini") else None
                log.warning("%s failed (%s): %s", target, role, msg[:100])
                time.sleep(2)
                break
    raise QuotaExhausted(f"no model available: {str(last)[:200]}")
