"""
Configuração do logger principal da aplicação DataWeaver.

Este módulo configura um logger com múltiplos *handlers* para registrar logs em diferentes arquivos
de acordo com o nível da mensagem (INFO, WARNING, ERROR) e também no console. A codificação dos
arquivos de log é UTF-8 para evitar problemas com caracteres especiais.

Antes da configuração, o módulo garante que o diretório de logs existe, criando-o se necessário.
"""

import logging
from utils import ensure_directory_exists
from log_config import LOG_FILE, ERROR_LOG_FILE, WARNING_LOG_FILE, LOG_DIR

if not ensure_directory_exists(LOG_DIR):
    # Aqui usamos logging pois, "logger" ainda não existe!
    logging.error(f"Erro ao criar diretório {LOG_DIR}")
    exit(1)

# ==================== CONFIGURAÇÃO DO LOGGER ====================

logger = logging.getLogger("DataWeaver")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# ========== Handlers ==========

# ========== INFO ==========

info_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)

# ========== WARNING ==========

warning_handler = logging.FileHandler(WARNING_LOG_FILE, encoding="utf-8")
warning_handler.setLevel(logging.WARNING)
warning_handler.setFormatter(formatter)

# ========== ERROR ==========

error_handler = logging.FileHandler(ERROR_LOG_FILE, encoding="utf-8")
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

# ========== STDOUT ==========

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# ========== Associação dos handlers ao logger ==========

logger.addHandler(info_handler)
logger.addHandler(warning_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)
