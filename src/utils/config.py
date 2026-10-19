"""Central configuration: YAML defaults plus the GEMINI_API_KEY from the environment."""
import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

with open(ROOT / "configs" / "agent_config.yaml", encoding="utf-8") as f:
    _CFG = yaml.safe_load(f)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = _CFG["gemini_config"]["model"]
TEMPERATURE = _CFG["gemini_config"]["temperature"]
MAX_TOKENS = _CFG["gemini_config"]["max_tokens"]
_LLM = _CFG["llm_config"]
LLM_PROVIDER = os.getenv("LLM_PROVIDER", _LLM["provider"])
GEMINI_ROLES = set(_LLM["gemini_roles"])
GEMINI_MODELS = _LLM["gemini_models"]
OLLAMA_URL = _LLM["ollama_url"]
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", _LLM["ollama_model"])
OLLAMA_TIMEOUT = _LLM["ollama_timeout"]
MAX_ITERATIONS = _CFG["agent_config"]["max_iterations"]
SANDBOX_TIMEOUT = _CFG["tools_config"]["sandbox_timeout"]
RESTRICTED_IMPORTS = set(_CFG["tools_config"]["restricted_imports"])
LOG_FILE = ROOT / "results" / "logs" / "agent_runs.log"
