"""
Pipeline Scraper - Fluxo Completo de Processamento
"""

from .interfaces import PDFProcessingServiceInterface
from .zip_compressor import ValidationZipCompressor, LoggingZipCompressor
from dataweaver.settings import logger

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interfaces import (
        PDFScraperInterface,
        FileManagerInterface,
        ZipCompressorInterface,
    )


class PDFProcessingService(PDFProcessingServiceInterface):
    """Coordena o fluxo completo de processamento de arquivos PDF.

    Padrão de Projeto/SOLID:
        Facade - fornece uma interface simplificada para um subsistema complexo
        Dependency Injection - recebe dependências via construtor

    Responsabilidades:
        1. Extração de links PDF
        2. Download dos arquivos
        3. Compactação em ZIP
    """

    def __init__(
        self,
        zip_name: str,
        file_extension: str,
        scraper: "PDFScraperInterface",
        file_manager: "FileManagerInterface",
        zip_compressor: "ZipCompressorInterface",
    ) -> None:
        """Inicializa o serviço com seus componentes.

        Args:
            zip_name: Nome do arquivo ZIP de saída
            file_extension: Extensão do arqvuio alvo (pdf)
            scraper: Componente para extração de links PDF
            file_manager: Componente para download de arquivos
            zip_compressor: Será automaticamente decorado com
                            Validation + Logging decorators
        """
        self.zip_name = zip_name
        self.file_extension = file_extension
        self.scraper = scraper
        self.file_manager = file_manager

        # Uso de Decorators
        self.zip_compressor = ValidationZipCompressor(
            LoggingZipCompressor(zip_compressor)
        )

    def process(self, url: str) -> None:
        """Executa o pipeline completo de processamento de PDFs.

        Fluxo:
            1. Extrai links de PDFs da URL fornecida
            2. Baixa cada arquivo individualmente
            3. Compacta todos em um único ZIP

        Args:
            url: URL da página contendo os PDFs

        Raises:
            Exception: Registra erros no logger mas não interrompe o fluxo
            Logs de informações detalhadas em cada etapa

        Exemplo:
            >>> service = PDFProcessingService(...)
            >>> service.process("http://exemplo.com/pdfs")
        """
        try:
            logger.info("Iniciando busca por PDFs...")
            pdf_links = self.scraper.get_pdf_links(url)

            if not pdf_links:
                logger.warning("Nenhum PDF encontrado na página.")
                return

            logger.info(f"Iniciando download de {len(pdf_links)} PDFs...")
            for link in pdf_links:
                try:
                    self.file_manager.save_file(link)
                except Exception as e:
                    logger.error(f"Falha no download: {link} - Erro: {str(e)}")
                    continue

            logger.info("Compactando arquivos...")
            self.zip_compressor.create_zip(self.zip_name, self.file_extension)

        except Exception as e:
            logger.critical(f"Falha crítica no processamento: {str(e)}")
            raise
