"""
Módulo de argumentos de aplicación.
Proporciona funciones para almacenar y recuperar argumentos de línea de comandos
utilizando variables de entorno.
"""

import os


def set_arg_str(name: str, value: str):
    """
    Establece un argumento de texto en las variables de entorno.

    Args:
        name: Nombre del argumento.
        value: Valor del argumento.
    """
    os.environ[name] = value


def set_arg_bool(name: str, value: bool):
    """
    Establece un argumento booleano en las variables de entorno.

    Args:
        name: Nombre del argumento.
        value: Valor booleano (True/False).
    """
    set_arg_str(name, '1' if value else '0')


def get_arg_str(name: str, default=None) -> str:
    """
    Obtiene un argumento de texto de las variables de entorno.

    Args:
        name: Nombre del argumento.
        default: Valor predeterminado si no existe.

    Returns:
        El valor del argumento o el valor predeterminado.
    """
    return os.environ.get(name, default)


def get_arg_bool(name: str, default=False) -> bool:
    """
    Obtiene un argumento booleano de las variables de entorno.

    Args:
        name: Nombre del argumento.
        default: Valor predeterminado si no existe.

    Returns:
        El valor booleano del argumento o el valor predeterminado.
    """
    x = get_arg_str(name, default=None)
    if x is None:
        return default
    return bool(int(x))
    