from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from conexionbd import *

class Gestionmedico(Frame):

    def __init__(self, master):
        Frame.__init__(self, master, bg="#e4c09f")
        self.master = master
        self.grid()
        self.createWidgets()

    def solo_letras(self, char):
        return char.isalpha() or char == " "

    def solo_numeros(self, char):
        return char.isdigit()

    def createWidgets(self):
        frame_Medicos = LabelFrame(
            self,
            text="Gestión de Medicos",
            font=("Robot", 10),
            padx=10,
            pady=10,
            bg="#c9c2b2",
        )
        frame_Medicos.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Carga la imagen de fondo
        img_fondo = Image.open("fondo3.png")
        img_fondo = img_fondo.resize((900, 200), Image.Resampling.LANCZOS)
        self.img_fondo = ImageTk.PhotoImage(img_fondo)

        # Label para la imagen de fondo
        fondo_label = Label(frame_Medicos, image=self.img_fondo)
        fondo_label.grid(row=0, column=0, columnspan=7)

        # Frame más chico para label y entry de búsqueda
        frame_busqueda = Frame(frame_Medicos, bg="#e6c885")
        frame_busqueda.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="w")

        # Widgets de búsqueda dentro del frame más chico
        etiqueta_buscar = Label(
            frame_busqueda, text="Buscar:", bg="#e6c885", font=("Robot", 13)
        )
        etiqueta_buscar.grid(row=1, column=1, padx=5, pady=5)

        self.entrada_buscar = Entry(frame_busqueda, width="50", font=("Robot", 11))
        self.entrada_buscar.grid(row=1, column=2, padx=5, pady=5)

        img_buscar = Image.open("buscar1.png").resize(
            (30, 30), Image.Resampling.LANCZOS
        )
        img_buscar = ImageTk.PhotoImage(img_buscar)
        btn_buscar = Button(
            frame_busqueda,
            image=img_buscar,
            width=30,
            height=30,
            bg="#e6c885",
            command=self.buscar_medico,
        )
        btn_buscar.grid(row=1, column=3)
        btn_buscar.image = img_buscar

        boton_agregar = Button(
            frame_Medicos,
            text="Agregar   +",
            width=15,
            bg="#e6c885",
            font=("Robot", 13),
            command=self.agregar_medico,
        )
        boton_agregar.grid(row=1, column=5, padx=10, pady=10)

        # Para que siempre esté atrás de los widgets
        fondo_label.lower()

        # Frame para el Treeview y el scrollbar
        frame_tabla = Frame(
            frame_Medicos, bg="#c9c2b2"
        )  # Frame para contener la tabla y el scrollbar
        frame_tabla.grid(row=2, column=0, columnspan=6, padx=10, pady=10)

        stilo = ttk.Style()
        stilo.configure(
            "Treeview", font=("Robot", 11), rowheight=25
        )  # Cambia la fuente y el alto de las filas
        stilo.configure(
            "Treeview.Heading", font=("Robot", 14)
        )  # Cambia la fuente de las cabeceras

        # Treeview para mostrar la tabla de Medicos dentro del frame_tabla
        self.tree = ttk.Treeview(
            frame_tabla,
            columns=("nombre", "Apellido", "DNI"),
            show="headings",
            height=5,
        )

        # Títulos de columnas
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("DNI", text="DNI")

        # Ancho de las columnas y datos centrados
        self.tree.column("nombre", anchor="center", width=250)
        self.tree.column("Apellido", anchor="center", width=350)
        self.tree.column("DNI", anchor="center", width=250)

        # Ejemplo
    

        # Grid del frame_tabla
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar para la tabla dentro del frame_tabla
        scrollbar = ttk.Scrollbar(
            frame_tabla, orient="vertical", command=self.tree.yview
        )
        scrollbar.grid(
            row=0, column=1, sticky="ns"
        )  # Se expande desde arriba hacia abajo
        self.tree.configure(yscrollcommand=scrollbar.set)

        frame_btn = Frame(frame_Medicos, bg="#c9c2b2")
        frame_btn.grid(row=4, columnspan=6)

        # Botones(ver, modificar, eliminar)
        btn_ver = Button(
            frame_btn,
            text="Ver",
            width=15,
            font=("Robot", 13),
            bg="#e6c885",
            command=self.ver_medico,
        )
        btn_ver.grid(row=4, column=1, padx=50)

        btn_editar = Button(
            frame_btn,
            text="Modificar",
            width=15,
            font=("Robot", 13),
            bg="#e6c885",
            command=self.modificar_medico,
        )
        btn_editar.grid(row=4, column=2, padx=50)

        btn_eliminar = Button(
            frame_btn,
            text="Eliminar",
            width=15,
            font=("Robot", 13),
            bg="#e6c885",
            command=self.eliminar_medico,
        )
        btn_eliminar.grid(row=4, column=3, padx=50)

    def agregar_medico(self):
        ventana_agregar = Toplevel(self)
        ventana_agregar.title("Agregar medico")
        ventana_agregar.config(bg="#e4c09f")
        ventana_agregar.resizable(False, False)

        frame_agregar = LabelFrame(
            ventana_agregar,
            text="Agregar Nuevo medico",
            font=("Robot", 12),
            padx=10,
            pady=10,
            bg="#c9c2b2",
        )
        frame_agregar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        campos = ["Nombre", "Apellido", "DNI", "Telefono", "Matricula", "Especialidad"]
        entradas = {}

        vcmd_letras = ventana_agregar.register(self.solo_letras)
        vcmd_numeros = ventana_agregar.register(self.solo_numeros)

        for i, campo in enumerate(campos):  # Devuelve índice y valor de cada elemento
            etiquetas = Label(
                frame_agregar, text=campo + ":", bg="#c9c2b2", font=("Robot", 10)
            )
            etiquetas.grid(row=i, column=0, padx=10, pady=5)
            entry = Entry(frame_agregar, width=40, font=("Robot", 10))
            if campo in ["Nombre", "Apellido"]:
                entry.config(validate="key", validatecommand=(vcmd_letras, '%S'))
            elif campo in ["DNI", "Telefono"]:
                entry.config(validate="key", validatecommand=(vcmd_numeros, '%S'))
            entry.grid(row=i, column=1, padx=10, pady=5)
            entradas[campo] = entry

        btn_nuevo_medico = Button(
            frame_agregar,
            text="Agregar",
            font=("Robot", 10),
            bg="#e6c885",
            command=lambda: self.guardar_nuevo_medico(entradas, ventana_agregar),
        )
        btn_nuevo_medico.grid(row=len(campos), column=0, columnspan=2, padx=10, pady=10)

    def ver_medico(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione un medico.")
            return

        medico_seleccionado = self.tree.item(
            seleccion[0], "values"
        )  # Item= valor del elemento
        self.abrir_ventana_medico(medico_seleccionado, seleccion[0], modo="ver")

    def modificar_medico(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione un medico.")
            return

        medico_seleccionado = self.tree.item(seleccion[0], "values")
        self.abrir_ventana_medico(medico_seleccionado, seleccion[0], modo="modificar")

    def abrir_ventana_medico(self, medico, id_seleccionado, modo="ver"):
        ventana = Toplevel(self)
        ventana.title("Detalles del medico")
        ventana.config(bg="#e4c09f")
        ventana.resizable(False, False)

        ventana.grid_columnconfigure(0, weight=1)
        ventana.grid_rowconfigure(0, weight=1)

        frame_detalles = LabelFrame(
            ventana,
            text="Detalles del medico",
            font=("Robot", 10),
            padx=10,
            pady=10,
            bg="#c9c2b2",
        )
        frame_detalles.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        campos = ["Nombre", "Apellido", "DNI", "Telefono", "Matricula", "Especialidad"]
        entradas = {}

        vcmd_letras = ventana.register(self.solo_letras)
        vcmd_numeros = ventana.register(self.solo_numeros)

        for i, campo in enumerate(campos):
            etiqueta = Label(
                frame_detalles, text=campo + ":", bg="#c9c2b2", font=("Robot", 10)
            )
            etiqueta.grid(row=i, column=0, padx=10, pady=5)
            entry = Entry(frame_detalles, width=40)
            if campo in ["Nombre", "Apellido"]:
                entry.config(validate="key", validatecommand=(vcmd_letras, '%S'))
            elif campo in ["DNI", "Telefono"]:
                entry.config(validate="key", validatecommand=(vcmd_numeros, '%S'))
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry.insert(0, medico[i])
            entradas[campo] = entry

        if modo == "ver":
            for entry in entradas.values():
                entry.config(state="readonly")
            btn_editar = Button(
                ventana,
                text="Modificar",
                width=15,
                font=("Robot", 13),
                bg="#e6c885",
                command=lambda: self.activar_edicion(entradas, btn_guardar),
            )
            btn_editar.grid(row=len(campos), column=0, pady=10)

            btn_guardar = Button(
                frame_detalles,
                text="Guardar Cambios",
                command=lambda: self.guardar_cambios(
                    entradas, ventana, id_seleccionado
                ),
            )
            btn_guardar.grid(
                row=len(campos), column=0, columnspan=2, padx=10, pady=10
            )
            btn_guardar.config(state="disabled")

        if modo == "modificar":
            btn_modificar = Button(
                frame_detalles,
                text="Guardar Cambios",
                command=lambda: self.guardar_cambios(
                    entradas, ventana, id_seleccionado
                ),
            )
            btn_modificar.grid(
                row=len(campos), column=0, columnspan=2, padx=10, pady=10
            )

    def activar_edicion(self, entradas, btn_guardar):
        for entry in entradas.values():
            entry.config(state="normal")
        btn_guardar.config(state="normal")

    def guardar_cambios(self, entradas, ventana, seleccion):
        nombre = entradas["Nombre"].get()
        apellido = entradas["Apellido"].get()
        dni = entradas["DNI"].get()
        telefono = entradas["Telefono"].get()
        matricula = entradas["Matricula"].get()
        descripcion = entradas["Especialidad"].get()

        if nombre and apellido and dni and telefono and matricula and descripcion:
            try:
                actualizar_medico(seleccion, nombre, apellido, matricula, telefono, dni)
                self.tree.item(seleccion, values=(nombre, apellido, dni, telefono, matricula, descripcion))
                messagebox.showinfo("Información", "Cambios guardados correctamente.")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar los cambios: {e}")
        else:
            messagebox.showwarning("Atención", "Complete todos los campos.")

    def eliminar_medico(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione un medico.")
            return

        medico_seleccionado = self.tree.item(seleccion[0], "values")
        id_medico = medico_seleccionado[0]  # Asumiendo que el ID es el primer valor

        respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este médico?")
        if respuesta:
            try:
                conexion = mysql.connector.connect(
                    host="localhost",
                    user="Gaspar",
                    password="yarco7mysql",
                    database="hospital"
                )
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM medico WHERE id_medico = %s", (id_medico,))
                conexion.commit()
                messagebox.showinfo("Éxito", "Médico eliminado correctamente.")
                self.tree.delete(seleccion[0])  # Eliminar de la interfaz
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al eliminar el médico: {err}")
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()


    def guardar_nuevo_medico(self, entradas, ventana):
        nombre = entradas["Nombre"].get()
        apellido = entradas["Apellido"].get()
        dni = entradas["DNI"].get()
        telefono = entradas["Telefono"].get()
        matricula = entradas["Matricula"].get()
        descripcion = entradas["Especialidad"].get()

        if nombre and apellido and dni and telefono and matricula and descripcion:
            try:
                insertar_medico(nombre, apellido, matricula, telefono, dni)
                self.tree.insert("", "end", values=(nombre, apellido, dni, telefono, matricula, descripcion))
                messagebox.showinfo("Información", "Médico agregado correctamente.")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar el médico: {e}")
        else:
            messagebox.showwarning("Atención", "Complete todos los campos.")

    def buscar_medico(self):
        busqueda = self.entrada_buscar.get().strip().lower()

        if not busqueda:
            self.tree.delete(*self.tree.get_children())
            self.cargar_medicos()
            return

        medico_encontrado = False

        for item in self.tree.get_children():
            valores = self.tree.item(item, 'values')
            nombre = valores[0].lower()
            apellido = valores[1].lower()

            if busqueda in nombre or busqueda in apellido:
                medico_encontrado = True
            else:
                self.tree.delete(item)

        if not medico_encontrado:
            messagebox.showwarning("Atención", "No se encontró el médico.")
            self.tree.delete(*self.tree.get_children())
            self.cargar_medicos()

    def cargar_medicos(self):
        self.tree.delete(*self.tree.get_children())
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre, apellido, documento, telefono, matricula FROM medico")
            medicos = cursor.fetchall()
            for medico in medicos:
                self.tree.insert("", "end", values=medico)
            conexion.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al cargar los médicos: {e}")

ventana = Tk()
ventana.title("Gestion de Medicos")
ventana.resizable(False, False)
root = Gestionmedico(ventana)
ventana.mainloop()