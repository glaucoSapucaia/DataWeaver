from dataweaver.scraper.modules.interfaces import (
    PDFScraperInterface,
    FileManagerInterface,
    ZipCompressorInterface,
)
from dataweaver.scraper.modules import PDFProcessingService

import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_components():
    """Fixture que retorna mocks de todos os componentes necessários"""
    return {
        "scraper": MagicMock(spec=PDFScraperInterface),
        "file_manager": MagicMock(spec=FileManagerInterface),
        "zip_compressor": MagicMock(spec=ZipCompressorInterface),
    }


def test_process_happy_path(mock_components):
    """Testa o fluxo completo bem-sucedido"""
    # Configura os mocks
    mock_components["scraper"].get_pdf_links.return_value = [
        "http://example.com/pdf1.pdf",
        "http://example.com/pdf2.pdf",
    ]

    # Cria o serviço com os mocks
    service = PDFProcessingService(
        zip_name="output.zip", file_extension="pdf", **mock_components
    )

    # Executa o processamento
    with patch("dataweaver.scraper.modules.pdf_processor.logger") as mock_logger:
        service.process("http://example.com")

    # Verificações
    mock_components["scraper"].get_pdf_links.assert_called_once_with(
        "http://example.com"
    )
    assert mock_components["file_manager"].save_file.call_count == 2
    mock_components["zip_compressor"].create_zip.assert_called_once_with(
        "output.zip", "pdf"
    )

    # Verifica logs
    assert mock_logger.info.call_count >= 3  # Início, download, compactação
    mock_logger.warning.assert_not_called()
    mock_logger.error.assert_not_called()


def test_process_no_pdfs_found(mock_components):
    """Testa quando nenhum PDF é encontrado"""
    mock_components["scraper"].get_pdf_links.return_value = []

    service = PDFProcessingService(
        zip_name="output", file_extension="pdf", **mock_components
    )

    with patch("dataweaver.scraper.modules.pdf_processor.logger") as mock_logger:
        service.process("http://example.com")

    mock_logger.warning.assert_called_once_with("Nenhum PDF encontrado na página.")
    mock_components["file_manager"].save_file.assert_not_called()
    mock_components["zip_compressor"].create_zip.assert_not_called()


def test_process_with_download_errors(mock_components):
    """Testa quando ocorrem erros no download de alguns PDFs"""
    mock_components["scraper"].get_pdf_links.return_value = [
        "http://example.com/good.pdf",
        "http://example.com/bad.pdf",
    ]

    # Configura o file_manager para falhar no segundo PDF
    mock_components["file_manager"].save_file.side_effect = [
        None,  # Primeiro chamado bem-sucedido
        Exception("Download failed"),  # Segundo chamado com erro
    ]

    service = PDFProcessingService(
        zip_name="output.zip", file_extension="pdf", **mock_components
    )

    with patch("dataweaver.scraper.modules.pdf_processor.logger") as mock_logger:
        service.process("http://example.com")

    # Verifica que continuou o fluxo apesar do erro
    assert mock_components["file_manager"].save_file.call_count == 2
    mock_components["zip_compressor"].create_zip.assert_called_once()

    # Verifica log de erro
    mock_logger.error.assert_called_once_with(
        "Falha no download: http://example.com/bad.pdf - Erro: Download failed"
    )


def test_process_critical_error(mock_components):
    """Testa quando ocorre um erro crítico na extração de links"""
    mock_components["scraper"].get_pdf_links.side_effect = Exception("Critical error")

    service = PDFProcessingService(
        zip_name="output", file_extension="pdf", **mock_components
    )

    with patch("dataweaver.scraper.modules.pdf_processor.logger") as mock_logger:
        with pytest.raises(Exception):
            service.process("http://example.com")

    mock_logger.critical.assert_called_once_with(
        "Falha crítica no processamento: Critical error"
    )


def test_process_with_zip_creation_error(mock_components):
    """Testa quando ocorre erro na criação do ZIP"""
    mock_components["scraper"].get_pdf_links.return_value = [
        "http://example.com/pdf1.pdf"
    ]
    mock_components["zip_compressor"].create_zip.side_effect = Exception(
        "Zip creation failed"
    )

    service = PDFProcessingService(
        zip_name="output.zip", file_extension="pdf", **mock_components
    )

    with patch("dataweaver.scraper.modules.pdf_processor.logger") as mock_logger:
        with pytest.raises(Exception):
            service.process("http://example.com")

    mock_logger.critical.assert_called_once_with(
        "Falha crítica no processamento: Zip creation failed"
    )
