"""
Este módulo define interfaces (ABCs) que padronizam a implementação de funcionalidades
relacionadas à extração, download, compressão e remoção de arquivos PDF, bem como
a comunicação HTTP necessária para essas operações.

Cada interface descreve contratos que devem ser seguidos pelas implementações concretas,
garantindo consistência e modularidade no sistema.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bs4 import BeautifulSoup  # type: ignore


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


class PDFExtractorStrategyInterface(ABC):
    """Interface para estratégias de extração de links de PDFs a partir do conteúdo HTML de uma página."""

    @abstractmethod
    def extract(self, soup: 'BeautifulSoup', base_url: str) -> list[str]:
        """
        Extrai links de arquivos PDF a partir do conteúdo HTML da página.

        Parâmetros:
            soup (BeautifulSoup): Objeto BeautifulSoup com o HTML da página.
            base_url (str): URL base da página para resolver links relativos.

        Retorna:
            list[str]: Lista de URLs de arquivos PDF.
        """
        pass
