from .interfaces import ZipCompressorInterface
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

    def create_zip(self, zip_name: str, file_extension: str) -> None:
        """Cria arquivo ZIP contendo todos os PDFs do diretório.

        Args:
            zip_name: Nome do arquivo ZIP
            file_extension: Extensão do arquivos (PDF ou CSV)

        Raises:
            Exception: Se ocorrer erro durante a compressão
            Logs dos detalhes do processo
        """
        try:
            zip_path = self._get_zip_path(zip_name)
            self._compress_files(zip_path, file_extension)
            logger.info(f"Arquivo CSV criado com sucesso.")
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

    def _compress_files(self, zip_path: "Path", extension: str) -> None:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in self._get_files_by_extension(extension):
                try:
                    arcname = file_path.relative_to(self.folder)
                    zipf.write(file_path, arcname)
                    logger.debug(f"Adicionado: {arcname}")
                except Exception as e:
                    logger.warning(f"Pulando {file_path.name}: {e}")
                    raise

    def _get_files_by_extension(self, extension: str) -> list["Path"]:
        try:
            return [f for f in self.folder.glob(f"*.{extension}") if f.is_file()]
        except Exception as e:
            logger.error(f"Falha ao listar {extension.upper()}s: {e}")
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

    def create_zip(self, zip_name: str, file_extension: str) -> None:
        """Delega a operação para o compressor interno."""
        self._compressor.create_zip(zip_name, file_extension)


class LoggingZipCompressor(ZipCompressorDecorator):
    """Decorador que adiciona logs detalhados ao processo.

    Padrão de Projeto:
        Decorator - estende funcionalidade sem modificar a classe original
    """

    def create_zip(self, zip_name: str, file_extension: str) -> None:
        """Adiciona logs antes e após a compressão."""
        logger.info(f"[DECORATOR] Iniciando compressão do CSV...")
        super().create_zip(zip_name, file_extension)
        logger.info(f"[DECORATOR] Compressão do CSV finalizada.")


class ValidationZipCompressor(ZipCompressorDecorator):
    """Decorador que valida o nome do arquivo ZIP.

    Padrão de Projeto:
        Decorator - adiciona validação prévia
    """

    def create_zip(self, zip_name: str, file_extension: str) -> None:
        """Valida se o nome termina com .zip antes de comprimir.

        Raises:
            ValueError: Se o nome for inválido
        """
        if not str(zip_name).endswith(".zip"):
            raise ValueError("O nome do arquivo deve terminar com .zip")
        super().create_zip(zip_name, file_extension)
