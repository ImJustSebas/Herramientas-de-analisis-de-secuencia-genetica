"""
Modulo para validar secuencias de ADN.
"""

import logging
import re

logger = logging.getLogger(__name__)

# Caracteres validos para secuencias de ADN (IUPAC)
ADN_VALIDO = set('ATCGNWSMKRYBDHV')
ARN_VALIDO = set('AUCGNWSMKRYBDHV')
PROTEINA_VALIDO = set('ACDEFGHIKLMNPQRSTVWY*')


def validar_secuencia(secuencia: str, tipo: str = 'adn') -> tuple[bool, str]:
    """
    Valida que una secuencia contenga solo caracteres validos.

    Args:
        secuencia: La secuencia a validar.
        tipo: 'adn', 'arn' o 'proteina'.

    Returns:
        Tupla (es_valida, mensaje_error).
    """
    if not secuencia:
        return False, "La secuencia esta vacia."

    secuencia_upper = secuencia.upper().replace(' ', '').replace('\n', '')

    if tipo.lower() == 'adn':
        caracteres_validos = ADN_VALIDO
        nombre_tipo = "ADN"
    elif tipo.lower() == 'arn':
        caracteres_validos = ARN_VALIDO
        nombre_tipo = "ARN"
    elif tipo.lower() == 'proteina':
        caracteres_validos = PROTEINA_VALIDO
        nombre_tipo = "proteina"
    else:
        return False, f"Tipo de secuencia desconocido: {tipo}"

    caracteres_invalidos = set(secuencia_upper) - caracteres_validos

    if caracteres_invalidos:
        return False, f"Caracteres no validos para {nombre_tipo}: {', '.join(caracteres_invalidos)}"

    return True, ""


def normalizar_secuencia(secuencia: str) -> str:
    """
    Normaliza una secuencia: mayusculas, sin espacios ni saltos de linea.
    """
    return secuencia.upper().replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '')