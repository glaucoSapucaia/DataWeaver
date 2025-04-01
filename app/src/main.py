"""
Este script inicializa e executa o serviço de processamento de PDFs.
Ele utiliza o padrão de design Factory para criar a instância do serviço
e executar o processamento de acordo com os parâmetros configurados.
"""

from modules import PDFProcessingServiceFactory
from config import URL, FILTER

if __name__ == "__main__":
    """
    Função principal do programa. Cria uma instância do serviço de processamento de PDFs
    através da fábrica e executa o processo de busca, download e compactação dos PDFs 
    com base na URL e no filtro fornecido.
    """
    
    # Criação do serviço usando a fábrica
    service = PDFProcessingServiceFactory.create()
    
    # Execução do processo de obtenção e compactação dos PDFs
    service.process(URL, FILTER)
