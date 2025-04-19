from dataweaver.settings import *
from dataweaver.utils import ensure_directory_exists

import zipfile


zip_pdf_file = config.scraper.zip_name
zip_folder = config.dirs.pdfs

if not ensure_directory_exists(zip_folder):
    logger.error(f"Erro ao criar diretório {zip_folder}")
    exit(1)

with zipfile.ZipFile(zip_pdf_file, "r") as zip_file:
    zip_file.extractall(zip_folder)
