"""
Testes para o módulo FileManager.

Cobre:
- Sucesso no download.
- Erros de conexão.
- Falhas no salvamento.
- Verificação de logs.
"""

from pathlib import Path
import sys

# Caminho para importar o módulo
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from requests.exceptions import RequestException  # type: ignore
import pytest                                     # type: ignore
from unittest.mock import patch, mock_open, MagicMock
from modules.file_manager import FileManager


@pytest.fixture
def setup_file_manager(tmp_path):
    folder = tmp_path
    return FileManager(folder), folder


def test_save_file_success(setup_file_manager):
    """
    Verifica se o arquivo é salvo corretamente quando o download é bem-sucedido.
    """

    file_manager, folder = setup_file_manager
    fake_url = "http://example.com/test.pdf"
    expected_path = folder / "test.pdf"

    mock_response = MagicMock()
    mock_response.iter_content.return_value = [b"chunk1", b"chunk2"]
    mock_response.raise_for_status.return_value = None

    with patch("modules.file_manager.requests.get", return_value=mock_response) as mock_get, \
         patch("builtins.open", mock_open()) as mock_file, \
         patch("modules.file_manager.logger.info") as mock_log:

        file_manager.save_file(fake_url)

        mock_get.assert_called_once_with(fake_url, stream=True)
        mock_file.assert_called_once_with(str(expected_path), 'wb')
        handle = mock_file()
        handle.write.assert_any_call(b"chunk1")
        handle.write.assert_any_call(b"chunk2")
        mock_log.assert_called_once()
        assert "Arquivo baixado com sucesso" in mock_log.call_args[0][0]


def test_save_file_request_exception(setup_file_manager):
    """
    Verifica se exceções do requests são tratadas e logadas.
    """

    file_manager, _ = setup_file_manager
    fake_url = "http://example.com/fail.pdf"

    with patch("modules.file_manager.requests.get", side_effect=RequestException("Erro de rede")), \
         patch("modules.file_manager.logger.error") as mock_log:

        file_manager.save_file(fake_url)
        assert mock_log.called
        assert "Erro ao baixar o arquivo" in mock_log.call_args[0][0]


def test_save_file_raise_for_status(setup_file_manager):
    """
    Verifica se raise_for_status gera log de erro.
    """

    file_manager, _ = setup_file_manager
    fake_url = "http://example.com/error.pdf"

    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = RequestException("Erro HTTP")

    with patch("modules.file_manager.requests.get", return_value=mock_response), \
         patch("modules.file_manager.logger.error") as mock_log:

        file_manager.save_file(fake_url)
        assert mock_log.called
        assert "Erro ao baixar o arquivo" in mock_log.call_args[0][0]


def test_save_file_write_error(setup_file_manager):
    """
    Verifica se exceções ao escrever no disco são tratadas e logadas.
    """

    file_manager, _ = setup_file_manager
    fake_url = "http://example.com/file.pdf"

    mock_response = MagicMock()
    mock_response.iter_content.return_value = [b"chunk"]
    mock_response.raise_for_status.return_value = None

    with patch("modules.file_manager.requests.get", return_value=mock_response), \
         patch("builtins.open", side_effect=OSError("Falha ao escrever")), \
         patch("modules.file_manager.logger.error") as mock_log:

        file_manager.save_file(fake_url)
        assert mock_log.called
        assert "Erro ao salvar o arquivo" in mock_log.call_args[0][0]
