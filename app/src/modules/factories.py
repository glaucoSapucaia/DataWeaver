from modules import *
from config import PDFS_DIR, ZIP_NAME

class PDFProcessingServiceFactory:
    """Fábrica para criar instâncias do serviço de processamento de PDFs."""
    
    @staticmethod
    def create():
        scraper = RequestsPDFScraper()
        file_manager = FileManager(PDFS_DIR)
        remove_pdf = PDFRemove()
        zip_compressor = ZipCompressor(PDFS_DIR, remove_pdf)
        
        return PDFProcessingService(ZIP_NAME, scraper, file_manager, zip_compressor)
