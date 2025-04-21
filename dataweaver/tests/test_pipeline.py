import pytest
from unittest.mock import patch, MagicMock

from dataweaver.pipeline import PDFProcessor, CSVExtractor, CleanupManager


def test_pdf_processor_run_executes_process():
    """Garante que PDFProcessor executa o serviço de scraping corretamente."""
    with patch("dataweaver.pipeline.DefaultPDFServiceFactory") as mock_factory:
        mock_service = MagicMock()
        mock_factory.return_value.create_service.return_value = mock_service

        processor = PDFProcessor()
        processor.run()

        mock_factory.assert_called_once()
        mock_factory.return_value.create_service.assert_called_once()
        mock_service.process.assert_called_once_with(processor.url)


def test_csv_extractor_requires_pdf_file():
    """Verifica que um erro é levantado se o PDF não for configurado antes do run()."""
    extractor = CSVExtractor()

    with pytest.raises(ValueError, match="PDF file not set"):
        extractor.run()


def test_csv_extractor_run_executes_extraction(tmp_path):
    """Testa se o CSVExtractor executa a extração corretamente após set_pdf_file()."""
    with patch("dataweaver.pipeline.TableExtractor") as mock_extractor:
        extractor = CSVExtractor()
        extractor.csv_dir = tmp_path  # Evita escrita em disco real
        extractor.set_pdf_file("documento.pdf")

        extractor.run()

        mock_extractor.assert_called_once()
        mock_extractor.return_value.run.assert_called_once()


def test_cleanup_manager_run_removes_pdfs():
    """Garante que CleanupManager chama corretamente a remoção de PDFs."""
    with patch("dataweaver.pipeline.PDFRemove") as mock_pdf_remove:
        manager = CleanupManager()
        manager.run()

        mock_pdf_remove.assert_called_once_with(manager.pdfs_dir)
        mock_pdf_remove.return_value.remove_pdfs.assert_called_once()
