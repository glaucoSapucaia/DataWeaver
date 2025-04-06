"""
Funções utilitárias para manipulação de diretórios e validação de variáveis.

Este módulo contém funções auxiliares utilizadas em diferentes partes da aplicação,
como verificação da existência de diretórios.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

def ensure_directory_exists(directory: 'Path') -> bool:
    """
    Garante que o diretório especificado exista.

    Cria o diretório (e seus pais, se necessário) caso ele não exista.
    Retorna True se o diretório foi criado com sucesso ou já existia,
    e False caso ocorra algum erro.

    Parâmetros:
        directory (Path): Caminho do diretório a ser garantido.

    Retorno:
        bool: True se o diretório existir ou for criado, False em caso de erro.
    """
    try:
        directory.mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False
