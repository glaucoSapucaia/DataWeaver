import pytest
from pathlib import Path
from dataweaver.scraper.modules.interfaces import *
from dataweaver.scraper.modules import (
    DefaultPDFServiceFactory,
    PDFProcessingService,
    PDFLinkExtractor,
)


@pytest.fixture
def mock_pdfs_dir():
    return Path("/fake/path")


@pytest.fixture
def factory(mock_pdfs_dir):
    return DefaultPDFServiceFactory(pdfs_dir=mock_pdfs_dir, key_filter="test")


def test_create_http_client(factory):
    client = factory.create_http_client()
    # Verifica se retorna a implementação correta
    assert isinstance(client, HttpClientInterface)


def test_create_link_extractor(factory):
    extractor = factory.create_link_extractor()
    assert isinstance(extractor, PDFLinkExtractor)
    # Deve conter as estratégias especificadas
    assert len(extractor.strategies) == 2


def test_create_scraper(factory):
    scraper = factory.create_scraper()

    # Verificação dos atributos com os nomes corretos
    required_attrs = {
        "http_client": HttpClientInterface,
        "extractor": PDFLinkExtractor,
        "get_pdf_links": callable,
    }

    for attr, expected_type in required_attrs.items():
        assert hasattr(scraper, attr), f"Scraper missing required attribute: {attr}"
        attr_value = getattr(scraper, attr)

        if expected_type is callable:
            assert callable(attr_value), f"{attr} should be callable"
        else:
            assert isinstance(
                attr_value, expected_type
            ), f"{attr} should be instance of {expected_type.__name__}"


def test_create_file_manager(factory, mock_pdfs_dir):
    manager = factory.create_file_manager()
    assert isinstance(manager, FileManagerInterface)
    assert manager.folder == mock_pdfs_dir


def test_create_zip_compressor(factory, mock_pdfs_dir):
    compressor = factory.create_zip_compressor()
    assert isinstance(compressor, ZipCompressorInterface)
    assert compressor.folder == mock_pdfs_dir


def test_create_pdf_remover(factory, mock_pdfs_dir):
    remover = factory.create_pdf_remover()
    assert isinstance(remover, PDFRemoveInterface)
    assert remover.folder == mock_pdfs_dir


def test_create_service(factory):
    zip_name = "test.zip"
    service = factory.create_service(zip_name)

    # Verificações básicas
    assert isinstance(service, PDFProcessingService)
    assert service.zip_name == zip_name

    # Verifica se as dependências foram injetadas corretamente
    assert isinstance(service.scraper, PDFScraperInterface)
    assert isinstance(service.file_manager, FileManagerInterface)
    assert isinstance(service.zip_compressor, ZipCompressorInterface)
    assert isinstance(service.pdf_remove, PDFRemoveInterface)
