import logging
from config import LOG_FILE

# Configuração do logger
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.INFO  # Pode ser alterado para DEBUG, WARNING, ERROR...

logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),  # Salva logs no arquivo
        logging.StreamHandler()  # Exibe logs no terminal
    ]
)

# Criando a instância do logger
logger = logging.getLogger("PDFProcessor")
