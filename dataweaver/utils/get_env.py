import os


def get_env_variable(var_name: str, default: str) -> str:
    """
    Obtém o valor de uma variável de ambiente, com fallback para um valor padrão.

    Se a variável não estiver definida ou estiver vazia, retorna o valor padrão fornecido.

    Parâmetros:
        var_name (str): Nome da variável de ambiente.
        default (str): Valor padrão a ser utilizado caso a variável não esteja definida ou seja inválida.

    Retorno:
        str: Valor da variável de ambiente ou o valor padrão fornecido.
    """
    value = os.getenv(var_name)

    if value is None or not value.strip():
        return default

    return value.strip()
