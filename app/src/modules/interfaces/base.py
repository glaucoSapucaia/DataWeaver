from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

class PDFScraperInterface(ABC):
    """Interface para classes que extraem links de arquivos PDF de uma página web."""
    
    @abstractmethod
    def get_pdf_links(self, url: str, filtro: str) -> list:
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
    def create_zip(name_zip: str) -> None:
        """
        Cria um arquivo ZIP com os arquivos especificados.
        
        Parâmetros:
            name_zip (str): Nome do arquivo ZIP a ser criado.
        """
        pass


class PDFProcessingServiceInterface(ABC):
    """Interface para classes que gerenciam o processo de busca, download e compressão de arquivos PDF."""
    
    @abstractmethod
    def process(self, url: str, filtro: str) -> None:
        """
        Executa o processo completo de busca, download e compactação dos arquivos PDF.
        
        Parâmetros:
            url (str): URL da página web de onde os PDFs serão baixados.
            filtro (str): Filtro para encontrar os PDFs desejados.
        """
        pass
