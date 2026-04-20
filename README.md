# 🧬 Analizador de Secuencias Biológicas

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)](https://docs.python.org/3/library/tkinter.html)

Aplicación de escritorio para el análisis local de secuencias biológicas desde archivos FASTA. Desarrollada con Python y Tkinter, sin dependencias de APIs externas.

## 📋 Características

- ✅ Carga de archivos FASTA (`.fasta`, `.fa`, `.fna`, `.ffn`, `.faa`, `.frn`)
- ✅ Validación de secuencias de ADN (caracteres IUPAC)
- ✅ Análisis de métricas básicas:
  - Longitud de secuencia
  - Contenido GC (%)
  - Conteo de nucleótidos (A, T, C, G, N)
- ✅ Detección de Marcos de Lectura Abiertos (ORFs) en 6 marcos de lectura
- ✅ Traducción de ADN a proteína (código genético estándar)
- ✅ Búsqueda de motivos usando expresiones regulares
- ✅ Exportación de resultados a CSV y TXT
- ✅ Interfaz gráfica intuitiva y profesional
- ✅ Manejo robusto de errores
- ✅ Logging integrado
- ✅ Código modular y mantenible

## 🚀 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/imjustsebas/herramientas-de-analisis-de-secuencia-genetica.git
cd herramientas-de-analisis-de-secuencia-genetica
Crear entorno virtual (opcional pero recomendado)

bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En Linux/Mac
source venv/bin/activate
Instalar dependencias

bash
pip install -r requirements.txt
Dependencias
text
biopython>=1.81
Nota: Biopython es opcional. La aplicación funciona sin él, pero su instalación permite extender funcionalidades futuras.

📦 Estructura del Proyecto
text
herramientas-de-analisis-de-secuencia-genetica/
├── app.py                 # Punto de entrada principal
├── src/                   # Código fuente
│   ├── __init__.py
│   ├── parser.py         # Carga de archivos FASTA
│   ├── validator.py      # Validación de secuencias
│   ├── analysis.py       # Análisis básico (longitud, GC, nucleótidos)
│   ├── orf.py           # Detección de ORFs
│   ├── translation.py    # Traducción ADN → Proteína
│   ├── motifs.py        # Búsqueda de motivos (regex)
│   ├── visualization.py  # Interfaz gráfica (Tkinter)
│   └── export.py        # Exportación CSV/TXT
├── data/                 # Directorio para archivos de entrada
├── outputs/              # Directorio para resultados exportados
├── tests/                # Pruebas unitarias
│   ├── __init__.py
│   └── test_analysis.py
├── requirements.txt      # Dependencias del proyecto
└── README.md            # Este archivo
🎯 Uso
Iniciar la Aplicación
bash
python app.py
Flujo de Trabajo Típico
Cargar archivo FASTA

Click en "Cargar Archivo FASTA" o Ctrl+O

Seleccionar archivo de secuencias

Analizar secuencias

Click en "Analizar Secuencias"

Ver resultados en pestaña "Análisis Básico"

Buscar ORFs

Seleccionar secuencia del desplegable

Click en "Buscar ORFs"

Ver resultados en pestaña "ORFs"

Traducir a proteína

Seleccionar secuencia del desplegable

Ver traducción automática en pestaña "Traducción"

Buscar motivos

Ingresar patrón (regex o texto literal)

Click en "Buscar"

Ver coincidencias en pestaña "Resultados Búsqueda"

Exportar resultados

Click en "Exportar Resultados a CSV" o "Exportar Resultados a TXT"

Seleccionar ubicación de guardado

Ejemplos de Patrones de Búsqueda
Patrón	Descripción	Ejemplo de uso
ATG	Codón de inicio	Busca todos los ATG en la secuencia
TATA[AT]A[AT]	TATA box	Identifica secuencias reguladoras
GAATTC	Sitio EcoRI	Localiza sitios de restricción
A{6,}	Poli-A	Encuentra 6 o más adeninas consecutivas
[GC]{4,}	Región rica en GC	Detecta 4 o más G/C consecutivas
TGA|TAA|TAG	Codones de parada	Busca codones de terminación
🧪 Ejecutar Pruebas
bash
# Ejecutar todas las pruebas
python -m pytest tests/

# O con unittest
python -m unittest discover tests/

# Prueba específica
python tests/test_analysis.py
📊 Formato de Archivos
Entrada: FASTA
fasta
>Secuencia_1
ATCGATCGATCGATCG
>Secuencia_2
GCTAGCTAGCTAGCTA
Salida: CSV
csv
identificador,longitud,contenido_gc,A,T,C,G,N,Otros
Secuencia_1,16,50.0,4,4,4,4,0,0
Secuencia_2,16,50.0,4,4,4,4,0,0
Salida: TXT
text
======================================================================
ANALISIS DE SECUENCIAS BIOLOGICAS
======================================================================

ID: Secuencia_1
----------------------------------------
Longitud: 16 pb
Contenido GC: 50.0%
Conteo de nucleotidos:
  A: 4
  T: 4
  C: 4
  G: 4

Secuencia:
  ATCGATCGATCGATCG
🔧 Configuración
El logging está configurado por defecto a nivel INFO. Para cambiar el nivel:

python
# En app.py
logging.basicConfig(
    level=logging.DEBUG,  # Cambiar a DEBUG para más detalles
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
🤝 Contribuir
Las contribuciones son bienvenidas. Por favor:

Haz Fork del repositorio

Crea una rama para tu feature (git checkout -b feature/AmazingFeature)

Haz Commit de tus cambios (git commit -m 'Add some AmazingFeature')

Haz Push a la rama (git push origin feature/AmazingFeature)

Abre un Pull Request

Áreas de Mejora
Soporte para archivos FASTQ

Alineamiento de secuencias

Visualización gráfica de ORFs

Análisis filogenético básico

Exportación a formato GenBank

Soporte para secuencias de ARN

Traducción con códigos genéticos alternativos

Análisis de calidad de secuencias

Predicción de estructuras secundarias

📝 Licencia
Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

👤 Autor
Sebastián Porras

GitHub: @imjustsebas

Email: sebastianporras067@gmail.com
