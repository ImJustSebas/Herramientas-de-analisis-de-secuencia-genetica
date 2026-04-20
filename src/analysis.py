"""
Modulo para analisis de secuencias: longitud, contenido GC y conteo de nucleotidos.
"""

import logging
from typing import Dict, List, Tuple
from collections import Counter

logger = logging.getLogger(__name__)


def calcular_longitud(secuencia: str) -> int:
    """Calcula la longitud de la secuencia."""
    return len(secuencia)


def calcular_contenido_gc(secuencia: str) -> float:
    """
    Calcula el porcentaje de G y C en la secuencia.
    """
    if not secuencia:
        return 0.0

    secuencia_upper = secuencia.upper()
    conteo_gc = secuencia_upper.count('G') + secuencia_upper.count('C')
    contenido_gc = (conteo_gc / len(secuencia_upper)) * 100

    return round(contenido_gc, 2)


def contar_nucleotidos(secuencia: str) -> Dict[str, int]:
    """
    Cuenta la frecuencia de cada nucleotido en la secuencia.
    """
    secuencia_upper = secuencia.upper()
    conteo = Counter(secuencia_upper)

    # Asegurar que los nucleotidos principales esten presentes
    resultado = {
        'A': conteo.get('A', 0),
        'T': conteo.get('T', 0),
        'C': conteo.get('C', 0),
        'G': conteo.get('G', 0),
        'N': conteo.get('N', 0),
        'Otros': sum(v for k, v in conteo.items() if k not in 'ATCGN')
    }

    return resultado


def analizar_secuencia(secuencia: str, identificador: str = "") -> Dict:
    """
    Realiza un analisis completo de una secuencia.

    Returns:
        Diccionario con todas las metricas calculadas.
    """
    secuencia_normalizada = secuencia.upper().replace(' ', '').replace('\n', '')

    if not secuencia_normalizada:
        return {
            'identificador': identificador,
            'longitud': 0,
            'contenido_gc': 0.0,
            'conteo_nucleotidos': {'A': 0, 'T': 0, 'C': 0, 'G': 0, 'N': 0, 'Otros': 0},
            'error': "Secuencia vacia"
        }

    resultado = {
        'identificador': identificador,
        'longitud': calcular_longitud(secuencia_normalizada),
        'contenido_gc': calcular_contenido_gc(secuencia_normalizada),
        'conteo_nucleotidos': contar_nucleotidos(secuencia_normalizada)
    }

    logger.debug(f"Secuencia {identificador} analizada: longitud={resultado['longitud']}, GC={resultado['contenido_gc']}%")

    return resultado


def analizar_multiples_secuencias(secuencias: List[Tuple[str, str]]) -> List[Dict]:
    """
    Analiza multiples secuencias y devuelve una lista de resultados.
    """
    resultados = []
    for identificador, secuencia in secuencias:
        resultado = analizar_secuencia(secuencia, identificador)
        resultados.append(resultado)
    return resultados
