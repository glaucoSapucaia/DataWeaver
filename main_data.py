# from pathlib import Path
from dataweaver.settings import config

from dataweaver.data.modules import TableExtractor
import zipfile

# Inicialização do script
if __name__ == "__main__":

    zip_pdf_file = config.scraper.zip_name
    zip_folder = config.dirs.pdfs

    full_path_zip = zip_folder / zip_pdf_file

    with zipfile.ZipFile(full_path_zip, "r") as zip_file:
        zip_file.extractall(zip_folder)

    # Define o diretório raiz do projeto
    ROOT_DIR = config.dirs.root

    # Define e cria o diretório onde os arquivos CSV serão armazenados
    CSV_DIR = ROOT_DIR / "dataweaver" / "data" / "csv"
    CSV_DIR.mkdir(exist_ok=True)

    # Caminho do arquivo PDF que será processado
    PDF_PATH = (
        ROOT_DIR
        / "dataweaver"
        / "scraper"
        / "pdfs"
        / "copy3_of_Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
    )

    # Caminho onde o arquivo CSV extraído será salvo
    CSV_PATH = CSV_DIR / "copy3_of_Anexo_I_Rol_2021RN_465.2021_RN627L.2024.csv"

    # Nome do arquivo ZIP onde o CSV será compactado
    CSV_ZIP_NAME = CSV_DIR / "Anexo_I_Rol.zip"

    # Dicionário de abreviações para renomear colunas do CSV
    abbreviations_dict = {"OD": "Seg. Odontológica", "AMB": "Seg. Ambulatorial"}

    # Instancia o extrator de tabelas e executa o processo
    extractor = TableExtractor(PDF_PATH, CSV_PATH, CSV_ZIP_NAME, abbreviations_dict)
    extractor.run()
