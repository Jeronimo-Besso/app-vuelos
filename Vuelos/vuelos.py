import customtkinter as ctk
import sqlite3
from datetime import datetime
from CTkMessagebox import CTkMessagebox

class TramosSeccion:
    def __init__(self, parent):
        self.parent = parent
        self.setup_database()
        self.id_cliente_seleccionado = None

    def setup_database(self):
        self.conn = sqlite3.connect('tramos.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tramos
                            (id INTEGER PRIMARY KEY, vuelo TEXT, fecha_salida TEXT, fecha_llegada TEXT,
                            hora_salida TEXT, hora_llegada TEXT, pasajero TEXT, precio REAL,
                            id_cliente INTEGER, estado TEXT DEFAULT 'Activo',
                            pagado INTEGER DEFAULT 0,
                            FOREIGN KEY(id_cliente) REFERENCES clientes(id))''')
        try:
            self.cursor.execute("ALTER TABLE tramos ADD COLUMN pagado INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            pass
        self.conn.commit()

    def render(self):
        frame_principal = ctk.CTkFrame(self.parent, fg_color="white", height=150)
        frame_principal.pack(fill="x")
        frame_principal.columnconfigure(0, weight=1)
        frame_principal.columnconfigure(1, weight=1)
        frame_principal.columnconfigure(2, weight=1)

        frame_titulo = ctk.CTkLabel(frame_principal, text="Vuelos", text_color="#8BC34A", font=("Arial", 30, "bold"))
        frame_titulo.grid(row=0, column=0, padx=(60,0), pady=30, sticky="w")
        
        boton_agregar_vuelo = ctk.CTkButton(frame_principal, text="+ Agregar Vuelo", 
                                            fg_color="#8BC34A", text_color="white",
                                            command=self.abrir_ventana_agregar)
        boton_agregar_vuelo.grid(row=0, column=2, padx=(0,60), pady=30, sticky="e")

        frame_secundario = ctk.CTkFrame(self.parent, fg_color="white", height=150)
        frame_secundario.pack(fill="x", padx=50)
        frame_secundario.columnconfigure(0, weight=1)
        frame_secundario.columnconfigure(1, weight=1)
        frame_secundario.columnconfigure(2, weight=1)

        self.frame_vuelos_activos = ctk.CTkFrame(frame_secundario, fg_color="#8BC34A", height=70, width=200)
        self.frame_vuelos_activos.grid(row=1, column=0, padx=20, pady=10)
        ctk.CTkLabel(self.frame_vuelos_activos, text="VUELOS ACTIVOS", font=("Arial", 14, "bold"), width=180).pack(pady=5)
        self.label_activos = ctk.CTkLabel(self.frame_vuelos_activos, text="0", font=("Arial", 12), width=180)
        self.label_activos.pack()

        self.frame_vuelos_totales = ctk.CTkFrame(frame_secundario, fg_color="#8BC34A", height=70, width=200)
        self.frame_vuelos_totales.grid(row=1, column=1, padx=20, pady=10)
        ctk.CTkLabel(self.frame_vuelos_totales, text="VUELOS TOTALES", font=("Arial", 14, "bold"), width=180).pack(pady=5)
        self.label_totales = ctk.CTkLabel(self.frame_vuelos_totales, text="0", font=("Arial", 12), width=180)
        self.label_totales.pack()

        frame_tabla = ctk.CTkFrame(self.parent, fg_color="#8BC34A")
        frame_tabla.pack(fill="x", padx=20, pady=20)
        self.encabezado = ["Vuelo", "Fecha Salida", "Fecha Llegada", "Hora Salida", "Hora Llegada", 
                          "Pasajero", "Precio", "Pagado", "     "]
        for col, encabezado_text in enumerate(self.encabezado):
            label = ctk.CTkLabel(frame_tabla, text=encabezado_text, font=("Arial", 12, "bold"), text_color="white")
            label.grid(row=0, column=col, padx=5, pady=5, sticky="ew")
            frame_tabla.columnconfigure(col, weight=1)

        self.tramos_frame = ctk.CTkScrollableFrame(self.parent, height=500)
        self.tramos_frame.pack(fill="both", expand=True, padx=20, pady=0)
        for col in range(len(self.encabezado)):
            self.tramos_frame.columnconfigure(col, weight=1)
        self.cargar_tramos()
        self.actualizar_estadisticas()

    def abrir_ventana_agregar(self):
        ventana = ctk.CTkToplevel(self.parent)
        ventana.title("Agregar Vuelo")
        ventana.geometry("700x400")
        ventana.transient(self.parent)
        ventana.grab_set()
        
        main_frame = ctk.CTkFrame(ventana)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=0)
        
        campos = ["Vuelo", "Fecha Salida", "Fecha Llegada", "Hora Salida", "Hora Llegada", 
                 "Pasajero", "Precio"]
        entradas = {}
        self.id_cliente_seleccionado = None
        
        for i, campo in enumerate(campos):
            row = i // 2
            col = (i % 2) * 2
            label = ctk.CTkLabel(main_frame, text=f"{campo}:")
            label.grid(row=row, column=col, padx=5, pady=5, sticky="e")
            if campo == "Pasajero":
                entrada = ctk.CTkEntry(main_frame, width=200, placeholder_text="Buscar por nombre, apellido o DNI")
                entrada.grid(row=row, column=col+1, padx=5, pady=5, sticky="w")
                buscar_btn = ctk.CTkButton(main_frame, text="Buscar", width=50, fg_color="#8BC34A",
                                          command=lambda e=entrada: self.buscar_pasajero(e))
                buscar_btn.grid(row=row, column=col+2, padx=5, pady=5, sticky="w")
            else:
                entrada = ctk.CTkEntry(main_frame, width=250)
                entrada.grid(row=row, column=col+1, padx=5, pady=5, sticky="w")
            entradas[campo.lower().replace(" ", "_")] = entrada
        
        pagado_var = ctk.BooleanVar(value=False)
        pagado_check = ctk.CTkCheckBox(main_frame, text="Pagado", variable=pagado_var)
        pagado_check.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        button_frame = ctk.CTkFrame(ventana)
        button_frame.pack(pady=10)
        
        ctk.CTkButton(button_frame, text="Guardar", fg_color="#8BC34A",
                     command=lambda: self.guardar_tramo(entradas, ventana, pagado_var)).pack(side="left", padx=5)
        
        ctk.CTkButton(button_frame, text="Cancelar", fg_color="#FF4444",
                     command=ventana.destroy).pack(side="left", padx=5)

        ventana.resizable(False, False)
        ventana.update()
        ventana.geometry(f"700x400+{int(ventana.winfo_screenwidth()/2-350)}+{int(ventana.winfo_screenheight()/2-200)}")

    def buscar_pasajero(self, entrada):
        texto = entrada.get().strip().lower()
        if not texto:
            CTkMessagebox(title="Error", message="Por favor, ingrese un nombre, apellido o DNI para buscar.", icon="warning")
            return
        
        try:
            conn_clientes = sqlite3.connect('clientes.db')
            cursor_clientes = conn_clientes.cursor()
            query = """SELECT id, nombre, apellido FROM clientes WHERE lower(nombre) LIKE ? 
                       OR lower(apellido) LIKE ? OR lower(documento) LIKE ?"""
            params = (f"%{texto}%", f"%{texto}%", f"%{texto}%")
            cursor_clientes.execute(query, params)
            cliente = cursor_clientes.fetchone()
            
            if cliente:
                entrada.delete(0, "end")
                entrada.insert(0, f"{cliente[1]} {cliente[2]}")
                self.id_cliente_seleccionado = cliente[0]
                CTkMessagebox(title="Éxito", message=f"Cliente encontrado: {cliente[1]} {cliente[2]}", icon="info")
            else:
                CTkMessagebox(title="Error", message="No se encontró un cliente con esos datos.", icon="warning")
                self.id_cliente_seleccionado = None
            
            conn_clientes.close()
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error al buscar cliente: {str(e)}", icon="cancel")

    def guardar_tramo(self, entradas, ventana, pagado_var):
        campos_requeridos = ['vuelo', 'fecha_salida', 'fecha_llegada', 'hora_salida', 
                            'hora_llegada', 'pasajero', 'precio']
        valores = {campo: entradas[campo].get().strip() for campo in campos_requeridos}
        
        if not all(valores[campo] for campo in campos_requeridos):
            CTkMessagebox(title="Error", message="Todos los campos son obligatorios.", icon="warning")
            return
        
        if not self.id_cliente_seleccionado:
            CTkMessagebox(title="Error", message="Por favor, busque y seleccione un pasajero válido.", icon="warning")
            return
        
        try:
            precio = float(valores['precio'])
            pagado = 1 if pagado_var.get() else 0
            self.cursor.execute('''INSERT INTO tramos (vuelo, fecha_salida, fecha_llegada, hora_salida, 
                                hora_llegada, pasajero, precio, id_cliente, estado, pagado)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Activo', ?)''', 
                               (valores['vuelo'], valores['fecha_salida'], valores['fecha_llegada'], 
                                valores['hora_salida'], valores['hora_llegada'], valores['pasajero'], 
                                precio, self.id_cliente_seleccionado, pagado))
            self.conn.commit()
            ventana.destroy()
            self.cargar_tramos()
            self.actualizar_estadisticas()
        except ValueError:
            CTkMessagebox(title="Error", message="El precio debe ser un número válido (ej. 1500.50).", icon="cancel")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"No se pudo guardar el vuelo: {str(e)}", icon="cancel")

    def cargar_tramos(self):
        for widget in self.tramos_frame.winfo_children():
            widget.destroy()

        self.cursor.execute("SELECT vuelo, fecha_salida, fecha_llegada, hora_salida, hora_llegada, pasajero, precio, pagado, id FROM tramos WHERE estado='Activo'")
        tramos = self.cursor.fetchall()
        
        for i, tramo in enumerate(tramos):
            for j, valor in enumerate(tramo[:-1]):
                if j == 7:  # Columna "Pagado"
                    pagado_var = ctk.BooleanVar(value=bool(valor))
                    checkbox = ctk.CTkCheckBox(self.tramos_frame, text="", variable=pagado_var,
                                              command=lambda t=tramo[-1], v=pagado_var: self.actualizar_pagado(t, v))
                    checkbox.grid(row=i+1, column=j, padx=5, pady=2)
                else:
                    label = ctk.CTkLabel(self.tramos_frame, text=str(valor) or "", font=("Arial", 10))
                    label.grid(row=i+1, column=j, padx=5, pady=2, sticky="ew")
            btn_finalizar = ctk.CTkButton(self.tramos_frame, text="Finalizar", width=50, font=("Arial", 10),
                                         command=lambda t=tramo[-1]: self.finalizar_tramo(t))
            btn_finalizar.grid(row=i+1, column=8, padx=5, pady=2, sticky="ew")

    def actualizar_pagado(self, tramo_id, pagado_var):
        pagado = 1 if pagado_var.get() else 0
        self.cursor.execute("UPDATE tramos SET pagado=? WHERE id=?", (pagado, tramo_id))
        self.conn.commit()

    def finalizar_tramo(self, tramo_id):
        self.cursor.execute("SELECT * FROM tramos WHERE id=?", (tramo_id,))
        tramo = self.cursor.fetchone()
        if tramo:
            conn_historial = sqlite3.connect('historial.db')
            cursor_historial = conn_historial.cursor()
            cursor_historial.execute('''CREATE TABLE IF NOT EXISTS historial_vuelos
                                        (id INTEGER PRIMARY KEY, vuelo TEXT, fecha_salida TEXT, fecha_llegada TEXT,
                                        hora_salida TEXT, hora_llegada TEXT, pasajero TEXT, precio REAL,
                                        id_cliente INTEGER, pagado INTEGER, fecha_finalizado TEXT)''')
            cursor_historial.execute('''INSERT INTO historial_vuelos (vuelo, fecha_salida, fecha_llegada, hora_salida, 
                                hora_llegada, pasajero, precio, id_cliente, pagado, fecha_finalizado)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                               (tramo[1], tramo[2], tramo[3], tramo[4], tramo[5], tramo[6], tramo[7], 
                                tramo[8], tramo[10], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn_historial.commit()
            conn_historial.close()
            
            self.cursor.execute("DELETE FROM tramos WHERE id=?", (tramo_id,))
            self.conn.commit()
            self.cargar_tramos()
            self.actualizar_estadisticas()

    def actualizar_estadisticas(self):
        self.cursor.execute("SELECT COUNT(*) FROM tramos WHERE estado='Activo'")
        activos = self.cursor.fetchone()[0]
        self.label_activos.configure(text=str(activos))

        conn_historial = sqlite3.connect('historial.db')
        cursor_historial = conn_historial.cursor()
        cursor_historial.execute("SELECT COUNT(*) FROM historial_vuelos")
        finalizados = cursor_historial.fetchone()[0]
        conn_historial.close()

        self.cursor.execute("SELECT COUNT(*) FROM tramos")
        activos_total = self.cursor.fetchone()[0]
        self.label_totales.configure(text=str(activos_total + finalizados))