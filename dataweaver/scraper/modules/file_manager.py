from .interfaces import FileManagerInterface
from dataweaver.settings import logger

from typing import TYPE_CHECKING
import requests
import os

if TYPE_CHECKING:
    from pathlib import Path


class FileDownloader:
    def download_file(self, url: str) -> bytes:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        return response.content


class FileSaver:
    def __init__(self, folder: "Path"):
        self.folder = folder

    def save_file(self, filename: str, content: bytes):
        file_path = self.folder / filename
        with open(file_path, "wb") as file:
            file.write(content)
        return file_path


class FileManager(FileManagerInterface):
    def __init__(
        self, folder: "Path", downloader: FileDownloader = None, saver: FileSaver = None
    ):
        self.folder = folder
        self.downloader = downloader or FileDownloader()
        self.saver = saver or FileSaver(folder)

    def save_file(self, url: str) -> None:
        try:
            filename = os.path.basename(url)
            content = self.downloader.download_file(url)
            self.saver.save_file(filename, content)
            logger.info(f"Arquivo baixado com sucesso: {filename[:30]}")
        except Exception as e:
            logger.error(f"Erro ao baixar/salvar o arquivo {url}: {e}")
            raise
