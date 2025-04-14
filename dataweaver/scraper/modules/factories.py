"""
Define a classe PDFProcessingServiceFactory, responsável por instanciar e configurar
todas as dependências necessárias para o serviço de processamento de arquivos PDF.

Este módulo centraliza a criação de objetos como o scraper, gerenciador de arquivos,
compressor ZIP e removedor de PDFs, promovendo injeção de dependência e facilitando testes.
"""

from dataweaver.scraper.modules import (
    RequestsPDFScraper, FileManager, PDFRemove, ZipCompressor,
    PDFProcessingService, RequestsHttpClient, PDFLinkExtractor
)
from paths import PDFS_DIR, ZIP_NAME, FILTER
from logger import logger

class PDFProcessingServiceFactory:
    """
    Fábrica responsável por montar e retornar uma instância totalmente configurada 
    do serviço de processamento de PDFs.
    """
    
    @staticmethod
    def create() -> PDFProcessingService:
        """
        Cria e configura todas as dependências necessárias para o serviço principal.

        :return: Instância do PDFProcessingService
        :raise: Propaga qualquer exceção ocorrida durante a criação dos componentes
        """
        try:
            http_client = RequestsHttpClient()
            extractor = PDFLinkExtractor(FILTER)
            scraper = RequestsPDFScraper(http_client, extractor)
            file_manager = FileManager(PDFS_DIR)
            remove_pdf = PDFRemove(PDFS_DIR)
            zip_compressor = ZipCompressor(PDFS_DIR)

            logger.info("Serviço de processamento de PDFs criado com sucesso.")
            return PDFProcessingService(
                ZIP_NAME,
                scraper,
                file_manager,
                zip_compressor,
                remove_pdf
            )

        except Exception as e:
            logger.error(f"Erro ao criar o serviço de processamento de PDFs: {e}")
            raise
