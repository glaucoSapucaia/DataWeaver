from dataweaver.data.modules import PdfExtractor

import pytest
from unittest.mock import patch
from pathlib import Path
import pandas as pd


# Fixture para mock do tabula
@pytest.fixture
def mock_tabula():
    with patch("tabula.read_pdf") as mock:
        yield mock


# Testes para PdfExtractor
def test_pdf_extractor_initialization(tmp_path):
    """Testa a inicialização correta da classe"""
    pdf_path = tmp_path / "test.pdf"
    extractor = PdfExtractor(pdf_path)
    assert extractor.pdf_path == pdf_path


def test_extract_tables_success(mock_tabula):
    """Testa extração bem-sucedida de tabelas"""
    # Configura o mock para retornar DataFrames de teste
    mock_tabula.return_value = [
        pd.DataFrame({"A": [1, 2], "B": [3, 4]}),
        pd.DataFrame({"C": [5, 6], "D": [7, 8]}),
    ]

    pdf_path = Path("dummy.pdf")
    extractor = PdfExtractor(pdf_path)

    result = extractor.extract_tables(pages="1")

    # Verifica chamada ao tabula
    mock_tabula.assert_called_once_with(
        str(pdf_path), pages="1", multiple_tables=True, lattice=True
    )

    # Verifica resultado
    assert len(result) == 2
    assert all(isinstance(df, pd.DataFrame) for df in result)


def test_extract_tables_empty_pdf(mock_tabula):
    """Testa comportamento com PDF sem tabelas"""
    mock_tabula.return_value = []

    pdf_path = Path("empty.pdf")
    extractor = PdfExtractor(pdf_path)

    result = extractor.extract_tables(pages="all")
    assert result == []


def test_extract_tables_invalid_path():
    """Testa comportamento com caminho inválido"""
    pdf_path = Path("nonexistent.pdf")
    extractor = PdfExtractor(pdf_path)

    with patch("tabula.read_pdf", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            extractor.extract_tables(pages="1")


def test_extract_tables_different_page_ranges(mock_tabula):
    """Testa diferentes formatos de especificação de páginas"""
    pdf_path = Path("test.pdf")
    extractor = PdfExtractor(pdf_path)

    test_cases = ["1", "1-3", "all", "1,3,5"]

    for pages in test_cases:
        mock_tabula.reset_mock()
        extractor.extract_tables(pages=pages)
        mock_tabula.assert_called_once_with(
            str(pdf_path), pages=pages, multiple_tables=True, lattice=True
        )


def test_extract_tables_with_lattice_disabled(mock_tabula):
    """Testa se o parâmetro lattice está corretamente habilitado"""
    pdf_path = Path("test.pdf")
    extractor = PdfExtractor(pdf_path)

    extractor.extract_tables(pages="1")

    # Verifica se lattice=True foi passado
    args, kwargs = mock_tabula.call_args
    assert kwargs["lattice"] is True


def test_extract_tables_with_multiple_tables_enabled(mock_tabula):
    """Testa se multiple_tables está corretamente habilitado"""
    pdf_path = Path("test.pdf")
    extractor = PdfExtractor(pdf_path)

    extractor.extract_tables(pages="1")

    # Verifica se multiple_tables=True foi passado
    args, kwargs = mock_tabula.call_args
    assert kwargs["multiple_tables"] is True
