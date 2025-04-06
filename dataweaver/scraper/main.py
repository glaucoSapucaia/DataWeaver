"""
Este script inicializa e executa o serviço de processamento de PDFs.
Ele utiliza o padrão de design Factory para criar a instância do serviço
e executar o processamento de acordo com os parâmetros configurados.
"""

from logger import logger
from modules import PDFProcessingServiceFactory
from config import URL

if __name__ == "__main__":
    logger.info("Iniciando o serviço de processamento de PDFs...")
    
    # Criação do serviço usando a fábrica
    service = PDFProcessingServiceFactory.create()
    
    # Execução do processo de obtenção e compactação dos PDFs
    logger.info("Executando o processo de coleta e compactação dos PDFs...")
    service.process(URL)
    logger.info("Processamento concluído!")
