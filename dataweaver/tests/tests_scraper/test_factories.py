from dataweaver.scraper.modules.interfaces import (
    PDFServiceAbstractFactory,
    HttpClientInterface,
    PDFScraperInterface,
    FileManagerInterface,
    ZipCompressorInterface,
    PDFProcessingServiceInterface,
    PDFExtractionStrategy,
)
from dataweaver.scraper.modules import DefaultPDFServiceFactory

from unittest.mock import patch, MagicMock


def test_factory_implements_abstract_factory():
    """Verifica se a fábrica implementa a interface abstrata esperada."""
    assert issubclass(DefaultPDFServiceFactory, PDFServiceAbstractFactory)


def test_create_http_client_returns_correct_type(tmp_path):
    """Testa se a fábrica retorna um cliente HTTP válido."""
    factory = DefaultPDFServiceFactory(tmp_path, "test")
    client = factory.create_http_client()
    assert isinstance(client, HttpClientInterface)


def test_create_link_extractor_with_strategies(tmp_path):
    """Garante que o extrator de links tenha estratégias configuradas."""
    key_filter = "important"
    factory = DefaultPDFServiceFactory(tmp_path, key_filter)
    extractor = factory.create_link_extractor()

    assert isinstance(extractor, PDFExtractionStrategy)
    assert len(extractor.strategies) == 2


def test_create_scraper_with_dependencies(tmp_path):
    """Verifica se o scraper é criado com as dependências necessárias."""
    factory = DefaultPDFServiceFactory(tmp_path, "test")
    scraper = factory.create_scraper()

    assert isinstance(scraper, PDFScraperInterface)
    assert isinstance(scraper.http_client, HttpClientInterface)


def test_create_file_manager_with_correct_path(tmp_path):
    """Testa se o gerenciador de arquivos usa o caminho correto."""
    factory = DefaultPDFServiceFactory(tmp_path, "test")
    file_manager = factory.create_file_manager()

    assert isinstance(file_manager, FileManagerInterface)
    assert file_manager.folder == tmp_path


def test_create_zip_compressor_with_correct_path(tmp_path):
    """Garante que o compressor usa o diretório correto."""
    factory = DefaultPDFServiceFactory(tmp_path, "test")
    compressor = factory.create_zip_compressor()

    assert isinstance(compressor, ZipCompressorInterface)
    assert compressor.folder == tmp_path


def test_create_service_with_all_components(tmp_path):
    """Testa se a criação do serviço utiliza todas as dependências corretamente."""
    zip_name = "output"
    file_extension = "pdf"
    factory = DefaultPDFServiceFactory(tmp_path, "test")

    with patch.object(factory, "create_scraper") as mock_scraper, patch.object(
        factory, "create_file_manager"
    ) as mock_file_manager, patch.object(
        factory, "create_zip_compressor"
    ) as mock_compressor:

        mock_scraper.return_value = MagicMock(spec=PDFScraperInterface)
        mock_file_manager.return_value = MagicMock(spec=FileManagerInterface)
        mock_compressor.return_value = MagicMock(spec=ZipCompressorInterface)

        service = factory.create_service(zip_name, file_extension)

        assert isinstance(service, PDFProcessingServiceInterface)
        mock_scraper.assert_called_once()
        mock_file_manager.assert_called_once()
        mock_compressor.assert_called_once()


def test_service_creation_integration(tmp_path):
    """Verifica a criação real do serviço com todas as dependências integradas."""
    factory = DefaultPDFServiceFactory(tmp_path, "important")
    service = factory.create_service("output", "pdf")

    assert isinstance(service, PDFProcessingServiceInterface)
    assert service.zip_name == "output"
    assert service.file_extension == "pdf"
    assert isinstance(service.scraper, PDFScraperInterface)
    assert isinstance(service.file_manager, FileManagerInterface)
    assert isinstance(service.zip_compressor, ZipCompressorInterface)
