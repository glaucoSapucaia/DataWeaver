from .interfaces import FileManagerInterface
import os
import requests

class FileManager(FileManagerInterface):
    """Gerencia operações de manipulação de arquivos, como download e compactação."""
    
    def __init__(self, pasta: str) -> None:
        """
        Inicializa o gerenciador de arquivos e garante que o diretório existe.
        
        Parâmetros:
            pasta (str): Caminho da pasta onde os arquivos serão armazenados.
        """
        self.pasta = pasta
        os.makedirs(self.pasta, exist_ok=True)
    
    def save_file(self, url: str) -> None:
        """
        Faz o download do arquivo e salva na pasta especificada.
        
        Parâmetros:
            url (str): URL do arquivo a ser baixado.
        """
        nome_arquivo = os.path.join(self.pasta, os.path.basename(url))
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(nome_arquivo, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        
        print(f"Baixado: {nome_arquivo}")