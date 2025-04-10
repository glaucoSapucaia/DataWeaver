"""
Configurações de diretórios e arquivos de log da aplicação.

Este módulo define os caminhos base para os arquivos de log utilizados pela aplicação.
Todos os arquivos são criados dentro de uma pasta `logs`.
"""

from pathlib import Path

ROOT_DIR: Path = Path(__file__).resolve().parent

# ========== Diretórios e arquivos de log ==========

LOG_DIR = ROOT_DIR / 'logs'
LOG_FILE = LOG_DIR / "app.log"
ERROR_LOG_FILE = LOG_DIR / 'error.log'
WARNING_LOG_FILE = LOG_DIR / 'warning.log'
