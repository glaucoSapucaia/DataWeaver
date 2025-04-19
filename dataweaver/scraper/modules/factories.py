from dataweaver.scraper.modules.interfaces import *
from dataweaver.scraper.modules import *

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


class DefaultPDFServiceFactory(PDFServiceAbstractFactory):
    def __init__(self, pdfs_dir: "Path", key_filter: str):
        self.pdfs_dir = pdfs_dir
        self.key_filter = key_filter

    def create_http_client(self) -> HttpClientInterface:
        return RequestsHttpClient()

    def create_link_extractor(self) -> PDFExtractionStrategy:
        return PDFLinkExtractor(
            [
                AnchorPDFExtractionStrategy(self.key_filter),
                ParagraphPDFExtractionStrategy(self.key_filter),
            ]
        )

    def create_scraper(self) -> PDFScraperInterface:
        return RequestsPDFScraper(
            self.create_http_client(), self.create_link_extractor()
        )

    def create_file_manager(self) -> FileManagerInterface:
        return FileManager(self.pdfs_dir)

    def create_zip_compressor(self) -> ZipCompressorInterface:
        return ZipCompressor(self.pdfs_dir)

    def create_pdf_remover(self) -> PDFRemoveInterface:
        return PDFRemove(self.pdfs_dir)

    def create_service(self, zip_name: str) -> PDFProcessingService:
        return PDFProcessingService(
            zip_name,
            self.create_scraper(),
            self.create_file_manager(),
            self.create_zip_compressor(),
            self.create_pdf_remover(),
        )
