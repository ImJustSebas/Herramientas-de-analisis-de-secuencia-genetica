"""
Modulo para exportacion de resultados a CSV y TXT.
"""

import csv
import logging
from typing import Dict, List
from pathlib import Path

logger = logging.getLogger(__name__)


def exportar_csv(resultados: List[Dict], ruta_salida: str) -> None:
    """
    Exporta los resultados de analisis a un archivo CSV.
    """
    try:
        with open(ruta_salida, 'w', newline='', encoding='utf-8') as archivo:
            if not resultados:
                logger.warning("No hay resultados para exportar")
                return

            # Definir campos a exportar
            campos = ['identificador', 'longitud', 'contenido_gc']
            campos.extend(['A', 'T', 'C', 'G', 'N', 'Otros'])

            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()

            for res in resultados:
                fila = {
                    'identificador': res['identificador'],
                    'longitud': res['longitud'],
                    'contenido_gc': res['contenido_gc']
                }
                # Agregar conteo de nucleotidos
                conteo = res.get('conteo_nucleotidos', {})
                fila.update({
                    'A': conteo.get('A', 0),
                    'T': conteo.get('T', 0),
                    'C': conteo.get('C', 0),
                    'G': conteo.get('G', 0),
                    'N': conteo.get('N', 0),
                    'Otros': conteo.get('Otros', 0)
                })
                escritor.writerow(fila)

        logger.info(f"Exportados {len(resultados)} registros a {ruta_salida}")

    except Exception as e:
        logger.error(f"Error exportando a CSV: {e}")
        raise


def exportar_txt(secuencias: Dict[str, str], resultados: List[Dict], ruta_salida: str) -> None:
    """
    Exporta secuencias y resultados a un archivo de texto formateado.
    """
    try:
        with open(ruta_salida, 'w', encoding='utf-8') as archivo:
            archivo.write("=" * 70 + "\n")
            archivo.write("ANALISIS DE SECUENCIAS BIOLOGICAS\n")
            archivo.write("=" * 70 + "\n\n")

            for resultado in resultados:
                archivo.write(f"ID: {resultado['identificador']}\n")
                archivo.write("-" * 40 + "\n")
                archivo.write(f"Longitud: {resultado['longitud']} pb\n")
                archivo.write(f"Contenido GC: {resultado['contenido_gc']}%\n")
                archivo.write("Conteo de nucleotidos:\n")

                conteo = resultado['conteo_nucleotidos']
                for nucleotido, cantidad in conteo.items():
                    if cantidad > 0:
                        archivo.write(f"  {nucleotido}: {cantidad}\n")

                # Secuencia completa
                identificador = resultado['identificador']
                if identificador in secuencias:
                    secuencia = secuencias[identificador]
                    archivo.write("\nSecuencia:\n")
                    for i in range(0, len(secuencia), 60):
                        archivo.write(f"  {secuencia[i:i+60]}\n")

                archivo.write("\n" + "=" * 70 + "\n\n")

        logger.info(f"Exportado a TXT: {ruta_salida}")

    except Exception as e:
        logger.error(f"Error exportando a TXT: {e}")
        raise