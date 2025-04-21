from dataweaver.settings import config

import pytest
import os

base_dir = config.dirs.root

# Configura o PYTHONPATH para o processo atual
os.environ["PYTHONPATH"] = str(base_dir)

# Executa o pytest diretamente (isso roda no mesmo processo)
pytest.main(["--cov=dataweaver", "--cov-report=html", "dataweaver/tests"])
