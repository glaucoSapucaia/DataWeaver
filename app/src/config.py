"""
Este arquivo contém as configurações para o diretório raiz, diretórios de arquivos,
e parâmetros de execução do programa.
"""

from pathlib import Path

# DIRETÓRIOS

ROOT_DIR: Path = Path(__file__).resolve().parent
PDFS_DIR: Path = ROOT_DIR / 'pdfs'
MODULES_DIR: Path = ROOT_DIR / 'modules'
TESTS_DIR: Path = ROOT_DIR / 'tests'
ZIP_FILE: Path = PDFS_DIR / 'pdfs_compactados.zip'

# EXECUÇÕES

# Garantir que os diretórios necessários existam
PDFS_DIR.mkdir(parents=True, exist_ok=True)
if not PDFS_DIR.exists():
    print(f"Erro: O diretório {PDFS_DIR} não pôde ser criado.")
    exit(1)

# Nome do arquivo ZIP
ZIP_NAME: str = "pdfs_compactados.zip"

# Filtro para busca de PDFs
FILTER: str = "ANEXO"

# Site para a busca
URL: str = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
