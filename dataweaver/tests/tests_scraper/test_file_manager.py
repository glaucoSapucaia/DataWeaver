from dataweaver.settings import logger
from dataweaver.scraper.modules import FileDownloader, FileSaver, FileManager

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import requests


@pytest.fixture
def mock_folder(tmp_path):
    """Fixture que cria um diretório temporário para testes."""
    return tmp_path / "pdfs"


@pytest.fixture
def mock_file_content():
    """Retorna conteúdo binário simulado para testes de arquivo."""
    return b"test file content"


@pytest.fixture
def mock_url():
    """URL fictícia para testes de download."""
    return "http://example.com/test.pdf"


@pytest.fixture
def mock_filename():
    """Nome de arquivo fictício para testes."""
    return "test.pdf"


class TestFileDownloader:
    """Testes para a classe FileDownloader."""

    @patch("requests.get")
    def test_download_file_success(self, mock_get, mock_url, mock_file_content):
        """Testa download bem-sucedido de arquivo.

        Verifica:
            - Conteúdo retornado é igual ao mockado
            - requests.get foi chamado corretamente
            - raise_for_status foi chamado
        """
        # Configuração do mock
        mock_response = MagicMock()
        mock_response.content = mock_file_content
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        downloader = FileDownloader()
        content = downloader.download_file(mock_url)

        assert content == mock_file_content
        mock_get.assert_called_once_with(mock_url, stream=True)
        mock_response.raise_for_status.assert_called_once()

    @patch("requests.get")
    def test_download_file_failure(self, mock_get, mock_url):
        """Testa falha no download com HTTPError.

        Verifica:
            - Exceção é propagada corretamente
        """
        mock_get.side_effect = requests.exceptions.HTTPError("404 Not Found")

        downloader = FileDownloader()

        with pytest.raises(requests.exceptions.HTTPError):
            downloader.download_file(mock_url)


class TestFileSaver:
    """Testes para a classe FileSaver."""

    def test_save_file(self, mock_folder, mock_file_content, mock_filename):
        """Testa salvamento bem-sucedido de arquivo.

        Verifica:
            - Arquivo é criado no local correto
            - Conteúdo está intacto
            - Nome do arquivo é preservado
        """
        mock_folder.mkdir(exist_ok=True)

        saver = FileSaver(mock_folder)
        file_path = saver.save_file(mock_filename, mock_file_content)

        assert file_path.exists()
        assert file_path.read_bytes() == mock_file_content
        assert file_path.name == mock_filename

    def test_save_file_invalid_path(self, mock_filename, mock_file_content):
        """Testa tentativa de salvar em caminho inválido.

        Verifica:
            - FileNotFoundError é levantado
        """
        with pytest.raises(FileNotFoundError):
            saver = FileSaver(Path("/invalid/path"))
            saver.save_file(mock_filename, mock_file_content)


class TestFileManager:
    """Testes para a classe FileManager."""

    @patch.object(logger, "info")
    @patch.object(logger, "error")
    def test_save_file_success(
        self,
        mock_error,
        mock_info,
        mock_folder,
        mock_url,
        mock_filename,
        mock_file_content,
    ):
        """Testa fluxo completo bem-sucedido.

        Verifica:
            - Downloader e Saver são chamados corretamente
            - Log de sucesso é registrado
            - Nenhum erro é logado
        """
        mock_downloader = MagicMock()
        mock_downloader.download_file.return_value = mock_file_content

        mock_saver = MagicMock()
        mock_saver.save_file.return_value = mock_folder / mock_filename

        manager = FileManager(mock_folder, downloader=mock_downloader, saver=mock_saver)
        manager.save_file(mock_url)

        mock_downloader.download_file.assert_called_once_with(mock_url)
        mock_saver.save_file.assert_called_once_with(mock_filename, mock_file_content)
        mock_info.assert_called()
        mock_error.assert_not_called()

    @patch.object(logger, "error")
    def test_save_file_download_failure(self, mock_error, mock_folder, mock_url):
        """Testa falha durante o download.

        Verifica:
            - Exceção é propagada
            - Erro é logado corretamente
        """
        mock_downloader = MagicMock()
        mock_downloader.download_file.side_effect = requests.exceptions.HTTPError(
            "404 Not Found"
        )

        manager = FileManager(mock_folder, downloader=mock_downloader)

        with pytest.raises(requests.exceptions.HTTPError):
            manager.save_file(mock_url)

        assert mock_error.call_count == 1

    @patch.object(logger, "error")
    def test_save_file_save_failure(
        self, mock_error, mock_folder, mock_url, mock_file_content
    ):
        """Testa falha durante o salvamento.

        Verifica:
            - Exceção é propagada
            - Erro é logado corretamente
        """
        mock_downloader = MagicMock()
        mock_downloader.download_file.return_value = mock_file_content

        mock_saver = MagicMock()
        mock_saver.save_file.side_effect = IOError("Disk full")

        manager = FileManager(mock_folder, downloader=mock_downloader, saver=mock_saver)

        with pytest.raises(IOError):
            manager.save_file(mock_url)

        assert mock_error.call_count == 1

    def test_default_initialization(self, mock_folder):
        """Testa inicialização com dependências padrão.

        Verifica:
            - Downloader padrão é criado
            - Saver padrão é criado
            - Folder é repassado corretamente
        """
        manager = FileManager(mock_folder)
        assert isinstance(manager.downloader, FileDownloader)
        assert isinstance(manager.saver, FileSaver)
        assert manager.saver.folder == mock_folder
