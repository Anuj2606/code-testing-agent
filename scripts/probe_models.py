"""Probe each candidate Gemini model with one tiny request to see which work and what quota they report.
Run: python scripts/probe_models.py  (costs 1 request per model)"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from google import genai  # noqa: E402
from google.genai import types  # noqa: E402

from src.utils import config  # noqa: E402

MODELS = ["gemini-2.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.5-flash-lite", "gemini-2.5-flash",
          "gemini-3.5-flash", "gemini-3.6-flash", "gemini-3.7-flash", "gemini-3.8-flash", "gemma-4-31b-it"]

client = genai.Client(api_key=config.GEMINI_API_KEY)
for m in MODELS:
    try:
        r = client.models.generate_content(
            model=m, contents="Reply with the word ok",
            config=types.GenerateContentConfig(
                max_output_tokens=64,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)))
        print(f"OK   {m:24} {(r.text or '')[:20]!r}")
    except Exception as e:
        s = str(e)
        qid = re.search(r"quotaId': '([^']+)'", s)
        qv = re.search(r"quotaValue': '(\d+)'", s)
        print(f"FAIL {m:24} {s[:50]!r} quota={qid.group(1) if qid else '-'} limit={qv.group(1) if qv else '-'}")
