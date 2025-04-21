from dataweaver.data.modules import CsvSaver

import pytest
from unittest.mock import patch
import pandas as pd


# Fixture para criar um DataFrame de teste
@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})


# Testes para CsvSaver
def test_csv_saver_initialization(tmp_path):
    """Testa a inicialização correta da classe"""
    csv_path = tmp_path / "output.csv"
    saver = CsvSaver(csv_path)
    assert saver.csv_path == csv_path


def test_save_csv_success(tmp_path, sample_dataframe):
    """Testa o salvamento bem-sucedido de um DataFrame"""
    csv_path = tmp_path / "output.csv"
    saver = CsvSaver(csv_path)

    with patch("dataweaver.data.modules.csv_saver.logger.info") as mock_logger:
        saver.save_csv(sample_dataframe)

        # Verifica se o arquivo foi criado
        assert csv_path.exists()

        # Verifica o conteúdo do arquivo
        saved_data = pd.read_csv(csv_path)
        pd.testing.assert_frame_equal(saved_data, sample_dataframe)

        # Verifica o log
        mock_logger.assert_called_once_with("Convertendo tabela para CSV...")


def test_save_csv_with_special_characters(tmp_path):
    """Testa salvamento com caracteres especiais"""
    test_df = pd.DataFrame({"texto": ["çãõé", "áéíóú", "ñÑ"]})
    csv_path = tmp_path / "special.csv"
    saver = CsvSaver(csv_path)

    saver.save_csv(test_df)
    saved_data = pd.read_csv(csv_path)
    pd.testing.assert_frame_equal(saved_data, test_df)


def test_save_csv_parameters(tmp_path, sample_dataframe):
    """Testa se os parâmetros do to_csv estão corretos"""
    csv_path = tmp_path / "output.csv"
    saver = CsvSaver(csv_path)

    with patch("pandas.DataFrame.to_csv") as mock_to_csv:
        saver.save_csv(sample_dataframe)

        mock_to_csv.assert_called_once_with(
            str(csv_path), index=False, header=True, encoding="utf-8"
        )


def test_save_csv_overwrite_existing(tmp_path, sample_dataframe):
    """Testa sobrescrita de arquivo existente"""
    csv_path = tmp_path / "output.csv"
    csv_path.write_text("old content")  # Cria arquivo existente

    saver = CsvSaver(csv_path)
    saver.save_csv(sample_dataframe)

    # Verifica se o conteúdo foi sobrescrito corretamente
    saved_data = pd.read_csv(csv_path)
    pd.testing.assert_frame_equal(saved_data, sample_dataframe)
