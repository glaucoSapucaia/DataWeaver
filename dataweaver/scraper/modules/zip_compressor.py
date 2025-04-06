from .interfaces import ZipCompressorInterface, PDFRemoveInterface
from logger import logger
from typing import TYPE_CHECKING
import zipfile

if TYPE_CHECKING:
    from pathlib import Path

class ZipCompressor(ZipCompressorInterface):
    def __init__(self, folder: 'Path') -> None:
        """
        Inicializa o compressor ZIP com o diretório onde os arquivos estão localizados.
        
        Parâmetros:
            folder (Path): Caminho da pasta que contém os arquivos a serem compactados.
            pdf_remove (PDFRemoverInterface): Instância responsável por remover os arquivos PDF.
        """
        self.folder = folder

    def create_zip(self, zip_name: str) -> None:
        """Compacta todos os arquivos da pasta em um arquivo ZIP."""
        try:
            zip_path = self._get_zip_path(zip_name)
            self._compress_files(zip_path)
            logger.info(f"Compactado: {zip_name}")
        except Exception as e:
            logger.error(f"Erro ao criar o ZIP {zip_name}: {e}")

    def _get_zip_path(self, zip_name: str) -> 'Path':
        """Retorna o caminho completo para o arquivo ZIP."""
        return self.folder / zip_name

    def _compress_files(self, zip_path: 'Path') -> None:
        """Realiza a compressão dos arquivos da pasta em um arquivo ZIP."""
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in self._get_pdf_files():
                    try:
                        zipf.write(file_path, file_path.relative_to(self.folder))
                        logger.info(f"Arquivo adicionado: {file_path.name}")
                    except Exception as e:
                        logger.warning(f"Erro ao adicionar {file_path.name} ao ZIP: {e}")
        except Exception as e:
            logger.error(f"Erro ao criar o arquivo ZIP {zip_path.name}: {e}")
            raise

    def _get_pdf_files(self) -> list['Path']:
        """Obtém apenas os arquivos PDF da pasta."""
        try:
            return [file for file in self.folder.rglob('*.pdf') if file.is_file()]
        except Exception as e:
            logger.error(f"Erro ao buscar arquivos PDF: {e}")
            return []

class PDFRemove(PDFRemoveInterface):
    def __init__(self, folder: 'Path') -> None:
        self.folder = folder

    def remove_pdfs(self) -> None:
        """Remove arquivos PDF após a compactação."""
        try:
            for pdf_file in self.folder.rglob("*.pdf"):
                try:
                    pdf_file.unlink()
                    logger.info(f"Arquivo excluído: {pdf_file.name}")
                except Exception as e:
                    logger.warning(f"Erro ao excluir {pdf_file.name}: {e}")
        except Exception as e:
            logger.error(f"Erro ao buscar arquivos PDF para exclusão: {e}")
