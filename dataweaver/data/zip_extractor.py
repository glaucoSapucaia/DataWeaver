from config import PDF_ZIP_FILE, DESTINATION_FOLDER
from utils import ensure_directory_exists
from logger import logger
import zipfile

if not ensure_directory_exists(DESTINATION_FOLDER):
    logger.error(f"Erro ao criar diretório {DESTINATION_FOLDER}")
    exit(1)

with zipfile.ZipFile(PDF_ZIP_FILE, 'r') as zip_file:
    zip_file.extractall(DESTINATION_FOLDER)
