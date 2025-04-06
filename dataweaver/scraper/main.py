"""
Módulo principal para execução do serviço de processamento de PDFs.
"""

from logger import logger
from modules import PDFProcessingServiceFactory
from config import URL

if __name__ == "__main__":
    """
    Ponto de entrada da aplicação.
    """
    logger.info("Iniciando o serviço de processamento de PDFs...")

    service = PDFProcessingServiceFactory.create()

    logger.info("Executando o processo de coleta e compactação dos PDFs...")
    service.process(URL)
    logger.info("Processamento concluído!")
