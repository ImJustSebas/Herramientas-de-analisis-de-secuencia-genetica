"""
Modulo para cargar y parsear archivos FASTA.
"""

import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)


def cargar_fasta(ruta_archivo: str) -> Dict[str, str]:
    """
    Carga un archivo FASTA y devuelve un diccionario con
    identificadores como claves y secuencias como valores.
    """
    secuencias = {}
    identificador_actual = None
    secuencia_actual = []

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue

                if linea.startswith('>'):
                    # Guardar secuencia anterior si existe
                    if identificador_actual is not None:
                        secuencias[identificador_actual] = ''.join(secuencia_actual)

                    # Nuevo identificador
                    identificador_actual = linea[1:].strip()
                    secuencia_actual = []
                else:
                    if identificador_actual is None:
                        logger.warning("Secuencia encontrada sin identificador previo")
                        continue
                    secuencia_actual.append(linea.upper())

            # Guardar ultima secuencia
            if identificador_actual is not None:
                secuencias[identificador_actual] = ''.join(secuencia_actual)

        logger.info(f"Cargadas {len(secuencias)} secuencias desde {ruta_archivo}")
        return secuencias

    except FileNotFoundError:
        logger.error(f"Archivo no encontrado: {ruta_archivo}")
        raise
    except Exception as e:
        logger.error(f"Error al cargar archivo FASTA: {e}")
        raise


def extraer_secuencias(secuencias: Dict[str, str]) -> List[Tuple[str, str]]:
    """
    Convierte el diccionario de secuencias en una lista de tuplas (id, secuencia).
    """
    return [(identificador, sec) for identificador, sec in secuencias.items()]