from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
from ConexionBD import *
from tkcalendar import Calendar
from datetime import datetime
import re

class Gestion_Ficha(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg="#e4c09f", width= 1370, height=700)
        self.master = master
        self.pack_propagate(False)
        self.pack(expand=True)
        self.createWidgets()
        self.actualizar_treeview()
        self.ventana_agregar_medico = None
        self.ventana_agregar_paciente = None
        self.master.protocol("WM_DELETE_WINDOW", lambda: None)

    #Funcion para volver al menú principal
    def volver_menu_principal(self):
        from Menu import MENU
        self.master.destroy()
        ventana = Tk()
        ventana.wm_title("Menú Recupero de Obra Social")
        ventana.wm_resizable(0,0)
        ventana.geometry("+0+0")
        menu = MENU(ventana)
        menu.mainloop()
    def volver_inicio(self):
        self.ventana_agregar.destroy()
        self.master.deiconify()

    #VALIDACIONES
    def solo_letras_numeros(self, char):
        if not char:
            return True
        return bool(re.match(r'[a-zA-Z0-9 ]', char))
    # Función para verificar si una ficha ya existe
    def ficha_duplicada(self, id_paciente, id_medico, fecha, tratamientos):
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            # Verificar si ya existe una ficha con los mismos datos de paciente, médico y fecha
            sql = "SELECT id_ficha FROM ficha WHERE id_paciente = %s AND id_medico = %s AND fecha = %s"
            cursor.execute(sql, (id_paciente, id_medico, fecha))
            ficha_existente = cursor.fetchone()
            
            if ficha_existente:
                id_ficha_existente = ficha_existente[0]
                # Verificar si los tratamientos son los mismos
                sql = "SELECT id_tratamiento, cantidad FROM detalle_ficha WHERE id_ficha = %s"
                cursor.execute(sql, (id_ficha_existente,))
                tratamientos_existentes = cursor.fetchall()
                
                if len(tratamientos) != len(tratamientos_existentes):
                    return False
                
                for tratamiento in tratamientos:
                    if tratamiento not in tratamientos_existentes:
                        return False
                
                return True
            return False
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se pudo verificar la ficha duplicada: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()
    #CONEXIONES CON BASE DE DATOS
    #recupera obras sociales utilizando id
    def conexion_bd_os(self, id):
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM obra_social WHERE id_obra_social = %s", (id,))
            obra_social = cursor.fetchall()
            return obra_social
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se pudo recuperar la obra social: {error}")
        finally:
            cursor.close()
            conexion.close()
    #Funciones para buscar un elemento en la base de datos
    def buscar_elemento_tabla(self, elemento, tabla):
        conexion = obtener_conexion()  # Llama a la función que establece la conexión
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return
        try:
            cursor = conexion.cursor()
            if tabla == "paciente":
                sentencia = "SELECT COUNT(*) from paciente WHERE documento = %s"
            elif tabla == "medico":
                sentencia = "SELECT COUNT(*) from medico WHERE matricula = %s"
            else:
                messagebox.showerror("Error", "No se pudo realizar la consulta a la base de datos. Error 1")
            cursor.execute(sentencia, (elemento,))
            resultado = cursor.fetchall()
            cursor.close()
            conexion.close()
            return resultado[0]
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Consulta", f"No se pudo realizar la consulta a la base de datos: {err}. Error 2")
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return
    #busca un elemento en la base de datos
    def obtener_unico(self, elemento, tabla):
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            if tabla == "paciente":
                cursor.execute("SELECT * FROM paciente WHERE documento = %s", (elemento,))
            elif tabla == "medico":
                cursor.execute("SELECT * FROM medico WHERE matricula = %s", (elemento,))
            else:
                messagebox.showerror("Error", "No se pudo realizar la consulta a la base de datos. Error 3")
            resultado = cursor.fetchall()
            if resultado is None:
                messagebox.showwarning("Advertencia", f"No se encontró ningún {tabla} con ese dato. Error 4")
            return resultado[0]
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se pudo recuperar el {tabla}: {error}. Error 5")
        finally:
            cursor.close()
            conexion.close()
    #Recupera datos de paciente, obra social y médico utilizando el ID
    def recuperar_paciente(self, id):
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre, apellido, documento, nro_afiliado FROM paciente WHERE id_paciente = %s", (id,))
            paciente = cursor.fetchone()
            if paciente:
                return paciente
            else:
                raise ValueError("Paciente no encontrado")
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se pudo recuperar el paciente: {error}")
        finally:
            cursor.close()
            conexion.close()
    def recuperar_obra_social(self,id):
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre FROM obra_social WHERE id_obra_social = %s", (id,))
            obra_social = cursor.fetchone()
            if obra_social:
                nombre_obra_social = ''.join(obra_social[0])  # Unir los caracteres en una cadena
                return nombre_obra_social
            else:
                messagebox.showwarning("Advertencia", "No se encontró la obra social.")
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se pudo recuperar la obra social: {error}")
        finally:
            cursor.close()
            conexion.close()
    def recuperar_medico(self, id):
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre, apellido, matricula FROM medico WHERE id_medico = %s", (id,))
            medico = cursor.fetchall()
            return medico
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se pudo recuperar el médico: {error}")
        finally:
            cursor.close()
            conexion.close()
    #Funciones para ver/modificar ficha
    def obtener_ficha_por_id(self, id_ficha):
        conexion = obtener_conexion()
        try:
            sql = "SELECT * FROM ficha WHERE id_ficha = %s"
            cursor = conexion.cursor()
            cursor.execute(sql, (id_ficha,))
            ficha = cursor.fetchone()
            if ficha is None:
                messagebox.showwarning("Advertencia", "No se encontró ningúna ficha con ese ID.")
            return ficha
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se pudo recuperar la ficha: {error}")
        finally:
            cursor.close()
            conexion.close()
    def buscar_ids(self, tabla, elemento):
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            if tabla == "paciente":
                sql = "SELECT id_paciente FROM paciente WHERE documento = %s"
            elif tabla == "obra_social":
                sql = "SELECT id_obra_social FROM obra_social WHERE nombre = %s"
            elif tabla == "medico":
                sql = "SELECT id_medico FROM medico WHERE matricula = %s"
            else:
                messagebox.showerror("Error", "Tabla no encontrada.")
                return
            cursor.execute(sql, (elemento,))
            id_elemento = cursor.fetchone()
            cursor.close()
            conexion.close()
            return id_elemento
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se pudo recuperar el ID: {error}")
            return
    #Se buscan los detalles_ficha que contengas en id de la ficha, y se recolectan los datos de los tratamientos de cada detalle.
    def ingresar_tratamientos_ver_ficha(self, id_ficha):
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            sql = "SELECT * FROM detalle_ficha WHERE id_ficha = %s"
            cursor.execute(sql, (id_ficha,))
            tratamientos = cursor.fetchall()
            for tratamiento in tratamientos:
                sql = "SELECT * FROM tratamiento WHERE id_tratamiento = %s"
                cursor.execute(sql, (tratamiento[2],))
                tratamiento_completo = cursor.fetchone()
                self.arbol_ficha.insert("", "end", iid=tratamiento_completo[0], values=(tratamiento_completo[1], tratamiento_completo[2], tratamiento[4], tratamiento[3]))
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se pudo recuperar los tratamientos: {error}")
        finally:
            cursor.close()
            conexion.close()
    
    #FUNCIONES QUE SE UTILIZAN
    #limpair todos los campos en la ficha
    def limpiar_campos(self):
        # Limpiar los campos de datos del paciente
        for campo in self.frame_datos_pacientes.winfo_children():
            if isinstance(campo, Entry):
                campo.config(state="normal")
                campo.delete(0, END)
                campo.config(state="readonly")
        
        # Limpiar los campos de datos del médico
        for campo in self.frame_datos_medico.winfo_children():
            if isinstance(campo, Entry):
                campo.config(state="normal")
                campo.delete(0, END)
                campo.config(state="readonly")
        
        # Limpiar el campo de fecha
        self.entry_fecha.config(state="normal")
        self.entry_fecha.delete(0, END)
        self.entry_fecha.config(state="readonly")
        
        # Limpiar el Treeview de tratamientos
        for item in self.arbol_ficha.get_children():
            self.arbol_ficha.delete(item)
        
        # Resetear el total
        self.total_var.set("")
    #coloca valores en los entrys de busqueda para que el usuario sepa que hacer
    def limpiar_marcador(self, entry):
        if entry.get() == "DOCUMENTO" or entry.get() == "MATRÍCULA":
            entry.delete(0, "end")
            entry.config(fg="black")
    def restaurar_marcador(self,entry):
        if not entry.get():
            if entry == self.buscar_paciente:
                entry.insert(0, "DOCUMENTO")
            elif entry == self.buscar_medico:
                entry.insert(0, "MATRÍCULA")
            elif entry == self.buscar_tratamiento:
                entry.insert(0, "CÓDIGO")
            entry.config(fg="gray")
    #Funciones para validar y agregar fecha
    def abrir_calendario(self):
        ventana_calendario = Toplevel(self)
        ventana_calendario.config(bg="#e4c09f")
        ventana_calendario.geometry("300x270+1000+200")
        ventana_calendario.resizable(0, 0)
        ventana_calendario.grab_set()  # Bloquear interacción con la ventana principal
        ventana_calendario.title("Fecha de la consulta")
        ventana_calendario.protocol("WM_DELETE_WINDOW", lambda: None)

        # Obtener la fecha actual
        fecha_actual = datetime.today().date()
        anio = fecha_actual.year
        mes = fecha_actual.month
        dia = fecha_actual.day

        # Configurar el calendario con la fecha actual
        calendario = Calendar(ventana_calendario, selectmode="day", year=anio, month=mes, day=dia)
        calendario.pack(pady=20)

        # Función para confirmar la selección de fecha y aplicar el formato deseado
        def confirmar_fecha():
            try:
                fecha_seleccionada = calendario.get_date()
                # Convertir la fecha seleccionada al formato deseado
                fecha_formateada = datetime.strptime(fecha_seleccionada, "%m/%d/%y").strftime("%Y/%m/%d")  # Formato año/mes/día
                fecha_actual_formateada = fecha_actual.strftime("%Y/%m/%d")
                if fecha_actual_formateada < fecha_formateada:
                    messagebox.showwarning("Advertencia", "Seleccione una fecha anterior a la actual.")
                    return
                else:
                    self.entry_fecha.config(state="normal")
                    self.entry_fecha.delete(0, END)  
                    self.entry_fecha.insert(0, fecha_formateada)
                    self.entry_fecha.config(state="readonly") 
                    ventana_calendario.destroy()
            except ValueError:
                messagebox.showwarning("Advertencia", "Seleccione una fecha válida.")
                return

        cont_botones = Frame(ventana_calendario, bg="#e4c09f")
        cont_botones.pack()

        # Botón para confirmar la fecha seleccionada
        boton_confirmar = Button(cont_botones, text="Confirmar", command=confirmar_fecha, width=10, font=("Robot", 13), bg="#e6c885")
        boton_confirmar.grid(row = 0, column=0, padx=10, pady=10)

        boton_volver = Button(cont_botones, text="Volver", command=ventana_calendario.destroy, width=10, font=("Robot", 13), bg="#e6c885")
        boton_volver.grid(row = 0, column=1, padx=10, pady=10)
    #Funcion que muestra una lista con los tratamientos activos y permite agregarlos a la ficha, con su cantidad
    def mostrar_tratamientos(self):
        def buscar_tratamiento():
            busqueda = self.entrada_buscar.get().strip().upper()
            if not busqueda:
                self.tree_tratamiento.delete(*self.tree_tratamiento.get_children())
                self.actualizar_treeview_tratamiento()
                return
            tratamiento_encontrado = False

            for item in self.tree_tratamiento.get_children():
                valores = self.tree_tratamiento.item(item, 'values')
                codigo = valores[0].upper()
                nombre = valores[1].upper()

                if busqueda in codigo or busqueda in nombre:
                    tratamiento_encontrado = True
                else:
                    self.tree_tratamiento.delete(item)

            if not tratamiento_encontrado:
                messagebox.showwarning("Atención", "No se encontró el tratamiento.")
                self.tree_tratamiento.delete(*self.tree_tratamiento.get_children())
                self.ventana_tratamientos.lift()
                self.actualizar_treeview_tratamiento()
                self.entrada_buscar.delete(0, END)

        self.ventana_tratamientos = Toplevel()
        self.ventana_tratamientos.title("Tratamientos")
        self.ventana_tratamientos.geometry("650x430+700+180")
        self.ventana_tratamientos.config(bg="#e4c09f")

        #Buscar tratamiento por nombre, codigo
        frame_busqueda = Frame(self.ventana_tratamientos, bg="#e4c09f")
        frame_busqueda.pack(pady=10)

        #Widgets de búsqueda dentro del frame más chico
        etiqueta_buscar = Label(frame_busqueda, text="Buscar:", bg="#e4c09f",font=("Robot",11))
        etiqueta_buscar.grid(row=1, column=1, padx=5, pady=5)

        self.entrada_buscar = Entry(frame_busqueda,width="40",font=("Robot",10))
        self.entrada_buscar.grid(row=1, column=2, padx=5, pady=5)

        img_buscar = Image.open("buscar1.png").resize((25, 25), Image.Resampling.LANCZOS)
        img_buscar = ImageTk.PhotoImage(img_buscar)
        btn_buscar = Button(frame_busqueda, image=img_buscar, width=25, height=25,bg="#e6c885",command= buscar_tratamiento)
        
        btn_buscar.grid(row=1, column=3)
        btn_buscar.image = img_buscar

        frame_tabla = Frame(self.ventana_tratamientos, bg="#c9c2b2", width= 1000)  # Frame para contener la tabla y el scrollbar
        frame_tabla.pack(expand=True, fill= "x")

        # Crear el Treeview para ver los tratamientos
        stilo = ttk.Style()
        stilo.configure("Custom.Treeview", font=("Robot",10), rowheight=21)  # Cambia la fuente y el alto de las filas
        stilo.configure("Custom.Treeview.Heading", font=("Robot",11), padding= [0, 5])  # Cambia la fuente de las cabeceras

        self.tree_tratamiento = ttk.Treeview(frame_tabla, columns=("Nombre", "Código", "Precio"), show='headings', style="Custom.Treeview")
        self.tree_tratamiento.heading("Nombre", text="Nombre")
        self.tree_tratamiento.heading("Código", text="Código")
        self.tree_tratamiento.heading("Precio", text="Precio")

        self.tree_tratamiento.column("Nombre", anchor='center', width=330, stretch=False)
        self.tree_tratamiento.column("Código", anchor='center', width=150, stretch=False)
        self.tree_tratamiento.column("Precio", anchor='center', width=150, stretch=False)
        self.tree_tratamiento.grid(row=0, column=0, sticky="nsew")

        #Scrollbar para la tabla dentro del frame_tabla
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree_tratamiento.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')  #Se expande desde arriba hacia abajo
        self.tree_tratamiento.configure(yscrollcommand=scrollbar.set)

        self.actualizar_treeview_tratamiento()

        self.cantidad_var = ttk.Combobox(self.ventana_tratamientos, font=("Robot",12), values=[str(i) for i in range(1, 10)], state="readonly", width=13, height=6)
        self.cantidad_var.pack()
        self.cantidad_var.current(0)

        # Crear el frame para los botones
        frame_botones = Frame(self.ventana_tratamientos, bg="#e4c09f")
        frame_botones.pack(pady=15)

        # Botón Agregar
        btn_agregar = Button(frame_botones, text="Agregar", font=("Robot", 13), bg="#e6c885", height=1, width=12, command= self.agregar_tratamiento_a_ficha)
        btn_agregar.grid(row=0, column=0, padx=13, pady=15)

        # Botón Volver
        btn_volver = Button(frame_botones, text="Volver", font=("Robot", 13), bg="#e6c885", height=1, width=12, command=self.ventana_tratamientos.destroy)
        btn_volver.grid(row=0, column=1, padx=13, pady=15)
    
    #actualiza los cuadros de las fichas y de los tratamientos
    def actualizar_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        seleccion = self.combo_activos.get()
        if seleccion == "Activos":
            cursor.execute("SELECT * FROM ficha where activo = 1")
        elif seleccion == "Inactivos":
            cursor.execute("SELECT * FROM ficha where activo = 0")
        elif seleccion == "Todos":
            cursor.execute("SELECT * FROM ficha")
        lista = cursor.fetchall()
        for ficha in lista:
            datos_paciente = list(self.recuperar_paciente(ficha[1]))
            datos_obra_social = self.recuperar_obra_social(ficha[2])
            self.tree.insert("", "0", iid=ficha[0], values= (datos_paciente[2], datos_paciente[0], datos_paciente[1], datos_obra_social, ficha[5], ficha[6]))
        cursor.close()
        conexion.close()
    def actualizar_treeview_tratamiento(self):
        for item in self.tree_tratamiento.get_children():
            self.tree_tratamiento.delete(item)
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT id_tratamiento, nombre, codigo, precio FROM tratamiento where activo = 1")
        tratamientos = cursor.fetchall()
        # Insertar los datos en el Treeview
        for tratamiento in tratamientos:
            self.tree_tratamiento.insert("", "end", iid= tratamiento[0] ,values=tratamiento[1:])
        cursor.close()
        conexion.close()
    
    #CREACION DE INTERFAZ Y MODIFICACIONES EN LA BASE DE DATOS
    #Función para generar el inicio
    def createWidgets(self):
        frame_fichas = LabelFrame(self, text="Gestión de Fichas", bg="#c9c2b2", height=800, width=1280)
        frame_fichas.pack_propagate(False)
        frame_fichas.pack(expand=True, pady=8)

        #primer frame, contiene la imagen y el titulo de la ventana
        contenedor_titulo = Frame(frame_fichas, bg="#c9c2b2")
        contenedor_titulo.pack(pady= 5)
        #Carga la imagen de fondo
        img_fondo = Image.open("fondo3.png")
        img_fondo = img_fondo.resize((1120, 180), Image.Resampling.LANCZOS)
        self.img_fondo = ImageTk.PhotoImage(img_fondo)
        #Label para la imagen de fondo
        fondo_label = Label(contenedor_titulo, image=self.img_fondo)
        fondo_label.pack(expand=True, fill="both")

        #segundo frame, contiene el buscador y el boton de agregar
        #buscador de fichas
        frame_busqueda = Frame(frame_fichas, bg="#c9c2b2")
        frame_busqueda.pack(padx = 30, fill="x")
        #separa el campo de busqueda del botón
        frame_busqueda.columnconfigure(4, weight=1)

        #Widgets de búsqueda dentro del frame más chico
        Label(frame_busqueda, text="Buscar:", bg="#c9c2b2",font=("Robot",15)).grid(row=1, column=0, padx=5, pady=2, sticky= W)

        self.entrada_buscar = Entry(frame_busqueda,width="40",font=("Robot",13))
        self.entrada_buscar.grid(row=1, column=1, padx=5, pady=2, sticky= W)

        img_buscar = Image.open("buscar1.png").resize((30, 30), Image.Resampling.LANCZOS)
        img_buscar = ImageTk.PhotoImage(img_buscar)
        btn_buscar = Button(frame_busqueda, image=img_buscar, width=40, height=30,bg="#e6c885", command= self.buscar_ficha)
        btn_buscar.grid(row=1, column=2, sticky= W)
        btn_buscar.image = img_buscar

        style = ttk.Style()
        style.theme_use("default")
        style.map("Custom.TCombobox",  fieldbackground=[("active", "white")],   # Fondo blanco en modo de solo lectura
                                        background=[("active", "white")],          # Fondo blanco al desplegar el menú
                                        selectbackground=[("focus", "white")],     # Fondo blanco cuando una opción está seleccionada
                                        selectforeground=[("focus", "black")])    # Text
        self.combo_activos = ttk.Combobox(frame_busqueda, width=10, font=("Robot", 13), state="readonly", style="Custom.TCombobox")
        self.combo_activos['values'] = ("Activos", "Inactivos", "Todos")
        self.combo_activos.set("Activos")
        self.combo_activos.grid(row=1, column=3, padx=10, pady=3)
        self.combo_activos.bind("<<ComboboxSelected>>", lambda event: self.actualizar_treeview())

        boton_agregar = Button(frame_busqueda, text="Agregar  +", width=15, bg="#e6c885",font=("Robot",15), command=self.agregar_ficha)
        boton_agregar.grid(row=1, column=5, padx=10, pady=3, sticky= E)
        #Para que siempre esté atrás de los widgets
        fondo_label.lower()

        #Tercer frame, contiene la tabla de fichas
        #Frame para el Treeview y el scrollbar
        frame_tabla = Frame(frame_fichas, bg="#c9c2b2", width= 1000)  # Frame para contener la tabla y el scrollbar
        frame_tabla.pack(expand=True, fill= "x", padx= 30)
        
        stilo = ttk.Style()
        stilo.configure("Inicio.Treeview", font=("Robot",11), rowheight=21)  # Cambia la fuente y el alto de las filas
        stilo.configure("Inicio.Treeview.Heading", font=("Robot",14), padding= [0, 5])  # Cambia la fuente de las cabeceras
        
        #Treeview para mostrar la tabla de tratamientos dentro del frame_tabla
        self.tree = ttk.Treeview(frame_tabla, columns=("Documento", "Nombre" ,"Apellido", "Obra Social", "Fecha prestación", "Total"), show='headings', height=15, style = "Inicio.Treeview")
        self.tree.grid(row=0, column=0, sticky="nsew")

        #Títulos de columnas
        self.tree.heading("Documento", text="Documento")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("Obra Social", text="Obra Social")
        self.tree.heading("Fecha prestación", text="Fecha prestación")
        self.tree.heading("Total", text="Total")

        #Ancho de las columnas y datos centrados
        self.tree.column("Documento", anchor='center', width=130)
        self.tree.column("Nombre", anchor='center', width=230)
        self.tree.column("Apellido", anchor='center', width=230)
        self.tree.column("Obra Social", anchor='center', width=300)
        self.tree.column("Fecha prestación", anchor='center', width=160)
        self.tree.column("Total", anchor='center', width=150)
        
        #Scrollbar para la tabla dentro del frame_tabla
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')  #Se expande desde arriba hacia abajo
        self.tree.configure(yscrollcommand=scrollbar.set)

        #Cuarto frame, contiene los botones de ver, modificar y eliminar
        frame_btn = Frame(frame_fichas, bg= "#c9c2b2")
        frame_btn.pack(ipady= 10)

        #Botones(ver, modificar, eliminar)
        btn_ver = Button(frame_btn, text="Ver", width=15, font=("Robot",15),bg="#e6c885", command= self.ver_ficha)
        btn_ver.grid(row=0, column=1,padx=50)

        btn_editar = Button(frame_btn, text="Modificar", width=15, font=("Robot",15),bg="#e6c885", command= self.modificar_ficha)
        btn_editar.grid(row=0, column=2,padx=50)
        
        btn_eliminar = Button(frame_btn, text="Eliminar", width=15,font=("Robot",15),bg="#e6c885", command= self.eliminar_ficha)
        btn_eliminar.grid(row=0, column=3, padx=50)

        btn_volver = Button(frame_btn, text="Volver", width=15 ,font=("Robot",15), bg="#e6c885", command = self.volver_menu_principal)
        btn_volver.grid(row=0, column=4, padx=50)

    #AGREGAR NUEVA FICHA 
    def agregar_ficha(self):
        self.master.withdraw()        
        self.ventana_agregar = Toplevel(self.master)
        self.ventana_agregar.title("Agregar ficha")
        self.ventana_agregar.config(bg="#e4c09f") 
        self.ventana_agregar.resizable(False,False)
        self.ventana_agregar.geometry("1370x700+0+0")
        self.ventana_agregar.protocol("WM_DELETE_WINDOW", lambda: None)

        validar_letynum = self.ventana_agregar.register(self.solo_letras_numeros)

        frame_agregar = LabelFrame(self.ventana_agregar, text="Agregar ficha", font= ("Robot", 12),padx=10, pady=10, bg="#c9c2b2")
        frame_agregar.pack(padx=10, pady=5)
        self.datos_ficha = {} #Diccionario para guardar los datos de la ficha

        #FRAME DE DATOS DEL PACIENTE
        frame_paciente = LabelFrame(frame_agregar, text="Datos del paciente", font=("Robot", 10), padx=10, pady=5, bg="#c9c2b2")
        frame_paciente.pack(fill="x")
        #buscador de pacientes
        frame_busqueda = Frame(frame_paciente, bg="#c9c2b2")
        frame_busqueda.pack(fill="x", pady=5)
        Label(frame_busqueda, text="Buscar:", bg="#c9c2b2",font=("Robot", 13)).grid(row=0, column=1, padx=5, pady=2, sticky= W)
        self.buscar_paciente = Entry(frame_busqueda, width=20,font=("Robot",12))
        self.buscar_paciente.grid(row=0, column=2, padx=5, pady=2, sticky= W)
        self.buscar_paciente.config(validate="key", validatecommand=(validar_letynum, '%S'))
        self.buscar_paciente.insert(0, "DOCUMENTO")  #Agrega marcador de posición
        self.buscar_paciente.config(fg="gray")
        self.buscar_paciente.bind("<FocusIn>", lambda event, e=self.buscar_paciente: self.limpiar_marcador(e))
        self.buscar_paciente.bind("<FocusOut>", lambda event, e=self.buscar_paciente: self.restaurar_marcador(e))
        img_buscar = Image.open("buscar1.png").resize((20, 20), Image.Resampling.LANCZOS)
        img_buscar = ImageTk.PhotoImage(img_buscar)
        btn_buscar = Button(frame_busqueda, image=img_buscar, width=25, height=25,bg="#e6c885", command=lambda: self.buscar_elemento("paciente"))
        btn_buscar.grid(row=0, column=3, sticky= W)
        btn_buscar.image = img_buscar

        frame_busqueda.columnconfigure(4, weight=2)
        frame_busqueda.columnconfigure(5, weight=2)

        btn_nuevo_paciente = Button(frame_busqueda, text="Nuevo Paciente", font=("Robot", 11, "bold"),bg="#e6c885", width = 15, command = self.agregar_paciente)
        btn_nuevo_paciente.grid(row = 0, column=6, padx=15)

        #Frame para los datos del PACIENTE
        self.frame_datos_pacientes = Frame(frame_paciente, bg="#c9c2b2")
        self.frame_datos_pacientes.pack(pady=5)

        campos_arriba = ["Nombre", "Apellido", "Documento"]
        campos_abajo = ["Obra Social", "Número de Afiliado"]
        for i, campos_arriba in enumerate(campos_arriba):
            Label(self.frame_datos_pacientes, text=campos_arriba + ":", bg="#c9c2b2", font=("Robot", 12), justify=LEFT).grid(row=0, column=i, padx=10, sticky=W)
            entry = Entry(self.frame_datos_pacientes, width=40, font=("Robot", 12))
            entry.grid(row=1, column=i, padx=10)
            entry.config(state="readonly")
        for j, campos_abajo in enumerate(campos_abajo):
            Label(self.frame_datos_pacientes, text=campos_abajo + ":", bg="#c9c2b2", font=("Robot", 12), justify=LEFT).grid(row=2, column=j, padx=10, sticky=W)
            entry = Entry(self.frame_datos_pacientes, width=40, font=("Robot", 12))
            entry.grid(row=3, column=j, padx=10)
            entry.config(state="readonly")

        #Frame para los datos del MEDICO
        frame_medico = LabelFrame(frame_agregar, text="Datos de la consulta", font=("Robot", 10), bg="#c9c2b2")
        frame_medico.pack(fill="x")

        #buscador de médico
        frame_busqueda_medico = Frame(frame_medico, bg="#c9c2b2")
        frame_busqueda_medico.pack(fill="x", pady=5, padx=8)

        Label(frame_busqueda_medico, text="Buscar:", bg="#c9c2b2",font=("Robot", 13)).grid(row=0, column=1, padx=5, pady=2, sticky= W)
        self.buscar_medico = Entry(frame_busqueda_medico, width=20,font=("Robot",12))
        self.buscar_medico.grid(row=0, column=2, padx=5, pady=2, sticky= W)
        self.buscar_medico.config(validate="key", validatecommand=(validar_letynum, '%S'))
        self.buscar_medico.insert(0, "MATRÍCULA")  #Agrega marcador de posición
        self.buscar_medico.config(fg="gray")
        self.buscar_medico.bind("<FocusIn>", lambda event, e=self.buscar_medico: self.limpiar_marcador(e))
        self.buscar_medico.bind("<FocusOut>", lambda event, e=self.buscar_medico: self.restaurar_marcador(e))
        img_buscar = Image.open("buscar1.png").resize((20, 20), Image.Resampling.LANCZOS)
        img_buscar = ImageTk.PhotoImage(img_buscar)
        btn_buscar = Button(frame_busqueda_medico, image=img_buscar, width=25, height=25,bg="#e6c885", command=lambda: self.buscar_elemento("medico"))
        btn_buscar.grid(row=0, column=3, sticky= W)
        btn_buscar.image = img_buscar

        frame_busqueda_medico.columnconfigure(4, weight=2)
        frame_busqueda_medico.columnconfigure(5, weight=2)

        btn_nuevo_medico = Button(frame_busqueda_medico, text="Nuevo Médico", font=("Robot", 11, "bold"),bg="#e6c885", width = 15, command= self.agregar_medico)
        btn_nuevo_medico.grid(row = 0, column=6, padx=15)

        frame_campos_medyfecha = Frame(frame_medico, bg="#c9c2b2")
        frame_campos_medyfecha.pack(fill="x", pady=5, padx=8)   

        #Frame para los datos del medico
        self.frame_datos_medico = Frame(frame_campos_medyfecha, bg="#c9c2b2")
        self.frame_datos_medico.grid(row = 0, column = 0, pady=5)

        campos_medico = ["Nombre del médico", "Apellido del médico", "Matrícula"]
        for m, campo in enumerate(campos_medico):
            Label(self.frame_datos_medico, text=campo + ":", bg="#c9c2b2", font=("Robot", 12), justify=LEFT).grid(row=0, column=m, padx=8, sticky=W)
            entry = Entry(self.frame_datos_medico, width=28, font=("Robot", 12))
            entry.grid(row=1, column=m, padx=10)
            entry.config(state="readonly")
        
        self.fecha= Frame(frame_campos_medyfecha, bg="#c9c2b2")
        self.fecha.grid(row=0, column=1, padx=8, sticky=W)

        Label(self.fecha, text="Fecha de consulta" + ":", bg="#c9c2b2", font=("Robot", 12), justify=LEFT).pack(anchor=W, padx=8)
        self.entry_fecha = Entry(self.fecha, width=20, font=("Robot", 12))
        self.entry_fecha.pack(anchor=W, padx=10)
        self.entry_fecha.config(state="readonly")
        self.entry_fecha.bind("<Button-1>", lambda e: self.abrir_calendario())

        #Frame para los datos del TRATAMIENTOS
        frame_tratamiento = LabelFrame(frame_agregar, text="Tratamiento", font=("Robot", 10), bg="#c9c2b2") 
        frame_tratamiento.pack(fill="x")

        campos_tratamiento = ["Código", "Nombre del procedimiento", "Precio"]

        #Tabla para mostar los tratamientos
        frame_tabla_tratamientos = Frame(frame_tratamiento, bg="#c9c2b2", width= 500)  # Frame para contener la tabla y el scrollbar
        frame_tabla_tratamientos.grid(row= 0, column=0, padx= 55, pady= 5)

        Label(frame_tabla_tratamientos, text="Tratamientos aplicados", font=("Robot", 12), bg="#c9c2b2").pack(pady=5)
        
        estilo = ttk.Style()
        estilo.configure("Treeview", font=("Robot",10), rowheight=16)  # Cambia la fuente y el alto de las filas
        estilo.configure("Treeview.Heading", font=("Robot",12), padding= [0, 8])  # Cambia la fuente de las cabeceras
        
        #Treeview para mostrar la tabla de tratamientos dentro del frame_tabla
        self.arbol_ficha = ttk.Treeview(frame_tabla_tratamientos, columns=("Código", "Nombre", "Precio", "Cantidad"), show='headings', height=11, style = "Treeview")
        self.arbol_ficha.pack(expand=True, fill="both")

        #Títulos de columnas
        self.arbol_ficha.heading("Código", text="Código")
        self.arbol_ficha.heading("Nombre", text="Nombre")
        self.arbol_ficha.heading("Precio", text="Precio")
        self.arbol_ficha.heading("Cantidad", text="Cantidad")

        #Ancho de las columnas y datos centrados
        self.arbol_ficha.column("Código", anchor='center', width=150, stretch=False)
        self.arbol_ficha.column("Nombre", anchor='center', width=300, stretch=False)
        self.arbol_ficha.column("Precio", anchor='center', width=200, stretch=False)
        self.arbol_ficha.column("Cantidad", anchor='center', width=100, stretch=False)

        #Frame para los botones de agregar y eliminar tratamientos
        frame_botones_tratamiento = Frame(frame_tratamiento, bg="#c9c2b2")
        frame_botones_tratamiento.grid(row=0, column=1, columnspan=2, padx=30)

        """btn_nuevo_t = Button(frame_botones_tratamiento, text="Nuevo Tratamiento", font=("Robot", 11, "bold"),bg="#e6c885", height=2, width=20)
        btn_nuevo_t.pack(pady=8)"""

        btn_agregar_t = Button(frame_botones_tratamiento, text="Agregar Tratamiento", font=("Robot", 11, "bold"),bg="#e6c885", height=2, width=20, command= self.mostrar_tratamientos)
        btn_agregar_t.pack(pady=8)

        btn_eliminar_t = Button(frame_botones_tratamiento, text="Eliminar Tratamiento", font=("Robot", 11, "bold"),bg="#e6c885", height=2, width=20, command= self.eliminar_tratamiento_a_ficha)
        btn_eliminar_t.pack(pady=8)

        self.total_var = StringVar()
        self.entry_total = Entry(frame_botones_tratamiento, textvariable=self.total_var, font=("Robot", 15), state='readonly', width=10)
        self.entry_total.pack(pady=8)

        #Frame botones
        frame_botones = Frame(self.ventana_agregar, bg="#e4c09f")
        frame_botones.pack()

        btn_guardar_ficha = Button(frame_botones, text="Guardar", font=("Robot", 15),bg="#e6c885", width= 15, command= lambda: self.guardar_nueva_ficha(self.datos_ficha, self.ventana_agregar))
        btn_guardar_ficha.grid(row = 0, column=0, columnspan=2, padx=20, pady=10)

        btn_limpiar = Button(frame_botones, text="Limpiar", font=("Robot", 15),bg="#e6c885", width=15, command= self.limpiar_campos)
        btn_limpiar.grid(row = 0, column=2, columnspan=2, padx=20, pady=10)
        
        btn_volver = Button(frame_botones, text="Volver", font=("Robot", 15),bg="#e6c885", width=15, command= self.volver_inicio)
        btn_volver.grid(row = 0, column=4, columnspan=2, padx=20, pady=10)
    #completa las entradas en la ficha al buscar el elemento
    def buscar_elemento(self, tabla):
        if tabla == "paciente":
            elemento = self.buscar_paciente.get()
            if not elemento:
                messagebox.showwarning("Atención", "Ingrese un Documento para buscar.")
                self.lift()
                return
            if not elemento.isdigit():
                messagebox.showwarning("Atención", "Ingrese un Documento válido.")
                self.lift()
                return
            resultado = self.buscar_elemento_tabla(elemento, "paciente")
            if resultado[0] == 0:
                messagebox.showwarning("Atención", "No se encontró ningún paciente con ese Documento.")
                ventana.lift()
                return
            elif resultado[0] == 1:
                valores = self.obtener_unico(elemento, "paciente")
                campos_arriba = ["Nombre", "Apellido", "Documento"]
                campos_abajo = ["Obra Social", "Número de Afiliado"]
                self.datos_ficha["Id_paciente"] = valores[0]
                for i, campos_arriba in enumerate(campos_arriba):
                    Label(self.frame_datos_pacientes, text=campos_arriba + ":", bg="#c9c2b2", font=("Robot", 12), justify=LEFT).grid(row=0, column=i, padx=10, sticky=W)
                    entry = Entry(self.frame_datos_pacientes, width=40, font=("Robot", 12))
                    entry.grid(row=1, column=i, padx=10)
                    if campos_arriba == "Documento":
                        entry.insert(0, valores[3])
                    elif campos_arriba == "Nombre":
                        entry.insert(0, valores[1])
                    elif campos_arriba == "Apellido":
                        entry.insert(0, valores[2])
                    entry.config(state="readonly")
                    self.datos_ficha[campos_arriba] = entry  # Guarda la entrada en un diccionario
                for j, campos_abajo in enumerate(campos_abajo):
                    Label(self.frame_datos_pacientes, text=campos_abajo + ":", bg="#c9c2b2", font=("Robot", 12), justify=LEFT).grid(row=2, column=j, padx=10, sticky=W)
                    entry = Entry(self.frame_datos_pacientes, width=40, font=("Robot", 12))
                    entry.grid(row=3, column=j, padx=10)
                    if campos_abajo == "Obra Social":
                        nombre = self.conexion_bd_os(valores[4])
                        entry.insert(0, nombre[0][1])
                        self.datos_ficha[campos_abajo] = valores[4]  #guarda el id de la obra social
                    elif campos_abajo == "Número de Afiliado":
                        entry.insert(0, valores[5])
                        self.datos_ficha[campos_abajo] = entry      #guarda el número de afiliado
                    entry.config(state="readonly")
                self.buscar_paciente.delete(0, END)
                if valores is None:
                    return
            else:
                messagebox.showwarning("Atención", "Se encontraron varios pacientes con ese Documento.")
                ventana.lift()
                return            
        elif tabla == "medico":
            elemento = self.buscar_medico.get()
            if not elemento:
                messagebox.showwarning("Atención", "Ingrese una matrícula para buscar.")
                ventana.lift()
                return
            if not elemento.isdigit():
                messagebox.showwarning("Atención", "Ingrese una matrícula válida.")
                ventana.lift()
                return
            resultado = self.buscar_elemento_tabla(elemento, "medico")
            if resultado[0] == 0:
                messagebox.showwarning("Atención", "No se encontró ningún médico con esa matrícula.")
                ventana.lift()
                return
            elif resultado[0] == 1:
                valores = self.obtener_unico(elemento, "medico")
                campos_medico = ["Nombre del médico", "Apellido del médico", "Matrícula"]
                self.datos_ficha["Id_medico"] = valores[0]
                for m, campo in enumerate(campos_medico):
                    Label(self.frame_datos_medico, text=campo + ":", bg="#c9c2b2", font=("Robot", 12), justify=LEFT).grid(row=0, column=m, padx=8, sticky= W)
                    entry = Entry(self.frame_datos_medico, width=28, font=("Robot", 12))
                    entry.grid(row=1, column=m, padx=8)
                    entry.insert(0, valores[m+1])
                    entry.config(state="readonly")
                    self.datos_ficha[campo] = entry # Guarda la entrada en un diccionario
                self.buscar_medico.delete(0, END)
                if valores is None:
                    return
    #Funciones para agregar, eliminar y calcular el total de los tratamientos en la ficha
    def actualizar_total_precios(self):
        total = 0.0
        for child in self.arbol_ficha.get_children():
            precio = self.arbol_ficha.item(child, 'values')[2]
            cantidad = self.arbol_ficha.item(child, 'values')[3]
            total += float(precio) * int(cantidad)
        self.total_var.set(f"{total:.2f}")
    def agregar_tratamiento_a_ficha(self):
        # Obtener el elemento seleccionado
        selected_item = self.tree_tratamiento.selection()
        if selected_item:
            id_tratamiento = selected_item[0]
            item_values = self.tree_tratamiento.item(selected_item, 'values')
            cantidad = self.cantidad_var.get()
            # Verificar si el elemento ya existe en el Treeview de la ficha
            for child in self.arbol_ficha.get_children():
                if self.arbol_ficha.item(child, 'values')[0] == item_values[0]:
                    messagebox.showwarning("Atención", "El tratamiento ya fue agregado.")
                    self.ventana_agregar.lift()
                    self.ventana_tratamientos.lift()
                    return
            # Agregar el elemento al Treeview de la ficha
            self.arbol_ficha.insert("", "end", iid = id_tratamiento ,values= (item_values[1], item_values[0], item_values[2], cantidad))
            self.actualizar_total_precios()
    def eliminar_tratamiento_a_ficha(self):
        selected_item = self.arbol_ficha.selection()
        if selected_item:
            # Eliminar el elemento del Treeview de la ficha
            self.arbol_ficha.delete(selected_item)
            # Actualizar el total de precios
            self.actualizar_total_precios()

    #Funciones para conectar con la base de datos
    #Funciones para subir los datos en la base de datos
    def guardar_nueva_ficha(self, entry, ventana):
        conexion = obtener_conexion()

        try:
            id_paciente = self.datos_ficha["Id_paciente"]
            nombre = entry["Nombre"].get()      #Obtenemos los valores que el usuario ingresó.
            apellido = entry["Apellido"].get()
            documento = entry["Documento"].get()
            obra_social = self.datos_ficha["Obra Social"]
            nro_afiliado = entry["Número de Afiliado"].get()
        except KeyError as e:
            messagebox.showwarning("Atención", "Complete todos los campos del paciente")
        try:
            id_medico = self.datos_ficha["Id_medico"]
            nombre_medico = entry["Nombre del médico"].get()
            apellido_medico = entry["Apellido del médico"].get()
            matricula = entry ["Matrícula"].get()
        except KeyError as e:
            messagebox.showwarning("Atención", "Complete todos los campos del médico")
            return
        try:
            total = self.total_var.get()
            fecha = self.entry_fecha.get()
        except KeyError as e:
            messagebox.showwarning("Atención", "Complete todos los campos de la consulta")
            return

        # Obtener los tratamientos de la ficha
        tratamientos = []
        for child in self.arbol_ficha.get_children():
            tratamiento = self.arbol_ficha.item(child, 'values')
            tratamientos.append((int(child), int(tratamiento[3])))

        # Validar datos y agregar al Treeview
        if nombre and apellido and documento and obra_social and nro_afiliado and nombre_medico and apellido_medico and matricula and total and fecha:
            if self.ficha_duplicada(id_paciente, id_medico, fecha, tratamientos):
                messagebox.showwarning("Atención", "Ya existe una ficha con los mismos datos.")
                return
            try:
                cursor = conexion.cursor()
                sql = "INSERT INTO ficha (id_paciente, id_obra_social, nro_afiliado ,id_medico, fecha, total) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (id_paciente, obra_social, nro_afiliado, id_medico, fecha, total)
                cursor.execute(sql, val)
                conexion.commit()
                #Obtenemos el id de la ficha que acabamos de agregar
                ficha_id = cursor.lastrowid
                for child in self.arbol_ficha.get_children():
                    id_tratamiento = child
                    tratamiento = self.arbol_ficha.item(child, 'values')
                    sql = "INSERT INTO detalle_ficha (id_ficha, id_tratamiento, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)"
                    val = (ficha_id, id_tratamiento, tratamiento[3], tratamiento[2])
                    cursor.execute(sql, val)
                    conexion.commit()
                messagebox.showinfo("Información", "Ficha agregada exitosamente")
                self.tree.insert("", 0, values=(documento, nombre, apellido, obra_social, fecha, total))
                self.volver_inicio()
                self.actualizar_treeview()
            except mysql.connector.Error as err:
                conexion.rollback()
                messagebox.showerror("Error", f"Error al agregar la ficha: {err}")
            finally:
                cursor.close()
                conexion.close()
        else:
            messagebox.showwarning("Atención", "Complete todos los campos.")

    #VER obra social seleccionada
    def ver_ficha(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione una ficha.")
            return

        # Usamos el primer elemento seleccionado (ID oculto)
        id_seleccionado = seleccion[0]
        
        # Obtenemos el obra_social usando el ID
        ficha_seleccionada = self.obtener_ficha_por_id(id_seleccionado)

        if ficha_seleccionada:
            # Abrimos la ventana sin mostrar el ID
            ficha_reducida = ficha_seleccionada[0:]  # Aquí excluimos el ID
            self.abrir_ventana_ficha(ficha_reducida, modo="ver", seleccion=id_seleccionado)  # Excluimos el ID
        else:
            messagebox.showerror("Error", "No se pudo obtener el obra_social.")
    #funcion para MODIFICAR ficha
    def modificar_ficha(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione una ficha.")
            return
        # Usamos el primer elemento seleccionado (ID oculto)
        id_seleccionado = seleccion[0]
        # Aquí obtenemos los valores del obra_social usando el ID
        ficha_seleccionada = self.obtener_ficha_por_id(id_seleccionado)
        if ficha_seleccionada:
            # Abrimos la ventana sin mostrar el ID
            ficha_reducida = ficha_seleccionada[0:]  # Aquí excluimos el ID
            self.abrir_ventana_ficha(ficha_reducida, modo="modificar", seleccion=id_seleccionado)
        else:
            messagebox.showerror("Error", "No se pudo obtener la ficha para modificar.")
    
    def abrir_ventana_ficha(self, ficha, modo, seleccion=None):
        def activar_edicion(entradas, btn_guardar):
            btn_guardar.config(state="normal")
            """btn_nuevo_t.config(state="normal")"""
            btn_agregar_t.config(state="normal")
            btn_eliminar_t.config(state="normal")
            btn_buscar1.config(state="normal")
            btn_buscar2.config(state="normal")
            self.buscar_paciente.config(state="normal")
            self.buscar_medico.config(state="normal")
            self.entry_fecha.bind("<Button-1>", lambda e: self.abrir_calendario())

        ventana = Toplevel(self)
        ventana.title("Detalles de ficha")
        ventana.config(bg="#e4c09f")
        ventana.resizable(False, False)
        ventana.geometry("1370x700+0+0")
        validar_letynum = ventana.register(self.solo_letras_numeros)

        frame_detalles = LabelFrame(ventana, text="Detalles de ficha", font=("Robot", 12), bg="#c9c2b2")
        frame_detalles.pack(padx=10, pady=5)

        frame_btns = Frame(ventana, bg="#e4c09f")
        frame_btns.pack()

        self.datos_ficha = {}  # Diccionario para guardar los datos de la ficha

        #FRAME DE DATOS DEL PACIENTE
        frame_paciente = LabelFrame(frame_detalles, text="Datos del paciente", font=("Robot", 10), padx=10, pady=5, bg="#c9c2b2")
        frame_paciente.pack(fill="x")
        #buscador de pacientes

        frame_busqueda = Frame(frame_paciente, bg="#c9c2b2")
        frame_busqueda.pack(fill="x", pady=5)
        Label(frame_busqueda, text="Buscar:", bg="#c9c2b2",font=("Robot", 13)).grid(row=0, column=1, padx=5, pady=2, sticky= W)
        self.buscar_paciente = Entry(frame_busqueda, width=20,font=("Robot",12))
        self.buscar_paciente.grid(row=0, column=2, padx=5, pady=2, sticky= W)
        self.buscar_paciente.config(validate="key", validatecommand=(validar_letynum, '%S'))
        self.buscar_paciente.insert(0, "DOCUMENTO")  #Agrega marcador de posición
        self.buscar_paciente.config(fg="gray")
        self.buscar_paciente.bind("<FocusIn>", lambda event, e=self.buscar_paciente: self.limpiar_marcador(e))
        self.buscar_paciente.bind("<FocusOut>", lambda event, e=self.buscar_paciente: self.restaurar_marcador(e))
        img_buscar = Image.open("buscar1.png").resize((20, 20), Image.Resampling.LANCZOS)
        img_buscar = ImageTk.PhotoImage(img_buscar)
        btn_buscar1 = Button(frame_busqueda, image=img_buscar, width=25, height=25,bg="#e6c885", command=lambda: self.buscar_elemento("paciente"))
        btn_buscar1.grid(row=0, column=3, sticky= W)
        btn_buscar1.image = img_buscar

        #Frame para los datos del PACIENTE
        self.frame_datos_pacientes = Label(frame_paciente, bg="#c9c2b2", font=("Robot", 10))
        self.frame_datos_pacientes.pack(pady=5)

        campos_arriba = ["Nombre", "Apellido", "Documento"]
        valores_arriba = list(self.recuperar_paciente(ficha[1]))
        campos_abajo = ["Obra Social", "Número de Afiliado"]
        obra_social = self.conexion_bd_os(ficha[2])
        nro_afiliado = ficha[3]
        for i, campo in enumerate(campos_arriba):
            Label(self.frame_datos_pacientes, text=campo + ":", bg="#c9c2b2", font=("Robot", 12), justify=LEFT).grid(row=0, column=i, padx=10, sticky=W)
            entry = Entry(self.frame_datos_pacientes, width=40, font=("Robot", 12))
            entry.grid(row=1, column=i, padx=10)
            if i + 1 < len(valores_arriba):
                entry.insert(0,str(valores_arriba[i]).upper())
            entry.config(state="readonly")
            self.datos_ficha[campo] = entry
        for j, campos_a in enumerate(campos_abajo):
            Label(self.frame_datos_pacientes, text=campos_a + ":", bg="#c9c2b2", font=("Robot", 12), justify=LEFT).grid(row=2, column=j, padx=10, sticky=W)
            entry = Entry(self.frame_datos_pacientes, width=40, font=("Robot", 12))
            entry.grid(row=3, column=j, padx=10)
            if campos_a == "Obra Social":
                entry.insert(0, obra_social[0][1])
            if campos_a == "Número de Afiliado":
                entry.insert(0, nro_afiliado)
            entry.config(state="readonly")
            self.datos_ficha[campos_a] = entry

        #Frame para los datos del MEDICO
        frame_medico = LabelFrame(frame_detalles, text="Datos del médico", font=("Robot", 10), bg="#c9c2b2")
        frame_medico.pack(fill="x")

        #buscador de médico
        frame_busqueda_medico = Frame(frame_medico, bg="#c9c2b2")
        frame_busqueda_medico.pack(fill="x", pady=5, padx=8)
        Label(frame_busqueda_medico, text="Buscar:", bg="#c9c2b2",font=("Robot", 13)).grid(row=0, column=1, padx=5, pady=2, sticky= W)
        self.buscar_medico = Entry(frame_busqueda_medico, width=20,font=("Robot",12))
        self.buscar_medico.grid(row=0, column=2, padx=5, pady=2, sticky= W)
        self.buscar_medico.config(validate="key", validatecommand=(validar_letynum, '%S'))
        self.buscar_medico.insert(0, "MATRÍCULA")  #Agrega marcador de posición
        self.buscar_medico.config(fg="gray")
        self.buscar_medico.bind("<FocusIn>", lambda event, e=self.buscar_medico: self.limpiar_marcador(e))
        self.buscar_medico.bind("<FocusOut>", lambda event, e=self.buscar_medico: self.restaurar_marcador(e))
        img_buscar = Image.open("buscar1.png").resize((20, 20), Image.Resampling.LANCZOS)
        img_buscar = ImageTk.PhotoImage(img_buscar)
        btn_buscar2 = Button(frame_busqueda_medico, image=img_buscar, width=25, height=25,bg="#e6c885", command=lambda: self.buscar_elemento("medico"))
        btn_buscar2.grid(row=0, column=3, sticky= W)
        btn_buscar2.image = img_buscar

        frame_campos_medyfecha = Frame(frame_medico, bg="#c9c2b2")
        frame_campos_medyfecha.pack(fill="x", pady=5, padx=8)
        #Frame para los datos del medico
        self.frame_datos_medico = Frame(frame_campos_medyfecha, bg="#c9c2b2")
        self.frame_datos_medico.grid(row = 0, column = 0, pady=5)

        campos_medico = ["Nombre del médico", "Apellido del médico", "Matrícula"]
        valores_medico= list(self.recuperar_medico(ficha[4]))
        for m, campo in enumerate(campos_medico):
            Label(self.frame_datos_medico, text=campo + ":", bg="#c9c2b2", font=("Robot", 12), justify=LEFT).grid(row=0, column=m, padx=8, sticky=W)
            entry = Entry(self.frame_datos_medico, width=28, font=("Robot", 12))
            entry.grid(row=1, column=m, padx=10, sticky=W)
            entry.insert(0, str(valores_medico[0][m]).upper())
            self.datos_ficha[campo] = entry
            entry.config(state="readonly")

        self.fecha= Frame(frame_campos_medyfecha, bg="#c9c2b2")
        self.fecha.grid(row=0, column=1, padx=8, sticky=W)

        Label(self.fecha, text="Fecha de consulta" + ":", bg="#c9c2b2", font=("Robot", 12), justify=LEFT).pack(anchor=W, padx=8)
        self.entry_fecha = Entry(self.fecha, width=20, font=("Robot", 12))
        self.entry_fecha.pack(anchor=W, padx=10)
        self.entry_fecha.insert(0, ficha[5])
        self.datos_ficha["Fecha"] = self.entry_fecha
        self.entry_fecha.config(state="readonly")

        #Frame para los datos del TRATAMIENTOS
        frame_tratamiento = LabelFrame(frame_detalles, text="Tratamiento", font=("Robot", 10), bg="#c9c2b2") 
        frame_tratamiento.pack(fill="x", pady=8)

        #Tabla para mostar los tratamientos
        frame_tabla_tratamientos = Frame(frame_tratamiento, bg="#c9c2b2", width= 500)  # Frame para contener la tabla y el scrollbar
        frame_tabla_tratamientos.grid(row= 0, column=0, padx= 55, pady= 5)

        campos_tratamiento = ["Código", "Nombre del procedimiento", "Precio"]
    
        Label(frame_tabla_tratamientos, text="Tratamientos aplicados", font=("Robot", 12), bg="#c9c2b2").pack(pady=5) 
        estilo = ttk.Style()
        estilo.configure("Treeview", font=("Robot",10), rowheight=16)  # Cambia la fuente y el alto de las filas
        estilo.configure("Treeview.Heading", font=("Robot",12), padding= [0, 8])  # Cambia la fuente de las cabeceras
        
        #Treeview para mostrar la tabla de tratamientos dentro del frame_tabla
        self.arbol_ficha = ttk.Treeview(frame_tabla_tratamientos, columns=("Código", "Nombre", "Precio", "Cantidad"), show='headings', height=11, style = "Treeview")
        self.arbol_ficha.pack(expand=True, fill="both")

        #Títulos de columnas
        self.arbol_ficha.heading("Código", text="Código")
        self.arbol_ficha.heading("Nombre", text="Nombre")
        self.arbol_ficha.heading("Precio", text="Precio")
        self.arbol_ficha.heading("Cantidad", text="Cantidad")

        #Ancho de las columnas y datos centrados
        self.arbol_ficha.column("Código", anchor='center', width=150, stretch=False)
        self.arbol_ficha.column("Nombre", anchor='center', width=300, stretch=False)
        self.arbol_ficha.column("Precio", anchor='center', width=200, stretch=False)
        self.arbol_ficha.column("Cantidad", anchor='center', width=100, stretch=False)

        self.ingresar_tratamientos_ver_ficha(seleccion)
        #Frame para los botones de agregar y eliminar tratamientos
        frame_botones_tratamiento = Frame(frame_tratamiento, bg="#c9c2b2")
        frame_botones_tratamiento.grid(row=0, column=1, columnspan=2, padx=30)

        """btn_nuevo_t = Button(frame_botones_tratamiento, text="Nuevo Tratamiento", font=("Robot", 11, "bold"),bg="#e6c885", height=2, width=20)
        btn_nuevo_t.pack(pady=8)"""

        btn_agregar_t = Button(frame_botones_tratamiento, text="Agregar Tratamiento", font=("Robot", 11, "bold"),bg="#e6c885", height=2, width=20, command= self.mostrar_tratamientos)
        btn_agregar_t.pack(pady=8)

        btn_eliminar_t = Button(frame_botones_tratamiento, text="Eliminar Tratamiento", font=("Robot", 11, "bold"),bg="#e6c885", height=2, width=20, command= self.eliminar_tratamiento_a_ficha)
        btn_eliminar_t.pack(pady=8)

        self.total_var = StringVar()
        self.entry_total = Entry(frame_botones_tratamiento, textvariable=self.total_var, font=("Robot", 15), state='readonly', width=10)
        self.entry_total.pack(pady=8)
        self.actualizar_total_precios()

        if modo == "ver":
            """ btn_nuevo_t.config(state="disabled")"""
            btn_agregar_t.config(state="disabled")
            btn_eliminar_t.config(state="disabled")
            btn_buscar1.config(state="disabled")
            btn_buscar2.config(state="disabled")
            self.buscar_paciente.config(state="disabled")
            self.buscar_medico.config(state="disabled")

            btn_editar = Button(frame_btns, text="Modificar", width=15, font=("Robot", 15), bg="#e6c885", command=lambda: activar_edicion(self.datos_ficha, btn_guardar))
            btn_editar.grid(row = 0, column=0, padx=25,pady=10)

            btn_guardar = Button(frame_btns, text="Guardar Cambios", width=15, font=("Robot", 15), bg="#e6c885", command=lambda: self.guardar_cambios(self.datos_ficha , ventana, seleccion))
            btn_guardar.grid(row = 0, column=1, padx=25,pady=10)
            btn_guardar.config(state="disabled")  # Iniciar como deshabilitado

            btn_editar = Button(frame_btns, text="Volver", width=15, font=("Robot", 15), bg="#e6c885", command=ventana.destroy)
            btn_editar.grid(row = 0, column=2, padx=25,pady=10)

        if modo == "modificar":
            """btn_nuevo_t.config(state="normal")"""
            btn_agregar_t.config(state="normal")
            btn_eliminar_t.config(state="normal")
            btn_buscar1.config(state="normal")
            btn_buscar2.config(state="normal")
            self.buscar_paciente.config(state="normal")
            self.buscar_medico.config(state="normal")
            self.entry_fecha.bind("<Button-1>", lambda e: self.abrir_calendario())

            btn_guardar = Button(frame_btns, text="Guardar Cambios", width=15, font=("Robot", 15), bg="#e6c885", command=lambda: self.guardar_cambios(self.datos_ficha, ventana, seleccion))
            btn_guardar.grid(row=0, column=0,  padx=40, pady=10)

            btn_cancelar = Button(frame_btns, text="Cancelar", width=15, font=("Robot", 15), bg="#e6c885", command=ventana.destroy)
            btn_cancelar.grid(row=0, column=1, padx= 40, pady=10)
    
    def guardar_cambios(self, entradas, ventana, seleccion):
        conexion = obtener_conexion()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return
        
        try:
            documento = self.datos_ficha["Documento"].get()
            id_paciente = self.buscar_ids("paciente", documento)[0]
            id_obra_social = self.datos_ficha["Obra Social"]
            nro_afiliado = self.datos_ficha["Número de Afiliado"].get()
        except KeyError as e:
            messagebox.showwarning("Atención", "Complete todos los campos del paciente")
        try:
            id_medico = self.buscar_ids("medico", self.datos_ficha["Matrícula"].get())[0]
            nombre_medico = self.datos_ficha["Nombre del médico"].get()
            apellido_medico = self.datos_ficha["Apellido del médico"].get()
            matricula = self.datos_ficha ["Matrícula"].get()
        except KeyError as e:
            messagebox.showwarning("Atención", "Complete todos los campos del médico")
            return
        try:
            total = self.total_var.get()
            fecha = self.entry_fecha.get()
        except KeyError as e:
            messagebox.showwarning("Atención", "Complete todos los campos de la consulta")
            return

        # Obtener los tratamientos de la ficha
        tratamientos = []
        for child in self.arbol_ficha.get_children():
            tratamiento = self.arbol_ficha.item(child, 'values')
            tratamientos.append((int(child), int(tratamiento[3])))

        if documento and id_paciente and id_obra_social and nro_afiliado and id_medico and total and fecha:
            if self.ficha_duplicada(id_paciente, id_medico, fecha, tratamientos):
                messagebox.showwarning("Atención", "Ya existe una ficha con los mismos datos.")
                ventana.lift()
                return
            try:
                cursor = conexion.cursor()
                sql1 = "UPDATE ficha SET id_paciente = %s, id_obra_social = %s, nro_afiliado = %s, id_medico = %s, fecha = %s, total = %s WHERE id_ficha = %s"
                val1 = (id_paciente, id_obra_social, nro_afiliado, id_medico, fecha, total, seleccion)
                cursor.execute(sql1, val1)

                # Obtener los tratamientos actuales de la ficha
                cursor.execute("SELECT id_tratamiento FROM detalle_ficha WHERE id_ficha = %s", (seleccion,))
                tratamientos_actuales = {row[0] for row in cursor.fetchall()}

                # Obtener los nuevos tratamientos de la interfaz
                nuevos_tratamientos = {}
                for child in self.arbol_ficha.get_children():
                    tratamiento = self.arbol_ficha.item(child, 'values')
                    id_tratamiento = int(child)
                    nuevos_tratamientos[id_tratamiento] = tratamiento
                
                if not nuevos_tratamientos:
                    messagebox.showerror("Error", "No se han agregado tratamientos a la ficha.")
                    ventana.lift()
                    return

                # Actualizar o agregar tratamientos
                for id_tratamiento, tratamiento in nuevos_tratamientos.items():
                    if id_tratamiento in tratamientos_actuales:
                        # Actualizar tratamiento existente
                        sql = "UPDATE detalle_ficha SET cantidad = %s, precio_unitario = %s WHERE id_ficha = %s AND id_tratamiento = %s"
                        val = (tratamiento[3], tratamiento[2], seleccion, id_tratamiento)
                        cursor.execute(sql, val)
                    else:
                        # Agregar nuevo tratamiento
                        sql = "INSERT INTO detalle_ficha (id_ficha, id_tratamiento, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)"
                        val = (seleccion, id_tratamiento, tratamiento[3], tratamiento[2])
                        cursor.execute(sql, val)

                # Eliminar tratamientos que ya no están en la interfaz
                tratamientos_a_eliminar = tratamientos_actuales - nuevos_tratamientos.keys()
                for id_tratamiento in tratamientos_a_eliminar:
                    cursor.execute("DELETE FROM detalle_ficha WHERE id_ficha = %s AND id_tratamiento = %s", (seleccion, id_tratamiento))

                conexion.commit()
                messagebox.showinfo("Información", "Ficha actualizada exitosamente")
                ventana.destroy()
                self.actualizar_treeview()
            except Exception as e:
                conexion.rollback()
                messagebox.showerror("Error", f"Error al actualizar la ficha: {e}")
                ventana.lift()
            finally:
                cursor.close()
                conexion.close()
        else:
            messagebox.showwarning("Atención", "Complete todos los campos.")

    #Funciones para ELIMINAR las fichas, y los detalles de la misma
    def eliminar_ficha(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione un paciente para eliminar.")
            return
        
        id_ficha = seleccion[0]  # Asumiendo que el ID es el primer valor
        
        #Pregunta al usuario si está seguro de eliminar 
        respuesta = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar la ficha seleccionada?")
        if respuesta:  
            try:
                conexion = obtener_conexion()
                cursor = conexion.cursor()
                sentencia1 = ("UPDATE ficha SET activo = 0 WHERE id_ficha = %s")
                cursor.execute(sentencia1, (id_ficha,)) # Elimina la ficha
                sentencia2 = ("UPDATE detalle_ficha SET activo = 0 WHERE id_ficha = %s")
                cursor.execute(sentencia2, (id_ficha,)) # Elimina los detalles de la ficha
                conexion.commit()
                messagebox.showinfo("Éxito", "Ficha eliminada correctamente.")
                self.tree.delete(seleccion)
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al eliminar la ficha: {err}")
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()
    #Funciones para BUSCAR fichas en la base de datos
    def buscar_ficha(self):
        busqueda = self.entrada_buscar.get().strip().upper() 
        if not busqueda:
            self.tree.delete(*self.tree.get_children())
            self.actualizar_treeview()
            return

        #evalua los documento que contengan ese número
        if busqueda.isdigit():
            tratamiento_encontrado = False
            for item in self.tree.get_children():
                valores = self.tree.item(item, 'values')
                documento = valores[0]

                if busqueda in documento:
                    tratamiento_encontrado = True
                else:
                    self.tree.delete(item)
                
            if not tratamiento_encontrado:
                messagebox.showwarning("Atención", "No se encontró la ficha.")
                self.tree.delete(*self.tree.get_children())
                self.actualizar_treeview()
        else:
            tratamiento_encontrado = False
            for item in self.tree.get_children():
                valores = self.tree.item(item, 'values')
                nombre = valores[1].upper()
                apellido = valores[2].upper()
                obra_social = valores[3].upper()

                if busqueda in nombre or busqueda in apellido:
                    tratamiento_encontrado = True
                else:
                    self.tree.delete(item)

            if not tratamiento_encontrado:
                messagebox.showwarning("Atención", "No se encontró la ficha.")
                self.tree.delete(*self.tree.get_children())
                self.actualizar_treeview()

    #Funciones para nuevo médico
    def agregar_medico(self):
        def solo_letras(char):
            return char.isalpha() or char == " "
        def solo_numeros(char):
            return char.isdigit()

        # Verifica si la ventana ya está abierta
        if self.ventana_agregar_medico is not None and Toplevel.winfo_exists(self.ventana_agregar_medico):
            self.ventana_agregar_medico.destroy()
        self.ventana_agregar_medico = Toplevel(self)
        self.ventana_agregar_medico.title("Agregar medico")
        self.ventana_agregar_medico.config(bg="#e4c09f")
        self.ventana_agregar_medico.geometry("+200+180")
        self.ventana_agregar_medico.resizable(False, False)
        self.ventana_agregar_medico.protocol("WM_DELETE_WINDOW", lambda: None)

        frame_agregar = LabelFrame(self.ventana_agregar_medico, text="Agregar Nuevo medico",font=("Robot", 12), padx=10,pady=10,bg="#c9c2b2")
        frame_agregar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        campos = ["Nombre", "Apellido", "DNI", "Telefono", "Matricula"]
        entradas = {}

        vcmd_letras = self.ventana_agregar_medico.register(solo_letras)
        vcmd_numeros = self.ventana_agregar_medico.register(solo_numeros)

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

        frame_btns = Frame(self.ventana_agregar_medico, bg="#e4c09f")
        frame_btns.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        btn_nuevo_medico = Button(frame_btns, text="Agregar", font=("Robot", 13),bg="#e6c885", width=15, command=lambda:self.guardar_nuevo_medico(entradas,self.ventana_agregar_medico))
        btn_nuevo_medico.grid(row=len(campos), column=0, padx=40, pady=10)

        btn_volver = Button(frame_btns, text="Volver", font=("Robot", 13),bg="#e6c885", width=15, command=self.ventana_agregar_medico.destroy)
        btn_volver.grid(row=len(campos), column=1, pady=10)
    def guardar_nuevo_medico(self, entradas, ventana):
        def validar_repetidos(documento):
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
        def insertar_medico(nombre, apellido, matricula, telefono, documento):
            conexion = obtener_conexion()
            if conexion is None:
                return
            try:
                cursor = conexion.cursor()
                sql = "INSERT INTO medico (nombre, apellido, matricula, telefono, documento) VALUES (%s, %s, %s, %s, %s)"
                val = (nombre, apellido, matricula, telefono, documento)
                cursor.execute(sql, val)
                conexion.commit()
                #messagebox.showinfo("Éxito", "Registro insertado correctamente.")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al insertar en la base de datos: {err}")
            finally:
                conexion.close()
        nombre = entradas["Nombre"].get().upper()
        apellido = entradas["Apellido"].get().upper()
        dni = entradas["DNI"].get()
        telefono = entradas["Telefono"].get()
        matricula = entradas["Matricula"].get()

        if not validar_repetidos(dni):
            messagebox.showwarning("Atención", "El documento ya está registrado.")
            return

        if nombre and apellido and dni and telefono and matricula:
            try:
                insertar_medico(nombre, apellido, matricula, telefono, dni)
                messagebox.showinfo("Información", "Médico agregado correctamente.")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar el médico: {e}")
        else:
            messagebox.showwarning("Atención", "Complete todos los campos.")

    #Funciones para agregar nuevo paciente
    def agregar_paciente(self):
        def solo_letras(char):
            return char.isalpha() or char == " "
        def solo_numeros(char):
            return char.isdigit()
        # Verifica si la ventana ya está abierta
        if self.ventana_agregar_paciente is not None and Toplevel.winfo_exists(self.ventana_agregar_paciente):
            self.ventana_agregar_paciente.destroy()
        self.ventana_agregar_paciente = Toplevel(self)
        self.ventana_agregar_paciente.title("Agregar Paciente")
        self.ventana_agregar_paciente.config(bg="#e4c09f")
        self.ventana_agregar_paciente.geometry("+200+180")
        self.ventana_agregar_paciente.resizable(False,False)
        self.ventana_agregar_paciente.protocol("WM_DELETE_WINDOW", lambda: None)  # Deshabilitar el botón "Cerrar" de la ventana  
        
        frame_agregar = LabelFrame(self.ventana_agregar_paciente, text="Agregar Nuevo Paciente", font= ("Roboto", 11),padx=10, pady=10, bg="#c9c2b2")
        frame_agregar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        frame_btns = Frame(self.ventana_agregar_paciente, bg="#e4c09f")
        frame_btns.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

        campos = ["Nombre","Apellido","DNI","Obra Social","Número de Afiliado"]
        entradas = {}
        vcmd_letras = self.ventana_agregar_paciente.register(solo_letras)
        vcmd_numeros = self.ventana_agregar_paciente.register(solo_numeros)

        for i, campo in enumerate(campos):
            etiquetas = Label(frame_agregar, text=campo + ":", bg="#c9c2b2", font=("Roboto", 10))
            etiquetas.grid(row=i, column=0, padx=10, pady=5)
            if campo == "Obra Social":
                # Crear ComboBox para Obra Social
                conexion = obtener_conexion()
                cursor = conexion.cursor()
                cursor.execute("SELECT nombre FROM obra_social")
                obras_sociales = [row[0] for row in cursor.fetchall()]
                cursor.close()
                conexion.close()
                combobox = ttk.Combobox(frame_agregar, values=obras_sociales, font=("Roboto", 10))
                combobox.grid(row=i, column=1, padx=10, pady=5)
                entradas[campo] = combobox
            else:
                entry = Entry(frame_agregar, width=40, font=("Roboto", 10))
                entry.grid(row=i, column=1, padx=10, pady=5)
                entradas[campo] = entry
            if campo in ["Nombre","Apellido"]:
                entry.config(validate="key", validatecommand=(vcmd_letras, '%S'))
            elif campo in ["DNI"]:
                entry.config(validate="key", validatecommand=(vcmd_numeros, '%S'))
        btn_nuevo_paciente = Button(frame_btns, text="Agregar", font=("Roboto", 13),bg="#e6c885", width=15, command=lambda: self.guardar_nuevo_paciente(entradas, self.ventana_agregar_paciente))
        btn_nuevo_paciente.grid(row=len(campos),column=0, padx=60, pady=10)

        btn_volver = Button(frame_btns, text="Cancelar", font=("Roboto", 13),bg="#e6c885", width=15,
                            command=self.ventana_agregar_paciente.destroy)
        btn_volver.grid(row=len(campos), column=1, pady=10, padx=10)
    def guardar_nuevo_paciente(self, entry, ventana):
        nombre = entry["Nombre"].get().upper()      # Obtenemos los valores que el usuario ingresó.
        apellido = entry["Apellido"].get().upper()
        documento = entry["DNI"].get()
        obra_social_nombre = entry["Obra Social"].get().upper()
        numeroafiliado = entry["Número de Afiliado"].get().upper()

        # Validar datos y agregar al Treeview
        if nombre and apellido and documento and obra_social_nombre and numeroafiliado:
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
                INSERT INTO paciente (nombre, apellido, documento, id_obra_social, nro_afiliado)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (nombre, apellido, documento, id_obra_social, numeroafiliado))
                conexion.commit()
                messagebox.showinfo("Información", "Paciente agregado correctamente.")
                ventana.destroy()
                cursor.close()

                self.buscar_paciente.delete(0, END)
                self.buscar_paciente.insert(0, documento)
                self.buscar_elemento("paciente")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al agregar el paciente: {err}")
            finally:
                if conexion.is_connected():
                    conexion.close()
        else:
            messagebox.showwarning("Atención", "Complete todos los campos.")

"""ventana = Tk()
ventana.title("Gestion de Fichas")
ventana.resizable(False,False)
ventana.geometry("+0+0")
root = GestionFicha(ventana)
ventana.mainloop()"""