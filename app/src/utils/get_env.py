import os

def get_env_variable(var_name: str, default: str) -> str:
    """
    Obtém uma variável de ambiente, garantindo que ela tenha um valor válido.
    
    :param var_name: Nome da variável de ambiente
    :param default: Valor padrão caso a variável não esteja definida
    :return: Valor da variável de ambiente ou o padrão
    """
    value = os.getenv(var_name, default).strip()
    return value if value else default