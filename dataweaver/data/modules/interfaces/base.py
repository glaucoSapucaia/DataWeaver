from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pandas import DataFrame


class PDFExtractorInterface(ABC):
    """
    Interface para a extração de tabelas de arquivos PDF.

    Esta classe abstrata define o método `extract_tables`, que deve ser implementado por
    qualquer classe que realize a extração de tabelas a partir de documentos PDF.
    """

    @abstractmethod
    def extract_tables(self, pages: str) -> "DataFrame":
        """
        Método abstrato para extrair tabelas de arquivos PDF.

        Parâmetros:
        pages (str): As páginas ou intervalo de páginas do PDF de onde as tabelas serão extraídas.
        """
        pass


class DataProcessorInterface(ABC):
    """
    Interface para o processamento de dados extraídos.

    Esta classe abstrata define o método `process_data`, que deve ser implementado por
    qualquer classe responsável por processar dados extraídos de tabelas.
    """

    @abstractmethod
    def process_data(self, tables: list["DataFrame"]) -> "DataFrame":
        """
        Método abstrato para processar dados extraídos.

        Parâmetros:
        tables: Dados extraídos das tabelas que devem ser processados.
        """
        pass


class CSVSaverInterface(ABC):
    """
    Interface para salvar dados em formato CSV.

    Esta classe abstrata define o método `save_csv`, que deve ser implementado por
    qualquer classe que deseje salvar dados em formato CSV.
    """

    @abstractmethod
    def save_csv(self, data_frame: "DataFrame") -> None:
        """
        Método abstrato para salvar dados em formato CSV.

        Parâmetros:
        data_frame: Dados a serem salvos no formato CSV.
        """
        pass


class TableExtractorInterface(ABC):
    """
    Interface para extração de tabelas.

    Esta classe abstrata define o método `run`, que deve ser implementado por
    qualquer classe que realize a extração de tabelas. Funciona como uma clase gerenciadora.
    """

    @abstractmethod
    def run(self) -> None:
        """
        Método abstrato para gerenciar o processo de extração de tabelas.
        """
        pass
