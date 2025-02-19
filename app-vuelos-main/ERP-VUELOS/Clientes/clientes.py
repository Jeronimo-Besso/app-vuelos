import customtkinter as ctk
import sqlite3
import tkinter as tk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox

class ClientesSeccion:    
    def __init__(self, parent):
        self.parent = parent
        self.tree = None

    def render(self):
        label = ctk.CTkLabel(self.parent, text="Sección de Clientes", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=20)        
        search_button = ctk.CTkButton(self.parent, text="Agregar cliente", command=self.create_client)
        search_button.pack(pady=10)
        self.mostrarClientes()

    def mostrarClientes(self):
        conn = sqlite3.connect('clientes.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes ORDER BY nombre ASC")  
        clientes = cursor.fetchall()
        conn.close()

        for widget in self.parent.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.destroy()

        frame = ctk.CTkFrame(self.parent, width=550, height=250)
        frame.pack(pady=10)
        scrollbar_y = ttk.Scrollbar(frame, orient="vertical")
        self.tree = ttk.Treeview(frame, height=10, yscrollcommand=scrollbar_y.set, selectmode="browse")
        scrollbar_y.config(command=self.tree.yview)
        self.tree["columns"] = ("one", "two", "three", "four", "editar")
        self.tree.column("#0", width=0, minwidth=0, stretch=tk.NO)
        self.tree.column("one", width=150, minwidth=150, stretch=tk.NO)
        self.tree.column("two", width=100, minwidth=100, stretch=tk.NO)
        self.tree.column("three", width=120, minwidth=120, stretch=tk.NO)
        self.tree.column("four", width=100, minwidth=100, stretch=tk.NO)
        self.tree.column("editar", width=80, minwidth=80, stretch=tk.NO)
        self.tree.heading("#0", text="")
        self.tree.heading("one", text="Nombre")
        self.tree.heading("two", text="DNI")
        self.tree.heading("three", text="Teléfono")
        self.tree.heading("four", text="Cumpleaños")
        self.tree.heading("editar", text="Editar")

        for cliente in clientes:
            self.tree.insert("", tk.END, iid=cliente[0], values=(cliente[1], cliente[2], cliente[3], cliente[4], "Presiona para editar"))
        self.tree.bind("<Double-1>", self.editarCliente)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

    def delete_client(self,top, cliente_id):
        conn = sqlite3.connect('clientes.db')
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
            conn.commit()
            self.mostrarClientes()
            self.tree.delete(cliente_id)
            self.show_success_dialog("Cliente eliminado con éxito")
            CTkMessagebox(title="Éxito", message="Cliente eliminado con éxito", icon="check")
        except sqlite3.Error as e:
            CTkMessagebox(title="Error", message=f"Error al eliminar cliente: {e}", icon="error")
        finally:
            conn.close()
            top.destroy()


    def editarCliente(self, event):
        item = self.tree.selection()
        if item:
            cliente_id = item[0]
            values = self.tree.item(item, "values")
            self.editar_cliente(cliente_id, values)

    def editar_cliente(self, cliente_id, values):
        top = tk.Toplevel(self.parent)
        top.title("Editar Cliente")

        ancho = 450
        alto = 600
        x = self.parent.winfo_rootx() + 100
        y = self.parent.winfo_rooty() + 100
        top.geometry(f"{ancho}x{alto}+{x}+{y}")

        nombre = ctk.CTkEntry(top, placeholder_text="Nombre", textvariable=tk.StringVar(value=values[0]))
        nombre.pack(pady=10)
        dni = ctk.CTkEntry(top, placeholder_text="DNI", textvariable=tk.StringVar(value=values[1]))
        dni.pack(pady=10)
        telefono = ctk.CTkEntry(top, placeholder_text="Teléfono", textvariable=tk.StringVar(value=values[2]))
        telefono.pack(pady=10)
        cumple = ctk.CTkEntry(top, placeholder_text="Cumpleaños", textvariable=tk.StringVar(value=values[3]))
        cumple.pack(pady=10)

        update_button = ctk.CTkButton(top, text="Guardar Cambios", 
                                      command=lambda: self.update_cliente(top, cliente_id, nombre.get(), dni.get(), telefono.get(), cumple.get()))
        update_button.pack(pady=10)
        delete_button = ctk.CTkButton(top, text="Eliminar cliente", command=lambda: self.delete_client(top,cliente_id))   
        delete_button.pack(pady=10)

    def update_cliente(self, top, cliente_id, nombre, dni, telefono, cumpleanos):
        conn = sqlite3.connect('clientes.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute("UPDATE clientes SET nombre=?, dni=?, telefono=?, cumpleanos=? WHERE id=?", 
                           (nombre, dni, telefono, cumpleanos, cliente_id))
            conn.commit()
            self.show_success_dialog("Cliente actualizado con éxito")
            self.mostrarClientes()
        except sqlite3.Error as e:
            CTkMessagebox(title="Error", message=f"Error al actualizar cliente: {e}", icon="error")
        finally:
            conn.close()
            top.destroy()

    def create_client(self):
        top = tk.Toplevel(self.parent)
        top.title("Agregar Cliente")

        ancho = 450
        alto = 600
        x = self.parent.winfo_rootx() + 100
        y = self.parent.winfo_rooty() + 100
        top.geometry(f"{ancho}x{alto}+{x}+{y}")

        nombre = ctk.CTkEntry(top, placeholder_text="Ingrese el nombre y apellido del cliente: ")
        nombre.pack(pady=10)
        dni = ctk.CTkEntry(top, placeholder_text="Ingrese el dni del cliente")
        dni.pack(pady=10)
        telefono = ctk.CTkEntry(top, placeholder_text="Ingrese el teléfono del cliente")
        telefono.pack(pady=10)
        cumple = ctk.CTkEntry(top, placeholder_text="Ingrese el cumpleaños del cliente (MES/DIA): ")
        cumple.pack(pady=10)

        add_button = ctk.CTkButton(top, text="Enviar", command=lambda: self.addClient(top, nombre.get(), dni.get(), telefono.get(), cumple.get()))
        add_button.pack(pady=10)

    def show_success_dialog(self, message):
        dialog = tk.Toplevel(self.parent)
        dialog.title("Éxito")
        dialog.geometry("200x100")

        message_label = ctk.CTkLabel(dialog, text=message, font=ctk.CTkFont(size=12, weight="normal"), text_color="black")
        message_label.pack(pady=20)

        dialog.after(1000, dialog.destroy)
