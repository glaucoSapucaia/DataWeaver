import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
import zipfile
import tempfile
from dataweaver.settings import logger
from dataweaver.scraper.modules import (
    ZipCompressor,
    PDFRemove,
    ZipCompressorDecorator,
    LoggingZipCompressor,
    ValidationZipCompressor,
)


@pytest.fixture
def tmp_folder(tmp_path):
    # Cria alguns arquivos PDF de teste
    (tmp_path / "file1.pdf").touch()
    (tmp_path / "file2.pdf").touch()
    (tmp_path / "subfolder").mkdir()
    (tmp_path / "subfolder" / "file3.pdf").touch()
    (tmp_path / "not_a_pdf.txt").touch()
    return tmp_path


@pytest.fixture
def empty_folder(tmp_path):
    return tmp_path


@pytest.fixture
def invalid_folder():
    return Path("/invalid/path")


class TestZipCompressor:
    def test_initialization(self, tmp_folder):
        compressor = ZipCompressor(tmp_folder)
        assert compressor.folder == tmp_folder

    @patch.object(logger, "info")
    @patch.object(logger, "error")
    def test_create_zip_success(self, mock_error, mock_info, tmp_folder):
        compressor = ZipCompressor(tmp_folder)
        zip_name = "test.zip"

        compressor.create_zip(zip_name)

        zip_path = tmp_folder / zip_name
        assert zip_path.exists()

        # Verifica se os PDFs foram adicionados
        with zipfile.ZipFile(zip_path, "r") as zipf:
            assert "file1.pdf" in zipf.namelist()
            assert "subfolder/file3.pdf" in zipf.namelist()

        mock_info.assert_any_call(f"Compactado: {zip_name}")
        mock_error.assert_not_called()

    @patch.object(logger, "error")
    def test_create_zip_invalid_folder(self, mock_error, invalid_folder):
        compressor = ZipCompressor(invalid_folder)

        with pytest.raises(Exception):
            compressor.create_zip("test.zip")

        mock_error.assert_called()

    @patch.object(logger, "warning")
    def test_create_zip_with_partial_errors(
        self, mock_warning, tmp_folder, monkeypatch
    ):
        # Força erro ao adicionar um arquivo específico
        def mock_write(self, file_path, arcname):
            if "file2.pdf" in str(file_path):
                raise Exception("Mocked error")
            return MagicMock()

        monkeypatch.setattr(zipfile.ZipFile, "write", mock_write)

        compressor = ZipCompressor(tmp_folder)
        compressor.create_zip("partial.zip")

        mock_warning.assert_called()
        assert (tmp_folder / "partial.zip").exists()

    def test_get_pdf_files(self, tmp_folder):
        compressor = ZipCompressor(tmp_folder)
        pdf_files = compressor._get_pdf_files()

        # Converte para strings e normaliza os separadores de caminho
        pdf_paths = [
            str(p.relative_to(tmp_folder)).replace("\\", "/") for p in pdf_files
        ]

        assert len(pdf_files) == 3
        assert "file1.pdf" in pdf_paths
        assert "file2.pdf" in pdf_paths
        assert "subfolder/file3.pdf" in pdf_paths

    def test_get_pdf_files_empty(self, empty_folder):
        compressor = ZipCompressor(empty_folder)
        assert len(compressor._get_pdf_files()) == 0

    def test_get_pdf_files_error(self, invalid_folder):
        compressor = ZipCompressor(invalid_folder)
        assert len(compressor._get_pdf_files()) == 0


class TestPDFRemove:
    @patch.object(logger, "info")
    @patch.object(logger, "error")
    def test_remove_pdfs_success(self, mock_error, mock_info, tmp_folder):
        remover = PDFRemove(tmp_folder)

        # Verifica que os PDFs existem antes
        assert (tmp_folder / "file1.pdf").exists()

        remover.remove_pdfs()

        # Verifica que foram removidos
        assert not (tmp_folder / "file1.pdf").exists()
        assert not (tmp_folder / "subfolder" / "file3.pdf").exists()
        # Arquivo não PDF deve permanecer
        assert (tmp_folder / "not_a_pdf.txt").exists()

        mock_info.assert_any_call("Arquivo excluído: file1.pdf")
        mock_error.assert_not_called()

    @patch.object(logger, "warning")
    def test_remove_pdfs_partial_failure(self, mock_warning, tmp_folder, monkeypatch):
        # Cria arquivos de teste
        file1 = tmp_folder / "file1.pdf"
        file2 = tmp_folder / "file2.pdf"
        file1.touch()
        file2.touch()

        # Força erro ao remover um arquivo específico
        original_unlink = Path.unlink

        def mock_unlink(self):
            if self == file2:
                raise Exception("Mocked error")
            return original_unlink(self)  # Executa a remoção real para outros arquivos

        monkeypatch.setattr(Path, "unlink", mock_unlink)

        remover = PDFRemove(tmp_folder)
        remover.remove_pdfs()

        # Verificações
        mock_warning.assert_called()
        assert not file1.exists(), "file1.pdf deveria ter sido removido"
        assert file2.exists(), "file2.pdf deveria permanecer devido ao erro"

    @patch.object(logger, "error")
    def test_remove_pdfs_folder_error(self, mock_error, monkeypatch):
        # Mock para simular erro ao listar arquivos
        def mock_rglob(self, pattern):
            raise Exception("Erro simulado ao listar arquivos")

        monkeypatch.setattr(Path, "rglob", mock_rglob)

        # Usa um diretório temporário válido, mas o mock causará erro
        with tempfile.TemporaryDirectory() as temp_dir:
            remover = PDFRemove(Path(temp_dir))
            with pytest.raises(Exception):
                remover.remove_pdfs()

        mock_error.assert_called_once()
        assert "Erro ao buscar arquivos PDF" in mock_error.call_args[0][0]


class TestZipCompressorDecorators:
    def test_base_decorator(self):
        mock_compressor = MagicMock()
        decorator = ZipCompressorDecorator(mock_compressor)
        decorator.create_zip("test.zip")
        mock_compressor.create_zip.assert_called_once_with("test.zip")

    @patch.object(logger, "info")
    def test_logging_decorator(self, mock_info):
        mock_compressor = MagicMock()
        decorator = LoggingZipCompressor(mock_compressor)
        decorator.create_zip("test.zip")

        mock_info.assert_any_call("Iniciando compressão: test.zip")
        mock_info.assert_any_call("Compressão concluída: test.zip")
        mock_compressor.create_zip.assert_called_once_with("test.zip")

    def test_validation_decorator_success(self):
        mock_compressor = MagicMock()
        decorator = ValidationZipCompressor(mock_compressor)
        decorator.create_zip("valid.zip")
        mock_compressor.create_zip.assert_called_once_with("valid.zip")

    def test_validation_decorator_failure(self):
        mock_compressor = MagicMock()
        decorator = ValidationZipCompressor(mock_compressor)

        with pytest.raises(ValueError, match="Nome do arquivo ZIP inválido"):
            decorator.create_zip("invalid_file")

        mock_compressor.create_zip.assert_not_called()
