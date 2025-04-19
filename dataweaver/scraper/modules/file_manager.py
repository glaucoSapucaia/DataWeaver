from .interfaces import FileManagerInterface
from dataweaver.settings import logger

from typing import TYPE_CHECKING
import requests
import os

if TYPE_CHECKING:
    from pathlib import Path


class FileDownloader:
    """Responsável por baixar arquivos via HTTP usando a biblioteca requests.

    SOLID:
        Princípio da Responsabilidade Única - foca apenas no download.
    """

    def download_file(self, url: str) -> bytes:
        """Baixa o conteúdo de um arquivo a partir de uma URL.

        Args:
            url: URL completa do arquivo a ser baixado.

        Returns:
            Conteúdo binário do arquivo baixado.

        Raises:
            requests.HTTPError: Se o download falhar (status 4xx/5xx).
        """
        response = requests.get(url, stream=True)
        response.raise_for_status()
        return response.content


class FileSaver:
    """Responsável por operações de salvamento de arquivos no sistema local.

    SOLID:
        Princípio da Responsabilidade Única - foca apenas no armazenamento.
    """

    def __init__(self, folder: "Path") -> None:
        self.folder = folder

    def save_file(self, filename: str, content: bytes) -> "Path":
        """Salva o conteúdo no sistema de arquivos local.

        Args:
            filename: Nome do arquivo a ser salvo.
            content: Conteúdo binário para escrita.

        Returns:
            Path: Caminho completo onde o arquivo foi salvo.
        """
        file_path = self.folder / filename
        with open(file_path, "wb") as file:
            file.write(content)
        return file_path


class FileManager(FileManagerInterface):
    """Orquestra as operações de download e armazenamento de arquivos.

    Padrões de Projeto/SOLID:
        Facade - fornece interface simples para operações complexas
        Injeção de Dependência - aceita componentes downloader/saver
    """

    def __init__(
        self, folder: "Path", downloader: FileDownloader = None, saver: FileSaver = None
    ) -> None:
        """Inicializa o gerenciador de arquivos com dependências.

        Args:
            folder: Diretório alvo para arquivos salvos.
            downloader: (Opcional) Instância de FileDownloader.
            saver: (Opcional) Instância de FileSaver.
        """
        self.folder = folder
        self.downloader = downloader or FileDownloader()
        self.saver = saver or FileSaver(folder)

    def save_file(self, url: str) -> None:
        """Baixa e salva um arquivo a partir de uma URL.

        Args:
            url: URL completa do arquivo para download/salvamento.

        Raises:
            Exception: Propaga quaisquer erros de download/salvamento.
            Logs com informações detalhadas em caso de erro.
        """
        try:
            filename = os.path.basename(url)
            content = self.downloader.download_file(url)
            saved_path = self.saver.save_file(filename, content)
            logger.info(f"Arquivo baixado com sucesso: {saved_path.name[:30]}...")
        except Exception as e:
            logger.error(
                f"Erro ao baixar/salvar {os.path.basename(url)[:30]}...: {str(e)}"
            )
            raise
