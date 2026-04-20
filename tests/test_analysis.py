"""
Pruebas unitarias basicas para los modulos de analisis.
"""

import unittest
import sys
from pathlib import Path

# Agregar directorio src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.validator import validar_secuencia, normalizar_secuencia
from src.analysis import calcular_longitud, calcular_contenido_gc, contar_nucleotidos
from src.translation import traducir_codon, traducir_adn
from src.orf import complemento_inverso


class TestValidador(unittest.TestCase):
    """Pruebas para el modulo validador."""

    def test_secuencia_valida(self):
        es_valida, error = validar_secuencia("ATCG", "adn")
        self.assertTrue(es_valida)
        self.assertEqual(error, "")

    def test_secuencia_invalida(self):
        es_valida, error = validar_secuencia("ATCXZ", "adn")
        self.assertFalse(es_valida)
        self.assertIn("Z", error)

    def test_secuencia_vacia(self):
        es_valida, error = validar_secuencia("", "adn")
        self.assertFalse(es_valida)

    def test_normalizar_secuencia(self):
        secuencia = "atc g\natc"
        normalizada = normalizar_secuencia(secuencia)
        self.assertEqual(normalizada, "ATCGATC")


class TestAnalisis(unittest.TestCase):
    """Pruebas para el modulo de analisis."""

    def test_calcular_longitud(self):
        self.assertEqual(calcular_longitud("ATCG"), 4)
        self.assertEqual(calcular_longitud(""), 0)

    def test_contenido_gc(self):
        self.assertEqual(calcular_contenido_gc("GCGC"), 100.0)
        self.assertEqual(calcular_contenido_gc("ATAT"), 0.0)
        self.assertEqual(calcular_contenido_gc("ATGC"), 50.0)

    def test_contar_nucleotidos(self):
        conteo = contar_nucleotidos("AATTCCGG")
        self.assertEqual(conteo['A'], 2)
        self.assertEqual(conteo['T'], 2)
        self.assertEqual(conteo['C'], 2)
        self.assertEqual(conteo['G'], 2)


class TestTraduccion(unittest.TestCase):
    """Pruebas para el modulo de traduccion."""

    def test_traducir_codon(self):
        self.assertEqual(traducir_codon("ATG"), "M")
        self.assertEqual(traducir_codon("TAA"), "*")
        self.assertEqual(traducir_codon("XXX"), "X")

    def test_traducir_adn(self):
        resultado = traducir_adn("ATGGCC", 0)
        self.assertEqual(resultado['secuencia_proteica'], "MA")
        self.assertEqual(resultado['longitud'], 2)


class TestORF(unittest.TestCase):
    """Pruebas para el modulo de ORFs."""

    def test_complemento_inverso(self):
        self.assertEqual(complemento_inverso("ATCG"), "CGAT")
        self.assertEqual(complemento_inverso("AATT"), "AATT")
        self.assertEqual(complemento_inverso("GCTA"), "TAGC")


if __name__ == "__main__":
    unittest.main()
