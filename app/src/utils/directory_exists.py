from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

def ensure_directory_exists(directory: 'Path') -> None:
    """Garante que um diretório existe. Se não existir, tenta criá-lo."""
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Erro ao criar {directory}: {e}")
        exit(1)