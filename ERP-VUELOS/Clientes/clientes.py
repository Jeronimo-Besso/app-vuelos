import customtkinter as ctk


class ClientesSeccion:
    def __init__(self, parent):
        self.parent = parent

    def render(self):
        # Agregar widgets para la sección de clientes
        label = ctk.CTkLabel(self.parent, text="Sección de Clientes", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=20)
        #1
        search_label = ctk.CTkLabel(self.parent, text="Agregar Cliente:")
        search_label.pack(pady=5)
        ###########
        search_button = ctk.CTkButton(self.parent, text="Agregar", command=self.add_client)
        search_button.pack(pady=10)
        #2

    def add_client(self):
        nombre = ctk.CTkEntry(self.parent, placeholder_text="Ingrese el nombre y apellido del cliente: ")
        nombre.pack(pady=10)
        dni = ctk.CTkEntry(self.parent, placeholder_text="Ingrese el dni del cliente")
        dni.pack(pady=10)
        telefono = ctk.CTkEntry(self.parent, placeholder_text="Ingrese el telefono del cliente")
        telefono.pack(pady=10)    
        cumple = ctk.CTkEntry(self.parent, placeholder_text="Ingrese el cumpleaños del cliente(MES/DIA): ")
        cumple.pack(pady=10)    