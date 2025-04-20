"""
Pipeline DataWeaver - Fluxo Completo de Processamento
"""

from .scraper.modules import DefaultPDFServiceFactory
from .data.modules import TableExtractor
from .utils import ensure_directory_exists, PDFRemove
from .settings import config, logger


class PDFProcessor:
    """Classe para processamento de PDFs"""

    def __init__(self):
        self.pdfs_dir = config.dirs.pdfs
        self.zip_name = config.scraper.zip_name
        self.key_filter = config.scraper.filter
        self.url = config.scraper.url
        self.pdf_extension = "pdf"

    def run(self):
        """Executa o processo completo de coleta e compactação de PDFs"""
        logger.info("Iniciando o serviço de processamento de PDFs...")

        factory = DefaultPDFServiceFactory(self.pdfs_dir, self.key_filter)
        service = factory.create_service(self.zip_name, self.pdf_extension)

        logger.info("Executando o processo de coleta e compactação dos PDFs...")
        service.process(self.url)
        logger.info("Processamento de PDFs concluído!")


class CSVExtractor:
    """Classe para extração de dados de PDF para CSV"""

    def __init__(self):
        self.csv_dir = config.dirs.csv
        self.csv_extension = "csv"
        self.csv_zip_file = self.csv_dir / config.data.zip_name
        self.abbreviations = {"OD": "Seg. Odontológica", "AMB": "Seg. Ambulatorial"}

        ensure_directory_exists(self.csv_dir)

    def set_pdf_file(self, pdf_filename):
        """Configura o arquivo PDF a ser processado"""
        self.pdf_file = config.dirs.pdfs / pdf_filename
        self.csv_file = self.csv_dir / f"{pdf_filename.rsplit('.', 1)[0]}.csv"

    def run(self):
        """Executa a extração de dados da tabela do PDF"""
        if not hasattr(self, "pdf_file"):
            raise ValueError("PDF file not set. Use set_pdf_file() first.")

        logger.info("Iniciando extração de dados da tabela do PDF...")
        extractor = TableExtractor(
            self.pdf_file,
            self.csv_file,
            self.csv_zip_file,
            self.csv_extension,
            self.abbreviations,
        )
        extractor.run()


class CleanupManager:
    """Classe para gerenciar a limpeza de arquivos temporários"""

    def __init__(self):
        self.pdfs_dir = config.dirs.pdfs

    def run(self):
        """Executa a limpeza dos arquivos PDF temporários"""
        logger.info("Limpando arquivos temporários...")
        pdf_remove = PDFRemove(self.pdfs_dir)
        pdf_remove.remove_pdfs()
