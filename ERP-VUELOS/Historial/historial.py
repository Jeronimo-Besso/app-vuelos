import customtkinter as ctk


class HistorialSeccion:
    def __init__(self, parent):
        self.parent = parent

    def render(self):
        # Agregar widgets para la sección de historial
        label = ctk.CTkLabel(self.parent, text="Sección de Historial", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=20)

        view_button = ctk.CTkButton(self.parent, text="Ver Historial", command=self.view_history)
        view_button.pack(pady=10)

    def view_history(self):
        print("Mostrando historial...")
