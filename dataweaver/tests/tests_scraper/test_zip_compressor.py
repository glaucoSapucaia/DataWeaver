from dataweaver.scraper.modules import (
    ZipCompressor,
    ValidationZipCompressor,
)

import pytest
from unittest.mock import Mock


# Testes para ZipCompressor
def test_zip_compressor_creation(tmp_path):
    """Testa inicialização correta"""
    compressor = ZipCompressor(tmp_path)
    assert compressor.folder == tmp_path


def test_get_zip_path(tmp_path):
    """Testa geração do caminho do ZIP"""
    compressor = ZipCompressor(tmp_path)
    zip_path = compressor._get_zip_path("teste")
    assert zip_path == tmp_path / "teste"


def test_get_files_by_extension(tmp_path):
    """Testa listagem de arquivos por extensão"""
    # Cria arquivos de teste
    (tmp_path / "file1.pdf").touch()
    (tmp_path / "file2.pdf").touch()
    (tmp_path / "ignore.txt").touch()

    compressor = ZipCompressor(tmp_path)
    files = compressor._get_files_by_extension("pdf")

    assert len(files) == 2
    assert all(f.suffix == ".pdf" for f in files)


# Testes para ValidationZipCompressor
def test_validation_decorator_failure():
    """Testa validação com nome inválido"""
    mock_compressor = Mock()
    decorator = ValidationZipCompressor(mock_compressor)

    with pytest.raises(ValueError, match="deve terminar com .zip"):
        decorator.create_zip("invalid", "pdf")

    mock_compressor.create_zip.assert_not_called()
