from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bs4 import BeautifulSoup


class PDFScraperInterface(ABC):
    """Interface para classes que extraem links de arquivos PDF de uma página web.

    Design Pattern:
        Strategy (via composição com PDFExtractionStrategy).
    """

    @abstractmethod
    def get_pdf_links(self, url: str) -> list[str]:
        """Obtém os links dos arquivos PDF.

        Args:
            url: URL da página a ser analisada.

        Returns:
            Lista de URLs absolutos dos arquivos PDF encontrados.
        """
        pass


class FileManagerInterface(ABC):
    """Interface para gerenciamento de arquivos (download/armazenamento)."""

    @abstractmethod
    def save_file(self, url: str) -> None:
        """Faz o download de um arquivo e o salva no local especificado.

        Args:
            url: URL do arquivo a ser baixado.
        """
        pass


class ZipCompressorInterface(ABC):
    """Interface para compressão de arquivos em ZIP."""

    @abstractmethod
    def create_zip(self, zip_name: str, file_extension: str) -> None:
        """Cria um arquivo ZIP com os arquivos gerenciados pela FileManagerInterface.

        Args:
            zip_name: Nome do arquivo ZIP (com extensão).
        """
        pass


class PDFProcessingServiceInterface(ABC):
    """Interface para o serviço completo de processamento de PDFs.

    Design Pattern:
        Facade (simplifica operações complexas: scrape/download/compressão).
    """

    @abstractmethod
    def process(self, url: str) -> None:
        """Executa o pipeline completo: busca, download e compactação de PDFs.

        Args:
            url: URL da página web alvo.
        """
        pass


class HttpClientInterface(ABC):
    """Interface para clientes HTTP (ex: requests, aiohttp)."""

    @abstractmethod
    def fetch_html(self, url: str) -> str:
        """Obtém o HTML bruto de uma URL.

        Args:
            url: Endereço web alvo.

        Returns:
            HTML da página como string.
        """
        pass


class PDFExtractionStrategy(ABC):
    """Interface para estratégias de extração de links PDF.

    Design Pattern:
        Strategy (permite variações na lógica de extração).
    """

    @abstractmethod
    def extract(self, soup: "BeautifulSoup", base_url: str) -> set[str]:
        """Extrai links de PDFs de um objeto BeautifulSoup.

        Args:
            soup: Objeto parseado do HTML.
            base_url: URL base para resolver links relativos.

        Returns:
            Conjunto de URLs absolutos de PDFs.
        """
        pass


class PDFServiceAbstractFactory(ABC):
    """Interface para fábrica abstrata de componentes do serviço de PDF.

    Design Pattern:
        Abstract Factory (familia de objetos relacionados).
    """

    @abstractmethod
    def create_http_client(self) -> HttpClientInterface:
        """Cria um cliente HTTP específico da implementação."""
        pass

    @abstractmethod
    def create_link_extractor(self) -> PDFExtractionStrategy:
        """Cria uma estratégia de extração de links."""
        pass

    @abstractmethod
    def create_scraper(self) -> PDFScraperInterface:
        """Cria um scraper de PDF configurado."""
        pass

    @abstractmethod
    def create_file_manager(self) -> FileManagerInterface:
        """Cria um gerenciador de arquivos."""
        pass

    @abstractmethod
    def create_zip_compressor(self) -> ZipCompressorInterface:
        """Cria um compressor ZIP."""
        pass
