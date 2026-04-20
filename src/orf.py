"""
Modulo para deteccion de marcos de lectura abiertos (ORFs).
"""

import logging
import re
from typing import List, Tuple, Dict

logger = logging.getLogger(__name__)

# Codones de inicio y parada
CODON_INICIO = 'ATG'
CODONES_PARADA = {'TAA', 'TAG', 'TGA'}


def complemento_inverso(secuencia: str) -> str:
    """
    Calcula el complemento inverso de una secuencia de ADN.
    """
    complemento = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C',
                   'N': 'N', 'W': 'W', 'S': 'S', 'M': 'K',
                   'K': 'M', 'R': 'Y', 'Y': 'R', 'B': 'V',
                   'V': 'B', 'D': 'H', 'H': 'D'}

    return ''.join(complemento.get(base, base) for base in reversed(secuencia.upper()))


def encontrar_orfs_en_marco(secuencia: str, marco: int = 0) -> List[Tuple[int, int]]:
    """
    Encuentra ORFs en un marco de lectura especifico.
    Devuelve lista de tuplas (posicion_inicio, posicion_fin).
    """
    orfs = []
    i = marco

    while i < len(secuencia) - 2:
        codon = secuencia[i:i+3]

        if codon == CODON_INICIO:
            # Buscar codon de parada
            for j in range(i + 3, len(secuencia) - 2, 3):
                codon_parada = secuencia[j:j+3]
                if codon_parada in CODONES_PARADA:
                    # ORF valido (minimo 100 bp incluyendo inicio y parada)
                    if j - i >= 99:
                        orfs.append((i, j + 2))
                    i = j + 3
                    break
            else:
                # No se encontro codon de parada, avanzar al siguiente ATG
                i += 3
        else:
            i += 3

    return orfs


def encontrar_orfs(secuencia: str) -> Dict[str, List[Dict]]:
    """
    Encuentra todos los ORFs en una secuencia (6 marcos de lectura).

    Returns:
        Diccionario con ORFs en hebra directa y complementaria.
    """
    secuencia_normalizada = secuencia.upper().replace(' ', '').replace('\n', '')

    if len(secuencia_normalizada) < 3:
        return {'directa': [], 'complementaria': []}

    # Hebra directa (3 marcos)
    orfs_directa = []
    for marco in range(3):
        orfs_marco = encontrar_orfs_en_marco(secuencia_normalizada, marco)
        for inicio, fin in orfs_marco:
            orfs_directa.append({
                'marco': marco,
                'inicio': inicio,
                'fin': fin,
                'longitud': fin - inicio + 1,
                'secuencia': secuencia_normalizada[inicio:fin+1],
                'hebra': 'directa'
            })

    # Hebra complementaria (3 marcos)
    secuencia_complementaria = complemento_inverso(secuencia_normalizada)
    orfs_complementaria = []
    for marco in range(3):
        orfs_marco = encontrar_orfs_en_marco(secuencia_complementaria, marco)
        for inicio, fin in orfs_marco:
            orfs_complementaria.append({
                'marco': marco,
                'inicio': len(secuencia_normalizada) - fin,
                'fin': len(secuencia_normalizada) - inicio,
                'longitud': fin - inicio + 1,
                'secuencia': secuencia_complementaria[inicio:fin+1],
                'hebra': 'complementaria'
            })

    logger.info(f"ORFs encontrados: {len(orfs_directa)} en hebra directa, {len(orfs_complementaria)} en complementaria")

    return {
        'directa': orfs_directa,
        'complementaria': orfs_complementaria
    }