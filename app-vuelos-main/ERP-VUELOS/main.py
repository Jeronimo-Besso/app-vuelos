import sqlite3
import customtkinter as ctk
from Clientes.clientes import ClientesSeccion
from Vuelos.vuelos import VuelosSeccion
from Historial.historial import HistorialSeccion

class ERPApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ERP System")
        self.geometry("1400x1000")

        # Configuración del layout principal
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Barra lateral
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color="#A9A9A9")
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar_label = ctk.CTkLabel(self.sidebar, text="Secciones", font=ctk.CTkFont(size=20, weight="bold"))
        self.sidebar_label.grid(pady=20)

        # Sección para notas derecha
        self.notas = ctk.CTkFrame(self, width=300, fg_color="black")  # Aumenté el ancho para que se vea mejor
        self.notas.grid(row=0, column=10, sticky="ns")
        self.notas_label = ctk.CTkLabel(self.notas, text="Notas", font=ctk.CTkFont(size=20, weight="bold"))
        self.notas_label.grid(pady=20)

        # Sección para notas izquierda
        self.nota_frame = ctk.CTkFrame(self.sidebar, fg_color="#333333", width=150, height=80)
        self.nota_frame.grid(row=10, column=0, sticky="ns", padx=10, pady=10)  # Usa grid para posicionar el frame
        self.nota_textbox = ctk.CTkTextbox(self.nota_frame, height=3, width=150)
        self.nota_textbox.grid(pady=5, padx=5, sticky="w")  # Usa grid para posicionar el textbox

        # Mueve la nota_label dentro de nota_frame usando grid
        self.nota_label = ctk.CTkButton(self.nota_frame, text="Agregar Nota", command=self.agregarNotas, font=ctk.CTkFont(size=14, weight="bold"))
        self.nota_label.grid(pady=5, padx=5, sticky="w")  # Usa grid para posicionar la label

        # Botones para cambiar entre secciones
        self.vuelos_button = ctk.CTkButton(self.sidebar, text="Vuelos", command=self.show_vuelos, fg_color="#1A1A1A", hover_color="#808080")
        self.vuelos_button.grid(pady=5, padx=5, sticky="ew")
        self.clientes_button = ctk.CTkButton(self.sidebar, text="Clientes", command=self.show_clientes, fg_color="#1A1A1A", hover_color="#808080")
        self.clientes_button.grid(pady=5, padx=5, sticky="ew")
        self.historial_button = ctk.CTkButton(self.sidebar, text="Historial", command=self.show_historial, fg_color="#1A1A1A", hover_color="#808080")
        self.historial_button.grid(pady=5, padx=5, sticky="ew")

        # Área principal
import sqlite3
import customtkinter as ctk
from Clientes.clientes import ClientesSeccion
from Vuelos.vuelos import VuelosSeccion
from Historial.historial import HistorialSeccion

class ERPApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ERP System")
        self.geometry("1400x1000")

        # Inicializar base de datos
        self.conectar_db()

        # Configuración del layout principal
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Barra lateral
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color="#A9A9A9")
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar_label = ctk.CTkLabel(self.sidebar, text="Secciones", font=ctk.CTkFont(size=20, weight="bold"))
        self.sidebar_label.pack(pady=20)

        # Sección de notas (derecha)
        self.notas = ctk.CTkFrame(self, width=100, fg_color="black")
        self.notas.grid(row=0, column=10, sticky="ns")
        self.notas_label = ctk.CTkLabel(self.notas, text="        Notas        ", font=ctk.CTkFont(size=20, weight="bold"))
        self.notas_label.pack(pady=20)

        # Sección para agregar notas (izquierda)
        nota_frame = ctk.CTkFrame(self.sidebar, fg_color="#333333", width=150, height=80)
        nota_frame.pack(pady=10, padx=10, fill="x", side="bottom")
        nota_label = ctk.CTkLabel(nota_frame, text="Agregar Nota", font=ctk.CTkFont(size=14, weight="bold"))
        nota_label.pack(pady=5, padx=5)

        self.nota_textbox = ctk.CTkTextbox(nota_frame, height=3, width=150)
        self.nota_textbox.pack(padx=10, pady=5)

        notas_button = ctk.CTkButton(nota_frame, text="Agregar", command=self.agregarNotas)
        notas_button.pack(pady=5, padx=5)

        # Botones para cambiar entre secciones
        self.vuelos_button = ctk.CTkButton(self.sidebar, text="Vuelos", command=self.show_vuelos, fg_color="#1A1A1A", hover_color="#808080")
        self.vuelos_button.pack(pady=5, padx=5, fill="x")

        self.clientes_button = ctk.CTkButton(self.sidebar, text="Clientes", command=self.show_clientes, fg_color="#1A1A1A", hover_color="#808080")
        self.clientes_button.pack(pady=5, padx=5, fill="x")

        self.historial_button = ctk.CTkButton(self.sidebar, text="Historial", command=self.show_historial, fg_color="#1A1A1A", hover_color="#808080")
        self.historial_button.pack(pady=5, padx=5, fill="x")

        # Área principal
        self.main_area = ctk.CTkFrame(self, corner_radius=0)
        self.main_area.grid(row=0, column=1, sticky="nsew")

        # Inicialización de secciones
        self.clientes_section = ClientesSeccion(self.main_area)
        self.vuelos_section = VuelosSeccion(self.main_area)
        self.historial_section = HistorialSeccion(self.main_area)

        # Cargar notas de la base de datos
        self.cargarNotas()

        # Mostrar la sección inicial
        self.show_vuelos()

    def conectar_db(self):
        """Crea la base de datos y la tabla si no existen."""
        self.conn = sqlite3.connect("notas.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS notas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                texto TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def agregarNotas(self):
        """Agrega una nota a la base de datos y a la interfaz."""
        nota_texto = self.nota_textbox.get("1.0", "end").strip()
        
        if not nota_texto:
            return  # No hacer nada si la nota está vacía

        # Guardar en la base de datos
        self.cursor.execute("INSERT INTO notas (texto) VALUES (?)", (nota_texto,))
        self.conn.commit()

        # Mostrar en la interfaz
        self.mostrarNota(nota_texto)

        # Limpiar el cuadro de texto
        self.nota_textbox.delete("1.0", "end")

    def cargarNotas(self):
        """Carga las notas almacenadas en la base de datos y las muestra en la interfaz."""
        self.cursor.execute("SELECT id, texto FROM notas")
        for nota_id, texto in self.cursor.fetchall():
            self.mostrarNota(texto, nota_id)

    def mostrarNota(self, texto, nota_id=None):
        """Muestra una nota en la interfaz con la opción de eliminarla."""
        nota_item = ctk.CTkFrame(self.notas, fg_color="#222222")
        nota_item.pack(pady=5, padx=10, fill="x")

        # Crear el label con wrap para limitar el ancho
        nota_label = ctk.CTkLabel(nota_item, text=texto, wraplength=250, justify="left")
        nota_label.pack(side="left", padx=10, pady=5, fill="both", expand=True)

        # Checkbox para marcar la nota como completada y eliminarla
        def eliminar_nota():
            nota_item.destroy()
            if nota_id:
                self.cursor.execute("DELETE FROM notas WHERE id=?", (nota_id,))
                self.conn.commit()

        check_var = ctk.IntVar()
        check_button = ctk.CTkCheckBox(nota_item, text="", variable=check_var, command=eliminar_nota)
        check_button.pack(side="right", padx=10)

    def show_vuelos(self):
        self.clear_main_area()
        self.vuelos_section.render()

    def show_clientes(self):
        self.clear_main_area()
        self.clientes_section.render()
        self.clientes_section.mostrarClientes()

    def show_historial(self):
        self.clear_main_area()
        self.historial_section.render()

    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = ERPApp()
    app.mainloop()
