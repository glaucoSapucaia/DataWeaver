"""
Testes para os componentes `ZipCompressor` e `PDFRemove` do módulo `zip_compressor`.

Este módulo testa a compressão de arquivos PDF em um diretório em um arquivo `.zip`
e a remoção de arquivos PDF de um diretório. Inclui testes de funcionalidade e testes
para tratamento de exceções e registro de logs.

Dependências:
- pytest
- unittest.mock
- modules.zip_compressor
"""

from pathlib import Path
from unittest.mock import patch
import pytest  # type: ignore
import zipfile
from modules.zip_compressor import ZipCompressor, PDFRemove

# === FIXTURES ===

@pytest.fixture
def pdf_files(tmp_path):
    """
    Cria e retorna um diretório temporário com três arquivos PDF de teste.
    """
    pdf1 = tmp_path / "file1.pdf"
    pdf2 = tmp_path / "file2.pdf"
    pdf3 = tmp_path / "subdir" / "file3.pdf"
    pdf3.parent.mkdir(exist_ok=True)

    for pdf in [pdf1, pdf2, pdf3]:
        pdf.write_text("Conteúdo PDF de teste")
        
    return tmp_path


# === TESTES FUNCIONAIS ===

def test_zip_compressor_create_zip(pdf_files):
    """
    Verifica se o ZipCompressor cria corretamente um arquivo ZIP com todos os PDFs.
    """
    zip_name = "test.zip"
    zip_path = pdf_files / zip_name
    compressor = ZipCompressor(folder=pdf_files)

    compressor.create_zip(zip_name)
    assert zip_path.exists()

    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zip_contents = zipf.namelist()
        expected_files = ['file1.pdf', 'file2.pdf', 'subdir/file3.pdf']
        for file in expected_files:
            assert file in zip_contents


def test_zip_compressor_empty_folder(tmp_path):
    """
    Testa criação de um ZIP a partir de uma pasta vazia.
    """
    zip_name = "empty.zip"
    zip_path = tmp_path / zip_name
    compressor = ZipCompressor(folder=tmp_path)

    compressor.create_zip(zip_name)
    assert zip_path.exists()

    with zipfile.ZipFile(zip_path, 'r') as zipf:
        assert zipf.namelist() == []


def test_pdf_remove(pdf_files):
    """
    Verifica se todos os arquivos PDF são removidos corretamente.
    """
    remover = PDFRemove(folder=pdf_files)
    remover.remove_pdfs()
    pdf_list = list(pdf_files.rglob("*.pdf"))
    assert len(pdf_list) == 0


def test_pdf_remove_with_no_pdfs(tmp_path):
    """
    Verifica se PDFRemove não falha ao tentar remover PDFs quando não existem.
    """
    remover = PDFRemove(folder=tmp_path)
    remover.remove_pdfs()
    assert list(tmp_path.rglob("*.pdf")) == []


# === TESTES DE EXCEÇÕES (ZipCompressor) ===

def test_create_zip_logs_error(tmp_path):
    """
    Testa se erro durante a obtenção do caminho do ZIP é capturado e logado.
    """
    compressor = ZipCompressor(folder=tmp_path)

    with patch.object(compressor, '_get_zip_path', side_effect=Exception("Falha")):
        compressor.create_zip("erro.zip")  # Não deve lançar exceção


def test_compress_files_outer_exception(tmp_path):
    """
    Verifica se exceção externa em ZipFile é propagada corretamente.
    """
    compressor = ZipCompressor(folder=tmp_path)
    zip_path = tmp_path / "fail.zip"

    with patch("zipfile.ZipFile", side_effect=Exception("Erro externo")):
        with pytest.raises(Exception):
            compressor._compress_files(zip_path)


def test_compress_files_inner_exception(tmp_path):
    """
    Verifica se erro interno durante `relative_to` é capturado.
    """
    compressor = ZipCompressor(folder=tmp_path)
    pdf = tmp_path / "file.pdf"
    pdf.write_text("conteúdo")
    zip_path = tmp_path / "test.zip"

    with patch.object(Path, "relative_to", side_effect=Exception("Erro relativo")):
        compressor._compress_files(zip_path)


