"""
Este arquivo contém as configurações para o diretório raiz, diretórios de arquivos,
e parâmetros de execução do programa.
"""

from pathlib import Path
from logger import logger
from dotenv import load_dotenv # type: ignore
from utils import get_env_variable, ensure_directory_exists
from log_config import LOG_DIR

# Carregando variáveis de ambiente
load_dotenv()

# DIRETÓRIOS

ROOT_DIR: Path = Path(__file__).resolve().parent
PDFS_DIR: Path = ROOT_DIR / 'pdfs'
MODULES_DIR: Path = ROOT_DIR / 'modules'
TESTS_DIR: Path = ROOT_DIR / 'tests'

# Garantir que os diretórios necessários existam
if not ensure_directory_exists(PDFS_DIR):
    logger.error(f"Erro ao criar diretório {PDFS_DIR}")
    exit(1)

# EXECUÇÕES

# Nome do arquivo ZIP
ZIP_NAME: str = get_env_variable('ZIP_NAME', "pdfs_compactados.zip")

# Filtro para busca de PDFs
FILTER: str = get_env_variable('FILTER', "ANEXO")

# Site para a busca
URL: str = get_env_variable('URL', "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos")
