from .interfaces import (FileManagerInterface, PDFProcessingServiceInterface,
                         PDFScraperInterface, ZipCompressorInterface, PDFRemoveInterface)

class PDFProcessingService(PDFProcessingServiceInterface):
    def __init__(self, zip_name: str,
                 scraper: PDFScraperInterface,
                 file_manager: FileManagerInterface,
                 zip_compressor: ZipCompressorInterface,
                 pdf_remove: PDFRemoveInterface) -> None:
        """
        Inicializa o serviço de processamento de PDFs.
        
        Parâmetros:
            scraper (PDFScraper): Instância de um scraper para buscar os PDFs.
            file_manager (FileManager): Instância do gerenciador de arquivos.
            zip_name (str): Nome do arquivo ZIP final.
        """
        self.zip_name = zip_name
        self.scraper = scraper
        self.file_manager = file_manager
        self.zip_compressor = zip_compressor
        self.pdf_remove = pdf_remove
    
    def process(self, url: str) -> None:
        """
        Executa todo o fluxo de busca, download e compactação dos PDFs.
        
        Parâmetros:
            url (str): URL da página onde os PDFs estão localizados.
            keyword (str): Palavra-chave para filtrar os PDFs desejados.
        """
        print("Buscando PDFs...")
        pdf_links = self.scraper.get_pdf_links(url)
        
        if not pdf_links:
            print("Nenhum PDF encontrado.")
            return
        
        print("Baixando PDFs...")
        for link in pdf_links:
            self.file_manager.save_file(link)
        
        print("Compactando arquivos...")
        self.zip_compressor.create_zip(self.zip_name)

        print('Excluindo arquivos baixados...')
        self.pdf_remove.remove_pdfs()
        
        print("Processo concluído!")
