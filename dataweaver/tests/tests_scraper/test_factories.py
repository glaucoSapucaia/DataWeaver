"""
Testes para PDFProcessingServiceFactory.

Cobre:
- Criação bem-sucedida da instância do serviço.
- Falha durante a criação de dependências.
"""

import pytest  # type: ignore
from unittest.mock import patch
from dataweaver.scraper.modules.factories import PDFProcessingServiceFactory
from dataweaver.scraper.modules.pdf_processor import PDFProcessingService


def test_factory_creates_valid_service():
    """
    Verifica se a factory retorna uma instância válida de PDFProcessingService.
    """

    with patch("dataweaver.scraper.modules.factories.RequestsHttpClient"), \
         patch("dataweaver.scraper.modules.factories.PDFLinkExtractor"),   \
         patch("dataweaver.scraper.modules.factories.RequestsPDFScraper"), \
         patch("dataweaver.scraper.modules.factories.FileManager"),        \
         patch("dataweaver.scraper.modules.factories.PDFRemove"),          \
         patch("dataweaver.scraper.modules.factories.ZipCompressor"):

        service = PDFProcessingServiceFactory.create()
        assert isinstance(service, PDFProcessingService)


def test_factory_logs_and_raises_error_if_creation_fails():
    """
    Verifica se erro na criação de uma dependência é capturado, logado e propagado.
    """

    with patch("dataweaver.scraper.modules.factories.RequestsHttpClient", side_effect=Exception("Falha na dependência")), \
         patch("dataweaver.scraper.modules.factories.logger.error") as mock_log:

        with pytest.raises(Exception, match="Falha na dependência"):
            PDFProcessingServiceFactory.create()

        assert mock_log.called
        assert "Erro ao criar o serviço de processamento de PDFs" in mock_log.call_args[0][0]
