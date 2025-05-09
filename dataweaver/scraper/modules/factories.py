from .interfaces import PDFServiceAbstractFactory
from .pdf_scraper import (
    RequestsHttpClient,
    PDFLinkExtractor,
    AnchorPDFExtractionStrategy,
    ParagraphPDFExtractionStrategy,
    RequestsPDFScraper,
)
from .file_manager import FileManager
from .zip_compressor import ZipCompressor
from .pdf_processor import PDFProcessingService

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interfaces import (
        HttpClientInterface,
        PDFScraperInterface,
        FileManagerInterface,
        ZipCompressorInterface,
        PDFProcessingServiceInterface,
        PDFExtractionStrategy,
    )
    from pathlib import Path


class DefaultPDFServiceFactory(PDFServiceAbstractFactory):
    """Implementação concreta da fábrica abstrata para serviços de PDF.

    Fornece as implementações padrão de todos os componentes necessários:
    - Cliente HTTP
    - Extrator de links
    - Scraper
    - Gerenciador de arquivos
    - Compressor ZIP

    Design Patterns:
        Abstract Factory (implementa PDFServiceAbstractFactory).
        Composition (agrega múltiplas estratégias de extração em PDFLinkExtractor).

    Args:
        pdfs_dir: Diretório onde os PDFs serão salvos.
        key_filter: Filtro de palavras-chave para extração de links.
    """

    def __init__(self, pdfs_dir: "Path", key_filter: str) -> None:
        self.pdfs_dir = pdfs_dir
        self.key_filter = key_filter

    def create_http_client(self) -> "HttpClientInterface":
        """Cria um cliente HTTP baseado na biblioteca requests.

        Returns:
            Instância de RequestsHttpClient.
        """
        return RequestsHttpClient()

    def create_link_extractor(self) -> "PDFExtractionStrategy":
        """Cria um PDFLinkExtractor com estratégias de extração de:
        - Links em tags ``<a>`` (AnchorPDFExtractionStrategy)
        - Links em parágrafos (ParagraphPDFExtractionStrategy)
        """
        return PDFLinkExtractor(
            [
                AnchorPDFExtractionStrategy(self.key_filter),
                ParagraphPDFExtractionStrategy(self.key_filter),
            ]
        )

    def create_scraper(self) -> "PDFScraperInterface":
        """Cria um scraper de PDFs com dependências injetadas.

        Returns:
            RequestsPDFScraper com cliente HTTP e extrator de links.
        """
        return RequestsPDFScraper(
            self.create_http_client(), self.create_link_extractor()
        )

    def create_file_manager(self) -> "FileManagerInterface":
        """Cria um gerenciador de arquivos para o diretório especificado.

        Returns:
            FileManager configurado com pdfs_dir.
        """
        return FileManager(self.pdfs_dir)

    def create_zip_compressor(self) -> "ZipCompressorInterface":
        """Cria um compressor ZIP para o diretório de PDFs.

        Returns:
            ZipCompressor configurado com pdfs_dir.
        """
        return ZipCompressor(self.pdfs_dir)

    def create_service(
        self, zip_name: str, file_extension: str
    ) -> "PDFProcessingServiceInterface":
        """Monta o serviço completo de processamento de PDFs.

        Args:
            zip_name: Nome do arquivo ZIP de saída.
            file_extension: Extensão do arquivo (pdf)

        Returns:
            PDFProcessingService
            com todos os componentes injetados:
            - zip_name
            - file_extension
            - Scraper
            - FileManager
            - ZipCompressor
        """
        return PDFProcessingService(
            zip_name,
            file_extension,
            self.create_scraper(),
            self.create_file_manager(),
            self.create_zip_compressor(),
        )
