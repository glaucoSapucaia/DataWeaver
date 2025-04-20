from .interfaces import CSVSaverInterface
from typing import TYPE_CHECKING

# Importação para tipagem
if TYPE_CHECKING:
    from pandas import DataFrame
    from pathlib import Path


class CsvSaver(CSVSaverInterface):
    """
    Implementação concreta da interface CSVSaverInterface.

    Esta classe implementa a interface `CSVSaverInterface` e fornece a funcionalidade de salvar
    um DataFrame em formato CSV em um caminho especificado.
    """

    def __init__(self, csv_path: "Path") -> None:
        """
        Inicializa o objeto CsvSaver com o caminho para o arquivo CSV.

        Parâmetros:
        csv_path: O caminho onde o arquivo CSV será salvo.
        """
        self.csv_path = csv_path

    def save_csv(self, data_frame: "DataFrame") -> None:
        """
        Salva o DataFrame fornecido em formato CSV no caminho especificado.

        O método escreve o conteúdo do DataFrame em um arquivo CSV, sem incluir o índice e com o cabeçalho.

        Parâmetros:
        data_frame: O DataFrame a ser salvo como arquivo CSV.
        """
        # debug
        print(f"DataFrame para salvar:\n{data_frame.head()}")

        data_frame.to_csv(str(self.csv_path), index=False, header=True)

        return None
