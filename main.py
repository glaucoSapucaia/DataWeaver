from dataweaver.settings import config, logger
from dataweaver.scraper.modules import DefaultPDFServiceFactory
from dataweaver.utils.zip_extractor import zip_file_extractor
from dataweaver.data.modules import TableExtractor

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
    logger.info("Processamento de PDFs concluído!")

    # Caminho completo do arquivo ZIP gerado
    full_path_zip = pdfs_dir / zip_name

    logger.info("Extraindo arquivos do ZIP...")
    zip_file_extractor(full_path_zip, pdfs_dir)
    logger.info("Extração concluída!")

    # Define e cria o diretório onde os arquivos CSV serão armazenados
    csv_dir = config.dirs.csv
    csv_dir.mkdir(exist_ok=True)

    # Caminho do arquivo PDF que será processado
    pdf_file = pdfs_dir / "copy3_of_Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"

    # Caminho onde o arquivo CSV extraído será salvo
    csv_file = csv_dir / "copy3_of_Anexo_I_Rol_2021RN_465.2021_RN627L.2024.csv"

    # Nome do arquivo ZIP onde o CSV será compactado
    csv_zip_file = csv_dir / config.data.zip_name

    # Dicionário de abreviações para renomear colunas do CSV
    abbreviations_dict = {"OD": "Seg. Odontológica", "AMB": "Seg. Ambulatorial"}

    logger.info("Iniciando extração de dados da tabela do PDF...")
    extractor = TableExtractor(pdf_file, csv_file, csv_zip_file, abbreviations_dict)
    extractor.run()
    logger.info("Extração de dados concluída com sucesso!")
