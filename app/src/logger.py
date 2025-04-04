import logging
from utils import ensure_directory_exists
from log_config import LOG_FILE, ERROR_LOG_FILE, WARNING_LOG_FILE, LOG_DIR

# Verificando existencia do diretório
if not ensure_directory_exists(LOG_DIR):
    logging.error(f"Erro ao criar diretório {LOG_DIR}")
    exit(1)

# ==================== INFO ====================

logger = logging.getLogger("PDFProcessor")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# ==================== ERROR ====================

error_logger = logging.getLogger("PDFProcessorError")
error_logger.setLevel(logging.ERROR)

error_file_handler = logging.FileHandler(ERROR_LOG_FILE)
error_file_handler.setLevel(logging.ERROR)
error_file_handler.setFormatter(formatter)

error_logger.addHandler(error_file_handler)
error_logger.propagate = False

# ==================== WARNING ====================

warning_logger = logging.getLogger("PDFProcessorWarning")
warning_logger.setLevel(logging.WARNING)

warning_file_handler = logging.FileHandler(WARNING_LOG_FILE)
warning_file_handler.setLevel(logging.WARNING)
warning_file_handler.setFormatter(formatter)

warning_logger.addHandler(warning_file_handler)
warning_logger.propagate = False
