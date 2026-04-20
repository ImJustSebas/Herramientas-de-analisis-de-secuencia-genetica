"""
Modulo de visualizacion e interfaz grafica con Tkinter.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import logging
from pathlib import Path
from typing import Dict, List, Optional

from .parser import cargar_fasta, extraer_secuencias
from .validator import validar_secuencia
from .analysis import analizar_multiples_secuencias, analizar_secuencia
from .orf import encontrar_orfs
from .translation import traducir_adn
from .motifs import buscar_motivo
from .export import exportar_csv, exportar_txt

logger = logging.getLogger(__name__)


class InterfazAnalizador:
    """
    Clase principal de la interfaz grafica.
    """

    def __init__(self, raiz: tk.Tk):
        self.raiz = raiz
        self.raiz.title("Analizador de Secuencias Biologicas")
        self.raiz.geometry("900x700")
        self.raiz.minsize(800, 600)

        # Variables de estado
        self.secuencias_cargadas: Dict[str, str] = {}
        self.resultados_analisis: List[Dict] = []
        self.ruta_archivo_actual: Optional[str] = None

        self._crear_menu()
        self._crear_widgets()
        self._configurar_estilos()

        logger.info("Interfaz grafica inicializada")

    def _crear_menu(self):
        """Crea la barra de menu superior."""
        barra_menu = tk.Menu(self.raiz)
        self.raiz.config(menu=barra_menu)

        # Menu Archivo
        menu_archivo = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Cargar FASTA", command=self._cargar_archivo, accelerator="Ctrl+O")
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Exportar CSV", command=self._exportar_csv)
        menu_archivo.add_command(label="Exportar TXT", command=self._exportar_txt)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.raiz.quit)

        # Menu Ayuda
        menu_ayuda = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Acerca de", command=self._mostrar_acerca)

        # Atajos de teclado
        self.raiz.bind('<Control-o>', lambda e: self._cargar_archivo())

    def _crear_widgets(self):
        """Crea todos los widgets de la interfaz."""
        # Frame principal
        frame_principal = ttk.Frame(self.raiz, padding="10")
        frame_principal.pack(fill=tk.BOTH, expand=True)

        # Frame superior: controles
        frame_controles = ttk.LabelFrame(frame_principal, text="Controles", padding="10")
        frame_controles.pack(fill=tk.X, pady=(0, 10))

        self.btn_cargar = ttk.Button(frame_controles, text="Cargar Archivo FASTA", command=self._cargar_archivo)
        self.btn_cargar.pack(side=tk.LEFT, padx=5)

        self.btn_analizar = ttk.Button(frame_controles, text="Analizar Secuencias", command=self._analizar_secuencias, state=tk.DISABLED)
        self.btn_analizar.pack(side=tk.LEFT, padx=5)

        self.btn_orfs = ttk.Button(frame_controles, text="Buscar ORFs", command=self._buscar_orfs, state=tk.DISABLED)
        self.btn_orfs.pack(side=tk.LEFT, padx=5)

        # Etiqueta de estado
        self.lbl_estado = ttk.Label(frame_controles, text="No hay archivo cargado")
        self.lbl_estado.pack(side=tk.RIGHT, padx=5)

        # Frame de busqueda de motivos
        frame_motivos = ttk.LabelFrame(frame_principal, text="Busqueda de Motivos", padding="10")
        frame_motivos.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(frame_motivos, text="Patron (regex o texto):").pack(side=tk.LEFT, padx=5)

        self.entrada_motivo = ttk.Entry(frame_motivos, width=40)
        self.entrada_motivo.pack(side=tk.LEFT, padx=5)

        self.btn_buscar_motivo = ttk.Button(frame_motivos, text="Buscar", command=self._buscar_motivo, state=tk.DISABLED)
        self.btn_buscar_motivo.pack(side=tk.LEFT, padx=5)

        # Frame de seleccion de secuencia
        frame_seleccion = ttk.Frame(frame_principal)
        frame_seleccion.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(frame_seleccion, text="Secuencia seleccionada:").pack(side=tk.LEFT, padx=5)

        self.combo_secuencias = ttk.Combobox(frame_seleccion, state="readonly", width=50)
        self.combo_secuencias.pack(side=tk.LEFT, padx=5)
        self.combo_secuencias.bind('<<ComboboxSelected>>', self._al_seleccionar_secuencia)

        # Frame de resultados con pestanas
        self.frame_resultados = ttk.Notebook(frame_principal)
        self.frame_resultados.pack(fill=tk.BOTH, expand=True)

        # Pestana de analisis basico
        self.pestana_analisis = ttk.Frame(self.frame_resultados)
        self.frame_resultados.add(self.pestana_analisis, text="Analisis Basico")

        self.texto_analisis = scrolledtext.ScrolledText(self.pestana_analisis, wrap=tk.WORD, font=("Courier", 10))
        self.texto_analisis.pack(fill=tk.BOTH, expand=True)

        # Pestana de ORFs
        self.pestana_orfs = ttk.Frame(self.frame_resultados)
        self.frame_resultados.add(self.pestana_orfs, text="ORFs")

        self.texto_orfs = scrolledtext.ScrolledText(self.pestana_orfs, wrap=tk.WORD, font=("Courier", 10))
        self.texto_orfs.pack(fill=tk.BOTH, expand=True)

        # Pestana de traduccion
        self.pestana_traduccion = ttk.Frame(self.frame_resultados)
        self.frame_resultados.add(self.pestana_traduccion, text="Traduccion")

        self.texto_traduccion = scrolledtext.ScrolledText(self.pestana_traduccion, wrap=tk.WORD, font=("Courier", 10))
        self.texto_traduccion.pack(fill=tk.BOTH, expand=True)

        # Pestana de resultados de busqueda
        self.pestana_busqueda = ttk.Frame(self.frame_resultados)
        self.frame_resultados.add(self.pestana_busqueda, text="Resultados Busqueda")

        self.texto_busqueda = scrolledtext.ScrolledText(self.pestana_busqueda, wrap=tk.WORD, font=("Courier", 10))
        self.texto_busqueda.pack(fill=tk.BOTH, expand=True)

        # Frame inferior: botones de exportacion
        frame_exportar = ttk.Frame(frame_principal)
        frame_exportar.pack(fill=tk.X, pady=(10, 0))

        self.btn_exportar_csv = ttk.Button(frame_exportar, text="Exportar Resultados a CSV", command=self._exportar_csv, state=tk.DISABLED)
        self.btn_exportar_csv.pack(side=tk.LEFT, padx=5)

        self.btn_exportar_txt = ttk.Button(frame_exportar, text="Exportar Resultados a TXT", command=self._exportar_txt, state=tk.DISABLED)
        self.btn_exportar_txt.pack(side=tk.LEFT, padx=5)

    def _configurar_estilos(self):
        """Configura los estilos visuales."""
        estilo = ttk.Style()
        estilo.configure("TButton", padding=6)
        estilo.configure("TLabel", padding=2)

    def _cargar_archivo(self):
        """Carga un archivo FASTA mediante dialogo."""
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo FASTA",
            filetypes=[("Archivos FASTA", "*.fasta *.fa *.fna *.ffn *.faa *.frn"),
                       ("Todos los archivos", "*.*")]
        )

        if not ruta:
            return

        try:
            self.secuencias_cargadas = cargar_fasta(ruta)
            self.ruta_archivo_actual = ruta

            if not self.secuencias_cargadas:
                messagebox.showwarning("Advertencia", "El archivo no contiene secuencias validas.")
                return

            # Validar secuencias
            secuencias_invalidas = []
            for id_seq, secuencia in self.secuencias_cargadas.items():
                es_valida, error = validar_secuencia(secuencia, 'adn')
                if not es_valida:
                    secuencias_invalidas.append(f"{id_seq}: {error}")

            if secuencias_invalidas:
                mensaje = "Algunas secuencias contienen caracteres no validos:\n\n"
                mensaje += "\n".join(secuencias_invalidas[:5])
                if len(secuencias_invalidas) > 5:
                    mensaje += f"\n... y {len(secuencias_invalidas) - 5} mas."
                messagebox.showwarning("Advertencia de validacion", mensaje)

            # Actualizar interfaz
            nombres_secuencias = list(self.secuencias_cargadas.keys())
            self.combo_secuencias['values'] = nombres_secuencias
            if nombres_secuencias:
                self.combo_secuencias.current(0)

            self.lbl_estado.config(text=f"Cargadas {len(self.secuencias_cargadas)} secuencias desde {Path(ruta).name}")
            self.btn_analizar.config(state=tk.NORMAL)
            self.btn_orfs.config(state=tk.NORMAL)
            self.btn_buscar_motivo.config(state=tk.NORMAL)

            # Mostrar resumen en area de texto
            self._mostrar_resumen_carga()

            logger.info(f"Archivo cargado: {ruta}, {len(self.secuencias_cargadas)} secuencias")

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar archivo:\n{str(e)}")
            logger.error(f"Error cargando archivo: {e}")

    def _mostrar_resumen_carga(self):
        """Muestra un resumen de las secuencias cargadas."""
        self.texto_analisis.delete(1.0, tk.END)

        resumen = "=" * 60 + "\n"
        resumen += "RESUMEN DE SECUENCIAS CARGADAS\n"
        resumen += "=" * 60 + "\n\n"

        for idx, (identificador, secuencia) in enumerate(self.secuencias_cargadas.items(), 1):
            resumen += f"{idx}. ID: {identificador}\n"
            resumen += f"   Longitud: {len(secuencia)} pb\n"
            resumen += f"   Inicio: {secuencia[:30]}...\n"
            resumen += f"   Fin: ...{secuencia[-30:]}\n\n"

        self.texto_analisis.insert(tk.END, resumen)

    def _analizar_secuencias(self):
        """Analiza todas las secuencias cargadas."""
        if not self.secuencias_cargadas:
            return

        try:
            secuencias_lista = extraer_secuencias(self.secuencias_cargadas)
            self.resultados_analisis = analizar_multiples_secuencias(secuencias_lista)

            # Mostrar resultados
            self.texto_analisis.delete(1.0, tk.END)

            resultado_texto = "=" * 70 + "\n"
            resultado_texto += "ANALISIS DE SECUENCIAS\n"
            resultado_texto += "=" * 70 + "\n\n"

            for res in self.resultados_analisis:
                resultado_texto += f"ID: {res['identificador']}\n"
                resultado_texto += "-" * 40 + "\n"
                resultado_texto += f"  Longitud: {res['longitud']} pb\n"
                resultado_texto += f"  Contenido GC: {res['contenido_gc']}%\n"
                resultado_texto += "  Conteo de nucleotidos:\n"

                conteo = res['conteo_nucleotidos']
                for nucleotido, cantidad in conteo.items():
                    if cantidad > 0:
                        resultado_texto += f"    {nucleotido}: {cantidad}\n"

                resultado_texto += "\n"

            self.texto_analisis.insert(tk.END, resultado_texto)

            # Habilitar botones de exportacion
            self.btn_exportar_csv.config(state=tk.NORMAL)
            self.btn_exportar_txt.config(state=tk.NORMAL)

            logger.info("Analisis completado")

        except Exception as e:
            messagebox.showerror("Error", f"Error durante el analisis:\n{str(e)}")
            logger.error(f"Error en analisis: {e}")

    def _buscar_orfs(self):
        """Busca ORFs en la secuencia seleccionada."""
        seleccion = self.combo_secuencias.get()
        if not seleccion or seleccion not in self.secuencias_cargadas:
            messagebox.showwarning("Advertencia", "Seleccione una secuencia primero.")
            return

        try:
            secuencia = self.secuencias_cargadas[seleccion]
            orfs = encontrar_orfs(secuencia)

            self.texto_orfs.delete(1.0, tk.END)

            resultado_texto = "=" * 70 + "\n"
            resultado_texto += f"ORFs ENCONTRADOS - {seleccion}\n"
            resultado_texto += "=" * 70 + "\n\n"

            resultado_texto += "HEBRA DIRECTA:\n"
            resultado_texto += "-" * 40 + "\n"
            if orfs['directa']:
                for i, orf in enumerate(orfs['directa'][:20], 1):  # Limitar a 20
                    resultado_texto += f"{i}. Marco {orf['marco']}: pos {orf['inicio']}-{orf['fin']} "
                    resultado_texto += f"({orf['longitud']} pb)\n"
                if len(orfs['directa']) > 20:
                    resultado_texto += f"... y {len(orfs['directa']) - 20} mas.\n"
            else:
                resultado_texto += "  No se encontraron ORFs en hebra directa.\n"

            resultado_texto += "\nHEBRA COMPLEMENTARIA:\n"
            resultado_texto += "-" * 40 + "\n"
            if orfs['complementaria']:
                for i, orf in enumerate(orfs['complementaria'][:20], 1):
                    resultado_texto += f"{i}. Marco {orf['marco']}: pos {orf['inicio']}-{orf['fin']} "
                    resultado_texto += f"({orf['longitud']} pb)\n"
                if len(orfs['complementaria']) > 20:
                    resultado_texto += f"... y {len(orfs['complementaria']) - 20} mas.\n"
            else:
                resultado_texto += "  No se encontraron ORFs en hebra complementaria.\n"

            self.texto_orfs.insert(tk.END, resultado_texto)

            logger.info(f"Busqueda de ORFs completada para {seleccion}")

        except Exception as e:
            messagebox.showerror("Error", f"Error buscando ORFs:\n{str(e)}")
            logger.error(f"Error en busqueda ORFs: {e}")

    def _buscar_motivo(self):
        """Busca un motivo en la secuencia seleccionada."""
        patron = self.entrada_motivo.get().strip()
        if not patron:
            messagebox.showwarning("Advertencia", "Ingrese un patron de busqueda.")
            return

        seleccion = self.combo_secuencias.get()
        if not seleccion or seleccion not in self.secuencias_cargadas:
            messagebox.showwarning("Advertencia", "Seleccione una secuencia primero.")
            return

        try:
            secuencia = self.secuencias_cargadas[seleccion]
            coincidencias = buscar_motivo(secuencia, patron)

            self.texto_busqueda.delete(1.0, tk.END)

            resultado_texto = "=" * 70 + "\n"
            resultado_texto += f"RESULTADOS DE BUSQUEDA - Patron: '{patron}'\n"
            resultado_texto += f"Secuencia: {seleccion}\n"
            resultado_texto += "=" * 70 + "\n\n"

            if coincidencias:
                resultado_texto += f"Se encontraron {len(coincidencias)} coincidencias:\n\n"
                for i, coin in enumerate(coincidencias[:50], 1):  # Limitar a 50
                    resultado_texto += f"{i}. Posicion {coin['inicio']}-{coin['fin']} "
                    resultado_texto += f"({coin['longitud']} pb): {coin['secuencia']}\n"

                if len(coincidencias) > 50:
                    resultado_texto += f"\n... y {len(coincidencias) - 50} coincidencias mas.\n"
            else:
                resultado_texto += "No se encontraron coincidencias para el patron especificado.\n"

            self.texto_busqueda.insert(tk.END, resultado_texto)

            # Cambiar automaticamente a la pestana de resultados de busqueda
            pestana_index = self.frame_resultados.index(self.pestana_busqueda)
            self.frame_resultados.select(pestana_index)

            logger.info(f"Busqueda de motivo '{patron}' completada: {len(coincidencias)} coincidencias")

        except ValueError as e:
            messagebox.showerror("Error de patron", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la busqueda:\n{str(e)}")
            logger.error(f"Error en busqueda de motivo: {e}")

    def _al_seleccionar_secuencia(self, event=None):
        """Evento al seleccionar una secuencia del combobox."""
        seleccion = self.combo_secuencias.get()
        if seleccion and seleccion in self.secuencias_cargadas:
            # Traducir automaticamente al seleccionar
            self._traducir_secuencia_seleccionada()

    def _traducir_secuencia_seleccionada(self):
        """Traduce la secuencia seleccionada en los tres marcos."""
        seleccion = self.combo_secuencias.get()
        if not seleccion or seleccion not in self.secuencias_cargadas:
            return

        try:
            secuencia = self.secuencias_cargadas[seleccion]

            self.texto_traduccion.delete(1.0, tk.END)

            resultado_texto = "=" * 70 + "\n"
            resultado_texto += f"TRADUCCION - {seleccion}\n"
            resultado_texto += "=" * 70 + "\n\n"

            for marco in range(3):
                traduccion = traducir_adn(secuencia, marco)

                resultado_texto += f"Marco {marco}:\n"
                resultado_texto += "-" * 40 + "\n"
                resultado_texto += f"Longitud: {traduccion['longitud']} aa\n"
                resultado_texto += f"Codones de parada (*): {traduccion['codones_parada']}\n"

                # Mostrar secuencia en bloques de 60 caracteres
                secuencia_prot = traduccion['secuencia_proteica']
                resultado_texto += "Secuencia:\n"
                for i in range(0, len(secuencia_prot), 60):
                    resultado_texto += f"  {secuencia_prot[i:i+60]}\n"

                resultado_texto += "\n"

            self.texto_traduccion.insert(tk.END, resultado_texto)

        except Exception as e:
            logger.error(f"Error en traduccion: {e}")

    def _exportar_csv(self):
        """Exporta resultados a CSV."""
        if not self.resultados_analisis:
            messagebox.showwarning("Advertencia", "No hay resultados para exportar.")
            return

        ruta = filedialog.asksaveasfilename(
            title="Exportar a CSV",
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )

        if ruta:
            try:
                exportar_csv(self.resultados_analisis, ruta)
                messagebox.showinfo("Exito", f"Resultados exportados a:\n{ruta}")
                logger.info(f"Resultados exportados a CSV: {ruta}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar:\n{str(e)}")
                logger.error(f"Error exportando CSV: {e}")

    def _exportar_txt(self):
        """Exporta resultados a TXT."""
        if not self.secuencias_cargadas:
            messagebox.showwarning("Advertencia", "No hay datos para exportar.")
            return

        ruta = filedialog.asksaveasfilename(
            title="Exportar a TXT",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )

        if ruta:
            try:
                exportar_txt(self.secuencias_cargadas, self.resultados_analisis, ruta)
                messagebox.showinfo("Exito", f"Datos exportados a:\n{ruta}")
                logger.info(f"Datos exportados a TXT: {ruta}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar:\n{str(e)}")
                logger.error(f"Error exportando TXT: {e}")

    def _mostrar_acerca(self):
        """Muestra la ventana Acerca de."""
        messagebox.showinfo(
            "Acerca de",
            "Analizador de Secuencias Biologicas\n\n"
            "Version 1.0.0\n\n"
            "Herramienta para analisis basico de secuencias\n"
            "de ADN desde archivos FASTA.\n\n"
            "Funcionalidades:\n"
            "- Carga de archivos FASTA\n"
            "- Analisis de contenido GC\n"
            "- Conteo de nucleotidos\n"
            "- Deteccion de ORFs\n"
            "- Traduccion a proteina\n"
            "- Busqueda de motivos"
        )