import logging
from config import LOG_FILE, ERROR_LOG_FILE

# Configuração do logger geral (INFO)
logger = logging.getLogger("PDFProcessor")
logger.setLevel(logging.INFO)  # Nível do logger principal

# Configuração do handler de arquivo para logs gerais
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.INFO)

# Configuração do handler de terminal para logs gerais
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

# Formato dos logs
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Adiciona os handlers ao logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


# Configuração do logger de erros (ERROR)
error_logger = logging.getLogger("PDFProcessorError")
error_logger.setLevel(logging.ERROR)  # Apenas logs de erro e acima

# Configuração do handler de arquivo para logs de erro
error_file_handler = logging.FileHandler(ERROR_LOG_FILE)
error_file_handler.setLevel(logging.ERROR)
error_file_handler.setFormatter(formatter)

# Adiciona o handler ao logger de erros
error_logger.addHandler(error_file_handler)

# Evita que logs de erro sejam duplicados no terminal ao herdar os handlers do logger raiz
error_logger.propagate = False
