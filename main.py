from dataweaver.settings import *
from dataweaver.scraper.modules import PDFProcessingServiceFactory

url = config.scraper.url

if __name__ == "__main__":
    """
    Ponto de entrada da aplicação.

    Inicializa e executa o serviço de processamento de PDFs, utilizando os parâmetros
    definidos no arquivo de configuração. O progresso é registrado por meio de logs.
    """
    logger.info("Iniciando o serviço de processamento de PDFs...")

    service = PDFProcessingServiceFactory.create()

    logger.info("Executando o processo de coleta e compactação dos PDFs...")
    service.process(url)
    logger.info("Processamento concluído!")
