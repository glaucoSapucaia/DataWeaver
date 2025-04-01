from .interfaces import FileManagerInterface
from typing import TYPE_CHECKING
import os
import requests

if TYPE_CHECKING:
    from pathlib import Path

class FileManager(FileManagerInterface):
    """Gerencia operações de manipulação de arquivos, como download e compactação."""
    
    def __init__(self, folder: 'Path') -> None:
        """
        Inicializa o gerenciador de arquivos e garante que o diretório existe.
        
        Parâmetros:
            folder (str): Caminho da folder onde os arquivos serão armazenados.
        """
        self.folder = folder
        os.makedirs(self.folder, exist_ok=True)
    
    def save_file(self, url: str) -> None:
        """
        Faz o download do arquivo e salva na folder especificada.
        
        Parâmetros:
            url (str): URL do arquivo a ser baixado.
        """
        file_name = os.path.join(self.folder, os.path.basename(url))
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        
        print(f"Baixado: {file_name}")