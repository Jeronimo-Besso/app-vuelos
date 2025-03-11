import customtkinter as ctk
import sqlite3
from CTkMessagebox import CTkMessagebox

class HistorialSeccion:    
    def __init__(self, parent):
        self.parent = parent
        self.tree = None
        self.setup_database()

    def setup_database(self):
        self.conn = sqlite3.connect('historial.db')
        self.cursor = self.conn.cursor()
        # Creamos la tabla con el campo 'pagado' incluido
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS historial_vuelos
                            (id INTEGER PRIMARY KEY, vuelo TEXT, fecha_salida TEXT, fecha_llegada TEXT,
                            hora_salida TEXT, hora_llegada TEXT, pasajero TEXT, precio REAL,
                            id_cliente INTEGER, pagado INTEGER DEFAULT 0, fecha_finalizado TEXT)''')
        # Migración para bases de datos existentes
        try:
            self.cursor.execute("ALTER TABLE historial_vuelos ADD COLUMN pagado INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            pass  # El campo ya existe, no hacemos nada
        self.conn.commit()

    def render(self):
        frame_principal = ctk.CTkFrame(self.parent, fg_color="white", height=150)
        frame_principal.pack(fill="x")
        frame_principal.columnconfigure(0, weight=1)

        frame_titulo = ctk.CTkLabel(frame_principal, text="Historial de Vuelos", text_color="#8BC34A", font=("Arial", 30, "bold"))
        frame_titulo.grid(row=0, column=0, padx=(60,0), pady=30, sticky="w")

        frame_buscador = ctk.CTkFrame(self.parent, fg_color="white", height=70)
        frame_buscador.pack(fill="x", padx=0, pady=0)
        frame_buscador.columnconfigure(0, weight=1)
        frame_buscador.columnconfigure(1, weight=0)
        frame_buscador.columnconfigure(2, weight=1)
        
        self.buscador = ctk.CTkEntry(frame_buscador, placeholder_text="Ingrese nombre, apellido o DNI del cliente", 
                                    bg_color="white", text_color="green", width=400)
        self.buscador.grid(row=0, column=1, padx=10, pady=30, sticky="ew")
        boton_buscador = ctk.CTkButton(frame_buscador, text="Buscar", fg_color="#8BC34A", 
                                     text_color="white", width=100, command=self.buscar_historial)
        boton_buscador.grid(row=0, column=2, padx=10, pady=30, sticky="w")

        frame_tabla = ctk.CTkFrame(self.parent, fg_color="#8BC34A")
        frame_tabla.pack(fill="x", padx=20, pady=20)
        # Agregamos "Pagado" al encabezado
        self.encabezado = ["Vuelo", "Fecha Salida", "Fecha Llegada", "Hora Salida", "Hora Llegada", 
                          "Pasajero", "Precio", "Pagado", "Fecha Finalizado"]
        for col, encabezado_text in enumerate(self.encabezado):
            label = ctk.CTkLabel(frame_tabla, text=encabezado_text, font=("Arial", 12, "bold"), text_color="white")
            label.grid(row=0, column=col, padx=5, pady=5, sticky="ew")
            frame_tabla.columnconfigure(col, weight=1)

        self.historial_frame = ctk.CTkScrollableFrame(self.parent, height=500)
        self.historial_frame.pack(fill="both", expand=True, padx=20, pady=0)
        for col in range(len(self.encabezado)):
            self.historial_frame.columnconfigure(col, weight=1)

    def buscar_historial(self):
        texto = self.buscador.get().strip().lower()
        if not texto:
            CTkMessagebox(title="Error", message="Por favor, ingrese un nombre, apellido o DNI para buscar.", icon="warning")
            return
        
        conn_clientes = sqlite3.connect('clientes.db')
        cursor_clientes = conn_clientes.cursor()
        
        partes = texto.split(" ", 1)
        nombre = partes[0]
        apellido = partes[1] if len(partes) > 1 else ""

        query = """SELECT id, nombre, apellido FROM clientes WHERE lower(nombre) LIKE ? 
                   OR lower(apellido) LIKE ? OR lower(documento) LIKE ?"""
        params = (f"%{texto}%", f"%{texto}%", f"%{texto}%")
        
        if apellido:
            query = """SELECT id, nombre, apellido FROM clientes WHERE (lower(nombre) LIKE ? AND lower(apellido) LIKE ?) 
                       OR lower(documento) LIKE ?"""
            params = (f"%{nombre}%", f"%{apellido}%", f"%{texto}%")
        
        cursor_clientes.execute(query, params)
        cliente = cursor_clientes.fetchone()
        conn_clientes.close()
        
        if cliente:
            self.mostrar_historial(cliente[0], f"{cliente[1]} {cliente[2]}")
        else:
            CTkMessagebox(title="Error", message="No se encontró un cliente con esos datos.", icon="warning")

    def mostrar_historial(self, id_cliente, nombre_cliente):
        for widget in self.historial_frame.winfo_children():
            widget.destroy()

        # Incluimos 'pagado' en la consulta
        self.cursor.execute("SELECT vuelo, fecha_salida, fecha_llegada, hora_salida, hora_llegada, pasajero, precio, pagado, fecha_finalizado FROM historial_vuelos WHERE id_cliente=?", (id_cliente,))
        vuelos = self.cursor.fetchall()
        
        if not vuelos:
            label = ctk.CTkLabel(self.historial_frame, text=f"No hay vuelos finalizados para {nombre_cliente}", font=("Arial", 12))
            label.grid(row=1, column=0, columnspan=len(self.encabezado), padx=5, pady=5)
        else:
            for i, vuelo in enumerate(vuelos):
                for j, valor in enumerate(vuelo):
                    # Convertimos 'pagado' a "Sí" o "No" para mejor legibilidad
                    texto = "Sí" if j == 7 and valor == 1 else "No" if j == 7 and valor == 0 else str(valor) or ""
                    label = ctk.CTkLabel(self.historial_frame, text=texto, font=("Arial", 10))
                    label.grid(row=i+1, column=j, padx=5, pady=2, sticky="ew")