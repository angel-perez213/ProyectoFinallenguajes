import os
import tempfile
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from clasificador import clasificar_gramatica_texto, comparar_gramaticas_texto
from automatas import cargar_automata_desde_json, clasificar_automata
from ejemplos import (
    obtener_ejemplo_gramatica,
    obtener_ejemplo_automata,
    generar_gramatica_aleatoria,
)
from tutor import generar_ejercicio, evaluar_respuesta
from visualizador import dibujar_gramatica, dibujar_automata
from reportes import generar_reporte_pdf


def parsear_gramatica_simple(texto: str):
    producciones = []
    for linea in texto.splitlines():
        linea = linea.strip()
        if not linea:
            continue
        if "->" in linea:
            izq, der = linea.split("->", 1)
        elif "→" in linea:
            izq, der = linea.split("→", 1)
        else:
            continue
        izquierda = izq.strip()
        rhs = der.strip()
        if "|" in rhs:
            alternativas = rhs.split("|")
        else:
            alternativas = [rhs]
        for alt in alternativas:
            derecha = alt.strip()
            producciones.append((izquierda, derecha))
    return producciones


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Chomsky Classifier AI")

        self.resultado_gram = None
        self.resultado_auto = None
        self.imagen_gram = None
        self.imagen_auto = None
        self.ejercicio_tutor = None

        self.crear_interfaz()

    def crear_interfaz(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True)

        frame_gram = ttk.Frame(notebook)
        frame_auto = ttk.Frame(notebook)
        frame_comp = ttk.Frame(notebook)
        frame_gen = ttk.Frame(notebook)
        frame_tutor = ttk.Frame(notebook)

        notebook.add(frame_gram, text="Clasificar gramatica")
        notebook.add(frame_auto, text="Clasificar automata")
        notebook.add(frame_comp, text="Comparar gramatica")
        notebook.add(frame_gen, text="Generador")
        notebook.add(frame_tutor, text="Tutor")

        self.crear_tab_gramatica(frame_gram)
        self.crear_tab_automata(frame_auto)
        self.crear_tab_comparar(frame_comp)
        self.crear_tab_generador(frame_gen)
        self.crear_tab_tutor(frame_tutor)

    def crear_tab_gramatica(self, frame):
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(5, weight=1)

        lbl = ttk.Label(frame, text="Ingresa la gramatica:")
        lbl.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.txt_gram = tk.Text(frame, height=8)
        self.txt_gram.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.txt_gram.insert("1.0", obtener_ejemplo_gramatica(3))

        cont_botones = ttk.Frame(frame)
        cont_botones.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        btn_clas = ttk.Button(cont_botones, text="Clasificar", command=self.clasificar_gramatica)
        btn_clas.grid(row=0, column=0, padx=2)

        btn_diag = ttk.Button(
            cont_botones, text="Ver diagrama", command=self.ver_diagrama_gramatica
        )
        btn_diag.grid(row=0, column=1, padx=2)

        btn_pdf = ttk.Button(
            cont_botones, text="Generar reporte PDF", command=self.generar_pdf_gramatica
        )
        btn_pdf.grid(row=0, column=2, padx=2)

        self.lbl_tipo_gram = ttk.Label(frame, text="Tipo: ")
        self.lbl_tipo_gram.grid(row=3, column=0, sticky="w", padx=5, pady=5)

        lbl_exp = ttk.Label(frame, text="Explicacion:")
        lbl_exp.grid(row=4, column=0, sticky="w", padx=5, pady=5)

        self.txt_exp_gram = tk.Text(frame, height=10)
        self.txt_exp_gram.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)

    def clasificar_gramatica(self):
        texto = self.txt_gram.get("1.0", "end").strip()
        if not texto:
            messagebox.showwarning("Aviso", "Ingresa una gramatica.")
            return
        try:
            resultado = clasificar_gramatica_texto(texto)
            self.resultado_gram = resultado
            self.lbl_tipo_gram.config(text="Tipo: " + resultado.etiqueta)
            self.txt_exp_gram.delete("1.0", "end")
            for linea in resultado.explicacion:
                self.txt_exp_gram.insert("end", linea + "\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error al analizar la gramatica:\n{e}")

    def ver_diagrama_gramatica(self):
        texto = self.txt_gram.get("1.0", "end").strip()
        if not texto:
            messagebox.showwarning("Aviso", "Ingresa una gramatica.")
            return
        try:
            producciones = parsear_gramatica_simple(texto)
            with tempfile.TemporaryDirectory() as tmpdir:
                ruta_base = os.path.join(tmpdir, "gramatica_diagrama")
                ruta_img = dibujar_gramatica(producciones, ruta_base)
                top = tk.Toplevel(self.root)
                top.title("Diagrama de gramatica")
                img = tk.PhotoImage(file=ruta_img)
                self.imagen_gram = img
                lbl_img = tk.Label(top, image=img)
                lbl_img.pack(padx=10, pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el diagrama:\n{e}")

    def generar_pdf_gramatica(self):
        if self.resultado_gram is None:
            messagebox.showwarning("Aviso", "Primero clasifica la gramatica.")
            return
        texto = self.txt_gram.get("1.0", "end").strip()
        if not texto:
            messagebox.showwarning("Aviso", "Ingresa una gramatica.")
            return

        ruta_pdf = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar reporte de gramatica",
        )
        if not ruta_pdf:
            return

        try:
            producciones = parsear_gramatica_simple(texto)
            with tempfile.TemporaryDirectory() as tmpdir:
                ruta_base = os.path.join(tmpdir, "gramatica_diagrama")
                ruta_img = dibujar_gramatica(producciones, ruta_base)
                generar_reporte_pdf(
                    ruta_pdf,
                    "Reporte de gramatica",
                    texto,
                    True,
                    self.resultado_gram,
                    [ruta_img],
                )
            messagebox.showinfo("Reporte", "Reporte PDF generado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte:\n{e}")

    def crear_tab_automata(self, frame):
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(5, weight=1)

        lbl = ttk.Label(frame, text="Automata en formato JSON:")
        lbl.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.txt_auto = tk.Text(frame, height=10)
        self.txt_auto.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.txt_auto.insert("1.0", obtener_ejemplo_automata(3))

        cont_botones = ttk.Frame(frame)
        cont_botones.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        btn_clas = ttk.Button(
            cont_botones, text="Clasificar automata", command=self.clasificar_automata_ui
        )
        btn_clas.grid(row=0, column=0, padx=2)

        btn_diag = ttk.Button(
            cont_botones, text="Ver diagrama", command=self.ver_diagrama_automata
        )
        btn_diag.grid(row=0, column=1, padx=2)

        btn_pdf = ttk.Button(
            cont_botones, text="Generar reporte PDF", command=self.generar_pdf_automata
        )
        btn_pdf.grid(row=0, column=2, padx=2)

        self.lbl_tipo_auto = ttk.Label(frame, text="Tipo: ")
        self.lbl_tipo_auto.grid(row=3, column=0, sticky="w", padx=5, pady=5)

        lbl_exp = ttk.Label(frame, text="Explicacion:")
        lbl_exp.grid(row=4, column=0, sticky="w", padx=5, pady=5)

        self.txt_exp_auto = tk.Text(frame, height=10)
        self.txt_exp_auto.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)

    def clasificar_automata_ui(self):
        texto = self.txt_auto.get("1.0", "end").strip()
        if not texto:
            messagebox.showwarning("Aviso", "Ingresa un automata en JSON.")
            return
        try:
            automata = cargar_automata_desde_json(texto)
            resultado = clasificar_automata(automata)
            self.resultado_auto = resultado
            self.lbl_tipo_auto.config(text="Tipo: " + resultado.etiqueta)
            self.txt_exp_auto.delete("1.0", "end")
            for linea in resultado.explicacion:
                self.txt_exp_auto.insert("end", linea + "\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error al analizar el automata:\n{e}")

    def ver_diagrama_automata(self):
        texto = self.txt_auto.get("1.0", "end").strip()
        if not texto:
            messagebox.showwarning("Aviso", "Ingresa un automata en JSON.")
            return
        try:
            automata = cargar_automata_desde_json(texto)
            with tempfile.TemporaryDirectory() as tmpdir:
                ruta_base = os.path.join(tmpdir, "automata_diagrama")
                ruta_img = dibujar_automata(automata, ruta_base)
                top = tk.Toplevel(self.root)
                top.title("Diagrama de automata")
                img = tk.PhotoImage(file=ruta_img)
                self.imagen_auto = img
                lbl_img = tk.Label(top, image=img)
                lbl_img.pack(padx=10, pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el diagrama:\n{e}")

    def generar_pdf_automata(self):
        if self.resultado_auto is None:
            messagebox.showwarning("Aviso", "Primero clasifica el automata.")
            return
        texto = self.txt_auto.get("1.0", "end").strip()
        if not texto:
            messagebox.showwarning("Aviso", "Ingresa un automata en JSON.")
            return

        ruta_pdf = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar reporte de automata",
        )
        if not ruta_pdf:
            return

        try:
            automata = cargar_automata_desde_json(texto)
            with tempfile.TemporaryDirectory() as tmpdir:
                ruta_base = os.path.join(tmpdir, "automata_diagrama")
                ruta_img = dibujar_automata(automata, ruta_base)
                generar_reporte_pdf(
                    ruta_pdf,
                    "Reporte de automata",
                    texto,
                    False,
                    self.resultado_auto,
                    [ruta_img],
                )
            messagebox.showinfo("Reporte", "Reporte PDF generado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte:\n{e}")

    def crear_tab_comparar(self, frame):
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(4, weight=1)

        lbl1 = ttk.Label(frame, text="Gramatica 1:")
        lbl1.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        lbl2 = ttk.Label(frame, text="Gramatica 2:")
        lbl2.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        self.txt_g1 = tk.Text(frame, height=10)
        self.txt_g2 = tk.Text(frame, height=10)
        self.txt_g1.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.txt_g2.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        self.txt_g1.insert("1.0", obtener_ejemplo_gramatica(2))
        self.txt_g2.insert("1.0", obtener_ejemplo_gramatica(2))

        lbl_long = ttk.Label(frame, text="Longitud maxima de cadenas a comparar:")
        lbl_long.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.spin_long = tk.Spinbox(frame, from_=1, to=8)
        self.spin_long.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.spin_long.delete(0, "end")
        self.spin_long.insert(0, "4")

        btn = ttk.Button(frame, text="Comparar", command=self.comparar_gramaticas_ui)
        btn.grid(row=3, column=0, sticky="w", padx=5, pady=5)

        self.txt_comp_res = tk.Text(frame, height=8)
        self.txt_comp_res.grid(
            row=4, column=0, columnspan=2, sticky="nsew", padx=5, pady=5
        )

    def comparar_gramaticas_ui(self):
        g1 = self.txt_g1.get("1.0", "end").strip()
        g2 = self.txt_g2.get("1.0", "end").strip()
        try:
            max_long = int(self.spin_long.get())
        except ValueError:
            messagebox.showwarning("Aviso", "Longitud maxima invalida.")
            return
        if not g1 or not g2:
            messagebox.showwarning("Aviso", "Ingresa ambas gramaticas.")
            return
        try:
            mensaje = comparar_gramaticas_texto(g1, g2, max_longitud=max_long)
            self.txt_comp_res.delete("1.0", "end")
            self.txt_comp_res.insert("end", mensaje)
        except Exception as e:
            messagebox.showerror("Error", f"Error al comparar gramaticas:\n{e}")

    def crear_tab_generador(self, frame):
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(7, weight=1)

        lbl_tipo = ttk.Label(frame, text="Tipo de gramatica a generar (0,1,2,3):")
        lbl_tipo.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.combo_tipo = ttk.Combobox(frame, values=["3", "2", "1", "0"])
        self.combo_tipo.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.combo_tipo.set("3")

        btn_gen = ttk.Button(frame, text="Generar gramatica", command=self.generar_gramatica_ui)
        btn_gen.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        self.txt_gen_gram = tk.Text(frame, height=8)
        self.txt_gen_gram.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)

        lbl_auto = ttk.Label(frame, text="Tipo de automata de ejemplo (0,2,3):")
        lbl_auto.grid(row=4, column=0, sticky="w", padx=5, pady=5)

        self.combo_auto = ttk.Combobox(frame, values=["3", "2", "0"])
        self.combo_auto.grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.combo_auto.set("3")

        btn_auto = ttk.Button(
            frame, text="Mostrar automata de ejemplo", command=self.mostrar_automata_ejemplo_ui
        )
        btn_auto.grid(row=6, column=0, sticky="w", padx=5, pady=5)

        self.txt_gen_auto = tk.Text(frame, height=8)
        self.txt_gen_auto.grid(row=7, column=0, sticky="nsew", padx=5, pady=5)

    def generar_gramatica_ui(self):
        try:
            tipo = int(self.combo_tipo.get())
        except ValueError:
            messagebox.showwarning("Aviso", "Selecciona un tipo valido.")
            return
        g = generar_gramatica_aleatoria(tipo)
        self.txt_gen_gram.delete("1.0", "end")
        self.txt_gen_gram.insert("end", g)

    def mostrar_automata_ejemplo_ui(self):
        try:
            tipo = int(self.combo_auto.get())
        except ValueError:
            messagebox.showwarning("Aviso", "Selecciona un tipo valido.")
            return
        a = obtener_ejemplo_automata(tipo)
        self.txt_gen_auto.delete("1.0", "end")
        self.txt_gen_auto.insert("end", a)

    def crear_tab_tutor(self, frame):
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        self.ejercicio_tutor = generar_ejercicio()

        btn_nuevo = ttk.Button(frame, text="Nuevo ejercicio", command=self.nuevo_ejercicio_tutor)
        btn_nuevo.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.txt_enunciado = tk.Text(frame, height=10)
        self.txt_enunciado.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.actualizar_enunciado()

        lbl_resp = ttk.Label(frame, text="Selecciona tu respuesta:")
        lbl_resp.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        self.combo_resp = ttk.Combobox(
            frame,
            values=[
                "Tipo 3 - Regular",
                "Tipo 2 - Libre de contexto",
                "Tipo 1 - Sensible al contexto",
                "Tipo 0 - Recursivamente enumerable",
            ],
        )
        self.combo_resp.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.combo_resp.set("Tipo 3 - Regular")

        btn_ver = ttk.Button(frame, text="Ver resultado", command=self.ver_resultado_tutor)
        btn_ver.grid(row=4, column=0, sticky="w", padx=5, pady=5)

    def actualizar_enunciado(self):
        self.txt_enunciado.delete("1.0", "end")
        self.txt_enunciado.insert("end", self.ejercicio_tutor.enunciado)

    def nuevo_ejercicio_tutor(self):
        self.ejercicio_tutor = generar_ejercicio()
        self.actualizar_enunciado()

    def ver_resultado_tutor(self):
        mapa = {
            "Tipo 3 - Regular": 3,
            "Tipo 2 - Libre de contexto": 2,
            "Tipo 1 - Sensible al contexto": 1,
            "Tipo 0 - Recursivamente enumerable": 0,
        }
        clave = self.combo_resp.get()
        if clave not in mapa:
            messagebox.showwarning("Aviso", "Selecciona una respuesta.")
            return
        tipo_usuario = mapa[clave]
        correcto, mensaje = evaluar_respuesta(self.ejercicio_tutor, tipo_usuario)
        if correcto:
            messagebox.showinfo("Resultado", mensaje)
        else:
            messagebox.showerror("Resultado", mensaje)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
