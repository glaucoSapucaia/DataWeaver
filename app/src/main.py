from modules import PDFProcessingService

if __name__ == "__main__":
    url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"  # Substitua pelo site desejado
    _filter = "ANEXO"  # Ajuste conforme necessário
    folder = "pdfs"
    nome_zip = "pdfs_compactados.zip"
    
    service = PDFProcessingService(folder, nome_zip)

    service.process(url, _filter)