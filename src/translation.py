"""
Modulo para traduccion de secuencias de ADN a proteina.
"""

import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Tabla de traduccion estandar (codigo genetico)
TABLA_TRADUCCION = {
    'ATA': 'I', 'ATC': 'I', 'ATT': 'I', 'ATG': 'M',
    'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
    'AAC': 'N', 'AAT': 'N', 'AAA': 'K', 'AAG': 'K',
    'AGC': 'S', 'AGT': 'S', 'AGA': 'R', 'AGG': 'R',
    'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L',
    'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',
    'CAC': 'H', 'CAT': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R',
    'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',
    'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',
    'GAC': 'D', 'GAT': 'D', 'GAA': 'E', 'GAG': 'E',
    'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
    'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S',
    'TTC': 'F', 'TTT': 'F', 'TTA': 'L', 'TTG': 'L',
    'TAC': 'Y', 'TAT': 'Y', 'TAA': '*', 'TAG': '*',
    'TGC': 'C', 'TGT': 'C', 'TGA': '*', 'TGG': 'W',
}


def traducir_codon(codon: str) -> str:
    """
    Traduce un codon de 3 nucleotidos a aminoacido.
    """
    codon_upper = codon.upper()
    return TABLA_TRADUCCION.get(codon_upper, 'X')


def traducir_adn(secuencia: str, marco: int = 0) -> Dict:
    """
    Traduce una secuencia de ADN a proteina en el marco especificado.

    Returns:
        Diccionario con la secuencia proteica y metadatos.
    """
    secuencia_normalizada = secuencia.upper().replace(' ', '').replace('\n', '')

    if marco not in (0, 1, 2):
        raise ValueError("El marco debe ser 0, 1 o 2")

    # Ajustar al marco seleccionado
    secuencia_ajustada = secuencia_normalizada[marco:]
    longitud_efectiva = len(secuencia_ajustada) - (len(secuencia_ajustada) % 3)

    proteinas = []
    for i in range(0, longitud_efectiva, 3):
        codon = secuencia_ajustada[i:i+3]
        aminoacido = traducir_codon(codon)
        proteinas.append(aminoacido)

    secuencia_proteica = ''.join(proteinas)

    # Contar aminoacidos
    from collections import Counter
    conteo_aminoacidos = dict(Counter(proteinas))

    resultado = {
        'secuencia_proteica': secuencia_proteica,
        'longitud': len(secuencia_proteica),
        'marco': marco,
        'codones_parada': secuencia_proteica.count('*'),
        'conteo_aminoacidos': conteo_aminoacidos
    }

    logger.debug(f"Traduccion completada: {len(secuencia_proteica)} aminoacidos, marco {marco}")

    return resultado


def traducir_todos_marcos(secuencia: str) -> Dict[int, Dict]:
    """
    Traduce una secuencia en los tres marcos de lectura.
    """
    resultados = {}
    for marco in range(3):
        resultados[marco] = traducir_adn(secuencia, marco)
    return resultados