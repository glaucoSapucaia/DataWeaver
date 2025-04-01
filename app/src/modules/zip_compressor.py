from .interfaces import ZipCompressorInterface
from typing import TYPE_CHECKING
import os
import zipfile

if TYPE_CHECKING:
    from pathlib import Path

class ZipCompressor(ZipCompressorInterface):
    def __init__(self, folder: 'Path') -> None:
        """
        Inicializa o compressor ZIP com o diretório onde os arquivos estão localizados.
        
        Parâmetros:
            folder (str): Caminho da folder que contém os arquivos a serem compactados.
        """
        self.folder = folder

    def create_zip(self, zip_name: str) -> None:
        """
        Compacta todos os arquivos da folder em um arquivo ZIP.
        
        Parâmetros:
            zip_name (str): Nome do arquivo ZIP gerado.
        """
        zip_path = os.path.join(self.folder, zip_name)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(self.folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    # Adicionar o arquivo ao ZIP
                    if file != zip_name and file.endswith('.pdf'):  # Excluir o próprio arquivo zip da compactação
                        zipf.write(file_path, os.path.relpath(file_path, self.folder))
                    
                    # Excluir o arquivo PDF após adicioná-lo ao ZIP
                    if file.endswith('.pdf'):
                        os.remove(file_path)

        print(f"Compactado: {zip_name}")
