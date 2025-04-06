from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

def ensure_directory_exists(directory: 'Path') -> bool:
    """Garante que um diretório existe. Retorna True se criado ou já existente, False em erro."""
    try:
        directory.mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False