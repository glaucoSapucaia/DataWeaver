from dataweaver.utils import get_env_variable

import os
from unittest.mock import patch


def test_get_env_variable_returns_value_when_set():
    """Testa quando a variável está definida e não vazia"""
    with patch.dict(os.environ, {"TEST_VAR": "valid_value"}):
        result = get_env_variable("TEST_VAR", "default_value")
        assert result == "valid_value"


def test_get_env_variable_returns_default_when_not_set():
    """Testa quando a variável não está definida"""
    with patch.dict(os.environ, {}, clear=True):
        result = get_env_variable("UNDEFINED_VAR", "default_value")
        assert result == "default_value"


def test_get_env_variable_returns_default_when_empty():
    """Testa quando a variável está definida mas vazia"""
    with patch.dict(os.environ, {"EMPTY_VAR": ""}):
        result = get_env_variable("EMPTY_VAR", "default_value")
        assert result == "default_value"


def test_get_env_variable_returns_default_when_whitespace():
    """Testa quando a variável contém apenas espaços em branco"""
    with patch.dict(os.environ, {"WHITESPACE_VAR": "   "}):
        result = get_env_variable("WHITESPACE_VAR", "default_value")
        assert result == "default_value"


def test_get_env_variable_strips_whitespace_from_valid_values():
    """Testa se remove espaços em branco de valores válidos"""
    with patch.dict(os.environ, {"TRIMMABLE_VAR": "  value  "}):
        result = get_env_variable("TRIMMABLE_VAR", "default_value")
        assert result == "value"


def test_get_env_variable_with_empty_default():
    """Testa comportamento com valor padrão vazio"""
    with patch.dict(os.environ, {}, clear=True):
        result = get_env_variable("MISSING_VAR", "")
        assert result == ""
