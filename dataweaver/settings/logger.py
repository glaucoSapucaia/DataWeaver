import logging
from .config import config

log_dir = config.logging.log_dir
log_file = config.logging.app_log
log_warning = config.logging.warning_log
log_error = config.logging.error_log

# ==================== FILTRO DE NÍVEL EXATO ====================


class ExactLevelFilter(logging.Filter):
    def __init__(self, level):
        super().__init__()
        self.level = level

    def filter(self, record):
        return record.levelno == self.level


# ==================== CONFIGURAÇÃO DO LOGGER ====================

logger = logging.getLogger("DataWeaver")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# ========== Handler: Todos os logs ==========

app_handler = logging.FileHandler(log_file, encoding="utf-8")
app_handler.setLevel(logging.DEBUG)  # Captura tudo
app_handler.setFormatter(formatter)

# ========== Handler: Apenas WARNING ==========

warning_handler = logging.FileHandler(log_warning, encoding="utf-8")
warning_handler.setLevel(logging.WARNING)
warning_handler.addFilter(ExactLevelFilter(logging.WARNING))
warning_handler.setFormatter(formatter)

# ========== Handler: Apenas ERROR ==========

error_handler = logging.FileHandler(log_error, encoding="utf-8")
error_handler.setLevel(logging.ERROR)
error_handler.addFilter(ExactLevelFilter(logging.ERROR))
error_handler.setFormatter(formatter)

# ========== Handler: Console (INFO+) ==========

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# ========== Adiciona handlers ao logger ==========

logger.addHandler(app_handler)
logger.addHandler(warning_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)
