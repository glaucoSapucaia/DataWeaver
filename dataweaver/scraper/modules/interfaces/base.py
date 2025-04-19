from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bs4 import BeautifulSoup


class PDFScraperInterface(ABC):
    """Interface para classes que extraem links de arquivos PDF de uma página web."""

    @abstractmethod
    def get_pdf_links(self, url: str) -> list:
        """
        Obtém os links dos arquivos PDF.

        Parâmetros:
            url (str): URL da página a ser analisada.

        Retorna:
            list: Lista de URLs dos arquivos PDF encontrados.
        """
        pass


class FileManagerInterface(ABC):
    """Interface para classes responsáveis pelo gerenciamento de arquivos, como download e armazenamento."""

    @abstractmethod
    def save_file(self, url: str) -> None:
        """
        Faz o download de um arquivo e o salva no local especificado.

        Parâmetros:
            url (str): URL do arquivo a ser baixado.
        """
        pass


class ZipCompressorInterface(ABC):
    """Interface para classes responsáveis por criar arquivos ZIP com arquivos específicos."""

    @abstractmethod
    def create_zip(self, zip_name: str) -> None:
        """
        Cria um arquivo ZIP com os arquivos especificados.

        Parâmetros:
            zip_name (str): Nome do arquivo ZIP a ser criado.
        """
        pass


class PDFProcessingServiceInterface(ABC):
    """Interface para classes que gerenciam o processo de busca, download e compressão de arquivos PDF."""

    @abstractmethod
    def process(self, url: str) -> None:
        """
        Executa o processo completo de busca, download e compactação dos arquivos PDF.

        Parâmetros:
            url (str): URL da página web de onde os PDFs serão baixados.
        """
        pass


class PDFRemoveInterface(ABC):
    """Interface para classes responsáveis pela remoção de arquivos PDF armazenados localmente."""

    @abstractmethod
    def remove_pdfs(self) -> None:
        """
        Remove os arquivos PDF armazenados localmente.
        """
        pass


class HttpClientInterface(ABC):
    """Interface para um cliente HTTP genérico, utilizado para realizar requisições a páginas web."""

    @abstractmethod
    def fetch_html(self, url: str) -> str:
        """
        Faz uma requisição HTTP GET e retorna o conteúdo HTML da resposta.

        Parâmetros:
            url (str): URL da página a ser requisitada.

        Retorna:
            str: Conteúdo HTML da resposta.
        """
        pass


class PDFExtractionStrategy(ABC):
    """Interface para estratégias de extração de links de PDFs a partir do conteúdo HTML de uma página."""

    @abstractmethod
    def extract(self, soup: "BeautifulSoup", base_url: str) -> set[str]:
        """
        Extrai links de arquivos PDF a partir do conteúdo HTML da página.

        Parâmetros:
            soup (BeautifulSoup): Objeto BeautifulSoup com o HTML da página.
            base_url (str): URL base da página para resolver links relativos.

        Retorna:
            list[str]: Lista de URLs de arquivos PDF.
        """
        pass


class PDFServiceAbstractFactory(ABC):
    @abstractmethod
    def create_http_client(self) -> HttpClientInterface:
        pass

    @abstractmethod
    def create_link_extractor(self) -> PDFExtractionStrategy:
        pass

    @abstractmethod
    def create_scraper(self) -> PDFScraperInterface:
        pass

    @abstractmethod
    def create_file_manager(self) -> FileManagerInterface:
        pass

    @abstractmethod
    def create_zip_compressor(self) -> ZipCompressorInterface:
        pass

    @abstractmethod
    def create_pdf_remover(self) -> PDFRemoveInterface:
        pass
