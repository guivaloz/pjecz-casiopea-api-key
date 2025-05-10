"""
Generadores de contraseñas
"""

import random
import string
import time


def generar_contrasena(largo=16):
    """Generar contraseña con minúsculas, mayúsculas, dígitos y signos"""
    minusculas = string.ascii_lowercase
    mayusculas = string.ascii_uppercase
    digitos = string.digits
    simbolos = string.punctuation
    todos = minusculas + mayusculas + digitos + simbolos
    temp = random.sample(todos, largo)
    return "".join(temp)


def generar_aleatorio(largo=16):
    """Generar cadena de texto aleatorio con minúsculas, mayúsculas y dígitos"""
    minusculas = string.ascii_lowercase
    mayusculas = string.ascii_uppercase
    digitos = string.digits
    todos = minusculas + mayusculas + digitos
    temp = random.sample(todos, largo)
    return "".join(temp)


def generar_identificador(largo: int = 16) -> str:
    """Generar identificador con el tiempo actual y algo aleatorio con letras en mayúsculas y dígitos"""
    timestamp_unique = str(int(time.time() * 1000))
    random_characters = "".join(random.sample(string.ascii_uppercase + string.digits, k=largo))
    return f"{timestamp_unique}{random_characters}"[:largo]
