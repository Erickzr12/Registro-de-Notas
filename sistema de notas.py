import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

class RegistroNotasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Sistema de Notas Profesional")
        self.root.geometry("1150x700")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)

        self.fuente = ("Segoe UI", 12)

        self.conexion = sqlite3.connect("notas.db")
        self.cursor = self.conexion.cursor()
        self.crear_tabla()
        self.actualizar_tabla()

        self.titulo = tk.Label(root, text="📘 REGISTRO ACADÉMICO", font=("Segoe UI", 20, "bold"), bg="#1e1e1e", fg="#00bfff")
        self.titulo.pack(pady=15)

        form_frame = tk.Frame(root, bg="#1e1e1e")
        form_frame.pack(pady=5)

        self._crear_entrada(form_frame, "👤 Nombre:", 0)
        self._crear_entrada(form_frame, "📝 Nota 1:", 1)
        self._crear_entrada(form_frame, "📝 Nota 2:", 2)
        self._crear_entrada(form_frame, "📝 Nota 3:", 3)

        tk.Button(form_frame, text="✅ Registrar", font=self.fuente, bg="#00bfff", fg="white", width=20, command=self.registrar).grid(row=4, column=0, columnspan=2, pady=10)

        filtro_frame = tk.Frame(root, bg="#1e1e1e")
        filtro_frame.pack(pady=5)

        tk.Label(filtro_frame, text="🔎 Buscar:", bg="#1e1e1e", fg="white", font=self.fuente).pack(side=tk.LEFT, padx=5)
        self.filtro_entry = tk.Entry(filtro_frame, font=self.fuente, width=30)
        self.filtro_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(filtro_frame, text="🔍 Aplicar", command=self.filtrar, bg="#3498db", fg="white", font=self.fuente).pack(side=tk.LEFT, padx=5)
        tk.Button(filtro_frame, text="🧹 Limpiar", command=self.cargar_datos, bg="#555", fg="white", font=self.fuente).pack(side=tk.LEFT)

        self.tree = ttk.Treeview(root, columns=("Nombre", "Nota 1", "Nota 2", "Nota 3", "Promedio", "Estado"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=130)
        self.tree.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2c2f33", foreground="white", rowheight=30,
                        fieldbackground="#2c2f33", font=("Segoe UI", 11))
        style.map("Treeview", background=[("selected", "#00bfff")])

        btn_frame = tk.Frame(root, bg="#1e1e1e")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="📈 Ver Gráfico", command=self.ver_grafico, bg="#f39c12", fg="white", font=self.fuente, width=16).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="📤 Exportar a Excel", command=self.exportar_excel, bg="#2ecc71", fg="white", font=self.fuente, width=16).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✏️ Editar Seleccionado", command=self.editar_registro, bg="#2980b9", fg="white", font=self.fuente, width=18).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑 Eliminar Seleccionado", command=self.eliminar_registro, bg="#e74c3c", fg="white", font=self.fuente, width=18).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="📥 Importar Excel", command=self.importar_excel, bg="#9b59b6", fg="white", font=self.fuente, width=16).pack(side=tk.LEFT, padx=5)

        self.cargar_datos()

    def _crear_entrada(self, frame, texto, fila):
        label = tk.Label(frame, text=texto, bg="#1e1e1e", fg="white", font=self.fuente)
        label.grid(row=fila, column=0, padx=10, pady=5, sticky=tk.W)
        entry = tk.Entry(frame, font=self.fuente, width=30)
        entry.grid(row=fila, column=1, padx=10, pady=5)
        if "Nombre" in texto:
            self.nombre_entry = entry
        elif "Nota 1" in texto:
            self.nota1_entry = entry
        elif "Nota 2" in texto:
            self.nota2_entry = entry
        elif "Nota 3" in texto:
            self.nota3_entry = entry

    def crear_tabla(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                nota1 REAL,
                nota2 REAL,
                nota3 REAL,
                promedio REAL,
                estado TEXT
            )
        ''')
        self.conexion.commit()

    def actualizar_tabla(self):
        self.cursor.execute("PRAGMA table_info(notas)")
        columnas = [col[1] for col in self.cursor.fetchall()]
        campos = [("nota1", "REAL"), ("nota2", "REAL"), ("nota3", "REAL"), ("promedio", "REAL"), ("estado", "TEXT")]
        for campo, tipo in campos:
            if campo not in columnas:
                self.cursor.execute(f"ALTER TABLE notas ADD COLUMN {campo} {tipo}")
        self.conexion.commit()

    def cargar_datos(self):
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("SELECT id, nombre, nota1, nota2, nota3, promedio, estado FROM notas")
        for fila in self.cursor.fetchall():
            self.tree.insert("", tk.END, values=fila[1:], tags=("aprobado" if fila[6] == "Aprobado" else "desaprobado"), iid=str(fila[0]))
        self.tree.tag_configure("aprobado", foreground="deepskyblue")
        self.tree.tag_configure("desaprobado", foreground="red")

    def registrar(self):
        nombre = self.nombre_entry.get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre no puede estar vacío.")
            return
        try:
            nota1 = float(self.nota1_entry.get())
            nota2 = float(self.nota2_entry.get())
            nota3 = float(self.nota3_entry.get())
            promedio = round((nota1 + nota2 + nota3) / 3, 2)
            estado = "Aprobado" if promedio >= 11 else "Desaprobado"

            self.cursor.execute(
                "INSERT INTO notas (nombre, nota1, nota2, nota3, promedio, estado) VALUES (?, ?, ?, ?, ?, ?)",
                (nombre, nota1, nota2, nota3, promedio, estado)
            )
            self.conexion.commit()
            self.cargar_datos()
            self.nombre_entry.delete(0, tk.END)
            self.nota1_entry.delete(0, tk.END)
            self.nota2_entry.delete(0, tk.END)
            self.nota3_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa notas numéricas válidas.")

    def editar_registro(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un estudiante.")
            return
        id_sel = seleccionado[0]
        nombre = self.nombre_entry.get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre no puede estar vacío.")
            return
        try:
            nota1 = float(self.nota1_entry.get())
            nota2 = float(self.nota2_entry.get())
            nota3 = float(self.nota3_entry.get())
            promedio = round((nota1 + nota2 + nota3) / 3, 2)
            estado = "Aprobado" if promedio >= 11 else "Desaprobado"
            self.cursor.execute(
                "UPDATE notas SET nombre=?, nota1=?, nota2=?, nota3=?, promedio=?, estado=? WHERE id=?",
                (nombre, nota1, nota2, nota3, promedio, estado, id_sel)
            )
            self.conexion.commit()
            self.cargar_datos()
            self.nombre_entry.delete(0, tk.END)
            self.nota1_entry.delete(0, tk.END)
            self.nota2_entry.delete(0, tk.END)
            self.nota3_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Datos inválidos al editar.")

    def eliminar_registro(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un estudiante.")
            return
        id_sel = seleccionado[0]
        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este registro?"):
            self.cursor.execute("DELETE FROM notas WHERE id=?", (id_sel,))
            self.conexion.commit()
            self.cargar_datos()

    def filtrar(self):
        texto = self.filtro_entry.get().strip().lower()
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("SELECT id, nombre, nota1, nota2, nota3, promedio, estado FROM notas")
        for fila in self.cursor.fetchall():
            if texto in fila[1].lower() or texto in fila[6].lower():
                self.tree.insert("", tk.END, values=fila[1:], tags=("aprobado" if fila[6] == "Aprobado" else "desaprobado"), iid=str(fila[0]))
        self.tree.tag_configure("aprobado", foreground="deepskyblue")
        self.tree.tag_configure("desaprobado", foreground="red")

    def exportar_excel(self):
        self.cursor.execute("SELECT nombre, nota1, nota2, nota3, promedio, estado FROM notas")
        datos = self.cursor.fetchall()
        if not datos:
            messagebox.showwarning("Atención", "No hay datos para exportar.")
            return
        archivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if archivo:
            df = pd.DataFrame(datos, columns=["Nombre", "Nota 1", "Nota 2", "Nota 3", "Promedio", "Estado"])
            df.to_excel(archivo, index=False)
            messagebox.showinfo("Éxito", "Archivo exportado correctamente.")

    def importar_excel(self):
        archivo = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx *.xls")])
        if not archivo:
            return
        try:
            df = pd.read_excel(archivo)
            for _, row in df.iterrows():
                if {"Nombre", "Nota 1", "Nota 2", "Nota 3"}.issubset(row.index):
                    nombre = str(row["Nombre"])
                    nota1 = float(row["Nota 1"])
                    nota2 = float(row["Nota 2"])
                    nota3 = float(row["Nota 3"])
                    promedio = round((nota1 + nota2 + nota3) / 3, 2)
                    estado = "Aprobado" if promedio >= 11 else "Desaprobado"
                    self.cursor.execute("INSERT INTO notas (nombre, nota1, nota2, nota3, promedio, estado) VALUES (?, ?, ?, ?, ?, ?)",
                                        (nombre, nota1, nota2, nota3, promedio, estado))
            self.conexion.commit()
            self.cargar_datos()
            messagebox.showinfo("Éxito", "Datos importados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al importar: {e}")

    def ver_grafico(self):
        self.cursor.execute("SELECT nombre, promedio FROM notas")
        datos = self.cursor.fetchall()
        if not datos:
            messagebox.showwarning("Sin datos", "Agrega estudiantes para ver el gráfico.")
            return
        nombres = [fila[0] for fila in datos]
        promedios = [fila[1] for fila in datos]

        plt.figure(figsize=(12, 6))
        colores = ["blue" if p >= 11 else "red" for p in promedios]
        plt.bar(nombres, promedios, color=colores)
        plt.axhline(11, color="gray", linestyle="--", label="Línea de Aprobación")
        plt.title("📊 Promedio por Estudiante")
        plt.ylabel("Promedio")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.legend()
        plt.show()

# EJECUCIÓN
if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroNotasApp(root)
    root.mainloop()
