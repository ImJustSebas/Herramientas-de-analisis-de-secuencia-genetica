"""
Punto de entrada principal de la aplicacion.
Lanza la interfaz grafica.
"""

import tkinter as tk
import sys
import logging
from pathlib import Path

# Configurar logging basico
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Agregar directorio src al path si es necesario
sys.path.insert(0, str(Path(__file__).parent))

from src.visualization import InterfazAnalizador


def main():
    """Funcion principal que inicia la aplicacion."""
    raiz = tk.Tk()
    app = InterfazAnalizador(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()