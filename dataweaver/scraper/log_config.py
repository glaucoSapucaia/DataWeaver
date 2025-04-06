from pathlib import Path

ROOT_DIR: Path = Path(__file__).resolve().parent

# LOGS

LOG_DIR = ROOT_DIR / 'logs'
LOG_FILE = LOG_DIR / "app.log"
ERROR_LOG_FILE = LOG_DIR / 'error.log'
WARNING_LOG_FILE = LOG_DIR / 'warning.log'
