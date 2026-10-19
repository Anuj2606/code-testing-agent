"""Logger that writes every agent step to the console and results/logs/agent_runs.log."""
import logging

from src.utils.config import LOG_FILE


def get_logger(name: str = "agent") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handlers = [logging.StreamHandler()]
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(LOG_FILE, encoding="utf-8"))
    except OSError:  # read-only or unwritable log dir (e.g. hardened container): console only
        pass
    for handler in handlers:
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    return logger
