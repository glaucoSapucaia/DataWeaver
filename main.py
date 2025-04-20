from dataweaver.pipeline import PDFProcessor, CSVExtractor, CleanupManager
from dataweaver.settings import logger, config


def main():
    try:
        # Processa os PDFs
        pdf_processor = PDFProcessor()
        pdf_processor.run()

        # Extrai dados para CSV (substitua pelo nome real do arquivo PDF baixado)
        csv_extractor = CSVExtractor()
        csv_extractor.set_pdf_file(config.data.target_file)
        csv_extractor.run()

        # Limpeza final
        cleanup = CleanupManager()
        cleanup.run()

        logger.info("Processo concluído com sucesso!")
    except Exception as e:
        logger.error(f"Erro durante a execução: {str(e)}")
        raise


if __name__ == "__main__":
    main()
