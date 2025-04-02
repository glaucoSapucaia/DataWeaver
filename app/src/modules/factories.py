from modules import (RequestsPDFScraper, FileManager, PDFRemove, ZipCompressor, PDFProcessingService,
                     RequestsHttpClient, PDFLinkExtractor)
from config import PDFS_DIR, ZIP_NAME, FILTER

class PDFProcessingServiceFactory:
    """Fábrica para criar instâncias do serviço de processamento de PDFs."""
    
    @staticmethod
    def create():
        http_client = RequestsHttpClient()
        extractor = PDFLinkExtractor(FILTER)
        scraper = RequestsPDFScraper(http_client, extractor)
        file_manager = FileManager(PDFS_DIR)
        remove_pdf = PDFRemove(PDFS_DIR)
        zip_compressor = ZipCompressor(PDFS_DIR)
        
        return PDFProcessingService(ZIP_NAME, scraper, file_manager, zip_compressor, remove_pdf)
