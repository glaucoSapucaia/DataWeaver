"""
Módulo responsável por orquestrar o processo completo de obtenção, download,
compactação e limpeza de arquivos PDF a partir de uma URL.
"""

from .interfaces import (
    FileManagerInterface,
    PDFProcessingServiceInterface,
    PDFScraperInterface,
    ZipCompressorInterface,
    PDFRemoveInterface,
)
from dataweaver.logger import logger

class PDFProcessingService(PDFProcessingServiceInterface):
    """
    Serviço principal que gerencia todo o fluxo de processamento de PDFs.
    
    Responsável por:
    - Obter os links dos PDFs por meio do scraper.
    - Baixar os arquivos com o gerenciador de arquivos.
    - Compactá-los em um único ZIP.
    - Remover os arquivos PDF após a compactação.
    """

    def __init__(self,
                 zip_name: str,
                 scraper: PDFScraperInterface,
                 file_manager: FileManagerInterface,
                 zip_compressor: ZipCompressorInterface,
                 pdf_remove: PDFRemoveInterface) -> None:
        """
        Inicializa o serviço de processamento de PDFs.

        Parâmetros:
            zip_name (str): Nome do arquivo ZIP a ser gerado.
            scraper (PDFScraperInterface): Scraper para buscar os links dos PDFs.
            file_manager (FileManagerInterface): Gerenciador de arquivos para download.
            zip_compressor (ZipCompressorInterface): Componente para compactação dos arquivos.
            pdf_remove (PDFRemoveInterface): Componente para remover os PDFs após compactação.
        """
        self.zip_name = zip_name
        self.scraper = scraper
        self.file_manager = file_manager
        self.zip_compressor = zip_compressor
        self.pdf_remove = pdf_remove

    def process(self, url: str) -> None:
        """
        Executa o fluxo completo de processamento dos arquivos PDF.

        Etapas:
            1. Busca por links de PDF na URL fornecida.
            2. Download dos arquivos encontrados.
            3. Compactação em um arquivo ZIP.
            4. Remoção dos PDFs da pasta após o processo.

        Parâmetros:
            url (str): Endereço da página onde os PDFs estão localizados.
        """
        try:
            logger.info("Buscando PDFs...")
            pdf_links = self.scraper.get_pdf_links(url)

            if not pdf_links:
                logger.warning("Nenhum PDF encontrado.")
                return

            logger.info("Baixando PDFs...")
            for link in pdf_links:
                try:
                    self.file_manager.save_file(link)
                except Exception as e:
                    logger.error(f"Erro ao baixar o arquivo {link}: {e}")

            logger.info("Compactando arquivos...")
            self.zip_compressor.create_zip(self.zip_name)

            logger.info("Excluindo arquivos baixados...")
            self.pdf_remove.remove_pdfs()

        except Exception as e:
            logger.error(f"Erro durante o processamento dos PDFs: {e}")
