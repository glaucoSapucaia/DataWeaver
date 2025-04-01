from modules import PDFProcessingService
from config import PDFS_DIR

if __name__ == "__main__":
    url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"  # Substitua pelo site desejado
    _filter = "ANEXO"  # Ajuste conforme necessário
    folder = PDFS_DIR
    zip_name = "pdfs_compactados.zip"
    
    service = PDFProcessingService(folder, zip_name)

    service.process(url, _filter)