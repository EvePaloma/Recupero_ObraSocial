import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Buscar Paciente")
        self.geometry("400x300")

        # Datos de ejemplo con DNI
        self.personas = {
            1: {"nombre": "Carlos", "dni": "12345678"},
            2: {"nombre": "Ana", "dni": "23456789"},
            3: {"nombre": "Clara", "dni": "34567890"},
            4: {"nombre": "Roberto", "dni": "45678901"},
            5: {"nombre": "Mariana", "dni": "56789012"},
        }

        self.create_widgets()
        self.listbox = None  # Inicializar el Listbox

    def create_widgets(self):
        contenedor = tk.Frame(self, padx=10, pady=10)
        contenedor.pack(expand=True)

        # Entry para buscar por DNI
        self.entry_dni = tk.Entry(contenedor, width=30)
        self.entry_dni.pack(pady=5)
        self.entry_dni.bind('<KeyRelease>', self.actualizar_lista)

        # Entry para mostrar el nombre de la persona
        self.entry_nombre = tk.Entry(contenedor, width=30, state='readonly')
        self.entry_nombre.pack(pady=5)

    def actualizar_lista(self, evento):
        # Verificar si hay un Listbox existente y destruirlo
        if self.listbox:
            self.listbox.destroy()

        termino = self.entry_dni.get().lower()
        if termino:  # Si hay un término de búsqueda
            # Filtrar DNIs que contengan el término
            dnis_encontrados = [
                valor['dni'] for valor in self.personas.values() if termino in valor['dni']
            ]

            if dnis_encontrados:  # Si hay DNIs encontrados
                self.listbox = tk.Listbox(self, height=5)
                self.listbox.pack()  # Agregar el Listbox a la ventana
                for dni in dnis_encontrados:
                    self.listbox.insert(tk.END, dni)
                self.listbox.bind('<<ListboxSelect>>', self.seleccionar_dni)
                self.listbox.bind('<FocusOut>', lambda e: self.listbox.destroy())  # Cerrar si pierde foco

    def seleccionar_dni(self, evento):
        # Obtener el DNI seleccionado
        seleccionado = self.listbox.get(self.listbox.curselection())
        self.entry_dni.delete(0, tk.END)  # Limpiar el Entry
        self.entry_dni.insert(0, seleccionado)  # Establecer el DNI en el Entry
        self.mostrar_nombre(seleccionado)  # Mostrar el nombre correspondiente
        self.listbox.destroy()  # Cerrar el Listbox

    def mostrar_nombre(self, dni_seleccionado):
        # Mostrar el nombre correspondiente al DNI seleccionado
        for valor in self.personas.values():
            if valor['dni'] == dni_seleccionado:
                self.entry_nombre.config(state='normal')  # Habilitar el Entry
                self.entry_nombre.delete(0, tk.END)  # Limpiar el Entry
                self.entry_nombre.insert(0, valor['nombre'])  # Insertar el nombre
                self.entry_nombre.config(state='readonly')  # Volver a poner en solo lectura

# Inicializar la aplicación
if __name__ == "__main__":
    app = App()
    app.mainloop()
    
"""import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Buscar Paciente")
        self.geometry("400x300")

        # Datos de ejemplo con DNI
        self.personas = {
            1: {"nombre": "Carlos", "dni": "12345678"},
            2: {"nombre": "Ana", "dni": "23456789"},
            3: {"nombre": "Clara", "dni": "34567890"},
            4: {"nombre": "Roberto", "dni": "45678901"},
            5: {"nombre": "Mariana", "dni": "56789012"},
        }

        self.create_widgets()
        self.listbox = None  # Inicializar el Listbox

    def create_widgets(self):
        contenedor = tk.Frame(self, padx=10, pady=10)
        contenedor.pack(expand=True)

        # Entry para buscar por DNI
        self.entry_dni = tk.Entry(contenedor, width=30)
        self.entry_dni.pack(pady=5)
        self.entry_dni.bind('<KeyRelease>', self.actualizar_lista)

        # Entry para mostrar el nombre de la persona
        self.entry_nombre = tk.Entry(contenedor, width=30, state='readonly')
        self.entry_nombre.pack(pady=5)

        # Binding para cerrar el Listbox si se hace clic fuera de él
        self.bind("<Button-1>", self.cerrar_listbox)

    def actualizar_lista(self, evento):
        termino = self.entry_dni.get().lower()
        if self.listbox:
            self.listbox.destroy()  # Eliminar el Listbox anterior si existe

        if termino:  # Si hay un término de búsqueda
            dnis_encontrados = [valor['dni'] for valor in self.personas.values() if termino in valor['dni']]
            if dnis_encontrados:  # Si hay DNIs encontrados
                self.listbox = tk.Listbox(self, height=5)
                self.listbox.pack()  # Agregar el Listbox a la ventana
                for dni in dnis_encontrados:
                    self.listbox.insert(tk.END, dni)
                self.listbox.bind('<<ListboxSelect>>', self.seleccionar_dni)

    def seleccionar_dni(self, evento):
        seleccionado = self.listbox.get(self.listbox.curselection())
        self.entry_dni.delete(0, tk.END)  # Limpiar el Entry
        self.entry_dni.insert(0, seleccionado)  # Establecer el DNI en el Entry
        self.mostrar_nombre(seleccionado)  # Mostrar el nombre correspondiente
        self.listbox.destroy()  # Cerrar el Listbox

    def mostrar_nombre(self, dni_seleccionado):
        for valor in self.personas.values():
            if valor['dni'] == dni_seleccionado:
                self.entry_nombre.config(state='normal')  # Habilitar el Entry
                self.entry_nombre.delete(0, tk.END)  # Limpiar el Entry
                self.entry_nombre.insert(0, valor['nombre'])  # Insertar el nombre
                self.entry_nombre.config(state='readonly')  # Volver a poner en solo lectura

    def cerrar_listbox(self, evento):
        if self.listbox and not self.listbox.winfo_containing(event.x_root, event.y_root):
            self.listbox.destroy()  # Cerrar el Listbox si se hace clic fuera de él

# Inicializar la aplicación
if __name__ == "__main__":
    app = App()
    app.mainloop()"""