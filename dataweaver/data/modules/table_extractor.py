"""
Pipeline Data - Fluxo Completo de Processamento
"""

from dataweaver.scraper.modules import (
    ZipCompressor,
    ValidationZipCompressor,
    LoggingZipCompressor,
)
from dataweaver.errors import ExtractionError
from dataweaver.settings import logger
from .interfaces import TableExtractorInterface
from .pdf_extractor import PdfExtractor
from .data_processor import DataProcessor
from .csv_saver import CsvSaver

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


class TableExtractor(TableExtractorInterface):
    """
    Classe responsável por gerenciar os processos: extrair, processar e salvar tabelas de um arquivo PDF.

    Esta classe coordena o fluxo de extração de tabelas de um PDF, processamento dos dados,
    salvamento em formato CSV e compactação do arquivo gerado.
    """

    def __init__(
        self,
        pdf_path: "Path",
        csv_path: "Path",
        zip_path: "Path",
        file_extension: str,
        abbreviation_dict: dict,
    ) -> None:
        """
        Inicializa o extrator de tabelas.

        Parâmetros:
        - pdf_path (Path): Caminho do arquivo PDF de origem.
        - csv_path (Path): Caminho onde o CSV será salvo.
        - zip_path (Path): Caminho onde o arquivo compactado será armazenado.
        - file_extension: Extensão do arquivo (csv).
        - abbreviation_dict (dict): Dicionário para renomear colunas no processamento de dados.
        """
        self.pdf_path = pdf_path
        self.csv_path = csv_path
        self.zip_path = zip_path
        self.file_extension = file_extension
        self.abbreviation_dict = abbreviation_dict

        self.pdf_extractor = PdfExtractor(pdf_path)
        self.data_processor = DataProcessor(abbreviation_dict)
        self.csv_saver = CsvSaver(csv_path)

        # ZipCompressor com Decorators
        self.zip_compressor = ValidationZipCompressor(
            LoggingZipCompressor(ZipCompressor(self.zip_path.parent))
        )

    def run(self) -> None:
        """
        Executa o processo completo de extração e processamento de tabelas do PDF.

        O fluxo de execução segue as seguintes etapas:

        1. Extração das tabelas do PDF.
        2. Processamento dos dados extraídos.
        3. Salvamento dos dados em formato CSV.
        4. Compactação do arquivo CSV gerado.
        """
        tables = self.pdf_extractor.extract_tables(pages="3-181")
        if not tables:
            logger.error("Nenhuma tabela encontrada durante a extração.")
            raise ExtractionError("A extração do PDF não retornou nenhuma tabela.")

        logger.info(f"Tabela extraída com sucesso.")

        table_df = self.data_processor.process_data(tables)

        self.csv_saver.save_csv(table_df)
        logger.info("Arquivo CSV salvo.")

        self.zip_compressor.create_zip(self.zip_path, self.file_extension)
        logger.info(f"Tabela salva e compactada!")
