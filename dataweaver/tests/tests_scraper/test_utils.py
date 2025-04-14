"""
Testes unitários para funções utilitárias do projeto.

Este módulo testa:
- ensure_directory_exists (criação e verificação de diretórios)
- get_env_variable (leitura segura de variáveis de ambiente)
"""

import shutil
from pathlib import Path
from tempfile import mkdtemp

from dataweaver.scraper.utils.directory_exists import ensure_directory_exists
from dataweaver.scraper.utils.get_env import get_env_variable

# ────────────────────────────────────────────────────────────────
# TESTES PARA A FUNÇÃO: ensure_directory_exists
# ────────────────────────────────────────────────────────────────

def test_ensure_directory_exists_creates_new_directory():
    """
    Verifica se um diretório inexistente é criado corretamente.
    """
    temp_dir = Path(mkdtemp()) / "novo_diretorio"
    assert not temp_dir.exists()

    resultado = ensure_directory_exists(temp_dir)

    assert resultado is True
    assert temp_dir.exists()
    assert temp_dir.is_dir()

    # limpeza
    shutil.rmtree(temp_dir.parent)


def test_ensure_directory_exists_existing_directory():
    """
    Verifica se a função retorna True ao receber um diretório já existente.
    """
    temp_dir = Path(mkdtemp())
    resultado = ensure_directory_exists(temp_dir)

    assert resultado is True
    assert temp_dir.exists()

    # limpeza
    shutil.rmtree(temp_dir)


def test_ensure_directory_exists_fails_with_invalid_path(monkeypatch):
    """
    Verifica se a função retorna False ao falhar na criação de um diretório.
    """
    import dataweaver.scraper.utils

    # simula erro no mkdir
    def raise_exception(*args, **kwargs):
        raise PermissionError("Acesso negado")

    monkeypatch.setattr("pathlib.Path.mkdir", raise_exception)

    path = Path("/caminho/qualquer")
    resultado = dataweaver.scraper.utils.ensure_directory_exists(path)

    assert resultado is False

# ────────────────────────────────────────────────────────────────
# TESTES PARA A FUNÇÃO: get_env_variable
# ────────────────────────────────────────────────────────────────

def test_get_env_variable_returns_env_value(monkeypatch):
    """
    Verifica se a função retorna o valor real da variável de ambiente.
    """
    monkeypatch.setenv("MY_ENV_VAR", "valor_real")
    resultado = get_env_variable("MY_ENV_VAR", "valor_padrao")
    assert resultado == "valor_real"


def test_get_env_variable_returns_default_when_not_set(monkeypatch):
    """
    Verifica se retorna o valor padrão quando a variável não está definida.
    """
    monkeypatch.delenv("VAR_INEXISTENTE", raising=False)
    resultado = get_env_variable("VAR_INEXISTENTE", "valor_padrao")
    assert resultado == "valor_padrao"


def test_get_env_variable_returns_default_when_empty(monkeypatch):
    """
    Verifica se retorna o valor padrão quando a variável está definida como string vazia.
    """
    monkeypatch.setenv("VAR_VAZIA", "")
    resultado = get_env_variable("VAR_VAZIA", "valor_padrao")
    assert resultado == "valor_padrao"


def test_get_env_variable_strips_value(monkeypatch):
    """
    Verifica se espaços em volta da variável são removidos.
    """
    monkeypatch.setenv("VAR_COM_ESPACOS", "   valor_com_espacos   ")
    resultado = get_env_variable("VAR_COM_ESPACOS", "valor_padrao")
    assert resultado == "valor_com_espacos"


def test_get_env_variable_returns_default_when_only_spaces(monkeypatch):
    """
    Verifica se retorna o valor padrão quando a variável contém apenas espaços.
    """
    monkeypatch.setenv("VAR_SO_ESPACOS", "     ")
    resultado = get_env_variable("VAR_SO_ESPACOS", "valor_padrao")
    assert resultado == "valor_padrao"
