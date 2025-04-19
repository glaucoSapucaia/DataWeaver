from dataweaver.config.paths import ROOT_DIR

import pytest
import os

# Configura o PYTHONPATH para o processo atual
os.environ["PYTHONPATH"] = str(ROOT_DIR)

# Executa o pytest diretamente (isso roda no mesmo processo)
pytest.main(["--cov=dataweaver.scraper", "--cov-report=html", "dataweaver/tests"])
