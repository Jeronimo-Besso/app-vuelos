import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import requests
from datetime import datetime
import sqlite3
from CTkMessagebox import CTkMessagebox

class VuelosSeccion:
    def __init__(self, parent):
        self.parent = parent

    def avisoVuelo(self, numero_vuelo, fecha_vuelo):
        api_key = "bf04807e05ccba8776180a2b456e5011"  # Reemplaza con tu clave de API
        url = "http://api.aviationstack.com/v1/flights"
        
        params = {
            'access_key': api_key,  # La clave debe estar bien configurada
            'flight_iata': numero_vuelo,  # Número de vuelo
            'flight_date': fecha_vuelo  # Fecha del vuelo (en formato YYYY-MM-DD)
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            # Verificar si la respuesta contiene la estructura esperada
            if 'data' in data and len(data['data']) > 0:
                vuelo = data['data'][0]

                # Extraer la información deseada
                numero_vuelo = vuelo['flight']['iata']
                aerolinea = vuelo['airline']['name']
                origen = vuelo['departure']['airport']
                destino = vuelo['arrival']['airport']
                fecha_salida = vuelo['departure']['estimated']
                fecha_salida_dt = datetime.fromisoformat(fecha_salida)
                puerta = vuelo['departure']['gate']
                terminal = vuelo['departure']['terminal']
                
                # Formatear el mensaje
                mensaje = (f"Tu vuelo {numero_vuelo} con la aerolínea {aerolinea}, "
                        f"desde {origen} hacia {destino} sale el {fecha_salida_dt.strftime('%d/%m/%Y a las %H:%M')}.")
                
                if puerta:
                    mensaje += f" La puerta de embarque es {puerta}."
                if terminal:
                    mensaje += f" El vuelo sale desde la terminal {terminal}."
                
                return mensaje
            else:
                return "No se encontraron datos para el vuelo."
        else:
            return f"Error en la solicitud: {response.status_code}, {response.text}"

    def render(self):
        # Crear un Frame para organizar los widgets
        frame = ctk.CTkFrame(self.parent)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Agregar widgets para la sección de vuelos
        label = ctk.CTkLabel(frame, text="Sección de Vuelos", font=ctk.CTkFont(size=20, weight="bold"))
        label.grid(row=0, column=0, columnspan=3, pady=10, sticky="ew")

        # Asegurarte de que las columnas se expandan proporcionalmente
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)

        # Agregar botón de "Agregar Tramo"
        add_vuelo = ctk.CTkButton(frame, text="Agregar Tramo", command=self.agregarTramo)
        add_vuelo.grid(row=1, column=0, columnspan=1, pady=10)
        self.mostrarVuelos()

    def agregarTramo(self):
        # Crear una nueva ventana Toplevel
        top = tk.Toplevel(self.parent)
        top.title("Agregar Tramo")
        
        ancho = 450 
        alto = 600  
        x = self.parent.winfo_rootx() + 100
        y = self.parent.winfo_rooty() + 100 
        top.geometry(f"{ancho}x{alto}+{x}+{y}")
        
        # Campos de entrada para agregar el tramo
        pasajero_ida = ctk.CTkEntry(top, placeholder_text="Pasajero")
        pasajero_ida.pack(pady=10)

        # Crear el Listbox para las sugerencias de pasajeros
        self.suggestions_listbox = tk.Listbox(top, height=4)  # Tamaño reducido
        self.suggestions_listbox.pack(pady=5, fill="both", expand=False)
        
        # Bind para actualizar las sugerencias cuando se escriba en el Entry
        pasajero_ida.bind("<KeyRelease>", lambda event: self.update_suggestions(event, pasajero_ida))
        
        # Bind para seleccionar el cliente al hacer clic en una sugerencia
        self.suggestions_listbox.bind("<ButtonRelease-1>", lambda event: self.select_suggestion(event, pasajero_ida))
        
        fechaVueloIda = ctk.CTkEntry(top, placeholder_text="Fecha vuelo")
        fechaVueloIda.pack(pady=10)
        
        ruta_ida = ctk.CTkEntry(top, placeholder_text="Ruta")
        ruta_ida.pack(pady=10)
        
        horarios_ida = ctk.CTkEntry(top, placeholder_text="Horarios")
        horarios_ida.pack(pady=10)
        
        codigo_reserva = ctk.CTkEntry(top, placeholder_text="Codigo de reserva")
        codigo_reserva.pack(pady=10)
        
        numVuelo = ctk.CTkEntry(top, placeholder_text="Numero de vuelo")
        numVuelo.pack(pady=10)
        
        compania = ctk.CTkEntry(top, placeholder_text="Compañia")
        compania.pack(pady=10)

        # Botón para enviar el formulario
        enviar = ctk.CTkButton(top, text="Enviar", command=lambda: self.cargarTramo(top, pasajero_ida, fechaVueloIda, ruta_ida, horarios_ida, codigo_reserva, numVuelo, compania))  
        enviar.pack(pady=10)

    def update_suggestions(self, event, nombre):
        query = nombre.get()
        if query:
            self.show_suggestions(query)
        else:
            self.suggestions_listbox.delete(0, tk.END)

    def show_suggestions(self, query):
        conn = sqlite3.connect('clientes.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM clientes WHERE nombre LIKE ?", ('%' + query + '%',))  # Buscar nombres que coincidan
        results = cursor.fetchall()
        conn.close()
        self.suggestions_listbox.delete(0, tk.END)
        for result in results:
            self.suggestions_listbox.insert(tk.END, result[0])

    def select_suggestion(self, event, entry_widget):
        selected = self.suggestions_listbox.get(self.suggestions_listbox.curselection())  # Obtener selección
        entry_widget.delete(0, tk.END)  # Borrar el contenido actual
        entry_widget.insert(0, selected)  # Insertar la sugerencia seleccionada en el Entry
        self.suggestions_listbox.delete(0, tk.END)  # Limpiar las sugerencias

    def cargarTramo(self, top, pasajero_ida, fechaVueloIda, ruta_ida, horarios_ida, codigo_reserva, numVuelo, compania):
        # Recibir datos del formulario
        pasajero = pasajero_ida.get()
        fecha_vuelo = fechaVueloIda.get()
        ruta = ruta_ida.get()
        horarios = horarios_ida.get()
        codigo = codigo_reserva.get()
        num_vuelo = numVuelo.get()
        aerolinea = compania.get()
        # Conectar con la base de datos
        conn = sqlite3.connect('vuelos.db')
        cursor = conn.cursor()
        # Insertar los datos en la base de datos
        cursor.execute('''
            INSERT INTO tramos (pasajero, fecha_vuelo, ruta, horarios, codigo_reserva, numero_vuelo, compania)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (pasajero, fecha_vuelo, ruta, horarios, codigo, num_vuelo, aerolinea))
        conn.commit()  # Guardar cambios
        conn.close()   # Cerrar conexión
        self.show_success_dialog(f"Tramo {ruta} de {pasajero} agregado con éxito")
        top.destroy()  # Cerrar la ventana después de enviar

    def editarVuelo(self, event):
        selected_item = self.tree.focus()  
        if not selected_item:
            return  

        values = self.tree.item(selected_item, "values")
        if not values:
            return  

        vuelo_id = selected_item  # ID de la base de datos
        top = tk.Toplevel(self.parent)
        top.title("Editar Vuelo")

        ancho = 450
        alto = 600
        x = self.parent.winfo_rootx() + 100
        y = self.parent.winfo_rooty() + 100
        top.geometry(f"{ancho}x{alto}+{x}+{y}")
        

        campos = ["Pasajero", "Fecha", "Ruta", "Horarios", "Código Reserva", "Número Vuelo", "Compañía"]
        entries = {}

        for idx, campo in enumerate(campos):
            label = ctk.CTkLabel(top, text=campo,text_color="black")
            label.pack(pady=5)
            entry = ctk.CTkEntry(top)
            entry.insert(0, values[idx])  
            entry.pack(pady=5)
            entries[campo] = entry
        actualizar_btn = ctk.CTkButton(top, text="Guardar Cambios", command=lambda: self.guardarEdicion(vuelo_id, entries, top))
        actualizar_btn.pack(pady=10)
    
    def guardarEdicion(self, vuelo_id, entries, top):
        nuevo_valor = {campo: entry.get() for campo, entry in entries.items()}

        conn = sqlite3.connect('vuelos.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tramos SET pasajero=?, fecha_vuelo=?, ruta=?, horarios=?, codigo_reserva=?, numero_vuelo=?, compania=?
            WHERE id=?
        ''', (nuevo_valor["Pasajero"], nuevo_valor["Fecha"], nuevo_valor["Ruta"], nuevo_valor["Horarios"], 
            nuevo_valor["Código Reserva"], nuevo_valor["Número Vuelo"], nuevo_valor["Compañía"], vuelo_id))

        conn.commit()
        conn.close()
        top.destroy()
        self.mostrarVuelos()


    def mostrarVuelos(self):
        conn = sqlite3.connect('vuelos.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tramos ORDER BY fecha_vuelo ASC")  
        vuelos = cursor.fetchall()
        conn.close()

        # Limpiar widgets previos
        for widget in self.parent.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.destroy()

        frame = ctk.CTkFrame(self.parent, width=700, height=300)
        frame.place(x=50, y=200)  # Ajustá según necesites


        scrollbar_y = ttk.Scrollbar(frame, orient="vertical")
        self.tree = ttk.Treeview(frame, height=10, yscrollcommand=scrollbar_y.set, selectmode="browse")
        scrollbar_y.config(command=self.tree.yview)

        self.tree["columns"] = ("pasajero", "fecha", "ruta", "horarios", "codigo", "vuelo", "compania", "editar")
        self.tree.column("#0", width=0, minwidth=0, stretch=tk.NO)
        self.tree.column("pasajero", width=120, minwidth=120, stretch=tk.NO)
        self.tree.column("fecha", width=100, minwidth=100, stretch=tk.NO)
        self.tree.column("ruta", width=120, minwidth=120, stretch=tk.NO)
        self.tree.column("horarios", width=100, minwidth=100, stretch=tk.NO)
        self.tree.column("codigo", width=100, minwidth=100, stretch=tk.NO)
        self.tree.column("vuelo", width=100, minwidth=100, stretch=tk.NO)
        self.tree.column("compania", width=120, minwidth=120, stretch=tk.NO)
        self.tree.column("editar", width=80, minwidth=80, stretch=tk.NO)

        self.tree.heading("#0", text="")
        self.tree.heading("pasajero", text="Pasajero")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("ruta", text="Ruta")
        self.tree.heading("horarios", text="Horarios")
        self.tree.heading("codigo", text="Código Reserva")
        self.tree.heading("vuelo", text="N° Vuelo")
        self.tree.heading("compania", text="Compañía")
        self.tree.heading("editar", text="Editar")

        for vuelo in vuelos:
            self.tree.insert("", tk.END, iid=vuelo[0], values=(vuelo[1], vuelo[2], vuelo[3], vuelo[4], vuelo[5], vuelo[6], vuelo[7], "Presiona para editar"))

        self.tree.bind("<Double-1>", self.editarVuelo)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

    def show_success_dialog(self, message):
        dialog = tk.Toplevel(self.parent)
        dialog.title("Éxito")
        dialog.geometry("200x100")

        message_label = ctk.CTkLabel(dialog, text=message, font=ctk.CTkFont(size=12, weight="normal"),text_color="black")
        message_label.pack(pady=20)

        # Cerrar el diálogo después de 2 segundos
        dialog.after(1000, dialog.destroy)