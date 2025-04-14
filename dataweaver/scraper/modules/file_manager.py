"""
Módulo responsável pelo gerenciamento de arquivos, incluindo download e salvamento local.
"""

from .interfaces import FileManagerInterface
from typing import TYPE_CHECKING
from logger import logger
import requests  # type: ignore
import os

if TYPE_CHECKING:
    from pathlib import Path  # pragma: no cover

class FileManager(FileManagerInterface):
    """
    Gerenciador de arquivos responsável por baixar e salvar arquivos em disco.

    Responsabilidades:
    - Garantir que o diretório de destino esteja disponível.
    - Baixar arquivos PDF a partir de URLs.
    - Salvar arquivos com segurança.
    """

    def __init__(self, folder: 'Path') -> None:
        """
        Inicializa o gerenciador com a pasta onde os arquivos serão armazenados.

        Parâmetros:
            folder (Path): Caminho do diretório onde os arquivos serão salvos.
        """
        self.folder = folder

    def save_file(self, url: str) -> None:
        """
        Realiza o download de um arquivo a partir de uma URL e o salva no diretório configurado.

        Parâmetros:
            url (str): Endereço do arquivo a ser baixado.
        """
        file_name = os.path.join(self.folder, os.path.basename(url))
        file_downloaded = os.path.basename(url)

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(file_name, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            logger.info(f"Arquivo baixado com sucesso: {file_downloaded[:30]}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao baixar o arquivo {url}: {e}")
        except Exception as e:
            logger.error(f"Erro ao salvar o arquivo {file_downloaded}: {e}")
