from modules import (RequestsPDFScraper, FileManager, PDFRemove, ZipCompressor, PDFProcessingService,
                     RequestsHttpClient, PDFLinkExtractor)
from config import PDFS_DIR, ZIP_NAME, FILTER
from logger import logger

class PDFProcessingServiceFactory:
    """Fábrica para criar instâncias do serviço de processamento de PDFs."""
    
    @staticmethod
    def create():
        try:
            http_client = RequestsHttpClient()
            extractor = PDFLinkExtractor(FILTER)
            scraper = RequestsPDFScraper(http_client, extractor)
            file_manager = FileManager(PDFS_DIR)
            remove_pdf = PDFRemove(PDFS_DIR)
            zip_compressor = ZipCompressor(PDFS_DIR)
            
            logger.info("Serviço de processamento de PDFs criado com sucesso.")
            return PDFProcessingService(ZIP_NAME, scraper, file_manager, zip_compressor, remove_pdf)
        
        except Exception as e:
            logger.error("Erro ao criar o serviço de processamento de PDFs.")
            raise e