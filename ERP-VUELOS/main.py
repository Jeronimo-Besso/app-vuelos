import customtkinter as ctk
from Clientes.clientes import ClientesSeccion
from Vuelos.vuelos import VuelosSeccion
from Historial.historial import HistorialSeccion


class ERPApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ERP System")
        self.geometry("900x600")

        # Configuración del layout principal
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        # Barra lateral
        self.sidebar = ctk.CTkFrame(self, width=200,fg_color="#A9A9A9")
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.sidebar_label = ctk.CTkLabel(self.sidebar, text="Secciones", font=ctk.CTkFont(size=20, weight="bold"))
        self.sidebar_label.pack(pady=20)

        # Botones para cambiar entre secciones
        self.vuelos_button = ctk.CTkButton(self.sidebar, text="Vuelos", command=self.show_vuelos, fg_color="#1A1A1A",hover_color="#808080")
        self.vuelos_button.pack(pady=5,padx=5, fill="x")

        self.clientes_button = ctk.CTkButton(self.sidebar, text="Clientes", command=self.show_clientes, fg_color="#1A1A1A",hover_color="#808080")
        self.clientes_button.pack(pady=5,padx=5, fill="x")

        self.historial_button = ctk.CTkButton(self.sidebar, text="Historial", command=self.show_historial, fg_color="#1A1A1A",hover_color="#808080")
        self.historial_button.pack(pady=5,padx=5, fill="x")

        # Área principal
        self.main_area = ctk.CTkFrame(self, corner_radius=0)
        self.main_area.grid(row=0, column=1, sticky="nsew")

        # Inicialización de secciones
        self.clientes_section = ClientesSeccion(self.main_area)
        self.vuelos_section = VuelosSeccion(self.main_area)
        self.historial_section = HistorialSeccion(self.main_area)

        # Mostrar la sección inicial
        self.show_vuelos()

    def show_vuelos(self):
        self.clear_main_area()
        self.vuelos_section.render()

    def show_clientes(self):
        self.clear_main_area()
        self.clientes_section.render()

    def show_historial(self):
        self.clear_main_area()
        self.historial_section.render()

    def clear_main_area(self):
        # Eliminar todos los widgets del área principal
        for widget in self.main_area.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = ERPApp()
    app.mainloop()
