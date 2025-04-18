from .interfaces import ZipCompressorInterface, PDFRemoveInterface
from dataweaver.settings import logger

from typing import TYPE_CHECKING
import zipfile

if TYPE_CHECKING:
    from pathlib import Path


class ZipCompressor(ZipCompressorInterface):
    """Responsável por compactar arquivos PDF em um arquivo ZIP.

    SOLID:
        Single Responsibility Principle - foca apenas na compressão
    """

    def __init__(self, folder: "Path") -> None:
        self.folder = folder

    def create_zip(self, zip_name: str) -> None:
        """Cria arquivo ZIP contendo todos os PDFs do diretório.

        Args:
            zip_name: Nome do arquivo ZIP

        Raises:
            Exception: Se ocorrer erro durante a compressão
            Logs dos detalhes do processo
        """
        try:
            zip_path = self._get_zip_path(zip_name)
            self._compress_files(zip_path)
            logger.info(f"Arquivo {zip_name} criado com sucesso")
        except Exception as e:
            logger.error(f"Falha ao criar {zip_name}: {e}")
            raise

    def _get_zip_path(self, zip_name: str) -> "Path":
        """Gera o Path completo para o arquivo ZIP.

        Args:
            zip_name: Nome base do arquivo

        Returns:
            Path completo
        """
        return self.folder / f"{zip_name}"

    def _compress_files(self, zip_path: "Path") -> None:
        """Adiciona PDFs ao arquivo ZIP.

        Args:
            zip_path: Localização do arquivo ZIP a ser criado

        Note:
            Ignora arquivos problemáticos individualmente
        """
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in self._get_pdf_files():
                try:
                    arcname = file_path.relative_to(self.folder)
                    zipf.write(file_path, arcname)
                    logger.debug(f"Adicionado: {arcname}")
                except Exception as e:
                    logger.warning(f"Pulando {file_path.name}: {e}")

    def _get_pdf_files(self) -> list["Path"]:
        """Lista todos os PDFs no diretório.

        Returns:
            Lista de Paths para arquivos .pdf

        Raises:
            Exception: Se não conseguir ler o diretório
        """
        try:
            return [f for f in self.folder.glob("*.pdf") if f.is_file()]
        except Exception as e:
            logger.error(f"Falha ao listar PDFs: {e}")
            raise


class ZipCompressorDecorator(ZipCompressorInterface):
    """Classe base para decoradores de compressão.

    Padrão de Projeto:
        Decorator - permite adicionar comportamentos dinamicamente
    """

    def __init__(self, compressor: ZipCompressorInterface) -> None:
        """Inicializa com o compressor a ser decorado.

        Args:
            compressor: Instância de ZipCompressorInterface
        """
        self._compressor = compressor

    def create_zip(self, zip_name: str) -> None:
        """Delega a operação para o compressor interno.

        Args:
            zip_name: Nome do arquivo ZIP
        """
        self._compressor.create_zip(zip_name)


class LoggingZipCompressor(ZipCompressorDecorator):
    """Decorador que adiciona logs detalhados ao processo.

    Padrão de Projeto:
        Decorator - estende funcionalidade sem modificar a classe original
    """

    def create_zip(self, zip_name: str) -> None:
        """Adiciona logs antes e após a compressão.

        Args:
            zip_name: Nome do arquivo ZIP
        """
        logger.info(f"[DECORATOR] Iniciando compressão: {zip_name}")
        super().create_zip(zip_name)
        logger.info(f"[DECORATOR] Compressão finalizada: {zip_name}")


class ValidationZipCompressor(ZipCompressorDecorator):
    """Decorador que valida o nome do arquivo ZIP.

    Padrão de Projeto:
        Decorator - adiciona validação prévia
    """

    def create_zip(self, zip_name: str) -> None:
        """Valida se o nome termina com .zip antes de comprimir.

        Args:
            zip_name: Nome do arquivo ZIP

        Raises:
            ValueError: Se o nome for inválido
        """
        if not zip_name.endswith(".zip"):
            raise ValueError("O nome do arquivo deve terminar com .zip")
        super().create_zip(zip_name)


class PDFRemove(PDFRemoveInterface):
    """Responsável por limpar arquivos PDF após processamento.

    SOLID:
        Single Responsibility Principle - foca apenas na remoção
    """

    def __init__(self, folder: "Path") -> None:
        self.folder = folder

    def remove_pdfs(self) -> None:
        """Remove todos os arquivos PDF do diretório.

        Note:
            Continua processo mesmo se alguns arquivos falharem
            Logs para cada operação individual
        """
        try:
            for pdf_file in self.folder.glob("*.pdf"):
                try:
                    pdf_file.unlink()
                    logger.info(f"Removido: {pdf_file.name}")
                except Exception as e:
                    logger.warning(f"Falha ao remover {pdf_file.name}: {e}")
        except Exception as e:
            logger.error(f"Erro geral ao limpar PDFs: {e}")
            raise
