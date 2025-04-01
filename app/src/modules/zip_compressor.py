from .interfaces import ZipCompressorInterface
import os
import zipfile

class ZipCompressor(ZipCompressorInterface):
    def __init__(self, folder: str) -> None:
        """
        Inicializa o compressor ZIP com o diretório onde os arquivos estão localizados.
        
        Parâmetros:
            folder (str): Caminho da folder que contém os arquivos a serem compactados.
        """
        self.folder = folder

    def create_zip(self, nome_zip: str) -> None:
        """
        Compacta todos os arquivos da folder em um arquivo ZIP.
        
        Parâmetros:
            nome_zip (str): Nome do arquivo ZIP gerado.
        """
        zip_path = os.path.join(self.folder, nome_zip)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(self.folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    # Adicionar o arquivo ao ZIP
                    if file != nome_zip and file.endswith('.pdf'):  # Excluir o próprio arquivo zip
                        zipf.write(file_path, os.path.relpath(file_path, self.folder))
                    
                    # Excluir o arquivo PDF após adicioná-lo ao ZIP
                    if file.endswith('.pdf'):
                        os.remove(file_path)

        print(f"Compactado: {nome_zip}")
