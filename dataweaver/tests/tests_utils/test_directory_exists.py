from dataweaver.utils import ensure_directory_exists

import pytest
from pathlib import Path
from tempfile import TemporaryDirectory


def test_ensure_directory_exists_creates_new_directory():
    """Garante que um novo diretório seja criado quando ele não existir."""
    with TemporaryDirectory() as tmp_dir:
        new_dir = Path(tmp_dir) / "new_dir"
        assert not new_dir.exists()

        result = ensure_directory_exists(new_dir)

        assert result is True
        assert new_dir.exists()
        assert new_dir.is_dir()


def test_ensure_directory_exists_handles_existing_directory():
    """Verifica que não há erro ao garantir a existência de um diretório já existente."""
    with TemporaryDirectory() as existing_dir:
        existing_path = Path(existing_dir)
        assert existing_path.exists()

        result = ensure_directory_exists(existing_path)

        assert result is True
        assert existing_path.exists()


def test_ensure_directory_exists_creates_nested_directories():
    """Testa a criação de diretórios aninhados que ainda não existem."""
    with TemporaryDirectory() as tmp_dir:
        nested_dir = Path(tmp_dir) / "dir1" / "dir2" / "dir3"
        assert not nested_dir.exists()

        result = ensure_directory_exists(nested_dir)

        assert result is True
        assert nested_dir.exists()
        assert nested_dir.is_dir()


def test_ensure_directory_exists_raises_error_when_creation_fails():
    """Garante que um erro seja levantado ao tentar criar um diretório com nome de arquivo existente."""
    with TemporaryDirectory() as tmp_dir:
        file_path = Path(tmp_dir) / "conflict"
        file_path.touch()
        assert file_path.exists()

        with pytest.raises(RuntimeError) as excinfo:
            ensure_directory_exists(file_path)

        assert "Erro na criação do diretório" in str(excinfo.value)
