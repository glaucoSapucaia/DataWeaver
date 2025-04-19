from dataweaver.settings import *
from dataweaver.scraper.modules import DefaultPDFServiceFactory

# Configurações do usuário

url = config.scraper.url
zip_name = config.scraper.zip_name
key_filter = config.scraper.filter

pdfs_dir = config.dirs.pdfs


if __name__ == "__main__":
    logger.info("Iniciando o serviço de processamento de PDFs...")

    # Cria a factory com as configurações necessárias
    factory = DefaultPDFServiceFactory(pdfs_dir, key_filter)

    # Cria o serviço
    service = factory.create_service(zip_name)

    logger.info("Executando o processo de coleta e compactação dos PDFs...")
    service.process(url)
    logger.info("Processamento concluído!")
