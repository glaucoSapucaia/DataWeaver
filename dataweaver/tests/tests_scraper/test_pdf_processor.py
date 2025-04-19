import pytest
from unittest.mock import MagicMock, patch
from dataweaver.settings import logger
from dataweaver.scraper.modules import PDFProcessingService
from dataweaver.scraper.modules.interfaces import (
    PDFProcessingServiceInterface,
    PDFScraperInterface,
    FileManagerInterface,
    ZipCompressorInterface,
    PDFRemoveInterface,
)


@pytest.fixture
def mock_dependencies():
    """Retorna mocks de todas as dependências do serviço"""
    return {
        "scraper": MagicMock(spec=PDFScraperInterface),
        "file_manager": MagicMock(spec=FileManagerInterface),
        "zip_compressor": MagicMock(spec=ZipCompressorInterface),
        "pdf_remove": MagicMock(spec=PDFRemoveInterface),
    }


@pytest.fixture
def processing_service(mock_dependencies):
    """Instância do serviço com dependências mockadas"""
    return PDFProcessingService(
        zip_name="test.zip",
        scraper=mock_dependencies["scraper"],
        file_manager=mock_dependencies["file_manager"],
        zip_compressor=mock_dependencies["zip_compressor"],
        pdf_remove=mock_dependencies["pdf_remove"],
    )


class TestPDFProcessingService:
    def test_initialization(self, processing_service, mock_dependencies):
        """Testa se o serviço é inicializado corretamente"""
        assert isinstance(processing_service, PDFProcessingServiceInterface)
        assert processing_service.zip_name == "test.zip"
        assert processing_service.scraper == mock_dependencies["scraper"]
        assert processing_service.file_manager == mock_dependencies["file_manager"]
        assert processing_service.zip_compressor == mock_dependencies["zip_compressor"]
        assert processing_service.pdf_remove == mock_dependencies["pdf_remove"]

    @patch.object(logger, "info")
    @patch.object(logger, "warning")
    def test_process_no_pdfs_found(
        self, mock_warning, mock_info, processing_service, mock_dependencies
    ):
        """Testa o fluxo quando nenhum PDF é encontrado"""
        mock_dependencies["scraper"].get_pdf_links.return_value = []

        processing_service.process("http://example.com")

        mock_dependencies["scraper"].get_pdf_links.assert_called_once_with(
            "http://example.com"
        )
        mock_warning.assert_called_with("Nenhum PDF encontrado.")
        mock_dependencies["file_manager"].save_file.assert_not_called()
        mock_info.assert_any_call("Buscando PDFs...")

    @patch.object(logger, "info")
    @patch.object(logger, "error")
    def test_process_success_flow(
        self, mock_error, mock_info, processing_service, mock_dependencies
    ):
        """Testa o fluxo completo bem-sucedido"""
        pdf_links = ["http://example.com/1.pdf", "http://example.com/2.pdf"]
        mock_dependencies["scraper"].get_pdf_links.return_value = pdf_links

        processing_service.process("http://example.com")

        # Verifica o fluxo principal
        mock_dependencies["scraper"].get_pdf_links.assert_called_once_with(
            "http://example.com"
        )
        assert mock_dependencies["file_manager"].save_file.call_count == len(pdf_links)
        mock_dependencies["zip_compressor"].create_zip.assert_called_once_with(
            "test.zip"
        )
        mock_dependencies["pdf_remove"].remove_pdfs.assert_called_once()

        # Verifica os logs
        mock_info.assert_any_call("Buscando PDFs...")
        mock_info.assert_any_call("Baixando PDFs...")
        mock_info.assert_any_call("Compactando arquivos...")
        mock_info.assert_any_call("Excluindo arquivos baixados...")
        mock_error.assert_not_called()

    @patch.object(logger, "error")
    def test_process_download_error(
        self, mock_error, processing_service, mock_dependencies
    ):
        """Testa quando ocorre erro no download de um PDF"""
        pdf_links = ["http://example.com/1.pdf", "http://example.com/2.pdf"]
        mock_dependencies["scraper"].get_pdf_links.return_value = pdf_links
        mock_dependencies["file_manager"].save_file.side_effect = [
            None,
            Exception("Download failed"),
        ]

        processing_service.process("http://example.com")

        # Verifica que continuou o fluxo apesar do erro
        mock_dependencies["zip_compressor"].create_zip.assert_called_once()
        mock_dependencies["pdf_remove"].remove_pdfs.assert_called_once()
        mock_error.assert_called_with(
            "Erro ao baixar o arquivo http://example.com/2.pdf: Download failed"
        )

    @patch.object(logger, "error")
    def test_process_scraper_error(
        self, mock_error, processing_service, mock_dependencies
    ):
        """Testa quando ocorre erro na fase de scraping"""
        mock_dependencies["scraper"].get_pdf_links.side_effect = Exception(
            "Scraping failed"
        )

        processing_service.process("http://example.com")

        # Verifica que o fluxo foi interrompido
        mock_dependencies["file_manager"].save_file.assert_not_called()
        mock_dependencies["zip_compressor"].create_zip.assert_not_called()
        mock_dependencies["pdf_remove"].remove_pdfs.assert_not_called()
        mock_error.assert_called_with(
            "Erro durante o processamento dos PDFs: Scraping failed"
        )

    @patch.object(logger, "error")
    def test_process_zip_error(self, mock_error, processing_service, mock_dependencies):
        """Testa quando ocorre erro na compactação"""
        pdf_links = ["http://example.com/1.pdf"]
        mock_dependencies["scraper"].get_pdf_links.return_value = pdf_links
        mock_dependencies["zip_compressor"].create_zip.side_effect = Exception(
            "Zip failed"
        )

        processing_service.process("http://example.com")

        # Verifica que remove_pdfs não foi chamado
        mock_dependencies["pdf_remove"].remove_pdfs.assert_not_called()
        mock_error.assert_called_with(
            "Erro durante o processamento dos PDFs: Zip failed"
        )
