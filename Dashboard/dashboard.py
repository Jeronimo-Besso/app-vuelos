import customtkinter as ctk
import sqlite3
from CTkMessagebox import CTkMessagebox

class DashboardSeccion:
    def __init__(self, parent):
        self.parent = parent
        self.conn = sqlite3.connect('tramos.db')
        self.cursor = self.conn.cursor()
        self.porcentaje_comision = 7.0
        self.frame_principal = None
        self.render()

    def render(self):
        if self.frame_principal is not None:
            self.frame_principal.destroy()

        self.frame_principal = ctk.CTkFrame(self.parent, fg_color="white")
        self.frame_principal.pack(fill="x", padx=20, pady=20)
        self.frame_principal.columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkLabel(self.frame_principal, text="Dashboard", text_color="#8BC34A", 
                     font=("Arial", 60, "bold")).grid(row=0, column=0, columnspan=4,padx=40, pady=20)

        self.crear_tarjeta(self.frame_principal, "       Vuelos Activos       ", self.calcular_vuelos_activos, 1, 1)
        self.crear_tarjeta(self.frame_principal, "        Ventas Brutas       ", self.calcular_ventas_brutas, 2, 1)
        self.crear_tarjeta(self.frame_principal, "       Comisión Total       ", self.calcular_comision, 1, 2)
        self.crear_tarjeta(self.frame_principal, "       Vuelos A Cobrar       ",self.calcular_vuelos_no_pagados, 2, 2)
        ###

        frame_comision = ctk.CTkFrame(self.frame_principal, fg_color="#8BC34A")
        frame_comision.grid(row=6, column=0, columnspan=3, pady=20, padx=20)
        ###
        ctk.CTkLabel(frame_comision, text="Porcentaje de Comisión (%):", text_color="white").pack(side="left", padx=10)
        self.entry_comision = ctk.CTkEntry(frame_comision, width=100)
        self.entry_comision.insert(0, str(self.porcentaje_comision))
        self.entry_comision.pack(side="left", padx=10)
        ctk.CTkButton(frame_comision, text="Actualizar", fg_color="#8BC34A", text_color="white",width=100,  
                      command=self.actualizar_comision).pack(side="left", padx=10)

    def crear_tarjeta(self, parent, titulo, calculo_func, fila, columna):
        frame = ctk.CTkFrame(parent, fg_color="#8BC34A", width=400, height=400)
        frame.grid(row=fila, column=columna, padx=30, pady=50)
        ctk.CTkLabel(frame, text=titulo.upper(), font=("Arial", 14, "bold"), text_color="white").pack(pady=5)
        valor = calculo_func()
        label_valor = ctk.CTkLabel(frame, text=str(valor), font=("Arial", 12), text_color="white")
        label_valor.pack()
        return label_valor

    def calcular_vuelos_activos(self):
        self.cursor.execute("SELECT COUNT(*) FROM tramos WHERE estado='Activo'")
        return self.cursor.fetchone()[0]

    def calcular_ventas_brutas(self):
        self.cursor.execute("SELECT SUM(precio) FROM tramos WHERE estado='Activo'")
        total = self.cursor.fetchone()[0]
        return f"${total:.2f}" if total else "$0.00"

    def calcular_comision(self):
        self.cursor.execute("SELECT SUM(precio) FROM tramos WHERE estado='Activo'")
        total = self.cursor.fetchone()[0] or 0
        comision = total * (self.porcentaje_comision / 100)
        return f"${comision:.2f}"
    
    def calcular_vuelos_no_pagados(self):
        self.cursor.execute("SELECT COUNT(*) FROM tramos WHERE estado='Activo' AND pagado=0")
        no_pagados = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM tramos WHERE estado='Activo'")
        total = self.cursor.fetchone()[0]
        return f"{no_pagados} / {total}"

    def actualizar_comision(self):
        try:
            nuevo_porcentaje = float(self.entry_comision.get())
            if 0 <= nuevo_porcentaje <= 100:
                self.porcentaje_comision = nuevo_porcentaje
                self.render()
            else:
                CTkMessagebox(title="Error", message="El porcentaje debe estar entre 0 y 100.", icon="warning")
        except ValueError:
            CTkMessagebox(title="Error", message="Por favor, ingrese un número válido.", icon="warning")

if __name__ == "__main__":
    root = ctk.CTk()
    dashboard = DashboardSeccion(root)
    root.mainloop()