from dataweaver.errors import TableProcessingError
from dataweaver.settings import logger
from .interfaces import DataProcessorInterface

import pandas as pd


class DataProcessor(DataProcessorInterface):
    """
    Implementação concreta da interface DataProcessorInterface.

    Esta classe realiza o processamento de dados extraídos de tabelas, incluindo a concatenação
    das tabelas e a renomeação das colunas conforme um dicionário de abreviações fornecido.
    """

    def __init__(self, abbreviation_dict: dict) -> None:
        self.abbreviation_dict = abbreviation_dict

    def process_data(self, tables: list[pd.DataFrame]) -> pd.DataFrame:
        """
        Processa uma lista de DataFrames extraídos, concatenando-os e renomeando as colunas.

        Parâmetros:
            tables (List[pd.DataFrame]): Lista de DataFrames extraídos para processamento.

        Retorna:
            pd.DataFrame: DataFrame concatenado.

        Lança:
            ValueError: Se a lista de tabelas estiver vazia.
            TableProcessingError: Se ocorrer erro durante a concatenação.
        """
        if not tables:
            logger.warning("Nenhuma tabela foi fornecida para processamento.")
            raise ValueError("A lista de tabelas está vazia.")

        logger.info("Processando tabelas...")

        try:
            logger.info("Concatenando tabelas...")
            final_df = pd.concat(tables, axis=0)
            return final_df
        except Exception as e:
            logger.error(f"ERRO na concatenação: {e}")
            raise TableProcessingError(f"Erro ao concatenar tabelas: {e}")
