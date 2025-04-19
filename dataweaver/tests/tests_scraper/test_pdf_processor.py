from dataweaver.settings import logger
from dataweaver.scraper.modules import PDFProcessingService
from dataweaver.scraper.modules.interfaces import (
    PDFProcessingServiceInterface,
    PDFScraperInterface,
    FileManagerInterface,
    ZipCompressorInterface,
    PDFRemoveInterface,
)

import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_dependencies():
    """Fixture que retorna mocks de todas as dependências do serviço.

    Returns:
        dict: Dicionário com mocks das dependências:
            - scraper: Mock de PDFScraperInterface
            - file_manager: Mock de FileManagerInterface
            - zip_compressor: Mock de ZipCompressorInterface
            - pdf_remove: Mock de PDFRemoveInterface
    """
    return {
        "scraper": MagicMock(spec=PDFScraperInterface),
        "file_manager": MagicMock(spec=FileManagerInterface),
        "zip_compressor": MagicMock(spec=ZipCompressorInterface),
        "pdf_remove": MagicMock(spec=PDFRemoveInterface),
    }


@pytest.fixture
def processing_service(mock_dependencies):
    """Fixture que retorna uma instância do serviço com dependências mockadas.

    Args:
        mock_dependencies: Fixture com mocks das dependências

    Returns:
        PDFProcessingService: Instância configurada para testes
    """
    return PDFProcessingService(
        zip_name="test.zip",
        scraper=mock_dependencies["scraper"],
        file_manager=mock_dependencies["file_manager"],
        zip_compressor=mock_dependencies["zip_compressor"],
        pdf_remove=mock_dependencies["pdf_remove"],
    )


class TestPDFProcessingService:
    """Testes para a classe PDFProcessingService."""

    def test_initialization(self, processing_service, mock_dependencies):
        """Testa a inicialização correta do serviço.

        Verifica:
            - Implementa a interface correta
            - Armazena o nome do ZIP corretamente
            - Recebe e armazena todas as dependências
        """
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
        """Testa o fluxo quando nenhum PDF é encontrado.

        Verifica:
            - Chama o scraper corretamente
            - Loga mensagem de aviso
            - Não chama as etapas seguintes
            - Loga etapas do processo
        """
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
        """Testa o fluxo completo bem-sucedido.

        Verifica:
            - Executa todas as etapas na ordem correta
            - Passa os parâmetros corretos
            - Loga cada etapa do processo
            - Não loga erros
        """
        pdf_links = ["http://example.com/1.pdf", "http://example.com/2.pdf"]
        mock_dependencies["scraper"].get_pdf_links.return_value = pdf_links

        processing_service.process("http://example.com")

        # Verifica ordem e chamadas
        mock_dependencies["scraper"].get_pdf_links.assert_called_once()
        assert mock_dependencies["file_manager"].save_file.call_count == len(pdf_links)
        mock_dependencies["zip_compressor"].create_zip.assert_called_once_with(
            "test.zip"
        )
        mock_dependencies["pdf_remove"].remove_pdfs.assert_called_once()

        # Verifica logs
        expected_logs = [
            "Buscando PDFs...",
            "Baixando PDFs...",
            "Compactando arquivos...",
            "Excluindo arquivos baixados...",
        ]
        for log in expected_logs:
            mock_info.assert_any_call(log)
        mock_error.assert_not_called()

    @patch.object(logger, "error")
    def test_process_download_error(
        self, mock_error, processing_service, mock_dependencies
    ):
        """Testa comportamento quando ocorre erro no download.

        Verifica:
            - Continua o fluxo mesmo com erro em um arquivo
            - Loga o erro específico
            - Completa as etapas seguintes
        """
        pdf_links = ["http://example.com/1.pdf", "http://example.com/2.pdf"]
        mock_dependencies["scraper"].get_pdf_links.return_value = pdf_links
        mock_dependencies["file_manager"].save_file.side_effect = [
            None,
            Exception("Download failed"),
        ]

        processing_service.process("http://example.com")

        mock_error.assert_called_with(
            "Erro ao baixar o arquivo http://example.com/2.pdf: Download failed"
        )
        mock_dependencies["zip_compressor"].create_zip.assert_called_once()
        mock_dependencies["pdf_remove"].remove_pdfs.assert_called_once()

    @patch.object(logger, "error")
    def test_process_scraper_error(
        self, mock_error, processing_service, mock_dependencies
    ):
        """Testa comportamento quando ocorre erro no scraping.

        Verifica:
            - Interrompe o fluxo imediatamente
            - Loga o erro corretamente
            - Não chama as etapas seguintes
        """
        mock_dependencies["scraper"].get_pdf_links.side_effect = Exception(
            "Scraping failed"
        )

        processing_service.process("http://example.com")

        mock_error.assert_called_with(
            "Erro durante o processamento dos PDFs: Scraping failed"
        )
        mock_dependencies["file_manager"].save_file.assert_not_called()
        mock_dependencies["zip_compressor"].create_zip.assert_not_called()
        mock_dependencies["pdf_remove"].remove_pdfs.assert_not_called()

    @patch.object(logger, "error")
    def test_process_zip_error(self, mock_error, processing_service, mock_dependencies):
        """Testa comportamento quando ocorre erro na compactação.

        Verifica:
            - Não executa a limpeza dos arquivos
            - Loga o erro corretamente
        """
        pdf_links = ["http://example.com/1.pdf"]
        mock_dependencies["scraper"].get_pdf_links.return_value = pdf_links
        mock_dependencies["zip_compressor"].create_zip.side_effect = Exception(
            "Zip failed"
        )

        processing_service.process("http://example.com")

        mock_error.assert_called_with(
            "Erro durante o processamento dos PDFs: Zip failed"
        )
        mock_dependencies["pdf_remove"].remove_pdfs.assert_not_called()
