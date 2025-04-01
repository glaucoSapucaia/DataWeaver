from .interfaces import PDFProcessingServiceInterface
from .pdf_scraper import RequestsPDFScraper
from .file_manager import FileManager
from .zip_compressor import ZipCompressor

class PDFProcessingService(PDFProcessingServiceInterface):
    def __init__(self, folder, nome_zip: str) -> None:
        """
        Inicializa o serviço de processamento de PDFs.
        
        Parâmetros:
            scraper (PDFScraper): Instância de um scraper para buscar os PDFs.
            file_manager (FileManager): Instância do gerenciador de arquivos.
            nome_zip (str): Nome do arquivo ZIP final.
        """
        self.scraper = RequestsPDFScraper()
        self.file_manager = FileManager(folder)
        self.nome_zip = nome_zip
        self.zip_compressor = ZipCompressor(folder)
    
    def process(self, url: str, _filter: str) -> None:
        """
        Executa todo o fluxo de busca, download e compactação dos PDFs.
        
        Parâmetros:
            url (str): URL da página onde os PDFs estão localizados.
            filtro (str): Palavra-chave para filtrar os PDFs desejados.
        """
        print("Buscando PDFs...")
        pdf_links = self.scraper.get_pdf_links(url, _filter)
        
        if not pdf_links:
            print("Nenhum PDF encontrado.")
            return
        
        print("Baixando PDFs...")
        for link in pdf_links:
            self.file_manager.save_file(link)
        
        print("Compactando arquivos...")
        self.zip_compressor.create_zip(self.nome_zip)
        
        print("Processo concluído!")