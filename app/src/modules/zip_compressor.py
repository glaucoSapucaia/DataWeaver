from .interfaces import ZipCompressorInterface, PDFRemoveInterface
from typing import TYPE_CHECKING
import zipfile
from pathlib import Path
import os

if TYPE_CHECKING:
    from pathlib import Path

class ZipCompressor(ZipCompressorInterface):
    def __init__(self, folder: 'Path', pdf_remover: PDFRemoveInterface) -> None:
        """
        Inicializa o compressor ZIP com o diretório onde os arquivos estão localizados.
        
        Parâmetros:
            folder (Path): Caminho da pasta que contém os arquivos a serem compactados.
            pdf_remover (PDFRemoverInterface): Instância responsável por remover os arquivos PDF.
        """
        self.folder = folder
        self.pdf_remover = pdf_remover

    def create_zip(self, zip_name: str) -> None:
        """Compacta todos os arquivos da pasta em um arquivo ZIP."""
        zip_path = self._get_zip_path(zip_name)
        self._compress_files(zip_path)
        self.pdf_remover.remove_pdfs(self.folder)
        print(f"Compactado: {zip_name}")

    def _get_zip_path(self, zip_name: str) -> Path:
        """Retorna o caminho completo para o arquivo ZIP."""
        return self.folder / zip_name

    def _compress_files(self, zip_path: Path) -> None:
        """Realiza a compressão dos arquivos da pasta em um arquivo ZIP."""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(self.folder):
                for file in files:
                    if file.endswith('.pdf') and file != zip_path.name:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, self.folder))

class PDFRemove(PDFRemoveInterface):
    def remove_pdfs(self, folder: Path) -> None:
        """Remove arquivos PDF após a compactação."""
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith('.pdf'):
                    os.remove(os.path.join(root, file))
                    print(f"Arquivo excluído: {file}")