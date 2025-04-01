from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

PDFS_DIR = ROOT_DIR / 'pdfs'
MODULES_DIR = ROOT_DIR / 'modules'
TESTS_DIR = ROOT_DIR / 'tests'

ZIP_FILE = PDFS_DIR / 'pdfs_compactados.zip'

# Garantir que os diretórios necessários existam
PDFS_DIR.mkdir(parents=True, exist_ok=True)
