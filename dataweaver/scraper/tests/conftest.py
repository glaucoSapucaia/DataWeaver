from pathlib import Path
import sys

# Adiciona o diretório pai de 'tests' ao sys.path, ou seja: o diretório 'scraper'
sys.path.append(str(Path(__file__).resolve().parent.parent))