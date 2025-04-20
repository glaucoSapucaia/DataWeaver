from .interfaces import ZipCompressorInterface
from typing import TYPE_CHECKING
import zipfile

# Importação para tipagem
if TYPE_CHECKING:
    from pathlib import Path


class ZipCompressor(ZipCompressorInterface):
    """
    Classe responsável por compactar arquivos em formato ZIP.

    Implementa a interface ZipCompressorInterface, garantindo a funcionalidade
    de compressão de arquivos de forma padronizada.
    """

    def __init__(self, zip_path: "Path") -> None:
        """
        Inicializa o compressor de arquivos ZIP.

        Parâmetros:
        - zip_path: Caminho onde o arquivo ZIP será salvo.
        """
        self.zip_path = zip_path

    def compress(self, file_path: "Path") -> None:
        """
        Compacta um arquivo específico para um arquivo ZIP.

        Parâmetros:
        - file_path: Caminho do arquivo que será compactado.
        """
        with zipfile.ZipFile(self.zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file_path, file_path.name)
