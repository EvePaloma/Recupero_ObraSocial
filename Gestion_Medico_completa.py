from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from ConexionBD import *

class Gestionmedico(Frame):

    def __init__(self, master):
        Frame.__init__(self, master, bg="#e4c09f")
        self.master = master
        self.grid()
        self.createWidgets()
        self.cargar_medicos()

    def solo_letras(self, char):
        return char.isalpha() or char == " "

    def solo_numeros(self, char):
        return char.isdigit()

    def actualizar_treeview(self):
        self.tree.delete(*self.tree.get_children())
        self.cargar_medicos()




    def validar_repetidos(self, documento):
        conexion = obtener_conexion()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return
        try:
            cursor = conexion.cursor()
            sentencia = "SELECT COUNT(*) FROM medico WHERE documento = %s"
            cursor.execute(sentencia, (documento,))
            resultado = cursor.fetchone()
            cursor.close()
            conexion.close()
            if resultado[0] > 0:
                return False
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Consulta", f"No se pudo realizar la consulta a la base de datos: {err}")
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return

    def guardar_nuevo_medico(self, entradas, ventana):
        nombre = entradas["Nombre"].get()
        apellido = entradas["Apellido"].get()
        dni = entradas["DNI"].get()
        telefono = entradas["Telefono"].get()
        matricula = entradas["Matricula"].get()

        if not self.validar_repetidos(dni):
            messagebox.showwarning("Atención", "El documento ya está registrado.")
            return

        if nombre and apellido and dni and telefono and matricula:
            try:
                insertar_medico(nombre, apellido, matricula, telefono, dni)
                self.tree.insert("", "end", values=(nombre, apellido, dni, telefono, matricula))
                messagebox.showinfo("Información", "Médico agregado correctamente.")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar el médico: {e}")
        else:
            messagebox.showwarning("Atención", "Complete todos los campos.")

        self.actualizar_treeview()


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
            command=self.buscar_todo,
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
            columns=("id_medico","nombre", "Apellido", "DNI"),
            show="headings",
            height=5,
        )

        # Títulos de columnas
      
        
        self.tree.heading("id_medico", text="")

        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("DNI", text="DNI")

        # Ancho de las columnas y datos centrados
        self.tree.column("id_medico", width=0, stretch=False)

        self.tree.column("nombre", anchor="center", width=250, stretch=False)
        self.tree.column("Apellido", anchor="center", width=350, stretch=False)
        self.tree.column("DNI", anchor="center", width=250, stretch=False)

        # Evitar que las columnas se puedan mover o redimensionar
        self.tree["displaycolumns"] = ("nombre", "Apellido", "DNI")
        for col in self.tree["displaycolumns"]:
            self.tree.heading(col, command=lambda: "break")
            self.tree.column(col, stretch=False)

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

        btn_volver = Button(
            frame_btn,
            text="Volver",
            width=15,
            font=("Robot", 13),
            bg="#e6c885",
            command=self.volver_menu_principal,
        )
        btn_volver.grid(row=4, column=4, padx=50)

    def agregar_medico(self):
        ventana_agregar = Toplevel(self)
        ventana_agregar.title("Agregar medico")
        ventana_agregar.config(bg="#e4c09f")
        ventana_agregar.resizable(False, False)
        ventana_agregar.protocol("WM_DELETE_WINDOW", lambda: None)


        frame_agregar = LabelFrame(
            ventana_agregar,
            text="Agregar Nuevo medico",
            font=("Robot", 12),
            padx=10,
            pady=10,
            bg="#c9c2b2",
        )
        frame_agregar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        campos = ["Nombre", "Apellido", "DNI", "Telefono", "Matricula"]
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

        btn_volver = Button(
            frame_agregar,
            text="Volver",
            font=("Robot", 10),
            bg="#e6c885",
            command=ventana_agregar.destroy,
        )
        btn_volver.grid(row=len(campos) + 1, column=4, columnspan=2, padx=10, pady=10)
        self.actualizar_treeview()

    def ver_medico(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione un medico.")
            return

        medico_seleccionado = self.tree.item(seleccion[0], "values")
        # Exclude the ID (first value) from the details
        detalles_medico = medico_seleccionado[1:]
        self.abrir_ventana_medico(detalles_medico, seleccion[0], modo="ver")
        self.actualizar_treeview()

    def modificar_medico(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione un medico.")
            return

        medico_seleccionado = self.tree.item(seleccion[0], "values")
        # Extract the ID (first value) separately
        id_medico = medico_seleccionado[0]
        # Exclude the ID from the details
        detalles_medico = medico_seleccionado[1:]
        self.abrir_ventana_medico(detalles_medico, id_medico, modo="modificar")
        self.actualizar_treeview()

    def abrir_ventana_medico(self, medico, id_seleccionado, modo="ver"):
        ventana = Toplevel(self)
        ventana.title("Detalles del medico")
        ventana.config(bg="#e4c09f")
        ventana.resizable(False, False)
        ventana.protocol("WM_DELETE_WINDOW", lambda: None)

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

        campos = ["Nombre", "Apellido", "DNI", "Telefono", "Matricula"]
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
            if i < len(medico):
                entry.insert(0, medico[i])
            entradas[campo] = entry

        # ComboBox for Estado
        etiqueta_estado = Label(
            frame_detalles, text="Estado:", bg="#c9c2b2", font=("Robot", 10)
        )
        etiqueta_estado.grid(row=len(campos), column=0, padx=10, pady=5)
        combo_estado = ttk.Combobox(frame_detalles, values=["1", "0"], width=37)
        combo_estado.grid(row=len(campos), column=1, padx=10, pady=5)
        combo_estado.set("1" if medico[-1] == "1" else "0")  # Set the current value of Estado
        entradas["Estado"] = combo_estado

        if modo == "ver":
            for entry in entradas.values():
                entry.config(state="readonly")

            
            btn_volver = Button(
                ventana,
                text="Volver",
                font=("Robot", 10),
                bg="#e6c885",
                command=ventana.destroy,
            )
            btn_volver.grid(row=len(campos) + 2, column=2, columnspan=2, padx=10, pady=10)
            
            

        if modo == "modificar":
            btn_modificar = Button(
                frame_detalles,
                text="Guardar Cambios",
                font=("Robot", 13),
                bg="#e6c885",

                command=lambda: self.guardar_cambios(
                    entradas, ventana, id_seleccionado
                ),
            )
            btn_modificar.grid(
                row=len(campos) + 1, column=0, columnspan=2, padx=10, pady=10
            )

            btn_volver = Button(
                frame_detalles,
                text="Volver",
                font=("Robot", 10),
                bg="#e6c885",
                command=ventana.destroy,
            )
            btn_volver.grid(
                row=len(campos) + 2, column=3, columnspan=2, padx=10, pady=10
            )
            self.actualizar_treeview()


    def activar_edicion(self, entradas, btn_guardar):
        for entry in entradas.values():
            entry.config(state="normal")
        btn_guardar.config(state="normal")

    def guardar_cambios(self, entradas, ventana, id_seleccionado):
        nombre = entradas["Nombre"].get()
        apellido = entradas["Apellido"].get()
        dni = entradas["DNI"].get()
        telefono = entradas["Telefono"].get()
        matricula = entradas["Matricula"].get()
        estado = entradas["Estado"].get()

        if nombre and apellido and dni and telefono and matricula:
            try:
                conexion = obtener_conexion()
                cursor = conexion.cursor()
                cursor.execute(
                    """
                    UPDATE medico
                    SET nombre = %s, apellido = %s, documento = %s, telefono = %s, matricula = %s, activo = %s
                    WHERE id_medico = %s
                    """,
                    (nombre, apellido, dni, telefono, matricula, estado, id_seleccionado)
                )
                conexion.commit()
                messagebox.showinfo("Éxito", "Datos del médico actualizados correctamente.")
                self.cargar_medicos()
                ventana.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al actualizar los datos del médico: {err}")
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()
        else:
            messagebox.showwarning("Atención", "Complete todos los campos.")

        self.actualizar_treeview()
        
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
                conexion = obtener_conexion()
                cursor = conexion.cursor()
                cursor.execute("UPDATE medico SET activo = 0 WHERE id_medico = %s", (id_medico,))
                conexion.commit()
                messagebox.showinfo("Éxito", "Médico eliminado correctamente.")
                self.tree.delete(seleccion[0])  # Eliminar de la interfaz
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al eliminar el médico: {err}")
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()

        self.actualizar_treeview()



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



    def buscar_todo(self):
        busqueda = self.entrada_buscar.get().strip().lower()

        if not busqueda:
            self.tree.delete(*self.tree.get_children())
            self.cargar_medicos()
            return

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            query = """
            SELECT id_medico, nombre, apellido, documento, telefono, matricula 
            FROM medico 
            WHERE (LOWER(nombre) LIKE %s OR LOWER(apellido) LIKE %s OR documento LIKE %s)
            AND (activo = 1 OR activo = 0)
            """
            like_pattern = f"%{busqueda}%"
            cursor.execute(query, (like_pattern, like_pattern, like_pattern))
            medicos = cursor.fetchall()
            conexion.close()

            self.tree.delete(*self.tree.get_children())
            if medicos:
                for medico in medicos:
                    self.tree.insert("", "end", values=medico)
            else:
                self.cargar_medicos()
                messagebox.showwarning("Atención", "No se encontró el médico. Se han cargado todos los médicos activos.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo buscar los médicos: {e}")

    def cargar_medicos(self):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT id_medico, nombre, apellido, documento,  telefono, matricula FROM medico WHERE activo = 1")

            medicos = cursor.fetchall()
            self.tree.delete(*self.tree.get_children())
            for medico in medicos:
                self.tree.insert("", "end", values=medico)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al cargar los médicos: {err}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()



    def volver_menu_principal(self):
        from Menu import MENU
        self.master.destroy()
        ventana = Tk()
        ventana.wm_title("Menú Recupero de Obra Social")
        ventana.wm_resizable(0,0)
        ventana.geometry("+30+15")
        menu = MENU(ventana)
        menu.mainloop()

ventana = Tk()
ventana.title("Gestion de Medicos")
ventana.resizable(False, False)
root = Gestionmedico(ventana)
ventana.mainloop()