"""
Modulo para busqueda de motivos usando expresiones regulares.
"""

import logging
import re
from typing import List, Dict, Tuple, Optional

logger = logging.getLogger(__name__)


def buscar_motivo(secuencia: str, patron: str, ignorar_mayusculas: bool = True) -> List[Dict]:
    """
    Busca un motivo o patron regex en una secuencia.

    Args:
        secuencia: La secuencia donde buscar.
        patron: Expresion regular o cadena literal a buscar.
        ignorar_mayusculas: Si es True, busca sin distincion de mayusculas/minusculas.

    Returns:
        Lista de coincidencias con posicion y secuencia encontrada.
    """
    secuencia_normalizada = secuencia.upper().replace(' ', '').replace('\n', '')

    if ignorar_mayusculas:
        flags = re.IGNORECASE
        patron_busqueda = patron
    else:
        flags = 0
        patron_busqueda = patron

    try:
        regex = re.compile(patron_busqueda, flags)
    except re.error as e:
        logger.error(f"Patron regex invalido '{patron}': {e}")
        raise ValueError(f"Patron regex invalido: {e}")

    coincidencias = []
    for coincidencia in regex.finditer(secuencia_normalizada):
        coincidencias.append({
            'inicio': coincidencia.start(),
            'fin': coincidencia.end() - 1,
            'secuencia': coincidencia.group(),
            'longitud': coincidencia.end() - coincidencia.start()
        })

    logger.info(f"Encontradas {len(coincidencias)} coincidencias para el patron '{patron}'")

    return coincidencias


def buscar_motivos_comunes(secuencia: str) -> Dict[str, List[Dict]]:
    """
    Busca motivos biologicos comunes en la secuencia.
    """
    motivos_comunes = {
        'TATA_box': r'TATA[AT]A[AT]',
        'CAAT_box': r'CCAAT',
        'GC_box': r'GGGCGG',
        'sitio_restriccion_EcoRI': r'GAATTC',
        'sitio_restriccion_BamHI': r'GGATCC',
        'sitio_restriccion_HindIII': r'AAGCTT',
        'poliA': r'A{6,}',
        'poliT': r'T{6,}'
    }

    resultados = {}
    for nombre, patron in motivos_comunes.items():
        try:
            coincidencias = buscar_motivo(secuencia, patron)
            if coincidencias:
                resultados[nombre] = coincidencias
        except Exception as e:
            logger.warning(f"Error buscando motivo {nombre}: {e}")

    return resultados


def formato_consenso(secuencias: List[str]) -> str:
    """
    Genera una secuencia consenso a partir de multiples secuencias alineadas.
    Utiliza el caracter mas frecuente en cada posicion.
    """
    if not secuencias:
        return ""

    longitud_max = max(len(s) for s in secuencias)
    consenso = []

    for i in range(longitud_max):
        conteo = {}
        for sec in secuencias:
            if i < len(sec):
                char = sec[i].upper()
                conteo[char] = conteo.get(char, 0) + 1

        if conteo:
            mas_comun = max(conteo, key=conteo.get)
            consenso.append(mas_comun)
        else:
            consenso.append('-')

    return ''.join(consenso)