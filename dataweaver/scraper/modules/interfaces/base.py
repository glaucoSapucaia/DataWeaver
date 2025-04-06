from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bs4 import BeautifulSoup # type: ignore

class PDFScraperInterface(ABC):
    """Interface para classes que extraem links de arquivos PDF de uma página web."""
    
    @abstractmethod
    def get_pdf_links(self, url: str) -> list:
        """
        Obtém os links dos arquivos PDF que correspondem ao filtro.
        
        Parâmetros:
            url (str): URL da página a ser analisada.
            filtro (str): Palavra-chave para filtrar os arquivos PDF.
        
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
            keyword (str): keyword para encontrar os PDFs desejados.
        """
        pass

class PDFRemoveInterface(ABC):
    @abstractmethod
    def remove_pdfs(self) -> None:
        pass

class HttpClientInterface(ABC):
    """Interface para um cliente HTTP genérico."""

    @abstractmethod
    def fetch_html(self, url: str) -> str:
        """Faz uma requisição HTTP GET e retorna a resposta."""
        pass

class PDFExtractorStrategy(ABC):
    """Interface para estratégias de extração de links de PDFs."""

    @abstractmethod
    def extract(self, keyword: str) -> list[str]:
        pass