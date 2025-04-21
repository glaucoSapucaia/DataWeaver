from dataweaver.data.modules import DataProcessor

import pytest
from unittest.mock import patch
import pandas as pd
import numpy as np


# Fixtures para criar DataFrames de teste
@pytest.fixture
def sample_tables():
    return [
        pd.DataFrame({"A": [1, 2], "B": [3, 4]}),
        pd.DataFrame({"A": [5, 6], "B": [7, 8]}),
    ]


@pytest.fixture
def empty_tables():
    return []


@pytest.fixture
def incompatible_tables():
    return [pd.DataFrame({"A": [1, 2]}), pd.DataFrame({"B": [3, 4]})]


# Testes para DataProcessor
def test_process_data_success(sample_tables):
    """Testa processamento bem-sucedido de tabelas compatíveis"""
    processor = DataProcessor(abbreviation_dict={})

    with patch("dataweaver.data.modules.data_processor.logger.info") as mock_logger:
        result = processor.process_data(sample_tables)

        # Verifica o resultado
        expected = pd.concat(sample_tables, axis=0)
        pd.testing.assert_frame_equal(result, expected)

        # Verifica logs
        mock_logger.assert_any_call("Processando tabelas...")
        mock_logger.assert_any_call("Concatenando tabelas...")


def test_process_data_empty_list(empty_tables):
    """Testa comportamento com lista vazia de tabelas"""
    processor = DataProcessor(abbreviation_dict={})

    with patch("dataweaver.data.modules.data_processor.logger.warning") as mock_logger:
        with pytest.raises(ValueError, match="A lista de tabelas está vazia"):
            processor.process_data(empty_tables)

        mock_logger.assert_called_once_with(
            "Nenhuma tabela foi fornecida para processamento."
        )


def test_process_data_preserves_index(sample_tables):
    """Testa se índices originais são preservados"""
    sample_tables[0].index = ["x", "y"]
    sample_tables[1].index = ["z", "w"]

    processor = DataProcessor(abbreviation_dict={})
    result = processor.process_data(sample_tables)

    # Verifica índices concatenados
    assert list(result.index) == ["x", "y", "z", "w"]


def test_process_data_with_empty_frames(sample_tables):
    """Testa concatenação quando uma tabela está vazia"""
    tables_with_empty = sample_tables + [pd.DataFrame()]
    processor = DataProcessor(abbreviation_dict={})

    result = processor.process_data(tables_with_empty)
    expected = pd.concat(sample_tables, axis=0)
    pd.testing.assert_frame_equal(result, expected)


def test_process_data_with_nan_values():
    """Testa tratamento de valores NaN"""
    tables = [pd.DataFrame({"A": [1, np.nan]}), pd.DataFrame({"A": [3, 4]})]
    processor = DataProcessor(abbreviation_dict={})

    result = processor.process_data(tables)
    assert result["A"].isna().sum() == 1
