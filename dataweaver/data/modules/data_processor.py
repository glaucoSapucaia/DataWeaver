from .interfaces import DataProcessorInterface
import pandas as pd


class DataProcessor(DataProcessorInterface):
    """
    Implementação concreta da interface DataProcessorInterface.

    Esta classe realiza o processamento de dados extraídos de tabelas, incluindo a concatenação
    das tabelas e a renomeação das colunas conforme um dicionário de abreviações fornecido.
    """

    def __init__(self, abbreviation_dict: dict) -> None:
        """
        Inicializa o processador de dados com um dicionário de abreviações.

        Parâmetros:
        abbreviation_dict (dict): Dicionário contendo o mapeamento de nomes de colunas.
        """
        self.abbreviation_dict = abbreviation_dict

    def process_data(self, tables: list[pd.DataFrame]) -> pd.DataFrame:
        """
        Processa uma lista de DataFrames extraídos, concatenando-os e renomeando as colunas.

        O método verifica se há tabelas disponíveis, concatena todas em um único DataFrame
        e renomeia suas colunas conforme o dicionário fornecido.

        Parâmetros:
        tables (list[pd.DataFrame]): Lista de DataFrames extraídos para processamento.
        """
        if not tables:
            return pd.DataFrame

        # debug
        print(f"Tabelas extraídas: {len(tables)}")
        print(f"0 - tabela extraída:\n{tables[0]}")
        print(f"50 - tabela extraída:\n{tables[50]}")
        print(f"100 - tabela extraída:\n{tables[100]}")
        print(f"150 -  tabela extraída:\n{tables[150]}")
        print(f"178 -  tabela extraída:\n{tables[178]}")

        try:
            final_df = pd.concat(tables, axis=0)
        except Exception as e:
            # debug
            print(f"ERRO na concatenação: {e}")

            return pd.DataFrame()

        final_df = final_df.rename(columns=self.abbreviation_dict)

        # debug
        print("\nTabela final após processamento:")
        print(final_df.tail())

        colunas_lista = final_df.columns.tolist()

        # degbug
        print(colunas_lista)

        return final_df
