"""
Módulo principal para execução do serviço de processamento de PDFs.

Este script atua como ponto de entrada da aplicação. Ele utiliza uma fábrica
para instanciar o serviço de processamento de PDFs, que realiza as seguintes etapas:
1. Busca de links de arquivos PDF em uma URL configurada.
2. Download dos arquivos encontrados.
3. Compactação dos arquivos em um arquivo .zip.
4. Remoção dos arquivos PDF originais após a compactação.

Todos os eventos importantes são registrados no sistema de logging configurado.
"""

from dataweaver.logger import logger
from dataweaver.scraper.modules import PDFProcessingServiceFactory
from dataweaver.config import URL

if __name__ == "__main__":
    """
    Ponto de entrada da aplicação.

    Inicializa e executa o serviço de processamento de PDFs, utilizando os parâmetros
    definidos no arquivo de configuração. O progresso é registrado por meio de logs.
    """
    logger.info("Iniciando o serviço de processamento de PDFs...")

    service = PDFProcessingServiceFactory.create()

    logger.info("Executando o processo de coleta e compactação dos PDFs...")
    service.process(URL)
    logger.info("Processamento concluído!")
