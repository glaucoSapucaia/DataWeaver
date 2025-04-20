from .interfaces import TableExtractorInterface
from .pdf_extractor import PdfExtractor
from .data_processor import DataProcessor
from .csv_saver import CsvSaver
from .zip_compressor import ZipCompressor
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
        abbreviation_dict: dict,
    ) -> None:
        """
        Inicializa o extrator de tabelas.

        Parâmetros:
        - pdf_path (Path): Caminho do arquivo PDF de origem.
        - csv_path (Path): Caminho onde o CSV será salvo.
        - zip_path (Path): Caminho onde o arquivo compactado será armazenado.
        - abbreviation_dict (dict): Dicionário para renomear colunas no processamento de dados.
        """
        self.pdf_path = pdf_path
        self.csv_path = csv_path
        self.zip_path = zip_path
        self.abbreviation_dict = abbreviation_dict

        self.pdf_extractor = PdfExtractor(pdf_path)
        self.data_processor = DataProcessor(abbreviation_dict)
        self.csv_saver = CsvSaver(csv_path)
        self.zip_compressor = ZipCompressor(zip_path)

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
            # debug
            print("Nenhuma tabela encontrada.")

            return None

        # debug
        print(
            f"Tabela extraída com sucesso - Total de linhas da página um: {len(tables[0])}."
        )

        table_df = self.data_processor.process_data(tables)

        self.csv_saver.save_csv(table_df)
        # debug
        print(f"Arquivo CSV criado - {self.csv_path}")

        self.zip_compressor.compress(self.csv_path)
        # debug
        print(f"Tabela salva e compactada em {self.zip_path}")
        print(table_df.iloc[:, :5])

        return None
