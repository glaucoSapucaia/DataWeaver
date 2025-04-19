from dataweaver.scraper.modules.interfaces import *
from dataweaver.scraper.modules import (
    DefaultPDFServiceFactory,
    PDFProcessingService,
    PDFLinkExtractor,
)

import pytest
from pathlib import Path


@pytest.fixture
def mock_pdfs_dir():
    """Fixture que retorna um Path falso para testes."""
    return Path("/fake/path")


@pytest.fixture
def factory(mock_pdfs_dir):
    """Fixture principal que retorna uma fábrica configurada para testes."""
    return DefaultPDFServiceFactory(pdfs_dir=mock_pdfs_dir, key_filter="test")


class TestDefaultPDFServiceFactory:
    """Testes para a fábrica concreta de serviços de PDF."""

    def test_create_http_client(self, factory):
        """Verifica se cria corretamente um cliente HTTP.

        Checks:
            - Retorna uma implementação válida de HttpClientInterface
        """
        client = factory.create_http_client()
        assert isinstance(client, HttpClientInterface)

    def test_create_link_extractor(self, factory):
        """Testa a criação do extrator de links PDF.

        Checks:
            - Retorna uma instância de PDFLinkExtractor
            - Inclui as 2 estratégias padrão (anchor e paragraph)
        """
        extractor = factory.create_link_extractor()
        assert isinstance(extractor, PDFLinkExtractor)
        assert len(extractor.strategies) == 2

    def test_create_scraper(self, factory):
        """Testa a criação do scraper com suas dependências.

        Checks:
            - Possui todos os atributos obrigatórios
            - Atributos são dos tipos corretos
            - Métodos necessários existem
        """
        scraper = factory.create_scraper()

        required_attrs = {
            "http_client": HttpClientInterface,
            "extractor": PDFLinkExtractor,
            "get_pdf_links": callable,
        }

        for attr, expected_type in required_attrs.items():
            assert hasattr(scraper, attr), f"Atributo faltando: {attr}"
            attr_value = getattr(scraper, attr)

            if expected_type is callable:
                assert callable(attr_value), f"{attr} deve ser callable"
            else:
                assert isinstance(
                    attr_value, expected_type
                ), f"{attr} deve ser {expected_type.__name__}"

    def test_create_file_manager(self, factory, mock_pdfs_dir):
        """Testa criação do gerenciador de arquivos.

        Checks:
            - Implementa a interface correta
            - Usa o diretório configurado
        """
        manager = factory.create_file_manager()
        assert isinstance(manager, FileManagerInterface)
        assert manager.folder == mock_pdfs_dir

    def test_create_zip_compressor(self, factory, mock_pdfs_dir):
        """Testa criação do compressor ZIP.

        Checks:
            - Implementa ZipCompressorInterface
            - Aponta para o diretório correto
        """
        compressor = factory.create_zip_compressor()
        assert isinstance(compressor, ZipCompressorInterface)
        assert compressor.folder == mock_pdfs_dir

    def test_create_pdf_remover(self, factory, mock_pdfs_dir):
        """Testa criação do serviço de remoção de PDFs.

        Checks:
            - Implementa PDFRemoveInterface
            - Configurado com o diretório correto
        """
        remover = factory.create_pdf_remover()
        assert isinstance(remover, PDFRemoveInterface)
        assert remover.folder == mock_pdfs_dir


class TestServiceCreation:
    """Testes para a criação do serviço completo."""

    def test_create_service(self, factory):
        """Testa a criação do serviço de processamento.

        Checks:
            - Retorna instância de PDFProcessingService
            - Nome do ZIP é repassado corretamente
            - Todas dependências são injetadas corretamente
        """
        zip_name = "test_archive"
        service = factory.create_service(zip_name)

        assert isinstance(service, PDFProcessingService)
        assert service.zip_name == zip_name

        # Verificação das dependências injetadas
        assert isinstance(service.scraper, PDFScraperInterface)
        assert isinstance(service.file_manager, FileManagerInterface)
        assert isinstance(service.zip_compressor, ZipCompressorInterface)
        assert isinstance(service.pdf_remove, PDFRemoveInterface)
