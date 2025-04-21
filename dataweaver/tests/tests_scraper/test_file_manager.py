from dataweaver.scraper.modules import FileDownloader, FileSaver, FileManager

import pytest
from unittest.mock import Mock, patch, MagicMock
from requests.exceptions import HTTPError


# Testes para FileDownloader
def test_file_downloader_success():
    """Testa download bem-sucedido"""
    mock_response = MagicMock()
    mock_response.content = b"file content"
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response) as mock_get:
        downloader = FileDownloader()
        content = downloader.download_file("http://example.com/file.pdf")

        assert content == b"file content"
        mock_get.assert_called_once_with("http://example.com/file.pdf", stream=True)


def test_file_downloader_http_error():
    """Testa tratamento de erro HTTP"""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError("404 Not Found")

    with patch("requests.get", return_value=mock_response):
        downloader = FileDownloader()

        with pytest.raises(HTTPError):
            downloader.download_file("http://example.com/missing.pdf")


# Testes para FileSaver
def test_file_saver_success(tmp_path):
    """Testa salvamento bem-sucedido"""
    saver = FileSaver(tmp_path)
    test_content = b"test content"

    saved_path = saver.save_file("test.txt", test_content)

    assert saved_path == tmp_path / "test.txt"
    assert saved_path.read_bytes() == test_content


def test_file_saver_invalid_filename(tmp_path):
    """Testa tratamento de nome de arquivo inválido"""
    saver = FileSaver(tmp_path)

    with pytest.raises(OSError):
        saver.save_file("", b"content")  # Nome vazio
    with pytest.raises(OSError):
        saver.save_file("/invalid/name", b"content")  # Caminho absoluto


# Testes para FileManager
def test_file_manager_default_dependencies(tmp_path):
    """Testa injeção de dependências padrão"""
    manager = FileManager(tmp_path)

    assert isinstance(manager.downloader, FileDownloader)
    assert isinstance(manager.saver, FileSaver)
    assert manager.saver.folder == tmp_path


def test_file_manager_custom_dependencies(tmp_path):
    """Testa injeção de dependências customizadas"""
    mock_downloader = Mock()
    mock_saver = Mock()

    manager = FileManager(tmp_path, downloader=mock_downloader, saver=mock_saver)

    assert manager.downloader == mock_downloader
    assert manager.saver == mock_saver


def test_file_manager_save_file_success(tmp_path):
    """Testa fluxo completo bem-sucedido"""
    mock_downloader = Mock()
    mock_downloader.download_file.return_value = b"content"

    mock_saver = Mock()
    mock_saver.save_file.return_value = tmp_path / "file.pdf"

    with patch("os.path.basename", return_value="file.pdf"):
        manager = FileManager(tmp_path, mock_downloader, mock_saver)
        manager.save_file("http://example.com/file.pdf")

        mock_downloader.download_file.assert_called_once_with(
            "http://example.com/file.pdf"
        )
        mock_saver.save_file.assert_called_once_with("file.pdf", b"content")