def test_get_pdf_files_exception_logs(tmp_path):
    """
    Testa se erro durante busca de PDFs com `rglob` é capturado e retorna lista vazia.
    """
    compressor = ZipCompressor(folder=tmp_path)

    with patch("pathlib.Path.rglob", side_effect=Exception("Erro em rglob")):
        result = compressor._get_pdf_files()
        assert result == []


# === TESTES DE EXCEÇÕES (PDFRemove) ===

def test_pdf_remove_rglob_error(tmp_path):
    """
    Verifica se erro ao buscar arquivos com `rglob` é tratado sem falhar.
    """
    remover = PDFRemove(folder=tmp_path)

    with patch("pathlib.Path.rglob", side_effect=Exception("Falha ao listar")):
        remover.remove_pdfs()


def test_pdf_remove_unlink_error(tmp_path):
    """
    Verifica se erro ao deletar arquivo é tratado sem falhar.
    """
    pdf = tmp_path / "file.pdf"
    pdf.write_text("teste")
    remover = PDFRemove(folder=tmp_path)

    with patch.object(Path, "unlink", side_effect=Exception("Falha ao excluir")):
        remover.remove_pdfs()


# === TESTES COM MOCAGEM DE FALHAS ===

def test_zip_file_write_error(pdf_files):
    """
    Verifica se erro ao escrever arquivos no ZIP é tratado.
    """
    compressor = ZipCompressor(folder=pdf_files)
    zip_path = pdf_files / "fail.zip"
    pdfs = list(pdf_files.rglob("*.pdf"))

    with patch.object(zipfile.ZipFile, "write", side_effect=Exception("Erro ao escrever")):
        with patch.object(compressor, "_get_pdf_files", return_value=pdfs):
            compressor._compress_files(zip_path)


def test_zip_get_zip_path_type_error(tmp_path):
    """
    Verifica se erro de tipo ao passar nome do ZIP é tratado.
    """
    compressor = ZipCompressor(folder=tmp_path)
    zip_name = 123  # tipo errado

    with pytest.raises(TypeError):
        compressor._get_zip_path(zip_name)


# === TESTES DE LOGGERS ===

def test_logger_error_on_create_zip(tmp_path):
    """
    Verifica se erro é registrado pelo logger.error na criação do ZIP.
    """
    compressor = ZipCompressor(folder=tmp_path)

    with patch("modules.zip_compressor.logger.error") as mock_logger:
        with patch.object(compressor, "_get_zip_path", side_effect=Exception("Falha")):
            compressor.create_zip("erro.zip")
            mock_logger.assert_called()


def test_logger_warning_on_write_pdf_error(tmp_path):
    """
    Verifica se erro ao escrever arquivo no ZIP aciona logger.warning.
    """
    pdf_path = tmp_path / "file.pdf"
    pdf_path.write_text("conteúdo")
    compressor = ZipCompressor(folder=tmp_path)
    zip_path = tmp_path / "log.zip"

    with patch.object(Path, "relative_to", side_effect=Exception("erro")):
        with patch("modules.zip_compressor.logger.warning") as mock_warning:
            compressor._compress_files(zip_path)
            assert mock_warning.called


def test_logger_warning_on_pdf_remove(tmp_path):
    """
    Verifica se erro ao remover PDF aciona logger.warning.
    """
    pdf_path = tmp_path / "file.pdf"
    pdf_path.write_text("conteúdo")
    remover = PDFRemove(folder=tmp_path)

    with patch.object(Path, "unlink", side_effect=Exception("erro")):
        with patch("modules.zip_compressor.logger.warning") as mock_warning:
            remover.remove_pdfs()
            assert mock_warning.called


def test_logger_error_on_pdf_search(tmp_path):
    """
    Verifica se erro ao buscar PDFs aciona logger.error no PDFRemove.
    """
    remover = PDFRemove(folder=tmp_path)

    with patch("pathlib.Path.rglob", side_effect=Exception("Erro")):
        with patch("modules.zip_compressor.logger.error") as mock_error:
            remover.remove_pdfs()
            assert mock_error.called


def test_logger_error_on_pdf_discovery(tmp_path):
    """
    Verifica se erro ao buscar PDFs aciona logger.error no ZipCompressor.
    """
    compressor = ZipCompressor(folder=tmp_path)

    with patch("pathlib.Path.rglob", side_effect=Exception("Erro")):
        with patch("modules.zip_compressor.logger.error") as mock_error:
            compressor._get_pdf_files()
            assert mock_error.called
