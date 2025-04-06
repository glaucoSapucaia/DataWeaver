import logging
from utils import ensure_directory_exists
from log_config import LOG_FILE, ERROR_LOG_FILE, WARNING_LOG_FILE, LOG_DIR

# Verificando existência do diretório de logs
if not ensure_directory_exists(LOG_DIR):
    logging.error(f"Erro ao criar diretório {LOG_DIR}")
    exit(1)

# ==================== INFO ====================
# Logger principal para mensagens informativas e logs gerais
logger = logging.getLogger("DataWeaver")
logger.setLevel(logging.DEBUG)  # permite INFO, WARNING e ERROR

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Handler INFO (grava INFO e acima)
info_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)

# Handler WARNING
warning_handler = logging.FileHandler(WARNING_LOG_FILE, encoding="utf-8")
warning_handler.setLevel(logging.WARNING)
warning_handler.setFormatter(formatter)

# Handler ERROR
error_handler = logging.FileHandler(ERROR_LOG_FILE, encoding="utf-8")
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

# Console também
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Adiciona todos
logger.addHandler(info_handler)
logger.addHandler(warning_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)