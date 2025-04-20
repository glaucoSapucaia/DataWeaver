from .interfaces import PDFRemoveInterface

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


class PDFRemove(PDFRemoveInterface):
    """Responsável por limpar arquivos PDF após processamento.

    SOLID:
        Single Responsibility Principle - foca apenas na remoção
    """

    def __init__(self, folder: "Path") -> None:
        self.folder = folder

    def remove_pdfs(self) -> None:
        """Remove todos os arquivos PDF do diretório."""
        try:
            for pdf_file in self.folder.glob("*.pdf"):
                try:
                    pdf_file.unlink()
                except Exception as e:
                    raise
        except Exception as e:
            raise
