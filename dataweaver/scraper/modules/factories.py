from dataweaver.scraper.modules import (
    RequestsPDFScraper,
    FileManager,
    PDFRemove,
    ZipCompressor,
    PDFProcessingService,
    RequestsHttpClient,
    PDFLinkExtractor,
)
from dataweaver.settings import *

pdfs_dir = config.dirs.pdfs
zip_name = config.scraper.zip_name
key_filter = config.scraper.filter


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
            extractor = PDFLinkExtractor(key_filter)
            scraper = RequestsPDFScraper(http_client, extractor)
            file_manager = FileManager(pdfs_dir)
            remove_pdf = PDFRemove(pdfs_dir)
            zip_compressor = ZipCompressor(pdfs_dir)

            logger.info("Serviço de processamento de PDFs criado com sucesso.")
            return PDFProcessingService(
                zip_name, scraper, file_manager, zip_compressor, remove_pdf
            )

        except Exception as e:
            logger.error(f"Erro ao criar o serviço de processamento de PDFs: {e}")
            raise
