"""
Configurações principais da aplicação.

Este módulo define os diretórios utilizados no projeto, carrega variáveis de ambiente
usadas durante a execução e garante a existência das pastas essenciais.
"""

from dataweaver.scraper.utils import get_env_variable, ensure_directory_exists
from dotenv import load_dotenv  # type: ignore
from pathlib import Path

load_dotenv()

# ========== Scraper Diretórios ==========

ROOT_DIR: Path = Path(__file__).resolve().parent.parent.parent
PDFS_DIR: Path = ROOT_DIR / "dataweaver" / "scraper" / "pdfs"
MODULES_DIR: Path = ROOT_DIR / "dataweaver" / "scraper" / "modules"
TESTS_DIR: Path = ROOT_DIR / "dataweaver" / "scraper" / "tests"

PDFS_DIR.mkdir(parents=True, exist_ok=True)

if not PDFS_DIR.exists() and not PDFS_DIR.is_dir():
    raise RuntimeError(f"Erro ao criar diretório {PDFS_DIR}")

# ========== Scraper - Parâmetros de Execução ==========

ZIP_NAME: str = get_env_variable("ZIP_NAME", "pdfs_compactados.zip")
FILTER: str = get_env_variable("FILTER", "ANEXO")
URL: str = get_env_variable(
    "URL",
    "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos",
)

# ========== Data - Diretórios ==========

PDF_ZIP_FILE = ROOT_DIR / "scraper" / "pdfs" / "pdfs_compactados.zip"
DESTINATION_FOLDER = ROOT_DIR / "data" / "files"

# ========== Diretórios e arquivos de log ==========

LOG_DIR = ROOT_DIR / "dataweaver" / "logs"
LOG_FILE = LOG_DIR / "app.log"
ERROR_LOG_FILE = LOG_DIR / "error.log"
WARNING_LOG_FILE = LOG_DIR / "warning.log"

LOG_DIR.mkdir(parents=True, exist_ok=True)
