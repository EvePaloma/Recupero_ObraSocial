from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
from ConexionBDpaciente import *


class GestionPaciente(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg="#e4c09f")
        self.master = master
        self.grid()
        self.createWidgets()
        self.cargar_paciente()
        #self.actualizar_treeview()
    

    def solo_letras(self, char):
        return char.isalpha() or char == " "

    def solo_numeros(self, char):
        return char.isdigit()


    def createWidgets(self):
        frame_pacientes = LabelFrame(self, text="Gestión de Pacientes", font=("Roboto",10),padx=10, pady=10, bg="#c9c2b2")
        frame_pacientes.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        #Carga la imagen de fondo
        img_fondo = Image.open("fondo3.png")
        img_fondo = img_fondo.resize((900, 200), Image.Resampling.LANCZOS)
        self.img_fondo = ImageTk.PhotoImage(img_fondo)

        #Label para la imagen de fondo
        fondo_label = Label(frame_pacientes, image=self.img_fondo)
        fondo_label.grid(row=0, column=0, columnspan=7)

        #Frame más chico para label y entry de búsqueda
        frame_busqueda = Frame(frame_pacientes, bg="#e6c885")
        frame_busqueda.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="w")

        #Widgets de búsqueda dentro del frame más chico
        etiqueta_buscar = Label(frame_busqueda, text="Buscar:", bg="#e6c885",font=("Roboto",13))
        etiqueta_buscar.grid(row=1, column=1, padx=5, pady=5)

        self.entrada_buscar = Entry(frame_busqueda,width="50",font=("Roboto",11))
        self.entrada_buscar.grid(row=1, column=2, padx=5, pady=5)

        img_buscar = Image.open("buscar1.png").resize((30, 30), Image.Resampling.LANCZOS)
        img_buscar = ImageTk.PhotoImage(img_buscar)
        btn_buscar = Button(frame_busqueda, image=img_buscar, width=30, height=30,bg="#e6c885", 
                            command=self.buscar_paciente)
        btn_buscar.grid(row=1, column=3)
        btn_buscar.image = img_buscar

        boton_agregar = Button(frame_pacientes, text="Agregar   +", width=15, bg="#e6c885",font=("Roboto",13),
                                command=self.agregar_paciente)
        boton_agregar.grid(row=1, column=5, padx=10, pady=10)

        #Para que siempre esté atrás de los widgets
        fondo_label.lower()

        #Frame para el Treeview y el scrollbar
        frame_tabla = Frame(frame_pacientes, bg="#c9c2b2")  # Frame para contener la tabla y el scrollbar
        frame_tabla.grid(row=2, column=0, columnspan=6, padx=10, pady=10)
        
        stilo = ttk.Style()
        stilo.configure("Treeview", font=("Roboto",11), rowheight=25)  # Cambia la fuente y el alto de las filas
        stilo.configure("Treeview.Heading", font=("Roboto",14))  # Cambia la fuente de las cabeceras
        # Treeview para mostrar la tabla de pacientes dentro del frame_tabla
        self.tree = ttk.Treeview(frame_tabla, columns=("id", "nombre", "apellido", "dni", "obra_social"), show='headings', height=5)

        # Títulos de columnas
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("apellido", text="Apellido")
        self.tree.heading("dni", text="DNI")
        self.tree.heading("obra_social", text="Obra Social")

        # Ancho de las columnas y datos centrados
        self.tree.column("id", anchor='center', width=50)
        self.tree.column("nombre", anchor='center', width=200)
        self.tree.column("apellido", anchor='center', width=200)
        self.tree.column("dni", anchor='center', width=150)
        self.tree.column("obra_social", anchor='center', width=200)

        
        #Grid del frame_tabla
        self.tree.grid(row=0, column=0, sticky="nsew")

        #Scrollbar para la tabla dentro del frame_tabla
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')  #Se expande desde arriba hacia abajo
        self.tree.configure(yscrollcommand=scrollbar.set)

        frame_btn = Frame(frame_pacientes,bg="#c9c2b2")
        frame_btn.grid(row=4, columnspan=6)

        #Botones(ver, modificar, eliminar)
        btn_ver = Button(frame_btn, text="Ver", width=15, font=("Roboto",13),bg="#e6c885", 
                         command=self.ver_paciente)
        btn_ver.grid(row=4, column=1,padx=50)

        btn_editar = Button(frame_btn, text="Modificar", width=15, font=("Roboto",13),bg="#e6c885",
                             command=self.modificar_paciente)
        btn_editar.grid(row=4, column=2,padx=50)
        
        btn_eliminar = Button(frame_btn, text="Eliminar", width=15,font=("Roboto",13),bg="#e6c885",
                               command=self.eliminar_paciente)
        btn_eliminar.grid(row=4, column=3, padx=50)


    def ver_paciente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione un paciente.")
            return
        
        paciente_seleccionado = self.tree.item(seleccion[0], 'values')   #Item= valor del elemento
        self.abrir_ventana_paciente(paciente_seleccionado,seleccion[0],modo="ver")

    def modificar_paciente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione un paciente.")
            return
        
        paciente_seleccionado = self.tree.item(seleccion[0], 'values')
        self.abrir_ventana_paciente(paciente_seleccionado, seleccion[0],modo="modificar")    
    
    def abrir_ventana_paciente(self, paciente, id_seleccionado, modo="ver"):
        ventana = Toplevel(self)
        ventana.title("Detalles del paciente")
        ventana.config(bg="#e4c09f")
        ventana.resizable(False,False)
        ventana.geometry("510x485+400+160")
        
        ventana.grid_columnconfigure(0, weight=1)
        ventana.grid_rowconfigure(0, weight=1)

        frame_detalles = LabelFrame(ventana, text="Detalles del Paciente", font=("Roboto", 10), padx=10, pady=10, bg="#c9c2b2")
        frame_detalles.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        campos = ["Nombre",  "Apellido","DNI","Obra Social","Propietario del Plan","Sexo","Teléfono del Paciente","Número de Afiliado"]
        id_paciente = paciente[0] #ACA ES

        vcmd_letras = ventana.register(self.solo_letras)
        vcmd_numeros = ventana.register(self.solo_numeros)
        
        try:
            conexion = mysql.connector.connect(host="localhost", user="root", password="12345", database="recupero_obra_social")
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre, apellido, dni, obra_social, propietario, sexo, telefono, nro_afiliado FROM paciente WHERE id_paciente = %s", (id_paciente,))
            valores = cursor.fetchone()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al cargar los datos del paciente: {err}")
            ventana.destroy()
            return
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
            
        entradas = {}

        vcmd_letras = ventana.register(self.solo_letras)
        vcmd_numeros = ventana.register(self.solo_numeros)

        for i, campo in enumerate(campos):
            etiqueta = Label(frame_detalles, text=campo + ":", bg="#c9c2b2", font=("Roboto", 10))
            etiqueta.grid(row=i, column=0, padx=10, pady=5)
            entry = Entry(frame_detalles, width=40)
            entry.grid(row=i, column=1, padx=10, pady=5)

            if campo in ["Nombre", "Apellido", "Obra Social", "Propietario del Plan", "Sexo"]:
                entry.config(validate="key", validatecommand=(vcmd_letras, '%S'))
            elif campo in ["DNI", "Teléfono del Paciente"]:
                entry.config(validate="key", validatecommand=(vcmd_numeros, '%S'))

            if i < len(valores):
                entry.insert(0, valores[i])
            entradas[campo] = entry     

                # ComboBox for Estado
        
        etiqueta_estado = Label(frame_detalles, text="Estado:", bg="#c9c2b2", font=("Roboto", 10))
        etiqueta_estado.grid(row=len(campos), column=0, padx=10, pady=5)
        combo_estado = ttk.Combobox(frame_detalles, values=["1", "0"], width=37)
        combo_estado.grid(row=len(campos), column=1, padx=10, pady=5)
        combo_estado.set("1" if paciente[-1] == "1" else "0")
        entradas["Estado"] = combo_estado

        if modo == "ver":
            entry.config(state="readonly")
            btn_guardar = Button(ventana, text="Guardar Cambios", width=15, font=("Roboto", 13), bg="#e6c885",
                                     command=lambda: self.guardar_cambios(entradas, ventana, id_seleccionado))
            btn_guardar.grid(row=len(campos), column=0, pady=10)
            btn_guardar.config(state="disabled")  # Initially disabled

            btn_editar = Button(ventana, text="Modificar", width=15, font=("Roboto", 13), bg="#e6c885",
                                    command=lambda: self.activar_edicion(entradas, btn_guardar))
            btn_editar.grid(row=len(campos) + 1, column=0, pady=10)
                                

        if modo == "modificar":
            btn_modificar = Button(frame_detalles, text="Guardar Cambios", bg="#e6c885",
                                   command=lambda: self.guardar_cambios(entradas, ventana, id_seleccionado))
            btn_modificar.grid(row=10, column=1, columnspan=2, padx=10, pady=0)

    def activar_edicion(self, entradas, btn_guardar):
    # Habilitar la edición en las entradas
        for entry in entradas.values():
            entry.config(state="normal")  # Permitir edición en todos los Entry
        
        # Activar el botón "Guardar Cambios"
        btn_guardar.config(state="normal")  # Activar el botón directamente

    def guardar_cambios(self, entradas, ventana, seleccion):
        nuevos_valores = {campo: entradas[campo].get().upper() for campo in entradas}
        id_paciente = self.tree.item(seleccion, 'values')[0]  # Asumiendo que el ID es el primer valor

        try:
            conexion = mysql.connector.connect(host="localhost", user="root", password="12345", database="recupero_obra_social")
            cursor = conexion.cursor()
            query = """
            UPDATE paciente
            SET nombre = %s, apellido = %s, dni = %s, obra_social = %s, propietario = %s, sexo = %s, telefono = %s, nro_afiliado = %s, activo = %s
            WHERE id_paciente = %s
            """
            cursor.execute(query, (
                nuevos_valores["Nombre"], nuevos_valores["Apellido"], nuevos_valores["DNI"], nuevos_valores["Obra Social"],
                nuevos_valores["Propietario del Plan"], nuevos_valores["Sexo"], nuevos_valores["Teléfono del Paciente"],
                nuevos_valores["Número de Afiliado"],nuevos_valores["Estado"], id_paciente
            ))
            conexion.commit()

            # Actualizar los valores en el Treeview
            self.tree.item(seleccion, values=(id_paciente, *nuevos_valores.values()))
            
            # Mostrar mensaje de confirmación
            messagebox.showinfo("Información", "Cambios guardados correctamente.")
            
            # Cerrar la ventana después de guardar
            ventana.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al guardar los cambios: {err}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def eliminar_paciente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione un paciente para eliminar.")
            return
        
        paciente_seleccionado = self.tree.item(seleccion[0], "values")
        id_paciente = paciente_seleccionado[0]  # Asumiendo que el ID es el primer valor
        
        #Pregunta al usuario si está seguro de eliminar 
        respuesta = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar el paciente seleccionado?")
        if respuesta:  
            try:
                conexion= mysql.connector.connect(host="localhost", user="root", password="12345", database="recupero_obra_social")
                cursor = conexion.cursor()
                cursor.execute("UPDATE paciente SET activo = 0 WHERE id_paciente = %s", (id_paciente,))
                conexion.commit()
                messagebox.showinfo("Éxito", "Paciente eliminado correctamente.")
                self.tree.delete(seleccion)
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al eliminar el paciente: {err}")
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()

            '''        
            messagebox.showinfo("Atención", "Paciente eliminado correctamente.")
        else:
            messagebox.showinfo("Atención", "Eliminación cancelada.")
'''
    def agregar_paciente(self):
        ventana_agregar = Toplevel(self)
        ventana_agregar.title("Agregar Paciente")
        ventana_agregar.config(bg="#e4c09f")
        ventana.resizable(False,False)
        
        frame_agregar = LabelFrame(ventana_agregar, text="Agregar Nuevo Paciente", font= ("Roboto", 11),padx=10, pady=10, bg="#c9c2b2")
        frame_agregar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        campos = ["Nombre","Apellido","DNI","Obra Social","Propietario del Plan","Sexo","Teléfono del Paciente","Número de Afiliado"]
        entradas = {}

        vcmd_letras = ventana_agregar.register(self.solo_letras)
        vcmd_numeros = ventana_agregar.register(self.solo_numeros)

        for i, campo in enumerate(campos):
            etiquetas = Label(frame_agregar, text=campo + ":", bg="#c9c2b2", font=("Roboto", 10))
            etiquetas.grid(row=i, column=0, padx=10, pady=5)
            entry = Entry(frame_agregar, width=40, font=("Roboto", 10))

            if campo in ["Nombre", "Apellido", "Obra Social", "Propietario del Plan", "Sexo"]:
                entry.config(validate="key", validatecommand=(vcmd_letras, '%S'))
            elif campo in ["DNI", "Teléfono del Paciente"]:
                entry.config(validate="key", validatecommand=(vcmd_numeros, '%S'))

            entry.grid(row=i, column=1, padx=10, pady=5)
            entradas[campo] = entry

        btn_nuevo_paciente = Button(frame_agregar, text="Agregar", font=("Roboto", 10),bg="#e6c885", command=lambda: self.guardar_nuevo_paciente(entradas, ventana_agregar))
        btn_nuevo_paciente.grid(row=len(campos), column=0, columnspan=2, padx=10, pady=10)

        

    def guardar_nuevo_paciente(self, entry, ventana):
        nombre = entry["Nombre"].get().upper()      #Obtenemos los valores que el usuario ingresó.
        apellido = entry["Apellido"].get().upper()
        dni = entry["DNI"].get()
        obrasocial = entry["Obra Social"].get().upper()
        propietario = entry["Propietario del Plan"].get().upper()
        sexo = entry["Sexo"].get().upper()
        telefonopaciente = entry["Teléfono del Paciente"].get()
        numeroafiliado = entry["Número de Afiliado"].get().upper()

        # Validar datos y agregar al Treeview
        if nombre and apellido and dni and obrasocial and propietario and telefonopaciente and numeroafiliado:
            try:
                conexion = mysql.connector.connect(host="localhost", user="root", password="12345", database="recupero_obra_social")
                cursor = conexion.cursor()
                
                # Verificar si el DNI ya existe
                cursor.execute("SELECT COUNT(*) FROM paciente WHERE dni = %s", (dni,))
                if cursor.fetchone()[0] > 0:
                    messagebox.showerror("Error", "El DNI ingresado ya existe. Por favor, ingrese un DNI diferente.")
                    return
                
                query = """
                INSERT INTO paciente (nombre, apellido, dni, obra_social, propietario, sexo, telefono, nro_afiliado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (nombre, apellido, dni, obrasocial, propietario, sexo, telefonopaciente, numeroafiliado))
                conexion.commit()
                messagebox.showinfo("Información", "Paciente agregado correctamente.")
                ventana.destroy()
                self.cargar_paciente()  # Recargar la lista de pacientes
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al agregar el paciente: {err}")
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()
        else:
            messagebox.showwarning("Atención", "Complete todos los campos.")

    def buscar_paciente(self):
        busqueda = self.entrada_buscar.get().strip().upper()
        if not busqueda:
            self.tree.delete(*self.tree.get_children())
            self.cargar_paciente()
            return
        
        paciente_encontrado = False

        try:
            conexion = mysql.connector.connect(host="localhost", user="root", password="12345", database="recupero_obra_social")
            cursor = conexion.cursor()
            query = """
            SELECT id_paciente, nombre, apellido, dni, obra_social 
            FROM paciente 
            WHERE LOWER(nombre) LIKE %s OR LOWER(apellido) LIKE %s OR dni LIKE %s
            """
            like_pattern = f"%{busqueda}%"
            cursor.execute(query, (like_pattern, like_pattern, like_pattern))
            pacientes = cursor.fetchall()
            
            self.tree.delete(*self.tree.get_children())
            for paciente in pacientes:
                self.tree.insert("", "end", values=paciente.upper())
            
            if not paciente_encontrado:
                messagebox.showwarning("Atención", "No se encontró el paciente.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al buscar el paciente: {err}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def cargar_paciente(self):
        try:
            conexion = mysql.connector.connect(host="localhost", user="root", password="12345", database="recupero_obra_social")
            cursor = conexion.cursor()
            cursor.execute("SELECT id_paciente, nombre, apellido, dni, obra_social FROM paciente")
            pacientes = cursor.fetchall()
            for paciente in pacientes:
                self.tree.insert("", "end", values=paciente)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al cargar los pacientes: {err}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

ventana = Tk()
ventana.title("Gestion de Paciente")
ventana.resizable(False,False)
ventana.geometry("+200+80")
root = GestionPaciente(ventana)
ventana.mainloop()