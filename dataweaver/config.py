"""
Configurações principais da aplicação.

Este módulo define os diretórios utilizados no projeto, carrega variáveis de ambiente
usadas durante a execução e garante a existência das pastas essenciais.
"""

from .scraper.utils import get_env_variable, ensure_directory_exists
from dotenv import load_dotenv  # type: ignore
from pathlib import Path
from .logger import logger

load_dotenv()

# ========== Scraper Diretórios ==========

ROOT_DIR: Path = Path(__file__).resolve().parent
PDFS_DIR: Path = ROOT_DIR / 'scraper' / 'pdfs'
MODULES_DIR: Path = ROOT_DIR / 'scraper' / 'modules'
TESTS_DIR: Path = ROOT_DIR / 'scraper' / 'tests'

if not ensure_directory_exists(PDFS_DIR):
    logger.error(f"Erro ao criar diretório {PDFS_DIR}")
    exit(1)

# ========== Scraper - Parâmetros de Execução ==========

ZIP_NAME: str = get_env_variable('ZIP_NAME', "pdfs_compactados.zip")
FILTER: str = get_env_variable('FILTER', "ANEXO")
URL: str = get_env_variable(
    'URL',
    "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
)
