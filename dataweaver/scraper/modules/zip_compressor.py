"""
Módulo responsável pela compactação de arquivos PDF em um único arquivo ZIP
e pela remoção dos PDFs após o processo.

Contém as classes:
- ZipCompressor: compacta arquivos PDF encontrados em um diretório.
- PDFRemove: remove arquivos PDF de um diretório.
"""

from .interfaces import ZipCompressorInterface, PDFRemoveInterface
from dataweaver.config.logger import logger
from typing import TYPE_CHECKING
import zipfile

if TYPE_CHECKING:
    from pathlib import Path  # pragma: no cover


class ZipCompressor(ZipCompressorInterface):
    """
    Classe responsável por compactar arquivos PDF em um único arquivo ZIP.
    """

    def __init__(self, folder: "Path") -> None:
        """
        Inicializa o compressor ZIP com o diretório onde os arquivos estão localizados.

        Parâmetros:
            folder (Path): Caminho da pasta que contém os arquivos a serem compactados.
        """
        self.folder = folder

    def create_zip(self, zip_name: str) -> None:
        """
        Compacta todos os arquivos PDF do diretório em um arquivo ZIP.

        Parâmetros:
            zip_name (str): Nome do arquivo ZIP de destino.
        """
        try:
            zip_path = self._get_zip_path(zip_name)
            self._compress_files(zip_path)
            logger.info(f"Compactado: {zip_name}")
        except Exception as e:
            logger.error(f"Erro ao criar o ZIP {zip_name}: {e}")

    def _get_zip_path(self, zip_name: str) -> "Path":
        """
        Gera o caminho completo do arquivo ZIP com base no nome fornecido.

        Parâmetros:
            zip_name (str): Nome do arquivo ZIP.

        Retorno:
            Path: Caminho completo do arquivo ZIP.
        """
        return self.folder / zip_name

    def _compress_files(self, zip_path: "Path") -> None:
        """
        Adiciona os arquivos PDF encontrados no diretório ao arquivo ZIP.

        Parâmetros:
            zip_path (Path): Caminho do arquivo ZIP que será criado.
        """
        try:
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for file_path in self._get_pdf_files():
                    try:
                        zipf.write(file_path, file_path.relative_to(self.folder))
                        logger.info(f"Arquivo adicionado: {file_path.name[:10]}")
                    except Exception as e:
                        logger.warning(
                            f"Erro ao adicionar {file_path.name} ao ZIP: {e}"
                        )
        except Exception as e:
            logger.error(f"Erro ao criar o arquivo ZIP {zip_path.name}: {e}")
            raise

    def _get_pdf_files(self) -> list["Path"]:
        """
        Recupera todos os arquivos PDF do diretório.

        Retorno:
            list[Path]: Lista de caminhos de arquivos PDF encontrados.
        """
        try:
            return [file for file in self.folder.rglob("*.pdf") if file.is_file()]
        except Exception as e:
            logger.error(f"Erro ao buscar arquivos PDF: {e}")
            return []


class PDFRemove(PDFRemoveInterface):
    """
    Classe responsável por remover arquivos PDF de um diretório após o processamento.
    """

    def __init__(self, folder: "Path") -> None:
        """
        Inicializa o removedor de PDFs com o diretório onde os arquivos estão localizados.

        Parâmetros:
            folder (Path): Caminho da pasta que contém os arquivos PDF.
        """
        self.folder = folder

    def remove_pdfs(self) -> None:
        """
        Remove todos os arquivos PDF encontrados no diretório.
        """
        try:
            for pdf_file in self.folder.rglob("*.pdf"):
                try:
                    pdf_file.unlink()
                    logger.info(f"Arquivo excluído: {pdf_file.name[:10]}")
                except Exception as e:
                    logger.warning(f"Erro ao excluir {pdf_file.name}: {e}")
        except Exception as e:
            logger.error(f"Erro ao buscar arquivos PDF para exclusão: {e}")
