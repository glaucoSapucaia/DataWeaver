from abc import ABC, abstractmethod


class PDFRemoveInterface(ABC):
    """Interface para remoção segura de PDFs locais."""

    @abstractmethod
    def remove_pdfs(self) -> None:
        """Remove todos os PDFs baixados durante o processamento."""
        pass
