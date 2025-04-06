"""
Testes para o serviço de processamento de PDFs.

Este conjunto de testes cobre:
- Execução do fluxo completo com links válidos.
- Cenários onde não há PDFs.
- Exceções durante o download, compactação e remoção de arquivos.
"""

import pytest  # type: ignore
from unittest.mock import Mock, patch
from modules.pdf_processor import PDFProcessingService


# === FIXTURE DE SETUP PADRÃO ===

@pytest.fixture
def setup_service():
    mock_scraper = Mock()
    mock_file_manager = Mock()
    mock_zip_compressor = Mock()
    mock_pdf_remove = Mock()

    service = PDFProcessingService(
        zip_name="teste.zip",
        scraper=mock_scraper,
        file_manager=mock_file_manager,
        zip_compressor=mock_zip_compressor,
        pdf_remove=mock_pdf_remove
    )

    return service, mock_scraper, mock_file_manager, mock_zip_compressor, mock_pdf_remove


# === TESTES FUNCIONAIS ===

def test_process_executes_all_steps(setup_service):
    """
    Verifica se o processo completo é executado quando há links de PDFs.
    """
    service, scraper, file_manager, compressor, remove = setup_service
    scraper.get_pdf_links.return_value = ["http://site.com/a.pdf", "http://site.com/b.pdf"]

    service.process("http://site.com")

    assert scraper.get_pdf_links.called
    assert file_manager.save_file.call_count == 2
    assert compressor.create_zip.called
    assert remove.remove_pdfs.called


def test_process_handles_no_links(setup_service):
    """
    Verifica se o processo é encerrado corretamente quando nenhum link é retornado.
    """
    service, scraper, file_manager, compressor, remove = setup_service
    scraper.get_pdf_links.return_value = []

    service.process("http://site.com")

    assert scraper.get_pdf_links.called
    file_manager.save_file.assert_not_called()
    compressor.create_zip.assert_not_called()
    remove.remove_pdfs.assert_not_called()


# === TESTES DE EXCEÇÕES ===

def test_process_continues_if_file_download_fails(setup_service):
    """
    Verifica se o processo continua mesmo se o download de um arquivo falhar.
    """
    service, scraper, file_manager, compressor, remove = setup_service
    scraper.get_pdf_links.return_value = ["http://site.com/a.pdf", "http://site.com/b.pdf"]

    # Simula erro no primeiro download
    file_manager.save_file.side_effect = [Exception("Falha no download"), None]

    service.process("http://site.com")

    assert file_manager.save_file.call_count == 2
    assert compressor.create_zip.called
    assert remove.remove_pdfs.called


def test_process_logs_error_if_zip_creation_fails(setup_service):
    """
    Verifica se a exceção durante a compactação é capturada e logada.
    """
    service, scraper, _, compressor, _ = setup_service
    scraper.get_pdf_links.return_value = ["http://site.com/a.pdf"]
    compressor.create_zip.side_effect = Exception("Erro de zip")

    with patch("modules.pdf_processor.logger.error") as mock_log:
        service.process("http://site.com")
        assert mock_log.called
        assert "Erro durante o processamento" in mock_log.call_args[0][0]


def test_process_logs_error_if_pdf_removal_fails(setup_service):
    """
    Verifica se a exceção ao excluir PDFs é capturada e logada.
    """
    service, scraper, _, _, remove = setup_service
    scraper.get_pdf_links.return_value = ["http://site.com/a.pdf"]
    remove.remove_pdfs.side_effect = Exception("Erro ao remover")

    with patch("modules.pdf_processor.logger.error") as mock_log:
        service.process("http://site.com")
        assert mock_log.called
        assert "Erro durante o processamento" in mock_log.call_args[0][0]


def test_process_logs_error_if_scraper_fails(setup_service):
    """
    Verifica se erro no scraper é capturado e logado.
    """
    service, scraper, _, _, _ = setup_service
    scraper.get_pdf_links.side_effect = Exception("Falha no scraping")

    with patch("modules.pdf_processor.logger.error") as mock_log:
        service.process("http://site.com")
        assert mock_log.called
        assert "Erro durante o processamento" in mock_log.call_args[0][0]
