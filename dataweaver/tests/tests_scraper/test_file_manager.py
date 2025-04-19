# test_file_manager.py
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import requests
from dataweaver.settings import logger

from dataweaver.scraper.modules import FileDownloader, FileSaver, FileManager


@pytest.fixture
def mock_folder(tmp_path):
    return tmp_path / "pdfs"


@pytest.fixture
def mock_file_content():
    return b"test file content"


@pytest.fixture
def mock_url():
    return "http://example.com/test.pdf"


@pytest.fixture
def mock_filename():
    return "test.pdf"


class TestFileDownloader:
    @patch("requests.get")
    def test_download_file_success(self, mock_get, mock_url, mock_file_content):
        # Configura o mock
        mock_response = MagicMock()
        mock_response.content = mock_file_content
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Testa
        downloader = FileDownloader()
        content = downloader.download_file(mock_url)

        # Verifica
        assert content == mock_file_content
        mock_get.assert_called_once_with(mock_url, stream=True)

    @patch("requests.get")
    def test_download_file_failure(self, mock_get, mock_url):
        # Configura o mock para levantar exceção
        mock_get.side_effect = requests.exceptions.HTTPError("404 Not Found")

        # Testa
        downloader = FileDownloader()

        with pytest.raises(requests.exceptions.HTTPError):
            downloader.download_file(mock_url)


class TestFileSaver:
    def test_save_file(self, mock_folder, mock_file_content, mock_filename):
        # Garante que a pasta existe
        mock_folder.mkdir(exist_ok=True)

        # Testa
        saver = FileSaver(mock_folder)
        file_path = saver.save_file(mock_filename, mock_file_content)

        # Verifica
        assert file_path.exists()
        assert file_path.read_bytes() == mock_file_content
        assert file_path.name == mock_filename

    def test_save_file_invalid_path(self, mock_filename, mock_file_content):
        with pytest.raises(FileNotFoundError):
            saver = FileSaver(Path("/invalid/path"))
            saver.save_file(mock_filename, mock_file_content)


class TestFileManager:
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
        # Configura mocks
        mock_downloader = MagicMock()
        mock_downloader.download_file.return_value = mock_file_content

        mock_saver = MagicMock()
        mock_saver.save_file.return_value = mock_folder / mock_filename

        # Testa
        manager = FileManager(mock_folder, downloader=mock_downloader, saver=mock_saver)
        manager.save_file(mock_url)

        # Verifica
        mock_downloader.download_file.assert_called_once_with(mock_url)
        mock_saver.save_file.assert_called_once_with(mock_filename, mock_file_content)
        mock_info.assert_called()
        mock_error.assert_not_called()

    @patch.object(logger, "error")
    def test_save_file_download_failure(self, mock_error, mock_folder, mock_url):
        # Configura mock para falhar no download
        mock_downloader = MagicMock()
        mock_downloader.download_file.side_effect = requests.exceptions.HTTPError(
            "404 Not Found"
        )

        # Testa
        manager = FileManager(mock_folder, downloader=mock_downloader)

        with pytest.raises(requests.exceptions.HTTPError):
            manager.save_file(mock_url)

        # Verifica se o erro foi logado
        mock_error.assert_called()

    @patch.object(logger, "error")
    def test_save_file_save_failure(
        self, mock_error, mock_folder, mock_url, mock_file_content
    ):
        # Configura mocks
        mock_downloader = MagicMock()
        mock_downloader.download_file.return_value = mock_file_content

        mock_saver = MagicMock()
        mock_saver.save_file.side_effect = IOError("Disk full")

        # Testa
        manager = FileManager(mock_folder, downloader=mock_downloader, saver=mock_saver)

        with pytest.raises(IOError):
            manager.save_file(mock_url)

        # Verifica se o erro foi logado
        mock_error.assert_called()

    def test_default_initialization(self, mock_folder):
        manager = FileManager(mock_folder)
        assert isinstance(manager.downloader, FileDownloader)
        assert isinstance(manager.saver, FileSaver)
        assert manager.saver.folder == mock_folder
