from dataweaver.utils.interfaces import PDFRemoveInterface
from dataweaver.utils import PDFRemove

from pathlib import Path
from tempfile import TemporaryDirectory


def test_pdfremove_implements_interface():
    assert issubclass(PDFRemove, PDFRemoveInterface)


def test_remove_pdfs_deletes_all_pdf_files():
    with TemporaryDirectory() as tmp_dir:
        # Cria alguns arquivos PDF e não-PDF para teste
        pdf_files = [
            Path(tmp_dir) / "test1.pdf",
            Path(tmp_dir) / "test2.pdf",
        ]
        non_pdf_files = [
            Path(tmp_dir) / "document.txt",
            Path(tmp_dir) / "image.png",
        ]

        for file in pdf_files + non_pdf_files:
            file.touch()

        # Executa a remoção
        remover = PDFRemove(Path(tmp_dir))
        remover.remove_pdfs()

        # Verifica se apenas os PDFs foram removidos
        for pdf in pdf_files:
            assert not pdf.exists()

        for non_pdf in non_pdf_files:
            assert non_pdf.exists()


def test_remove_pdfs_works_with_empty_directory():
    with TemporaryDirectory() as tmp_dir:
        remover = PDFRemove(Path(tmp_dir))
        remover.remove_pdfs()  # Não deve levantar exceção

        assert len(list(Path(tmp_dir).iterdir())) == 0


def test_remove_pdfs_handles_nested_pdf_files():
    with TemporaryDirectory() as tmp_dir:
        # Cria estrutura com subdiretórios
        nested_dir = Path(tmp_dir) / "subdir"
        nested_dir.mkdir()

        pdf_file = nested_dir / "nested.pdf"
        pdf_file.touch()

        # Verifica que por padrão não remove em subdiretórios
        remover = PDFRemove(Path(tmp_dir))
        remover.remove_pdfs()

        assert pdf_file.exists()  # Arquivo em subdiretório não deve ser afetado
