import customtkinter as ctk
from customtkinter import *
from PIL import Image
from Clientes.clientes import ClientesSeccion
from Vuelos.vuelos import TramosSeccion
from Historial.historial import HistorialSeccion
from Finanzas.finanzas import FinanzaSeccion
from Dashboard.dashboard import DashboardSeccion
import tkinter as tk
import sqlite3

class ERPApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ERP System")
        self.geometry("1400x1080")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Configuración inicial de la base de datos
        self.conn = sqlite3.connect('notas.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS notas 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            texto TEXT NOT NULL)''')
        self.conn.commit()

        # Sidebar izquierda (sin cambios)
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color="lightblue", border_width=2, border_color="lightgrey")
        self.sidebar.pack(side="left", fill="y")
        img = ctk.CTkImage(light_image=Image.open("IMGS/no-mads aviation (2).png"), size=(160, 160))
        imagen_label = ctk.CTkLabel(self.sidebar, image=img, text="")
        imagen_label.pack(pady=(20,0), padx=20)
        
        self.boton_dashboard = ctk.CTkButton(self.sidebar, border_width=2, border_color="white", fg_color="lightblue", 
                                           text="Dashboard", font=("Arial",20,"bold"), text_color="white", 
                                           height=90, width=140, command=self.show_dashboard)
        self.boton_dashboard.pack(padx=30, pady=(70, 10))
        
        self.img_clientes = ctk.CTkImage(light_image=Image.open("IMGS/fotoClientes.png"), size=(110, 80))
        self.imagen_label = ctk.CTkButton(self.sidebar, fg_color="lightblue", border_width=2, border_color="white", 
                                        image=self.img_clientes, text="", command=self.show_clientes)
        self.imagen_label.pack(padx=30, pady=10)
        
        self.img_vuelos = ctk.CTkImage(light_image=Image.open("IMGS/seccion_vuelos.png"), size=(110,80))
        self.vuelos = ctk.CTkButton(self.sidebar, fg_color="lightblue", border_width=2, border_color="white", 
                                  image=self.img_vuelos, text="", command=self.show_vuelos)
        self.vuelos.pack(padx=30, pady=10)
        
        self.img_historial = ctk.CTkImage(light_image=Image.open("IMGS/icono_historial.png"), size=(110, 80))
        self.historial = ctk.CTkButton(self.sidebar, fg_color="lightblue", border_width=2, border_color="white", 
                                     image=self.img_historial, text="", command=self.show_historial)
        self.historial.pack(padx=30, pady=10)

        # Sidebar de notas (modificado)
        self.side_notas = ctk.CTkFrame(self, width=200, fg_color="#8BC34A", border_color="white", border_width=2)
        self.side_notas.pack(side="right", fill="y")
        self.notas_label = ctk.CTkLabel(self.side_notas, text="Notas", font=("Arial",30,"bold"), text_color="white", width=150)
        self.notas_label.pack(pady=(20, 20))
        self.linea_dec = ctk.CTkFrame(self.side_notas, height=2, fg_color="white")
        self.linea_dec.pack(fill="x", padx=20)
        ###
        # Frame para las notas con scroll
        self.notas_container = ctk.CTkScrollableFrame(self.side_notas, fg_color="#8BC34A")
        self.notas_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.boton_agregar_notas = ctk.CTkButton(self.side_notas, text="+", font=("Arial",30,"bold"), 
                                               fg_color="#8BC34A", border_width=2, corner_radius=100, 
                                               border_color="white", text_color="white", width=30, 
                                               height=30, command=self.crear_nota)
        self.boton_agregar_notas.pack(side="bottom", padx=(190,0), pady=2)

        # Área principal (sin cambios)
        self.area_principal = ctk.CTkFrame(self, fg_color="white")
        self.area_principal.pack(fill="both", expand=True)
        
        self.clientes_section = ClientesSeccion(self.area_principal)
        self.vuelos_section = TramosSeccion(self.area_principal)
        self.historial_section = HistorialSeccion(self.area_principal)
        self.finanzas_section = FinanzaSeccion(self.area_principal)
        self.dashboard_section = DashboardSeccion(self.area_principal)
        
        self.cargarNotas()

    def crear_nota(self):
        # Ventana emergente para nueva nota
        ventana_nota = ctk.CTkToplevel(self)
        ventana_nota.title("Nueva Nota")
        ventana_nota.geometry("300x200")
        ventana_nota.transient(self)  # Hace que la ventana sea modal
        ventana_nota.grab_set()      # Bloquea la ventana principal

        # Entrada de texto
        entrada = ctk.CTkEntry(ventana_nota, width=250, height=100, placeholder_text="Escribe tu nota aquí...")
        entrada.pack(pady=20)

        # Botón de enviar
        boton_enviar = ctk.CTkButton(ventana_nota, text="Enviar", command=lambda: self.guardar_nota(entrada.get(), ventana_nota))
        boton_enviar.pack(pady=10)

    def guardar_nota(self, texto, ventana):
        if texto.strip():  # Verifica que no esté vacío
            # Guardar en la base de datos
            self.cursor.execute("INSERT INTO notas (texto) VALUES (?)", (texto,))
            self.conn.commit()
            
            # Cerrar ventana y recargar notas
            ventana.destroy()
            self.cargarNotas()
    def cargarNotas(self):
        # Limpiar notas existentes
        for widget in self.notas_container.winfo_children():
            widget.destroy()

        # Cargar notas desde la base de datos
        self.cursor.execute("SELECT id, texto FROM notas")
        notas = self.cursor.fetchall()

        for nota_id, texto in notas:
            # Frame para cada nota
            nota_frame = ctk.CTkFrame(self.notas_container, fg_color="#8BC34A")
            nota_frame.pack(fill="x", pady=5, padx=5)

            # Checkbox para eliminar
            checkbox = ctk.CTkCheckBox(nota_frame, text="", width=20, 
                                     command=lambda id=nota_id: self.eliminar_nota(id))
            checkbox.pack(side="left", padx=5)

            # Texto de la nota
            label = ctk.CTkLabel(nota_frame, text=texto, text_color="white", wraplength=150)
            label.pack(side="left")

    def eliminar_nota(self, nota_id):
        # Eliminar de la base de datos
        self.cursor.execute("DELETE FROM notas WHERE id = ?", (nota_id,))
        self.conn.commit()
        
        # Recargar notas
        self.cargarNotas()

    # Métodos existentes (sin cambios)
    def show_vuelos(self):
        self.clear_main_area()
        self.vuelos_section.render()

    def show_dashboard(self):
        self.clear_main_area()
        self.dashboard_section.render()

    def show_historial(self):
        self.clear_main_area()
        self.historial_section.render()

    def show_clientes(self):
        self.clear_main_area()
        self.clientes_section.render()

    def show_finanzas(self):
        self.clear_main_area()
        self.finanzas_section.render()

    def clear_main_area(self):
        for widget in self.area_principal.winfo_children():
            widget.destroy()

    def __del__(self):
        # Cerrar conexión a la base de datos al cerrar la app
        self.conn.close()

if __name__ == "__main__":
    app = ERPApp()
    app.mainloop()

    ######################################################################################################################################################
    def crear_nota(self):
        pass
