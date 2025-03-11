import customtkinter as ctk
import sqlite3
import tkinter as tk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from datetime import datetime, timedelta

class ClientesSeccion:    
    def __init__(self, parent):
        self.parent = parent
        self.tree = None
        self.setup_database()

    def setup_database(self):
        self.conn = sqlite3.connect('clientes.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS clientes
                            (id INTEGER PRIMARY KEY, nombre TEXT, apellido TEXT, documento TEXT,
                            telefono TEXT, email TEXT, domicilio TEXT, cumpleanos TEXT,
                            num_pasajero TEXT, notas TEXT, fecha_agregado TEXT)''')
        self.conn.commit()

    def render(self):
        frame_principal = ctk.CTkFrame(self.parent, fg_color="white", height=150)
        frame_principal.pack(fill="x")
        frame_principal.columnconfigure(0, weight=1)
        frame_principal.columnconfigure(1, weight=1)
        frame_principal.columnconfigure(2, weight=1)

        frame_titulo = ctk.CTkLabel(frame_principal, text="Clientes", text_color="#8BC34A", font=("Arial", 30, "bold"))
        frame_titulo.grid(row=0, column=0, padx=(60,0), pady=30, sticky="w")
        
        boton_agregar_cliente = ctk.CTkButton(frame_principal, text="+ Agregar Cliente", 
                                            fg_color="#8BC34A", text_color="white",
                                            command=self.abrir_ventana_agregar)
        boton_agregar_cliente.grid(row=0, column=2, padx=(0,60), pady=30, sticky="e")

        frame_secundario = ctk.CTkFrame(self.parent, fg_color="white", height=150)
        frame_secundario.pack(fill="x", padx=50)
        frame_secundario.columnconfigure(0, weight=1)
        frame_secundario.columnconfigure(1, weight=1)
        frame_secundario.columnconfigure(2, weight=1)

        self.frame_cant_cliente = ctk.CTkFrame(frame_secundario, fg_color="#8BC34A", height=70, width=200)
        self.frame_cant_cliente.grid(row=1, column=0, padx=20, pady=10)
        ctk.CTkLabel(self.frame_cant_cliente, text="CLIENTE RECIENTE", font=("Arial", 14, "bold"), width=180).pack(pady=5)
        self.label_reciente = ctk.CTkLabel(self.frame_cant_cliente, text="Sin clientes", font=("Arial", 12), width=180)
        self.label_reciente.pack()

        self.frame_cliente_activo = ctk.CTkFrame(frame_secundario, fg_color="#8BC34A", height=70, width=200)
        self.frame_cliente_activo.grid(row=1, column=1, padx=20, pady=10)
        ctk.CTkLabel(self.frame_cliente_activo, text="CLIENTES", font=("Arial", 14, "bold"), width=180).pack(pady=5)
        self.label_total = ctk.CTkLabel(self.frame_cliente_activo, text="0", font=("Arial", 12), width=180)
        self.label_total.pack()

        self.frame_cliente_nuevo = ctk.CTkFrame(frame_secundario, fg_color="#8BC34A", height=70, width=200)
        self.frame_cliente_nuevo.grid(row=1, column=2, padx=20, pady=10)
        ctk.CTkLabel(self.frame_cliente_nuevo, text="ÚLTIMO MES", font=("Arial", 14, "bold"), width=180).pack(pady=5)
        self.label_mes = ctk.CTkLabel(self.frame_cliente_nuevo, text="0", font=("Arial", 12), width=180)
        self.label_mes.pack()

        frame_buscador = ctk.CTkFrame(self.parent, fg_color="white", height=70)
        frame_buscador.pack(fill="x", padx=0, pady=0)
        frame_buscador.columnconfigure(0, weight=1)
        frame_buscador.columnconfigure(1, weight=0)
        frame_buscador.columnconfigure(2, weight=1)
        
        self.buscador = ctk.CTkEntry(frame_buscador, placeholder_text="Ingrese nombre, apellido, DNI o teléfono", 
                                    bg_color="white", text_color="green", width=400)
        self.buscador.grid(row=0, column=1, padx=10, pady=30, sticky="ew")
        boton_buscador = ctk.CTkButton(frame_buscador, text="Buscar", fg_color="#8BC34A", 
                                     text_color="white", width=100, command=self.buscar_cliente)
        boton_buscador.grid(row=0, column=2, padx=10, pady=30, sticky="w")

        # Eliminamos resultados_frame ya que no se usará para la lista en tiempo real
        frame_tabla = ctk.CTkFrame(self.parent, fg_color="#8BC34A")
        frame_tabla.pack(fill="x", padx=20, pady=20)
        self.encabezado = ["Nombre", "Apellido", "Documento", "Teléfono", "Email", "Domicilio", 
                         "Cumpleaños", "Num.pasajero", "Notas", "     "]
        for col, encabezado_text in enumerate(self.encabezado):
            label = ctk.CTkLabel(frame_tabla, text=encabezado_text, font=("Arial", 12, "bold"), text_color="white")
            label.grid(row=0, column=col, padx=5, pady=5, sticky="ew")
            frame_tabla.columnconfigure(col, weight=1)

        self.clientes_frame = ctk.CTkScrollableFrame(self.parent, height=500)
        self.clientes_frame.pack(fill="both", expand=True, padx=20, pady=0)
        for col in range(len(self.encabezado)):
            self.clientes_frame.columnconfigure(col, weight=1)
        self.cargar_clientes()
        self.actualizar_estadisticas()

    def abrir_ventana_agregar(self):
        ventana = ctk.CTkToplevel(self.parent)
        ventana.title("Agregar Cliente")
        ventana.geometry("700x400")
        
        ventana.transient(self.parent)
        ventana.grab_set()
        
        main_frame = ctk.CTkFrame(ventana)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        campos = ["Nombre", "Apellido", "Documento", "Teléfono", "Email", 
                 "Domicilio", "Cumpleaños", "Num.pasajero", "Notas"]
        entradas = {}
        
        for i, campo in enumerate(campos):
            row = i // 2
            col = (i % 2) * 2
            label = ctk.CTkLabel(main_frame, text=f"{campo}:")
            label.grid(row=row, column=col, padx=5, pady=5, sticky="e")
            entrada = ctk.CTkEntry(main_frame, width=250)
            entrada.insert(0, "")
            entrada.grid(row=row, column=col+1, padx=5, pady=5, sticky="w")
            entradas[campo.lower()] = entrada
        
        button_frame = ctk.CTkFrame(ventana)
        button_frame.pack(pady=10)
        
        guardar_btn = ctk.CTkButton(button_frame, text="Guardar", fg_color="#8BC34A",
                                  command=lambda: self.guardar_cliente(entradas, ventana))
        guardar_btn.pack(side="left", padx=5)
        
        ctk.CTkButton(button_frame, text="Cancelar", fg_color="#FF4444",
                     command=ventana.destroy).pack(side="left", padx=5)

        ventana.resizable(False, False)
        ventana.update()
        ventana.geometry(f"700x400+{int(ventana.winfo_screenwidth()/2-350)}+{int(ventana.winfo_screenheight()/2-200)}")

    def guardar_cliente(self, entradas, ventana):
        campos_requeridos = ['nombre', 'apellido', 'documento', 'teléfono', 
                            'email', 'domicilio', 'cumpleaños', 'num.pasajero', 'notas']
        valores = {campo: entradas[campo].get() or "" for campo in campos_requeridos}
        valores['fecha_agregado'] = datetime.now().strftime("%Y-%m-%d")
        
        try:
            self.cursor.execute('''INSERT INTO clientes (nombre, apellido, documento, telefono, 
                                email, domicilio, cumpleanos, num_pasajero, notas, fecha_agregado)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                               (valores['nombre'], valores['apellido'], valores['documento'], 
                                valores['teléfono'], valores['email'], valores['domicilio'], 
                                valores['cumpleaños'], valores['num.pasajero'], valores['notas'], 
                                valores['fecha_agregado']))
            self.conn.commit()
            ventana.destroy()
            self.cargar_clientes()
            self.actualizar_estadisticas()
        except Exception as e:
            CTkMessagebox(title="Error", message=f"No se pudo guardar el cliente: {str(e)}", icon="cancel")

    def actualizar_estadisticas(self):
        self.cursor.execute("SELECT nombre, apellido FROM clientes ORDER BY id DESC LIMIT 1")
        ultimo = self.cursor.fetchone()
        if ultimo:
            self.label_reciente.configure(text=f"{ultimo[0]} {ultimo[1]}")
        else:
            self.label_reciente.configure(text="Sin clientes")

        self.cursor.execute("SELECT COUNT(*) FROM clientes")
        total = self.cursor.fetchone()[0]
        self.label_total.configure(text=str(total))

        mes_antes = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        self.cursor.execute("SELECT COUNT(*) FROM clientes WHERE fecha_agregado >= ?", (mes_antes,))
        ult_mes = self.cursor.fetchone()[0]
        self.label_mes.configure(text=str(ult_mes))

    def cargar_clientes(self):
        for widget in self.clientes_frame.winfo_children():
            widget.destroy()

        self.cursor.execute("SELECT * FROM clientes")
        clientes = self.cursor.fetchall()
        
        for i, cliente in enumerate(clientes):
            for j, valor in enumerate(cliente[1:-1]):
                label = ctk.CTkLabel(self.clientes_frame, text=valor or "", font=("Arial", 10))
                label.grid(row=i+1, column=j, padx=5, pady=2, sticky="ew")
            btn_editar = ctk.CTkButton(self.clientes_frame, text="Editar", width=50, font=("Arial", 10),
                                     command=lambda c=cliente: self.editar_cliente(c))
            btn_editar.grid(row=i+1, column=9, padx=5, pady=2, sticky="ew")

    def editar_cliente(self, cliente):
        ventana = ctk.CTkToplevel(self.parent)
        ventana.title("Editar Cliente")
        ventana.geometry("700x400")
        ventana.transient(self.parent)
        ventana.grab_set()
        
        main_frame = ctk.CTkFrame(ventana)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        campos = ["Nombre", "Apellido", "Documento", "Teléfono", "Email", "Domicilio", 
                 "Cumpleaños", "Num.pasajero", "Notas"]
        entradas = {}
        
        for i, campo in enumerate(campos):
            row = i // 2
            col = (i % 2) * 2
            label = ctk.CTkLabel(main_frame, text=f"{campo}:")
            label.grid(row=row, column=col, padx=5, pady=5, sticky="e")
            entrada = ctk.CTkEntry(main_frame, width=250)
            entrada.insert(0, cliente[i+1] or "")
            entrada.grid(row=row, column=col+1, padx=5, pady=5, sticky="w")
            entradas[campo.lower()] = entrada

        button_frame = ctk.CTkFrame(ventana)
        button_frame.pack(pady=10)
        
        ctk.CTkButton(button_frame, text="Guardar", fg_color="#8BC34A",
                     command=lambda: self.actualizar_cliente(cliente[0], entradas, ventana)).pack(side="left", padx=5)
        
        ctk.CTkButton(button_frame, text="Eliminar", fg_color="#FF4444",
                     command=lambda: self.eliminar_cliente(cliente[0], ventana)).pack(side="left", padx=5)
        
        ctk.CTkButton(button_frame, text="Cancelar", fg_color="#AAAAAA",
                     command=ventana.destroy).pack(side="left", padx=5)

        ventana.resizable(False, False)
        ventana.update()
        ventana.geometry(f"700x400+{int(ventana.winfo_screenwidth()/2-350)}+{int(ventana.winfo_screenheight()/2-200)}")

    def actualizar_cliente(self, cliente_id, entradas, ventana):
        campos_requeridos = ['nombre', 'apellido', 'documento', 'teléfono', 
                            'email', 'domicilio', 'cumpleaños', 'num.pasajero', 'notas']
        valores = [entradas[campo].get() or "" for campo in campos_requeridos]
        
        try:
            self.cursor.execute('''UPDATE clientes SET nombre=?, apellido=?, documento=?, telefono=?, 
                                email=?, domicilio=?, cumpleanos=?, num_pasajero=?, notas=? 
                                WHERE id=?''', valores + [cliente_id])
            self.conn.commit()
            ventana.destroy()
            self.cargar_clientes()
            self.actualizar_estadisticas()
        except Exception as e:
            CTkMessagebox(title="Error", message=f"No se pudo actualizar el cliente: {str(e)}", icon="cancel")

    def eliminar_cliente(self, cliente_id, ventana):
        respuesta = CTkMessagebox(title="Confirmar", message="¿Estás seguro de eliminar este cliente?",
                                icon="warning", option_1="Sí", option_2="No")
        if respuesta.get() == "Sí":
            self.cursor.execute("DELETE FROM clientes WHERE id=?", (cliente_id,))
            self.conn.commit()
            ventana.destroy()
            self.cargar_clientes()
            self.actualizar_estadisticas()

    def buscar_cliente(self):
        texto = self.buscador.get().strip().lower()
        if not texto:
            CTkMessagebox(title="Error", message="Por favor, ingrese un nombre, apellido, DNI o teléfono para buscar.", icon="warning")
            return
        
        # Separar nombre y apellido si hay un espacio
        partes = texto.split(" ", 1)
        nombre = partes[0]
        apellido = partes[1] if len(partes) > 1 else ""

        # Buscar por nombre, apellido, documento o teléfono
        query = """SELECT * FROM clientes WHERE lower(nombre) LIKE ? OR lower(apellido) LIKE ? 
                   OR lower(documento) LIKE ? OR lower(telefono) LIKE ?"""
        params = (f"%{texto}%", f"%{texto}%", f"%{texto}%", f"%{texto}%")
        
        if apellido:
            # Si hay apellido, priorizamos coincidencia por nombre y apellido
            query = """SELECT * FROM clientes WHERE (lower(nombre) LIKE ? AND lower(apellido) LIKE ?) 
                       OR lower(documento) LIKE ? OR lower(telefono) LIKE ?"""
            params = (f"%{nombre}%", f"%{apellido}%", f"%{texto}%", f"%{texto}%")
        
        self.cursor.execute(query, params)
        cliente = self.cursor.fetchone()
        
        if cliente:
            self.mostrar_cliente(cliente)
        else:
            CTkMessagebox(title="Error", message="No se encontró un cliente con esos datos.", icon="warning")

    def mostrar_cliente(self, cliente):
        ventana = ctk.CTkToplevel(self.parent)
        ventana.title(f"Cliente: {cliente[1]} {cliente[2]}")
        ventana.geometry("700x400")
        ventana.transient(self.parent)
        ventana.grab_set()
        
        main_frame = ctk.CTkFrame(ventana)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        campos = ["Nombre", "Apellido", "Documento", "Teléfono", "Email", "Domicilio", 
                 "Cumpleaños", "Num.pasajero", "Notas"]
        
        for i, campo in enumerate(campos):
            row = i // 2
            col = (i % 2) * 2
            ctk.CTkLabel(main_frame, text=f"{campo}:").grid(row=row, column=col, padx=5, pady=5, sticky="e")
            valor = ctk.CTkLabel(main_frame, text=cliente[i+1] or "", font=("Arial", 12))
            valor.grid(row=row, column=col+1, padx=5, pady=5, sticky="w")

        button_frame = ctk.CTkFrame(ventana)
        button_frame.pack(pady=10)
        ctk.CTkButton(button_frame, text="Cerrar", fg_color="#AAAAAA",
                     command=ventana.destroy).pack(side="left", padx=5)

        ventana.resizable(False, False)
        ventana.update()
        ventana.geometry(f"700x400+{int(ventana.winfo_screenwidth()/2-350)}+{int(ventana.winfo_screenheight()/2-200)}")

