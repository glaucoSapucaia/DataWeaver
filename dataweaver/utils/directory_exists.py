from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def ensure_directory_exists(directory: "Path") -> bool:
    """
    Método auxiliar para criar diretórios com tratamento de erros

    Args:
        path: Caminho do diretório a ser criado

    Raises:
        RuntimeError: Se a criação do diretório falhar
    """
    try:
        directory.mkdir(parents=True, exist_ok=True)
        if not directory.exists():
            raise RuntimeError(f"Falha ao criar diretório: {directory}")
        return True
    except OSError as e:
        raise RuntimeError(f"Erro na criação do diretório {directory}: {str(e)}")
