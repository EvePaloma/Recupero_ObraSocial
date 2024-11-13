from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
from ConexionBD import *
import mysql
from Gestion_obra_social import *
#import mysql.connector as mysql_connector

class GestionPaciente(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg="#e4c09f")
        self.master = master
        self.grid()
        self.createWidgets()
        self.cargar_paciente()
        self.master.protocol("WM_DELETE_WINDOW", lambda: None)
        #self.actualizar_treeview()
    
    def insertar_paciente_bd(nombre, apellido, tipo_documento, documento, id_obra_social, numeroafiliado):
        conexion = obtener_conexion()
        if conexion is None:
            return
        try:
            cursor = conexion.cursor()
            sql = "INSERT INTO paciente (nombre, apellido, tipo_documento, documento, id_obra_social, nro_afiliado,) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (nombre, apellido, tipo_documento, documento, id_obra_social, numeroafiliado)
            cursor.execute(sql, val)
            conexion.commit()
            messagebox.showinfo("Éxito", "Registro insertado correctamente.")
        except mysql_connector.Error as err:
            messagebox.showerror("Error", f"Error al insertar en la base de datos: {err}")
        finally:
            conexion.close()

        #nombre, apellido, documento, id_obra_social, obrasocialsec, propietario, fechanac, sexo, telefonopaciente, contactoemergencia, numeroafiliado)
    def actualizar_paciente(nombre, apellido,  tipo_documento, documento, id_obra_social, numeroafiliado):
        
        conexion = obtener_conexion()
        if conexion is None:
            return
        try:
            cursor = conexion.cursor()
            sql = "UPDATE paciente SET nombre=%s, apellido=%s, tipo_documento=%s, documento=%s, id_obra_social = %s, nro_afiliado = %s WHERE id=%s"
            val = (nombre, apellido, tipo_documento, documento, id_obra_social, numeroafiliado)
            cursor.execute(sql, val)
            conexion.commit()
            messagebox.showinfo("Éxito", "Registro actualizado correctamente.")
        except mysql_connector.Error as err:
            messagebox.showerror("Error", f"Error al actualizar en la base de datos: {err}")
        finally:
            conexion.close()
    
    def solo_letras(self, char):
        return char.isalpha() or char == " "

    def solo_numeros(self, char):
        return char.isdigit()

    def actualizar_treeview(self):
        self.tree.delete(*self.tree.get_children())
        conexion = obtener_conexion()
        if conexion is None:
            return
        try:
            cursor = conexion.cursor()
            seleccion = self.combo_activos.get()
            if seleccion == "Activos":
                cursor.execute("SELECT id_paciente, nombre, apellido, documento, id_obra_social FROM paciente WHERE activo = 1")
            elif seleccion == "Inactivos":
                cursor.execute("SELECT id_paciente, nombre, apellido, documento, id_obra_social FROM paciente WHERE activo = 0")
            elif seleccion == "Todos":
                cursor.execute("SELECT id_paciente, nombre, apellido, documento, id_obra_social FROM paciente")
            pacientes = cursor.fetchall()
            for paciente in pacientes:
                self.tree.insert("", "end", values=paciente)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al actualizar el Treeview: {err}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def createWidgets(self):
        frame_pacientes = LabelFrame(self, text="Gestión de Pacientes", font=("Roboto",10),padx=10, pady=10, bg="#c9c2b2")
        frame_pacientes.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        #Carga la imagen de fondo
        img_fondo = Image.open("fondo3.png")
        img_fondo = img_fondo.resize((1310, 200), Image.Resampling.LANCZOS)
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

        self.combo_activos = ttk.Combobox(frame_busqueda, width=10, font=("Robot", 14), state="readonly", style="Custom.TCombobox")
        self.combo_activos['values'] = ("Activos", "Inactivos", "Todos")
        self.combo_activos.set("Activos")
        self.combo_activos.grid(row=1, column=4, padx=20, pady=3)
        self.combo_activos.bind("<<ComboboxSelected>>", lambda event: self.actualizar_treeview())

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
        self.tree = ttk.Treeview(frame_tabla, columns=("id", "nombre", "apellido", "documento", "id_obra_social"), show='headings', height=11)
        
        # Títulos de columnas
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("apellido", text="Apellido")
        self.tree.heading("documento", text="DNI")
        self.tree.heading("id_obra_social", text="Obra Social")

        # Ancho de las columnas y datos centrados
        self.tree.column("id", anchor='center', width=0)
        self.tree.column("nombre", anchor='center', width=300)
        self.tree.column("apellido", anchor='center', width=300)
        self.tree.column("documento", anchor='center', width=300)
        self.tree.column("id_obra_social", anchor='center', width=300)
        
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

        btn_volver = Button(frame_btn, text="Volver al menú", width=15,font=("Robot",13),bg="#e6c885",
                            command=self.volver_menu_principal)
        btn_volver.grid(row=4, column=4, padx=50)

    def volver_menu_principal(self):
        self.master.destroy()
        import os
        os.system('python Menu.py')


    def conectar_tabla(self, tabla):
            conexion = obtener_conexion()  # Llama a la función que establece la conexión
            if conexion is None:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
                return
            try:
                cursor = conexion.cursor()  # Crea el cursor
                sentencia = f"SELECT * from {tabla}"
                cursor.execute(sentencia)  # Ejecuta la consulta
                datos = cursor.fetchall()  # Obtén todos los resultados
                cursor.close()  # Cierra el cursor
                conexion.close()  # Cierra la conexión a la base de datos. Devuelve la clave y el valor
                return datos  # Devuelve los datos obtenidos
            except mysql.connector.Error as err:
                messagebox.showerror("Error de Consulta", f"No se pudo realizar la consulta a la base de datos: {err}")
                if cursor:
                    cursor.close()
                if conexion:
                    conexion.close()
                messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
                return

    #al seleccionar una opción en la compo, retorna el id
    def on_seleccion(self, campo):
        try:
            if campo == "Obra Social":
                seleccion = self.combo_valores.get()
                if seleccion in self.datos_tabla:
                    self.dato_obra = self.datos_tabla[seleccion]
                    return self.dato_obra
                else:
                    raise ValueError(f"Selección '{seleccion}' no encontrada en datos_tabla.")
            elif campo == "Estado":
                seleccion = self.combo_valores_2.get()
                if seleccion in self.datos_tabla_1:
                    self.dato_estado = self.datos_tabla_1[seleccion]
                    return self.dato_estado
                else:
                    raise ValueError(f"Selección '{seleccion}' no encontrada en datos_tabla.")
            else:
                raise ValueError(f"Campo '{campo}' no es válido.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return None

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
        ventana_abrir = Toplevel(self)
        ventana_abrir.title("Detalles del paciente")
        ventana_abrir.config(bg="#e4c09f")
        ventana_abrir.resizable(False, False)
        ventana_abrir.geometry("510x445+400+160")
        ventana_abrir.protocol("WM_DELETE_WINDOW", lambda: None)  # Deshabilitar el botón "Cerrar" de la ventana

        ventana_abrir.grid_columnconfigure(0, weight=1)
        ventana_abrir.grid_rowconfigure(0, weight=1)

        frame_detalles = LabelFrame(ventana_abrir, text="Detalles del Paciente", font=("Roboto", 13), padx=10, pady=10, bg="#c9c2b2")
        frame_detalles.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        campos = ["Nombre", "Apellido", "Tipo de Documento", "DNI", "Obra Social", "Número de Afiliado"]
        id_paciente = paciente[0]  # Asumiendo que el ID es el primer valor

        vcmd_letras = ventana_abrir.register(self.solo_letras)
        vcmd_numeros = ventana_abrir.register(self.solo_numeros)

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            # Obtener los datos del paciente
            cursor.execute("SELECT nombre, apellido, tipo_documento, documento, id_obra_social, nro_afiliado, activo FROM paciente WHERE id_paciente = %s", (id_paciente,))
            valores = cursor.fetchone()

            # Obtener el nombre de la obra social
            cursor.execute("SELECT nombre FROM obra_social WHERE id_obra_social = %s", (valores[4],))
            obra_social_nombre = cursor.fetchone()[0]

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al obtener los datos del paciente: {err}")
            return
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

        entradas = {}

        for i, campo in enumerate(campos):
            etiquetas = Label(frame_detalles, text=campo + ":", bg="#c9c2b2", font=("Roboto", 10))
            etiquetas.grid(row=i, column=0, padx=10, pady=5)
            entry = Entry(frame_detalles, width=40, font=("Roboto", 10))
            entry.grid(row=i, column=1, padx=10, pady=5)
            entradas[campo] = entry

            if campo in ["Nombre","Apellido","Obra Social"]:
                entry.config(validate="key", validatecommand=(vcmd_letras, '%S'))
            elif campo in ["Tipo de Documento","DNI"]:
                entry.config(validate="key", validatecommand=(vcmd_numeros, '%S'))

        # Establecer los valores en los campos
        entradas["Nombre"].insert(0, valores[0])
        entradas["Apellido"].insert(0, valores[1])
        entradas["Tipo de Documento"].insert(0, valores[2])
        entradas["DNI"].insert(0, valores[3])
        entradas["Obra Social"].insert(0, obra_social_nombre)
        entradas["Número de Afiliado"].insert(0, valores[5])

        # ComboBox para Estado
        etiqueta_estado = Label(frame_detalles, text="Estado:", bg="#c9c2b2", font=("Roboto", 10))
        etiqueta_estado.grid(row=len(campos), column=0, padx=10, pady=5)
        combo_estado = ttk.Combobox(frame_detalles, values=["Activo", "Inactivo"], width=37)
        combo_estado.grid(row=len(campos), column=1, padx=10, pady=5)
        combo_estado.set("Activo" if valores[5] == 1 else "Inactivo")
        entradas["Estado"] = combo_estado

        # ComboBox para Obra Social
        '''etiqueta_obra_social = Label(frame_detalles, text="Obra Socials:", bg="#c9c2b2", font=("Roboto", 10))
        etiqueta_obra_social.grid(row=len(campos), column=0, padx=10, pady=50)
        combo_obra_social = ttk.Combobox(frame_detalles, values=["OSDE", "Swiss Medical", "Galeno", "Medifé", "Sancor Salud", "Otra"], width=37)
        combo_obra_social.grid(row=len(campos), column=1, padx=30, pady=35)
        combo_obra_social.set("Seleccionar obra social")
        entradas["Obra Social"] = combo_obra_social'''

        if modo == "ver":
            for entry in entradas.values():
                entry.config(state="readonly")
            combo_estado.config(state="readonly")
            #combo_obra_social.config(state="readonly")
            if campo in ["Nombre","Apellido","Obra Social"]:
                entry.config(validate="key", validatecommand=(vcmd_letras, '%S'))
            elif campo in ["Tipo de Documento","DNI"]:
                entry.config(validate="key", validatecommand=(vcmd_numeros, '%S'))
            
            frame_btns = Frame(ventana_abrir, bg="#e4c09f")
            frame_btns.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

            btn_guardar = Button(frame_btns, text="Guardar Cambios", width=15, font=("Roboto", 13), bg="#e6c885",
                                command=lambda: self.guardar_cambios(entradas, ventana_abrir, id_seleccionado))
            btn_guardar.grid(row=len(campos), column=1, padx=10, pady=10)
            btn_guardar.config(state="disabled")  

            btn_editar = Button(frame_btns, text="Modificar", width=15, font=("Roboto", 13), bg="#e6c885",
                                command=lambda: self.activar_edicion(entradas, btn_guardar))
            btn_editar.grid(row=len(campos), column=0, padx=10, pady=10)

            btn_volver = Button(frame_btns, text="Volver", font=("Roboto", 13),bg="#e6c885", width=15,
                            command=ventana_abrir.destroy)
            btn_volver.grid(row=len(campos), column=2, pady=10, padx=10)

        if modo == "modificar":

            frame_btns = Frame(ventana_abrir, bg="#e4c09f")
            frame_btns.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

            btn_volver = Button(frame_btns, text="Volver", font=("Roboto", 13),bg="#e6c885", width=15,
                            command=ventana_abrir.destroy)
            btn_volver.grid(row=len(campos), column=2, pady=10, padx=10)

            btn_guardar = Button(frame_detalles, text="Guardar Cambios", font=("Roboto", 13), bg="#e6c885", width=15,
                                command=lambda: self.guardar_cambios(entradas, ventana_abrir, id_seleccionado))
            btn_guardar.grid(row=len(campos) + 1, column=1, padx=10, pady=10)

    def activar_edicion(self, entradas, btn_guardar):
    # Habilitar la edición en las entradas
        for entry in entradas.values():
            entry.config(state="normal")  # Permitir edición en todos los Entry
        
        # Activar el botón "Guardar Cambios"
        btn_guardar.config(state="normal")  # Activar el botón directamente

    def guardar_cambios(self, entradas, ventana, seleccion):
        nuevos_valores = {campo: entradas[campo].get().upper() for campo in entradas}
        id_paciente = self.tree.item(seleccion, 'values')[0]  # Asumiendo que el ID es el primer valor

        # Convertir el estado a 1 o 0
        estado = 1 if entradas["Estado"].get() == "Activo" else 0

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            # Obtener el ID de la obra social
            cursor.execute("SELECT id_obra_social FROM obra_social WHERE nombre = %s", (nuevos_valores["Obra Social"],))
            result = cursor.fetchone()
            if result is None:
                messagebox.showerror("Error", "La obra social ingresada no existe. Por favor, ingrese una obra social válida.")
                return
            id_obra_social = result[0]

            query = """
            UPDATE paciente
            SET nombre = %s, apellido = %s, tipo_documento= %s, documento = %s, id_obra_social = %s, nro_afiliado = %s, activo = %s
            WHERE id_paciente = %s
            """
            cursor.execute(query, (
                nuevos_valores["Nombre"], nuevos_valores["Apellido"], nuevos_valores["Tipo de Documento"], nuevos_valores["DNI"], id_obra_social,
                nuevos_valores["Número de Afiliado"], estado, id_paciente
            ))
            conexion.commit()

            # Actualizar los valores en el Treeview
            self.tree.item(seleccion, values=(id_paciente, *nuevos_valores.values(), "Activo" if estado == 1 else "Inactivo"))
            
            # Mostrar mensaje de confirmación
            messagebox.showinfo("Información", "Cambios guardados correctamente.")
            
            # Cerrar la ventana después de guardar
            ventana.destroy()

            # Recargar la lista de pacientes para reflejar los cambios en el estado
            self.cargar_paciente()
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
                conexion= obtener_conexion()
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

    def agregar_paciente(self):
        ventana_agregar = Toplevel(self)
        ventana_agregar.title("Agregar Paciente")
        ventana_agregar.config(bg="#e4c09f")
        ventana_agregar.resizable(False,False)
        ventana_agregar.protocol("WM_DELETE_WINDOW", lambda: None)  # Deshabilitar el botón "Cerrar" de la ventana  
        
        frame_agregar = LabelFrame(ventana_agregar, text="Agregar Nuevo Paciente", font= ("Roboto", 11),padx=10, pady=10, bg="#c9c2b2")
        frame_agregar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        frame_btns = Frame(ventana_agregar, bg="#e4c09f")
        frame_btns.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

        campos = ["Nombre","Apellido","Tipo de Documento","DNI","Obra Social","Número de Afiliado"]
        entradas = {}

        vcmd_letras = ventana_agregar.register(self.solo_letras)
        vcmd_numeros = ventana_agregar.register(self.solo_numeros)

                # ComboBox para Obra Social
        etiqueta_obra_social = Label(frame_agregar, text="Obra Socials:", bg="#c9c2b2", font=("Roboto", 10))
        etiqueta_obra_social.grid(row=len(campos), column=0, padx=10, pady=50)
        combo_obra_social = ttk.Combobox(frame_agregar, values= ["OSDE", "Swiss Medical", "Galeno", "Medifé", "Sancor Salud", "Otra"], width=37)
        combo_obra_social.grid(row=len(campos), column=1, padx=10, pady=35)
        combo_obra_social.set("Seleccionar obra social") 
        entradas["Obra Social"] = combo_obra_social

        for i, campo in enumerate(campos):
            etiquetas = Label(frame_agregar, text=campo + ":", bg="#c9c2b2", font=("Roboto", 10))
            etiquetas.grid(row=i, column=0, padx=10, pady=5)
            entry = Entry(frame_agregar, width=40, font=("Roboto", 10))

            if campo in ["Nombre","Apellido","Obra Social"]:
                entry.config(validate="key", validatecommand=(vcmd_letras, '%S'))
            elif campo in ["Tipo de Documento","DNI"]:
                entry.config(validate="key", validatecommand=(vcmd_numeros, '%S'))

            entry.grid(row=i, column=1, padx=10, pady=5)
            entradas[campo] = entry

        btn_nuevo_paciente = Button(frame_btns, text="Agregar", font=("Roboto", 13),bg="#e6c885", width=15, command=lambda: self.guardar_nuevo_paciente(entradas, ventana_agregar))
        btn_nuevo_paciente.grid(row=len(campos),column=0, padx=60, pady=10)

        btn_volver = Button(frame_btns, text="Volver", font=("Roboto", 13),bg="#e6c885", width=15,
                            command=ventana_agregar.destroy)
        btn_volver.grid(row=len(campos), column=1, pady=10, padx=10)

    def guardar_nuevo_paciente(self, entry, ventana):
        nombre = entry["Nombre"].get().upper()      # Obtenemos los valores que el usuario ingresó.
        apellido = entry["Apellido"].get().upper()
        tipo_documento = entry["Tipo de Documento"].get().upper()
        documento = entry["DNI"].get()
        obra_social_nombre = entry["Obra Social"].get().upper()
        numeroafiliado = entry["Número de Afiliado"].get().upper()

        #cursor.execute("SELECT nombre FROM obra_social WHERE id_obra_social = %s", (id_obra_social,))
        #obra_social_nombre = cursor.fetchone()[0]

        # Validar datos y agregar al Treeview
        if nombre and apellido and tipo_documento and documento and obra_social_nombre and numeroafiliado:
            try:
                conexion = obtener_conexion()
                cursor = conexion.cursor()
                
                # Verificar si el DNI ya existe
                cursor.execute("SELECT COUNT(*) FROM paciente WHERE documento = %s", (documento,))
                if cursor.fetchone()[0] > 0:
                    messagebox.showerror("Error", "El DNI ingresado ya existe. Por favor, ingrese un DNI diferente.")
                    return
                
                # Obtener el ID de la obra social
                cursor.execute("SELECT id_obra_social FROM obra_social WHERE nombre = %s", (obra_social_nombre,))
                result = cursor.fetchone()
                if result is None:
                    messagebox.showerror("Error", "La obra social ingresada no existe. Por favor, ingrese una obra social válida.")
                    return
                id_obra_social = result[0]
                
                query = """
                INSERT INTO paciente (nombre, apellido, tipo_documento, documento, id_obra_social, nro_afiliado)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (nombre, apellido, tipo_documento, documento, id_obra_social, numeroafiliado))
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
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            query = """
            SELECT id_paciente, nombre, apellido, documento, id_obra_social 
            FROM paciente 
            WHERE (LOWER(nombre) LIKE %s OR LOWER(apellido) LIKE %s OR documento LIKE %s)
            """
            like_pattern = f"%{busqueda}%"
            cursor.execute(query, (like_pattern, like_pattern, like_pattern))
            pacientes = cursor.fetchall()
            
            self.tree.delete(*self.tree.get_children())
            for paciente in pacientes:
                self.tree.insert("", "end", values=paciente)
                paciente_encontrado = True
            
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
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            query = """
            SELECT p.id_paciente, p.nombre, p.apellido, p.documento, o.nombre as obra_social 
            FROM paciente p
            JOIN obra_social o ON p.id_obra_social = o.id_obra_social
            WHERE p.activo = 1
            """
            cursor.execute(query)
            pacientes = cursor.fetchall()
            self.tree.delete(*self.tree.get_children())  # Limpiar el Treeview antes de cargar los datos
            for paciente in pacientes:
                self.tree.insert("", "end", values=paciente)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al cargar los pacientes: {err}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

'''ventana = Tk()
ventana.title("Gestion de Paciente")
ventana.resizable(False,False)
ventana.geometry("+0+0")
ventana.protocol("WM_DELETE_WINDOW", lambda: None)
root = GestionPaciente(ventana)
ventana.mainloop()'''