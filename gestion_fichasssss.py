from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
from ConexionBD import *

class GestionFicha(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg="#e4c09f", width= 1370, height=700)
        self.master = master
        self.pack_propagate(False)
        self.pack(expand=True)
        self.createWidgets()

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

    def buscar_elemento_paciente(self, elemento):
        conexion = obtener_conexion()  # Llama a la función que establece la conexión
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return
        try:
            cursor = conexion.cursor()
            sentencia = "SELECT COUNT(*) from paciente WHERE documento = %s"
            cursor.execute(sentencia, (elemento,))
            resultado = cursor.fetchall()
            cursor.close()
            conexion.close()
            print(resultado)
            return resultado[0]
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Consulta", f"No se pudo realizar la consulta a la base de datos: {err}")
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return

    def obtener_paciente(self, elemento):
        conexion = obtener_conexion()
        print(elemento)
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM paciente WHERE documento = %s", (elemento,))
            paciente = cursor.fetchall()
            if paciente is None:
                messagebox.showwarning("Advertencia", "No se encontró ningún paciente con ese DNI.")
            return paciente
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se pudo recuperar el paciente: {error}")
        finally:
            cursor.close()
            conexion.close()
    
    def buscar_elemento(self, tabla):
        if tabla == "paciente":
            elemento = self.buscar_paciente.get()
            if not elemento:
                messagebox.showwarning("Atención", "Ingrese un DNI para buscar.")
                return
            if not elemento.isdigit():
                messagebox.showwarning("Atención", "Ingrese un DNI válido.")
                return
            resultado = self.buscar_elemento_paciente(elemento)
            if resultado[0] == 0:
                messagebox.showwarning("Atención", "No se encontró ningún paciente con ese DNI.")
                return
            elif resultado[0] == 1:
                paciente = self.obtener_paciente(elemento)
                campos_arriba = ["Nombre", "Apellido", "DNI"]
                campos_abajo = ["Obra Social", "Número de Afiliado"]
                self.datos_ficha = {}
                valores = list(paciente[0])
                for i, campos_arriba in enumerate(campos_arriba):
                    Label(self.frame_datos_pacientes, text=campos_arriba + ":", bg="#c9c2b2", font=("Robot", 12), justify=LEFT).grid(row=0, column=i, padx=10, sticky=W)
                    entry = Entry(self.frame_datos_pacientes, width=40, font=("Robot", 12))
                    entry.grid(row=1, column=i, padx=10)
                    if campos_arriba == "DNI":
                        entry.insert(0, valores[5])
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
                        nombre = self.conexion_bd_os(valores[6])
                        entry.insert(0, nombre[0][1])
                        self.datos_ficha[campos_arriba] = valores[6]  #guarda el id de la obra social
                    elif campos_abajo == "Número de Afiliado":
                        entry.insert(0, valores[7])
                        self.datos_ficha[campos_arriba] = entry      #guarda el número de afiliado
                    entry.config(state="readonly")
                self.buscar_paciente.delete(0, END)
                if paciente is None:
                    return
        

    def volver_menu_principal(self):
        from Menu import MENU
        self.master.destroy()
        ventana = Tk()
        ventana.wm_title("Menú Recupero de Obra Social")
        ventana.wm_resizable(0,0)
        ventana.geometry("+30+15")
        menu = MENU(ventana)
        menu.mainloop()

    def createWidgets(self):
        frame_fichas = LabelFrame(self, text="Gestión de Fichas", font=("Robot",15),padx=10, pady=10, bg="#c9c2b2")
        frame_fichas.pack(expand=True)

        #primer frame, contiene la imagen y el titulo de la ventana
        contenedor_titulo = Frame(frame_fichas, bg="#c9c2b2")
        contenedor_titulo.pack(pady= 5)
        #Carga la imagen de fondo
        img_fondo = Image.open("fondo3.png")
        img_fondo = img_fondo.resize((1100, 120), Image.Resampling.LANCZOS)
        self.img_fondo = ImageTk.PhotoImage(img_fondo)
        #Label para la imagen de fondo
        fondo_label = Label(contenedor_titulo, image=self.img_fondo)
        fondo_label.pack(expand=True, fill="both")

        #segundo frame, contiene el buscador y el boton de agregar
        #buscador de fichas
        frame_busqueda = Frame(frame_fichas, bg="#c9c2b2")
        frame_busqueda.pack(padx = 5, fill="x")
        #separa el campo de busqueda del botón
        frame_busqueda.columnconfigure(4, weight=1)

        #Widgets de búsqueda dentro del frame más chico
        Label(frame_busqueda, text="Buscar:", bg="#c9c2b2",font=("Robot",15)).grid(row=1, column=0, padx=5, pady=2, sticky= W)

        self.entrada_buscar = Entry(frame_busqueda,width="50",font=("Robot",13))
        self.entrada_buscar.grid(row=1, column=1, padx=5, pady=2, sticky= W)

        img_buscar = Image.open("buscar1.png").resize((30, 30), Image.Resampling.LANCZOS)
        img_buscar = ImageTk.PhotoImage(img_buscar)
        btn_buscar = Button(frame_busqueda, image=img_buscar, width=40, height=30,bg="#e6c885")
        btn_buscar.grid(row=1, column=2, sticky= W)
        btn_buscar.image = img_buscar

        self.combo_activos = ttk.Combobox(frame_busqueda, width=10, font=("Robot", 14), state="readonly")
        self.combo_activos['values'] = ("Activos", "Inactivos", "Todos")
        self.combo_activos.set("Activos")
        self.combo_activos.grid(row=1, column=3, padx=20, pady=3)

        boton_agregar = Button(frame_busqueda, text="Agregar  +", width=15, bg="#e6c885",font=("Robot",15), command=self.agregar_ficha)
        boton_agregar.grid(row=1, column=5, padx=10, pady=3, sticky= E)
        #Para que siempre esté atrás de los widgets
        fondo_label.lower()

        #Tercer frame, contiene la tabla de fichas
        #Frame para el Treeview y el scrollbar
        frame_tabla = Frame(frame_fichas, bg="#c9c2b2", width= 1000)  # Frame para contener la tabla y el scrollbar
        frame_tabla.pack(expand=True, pady=8)
        
        stilo = ttk.Style()
        stilo.configure("Treeview", font=("Robot",11), rowheight=22)  # Cambia la fuente y el alto de las filas
        stilo.configure("Treeview.Heading", font=("Robot",14), padding= [0, 10])  # Cambia la fuente de las cabeceras
        
        #Treeview para mostrar la tabla de tratamientos dentro del frame_tabla
        self.tree = ttk.Treeview(frame_tabla, columns=("DNI", "Nombre" ,"Apellido", "Obra Social", "Fecha prestación", "Total"), show='headings', height=16)
        self.tree.pack(expand=True, fill="both")

        #Títulos de columnas
        self.tree.heading("DNI", text="DNI")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("Obra Social", text="Obra Social")
        self.tree.heading("Fecha prestación", text="Fecha prestación")
        self.tree.heading("Total", text="Total")

        #Ancho de las columnas y datos centrados
        self.tree.column("DNI", anchor='center', width=120)
        self.tree.column("Nombre", anchor='center', width=300)
        self.tree.column("Apellido", anchor='center', width=300)
        self.tree.column("Obra Social", anchor='center', width=250)
        self.tree.column("Fecha prestación", anchor='center', width=160)
        self.tree.column("Total", anchor='center', width=100)

        #Grid del frame_tabla
        self.tree.grid(row=0, column=0, sticky="nsew")
        #Scrollbar para la tabla dentro del frame_tabla
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')  #Se expande desde arriba hacia abajo
        self.tree.configure(yscrollcommand=scrollbar.set)

        #Cuarto frame, contiene los botones de ver, modificar y eliminar
        frame_btn = Frame(frame_fichas, bg= "#c9c2b2")
        frame_btn.pack(ipady= 10)

        #Botones(ver, modificar, eliminar)
        btn_ver = Button(frame_btn, text="Ver", width=15, font=("Robot",15),bg="#e6c885")
        btn_ver.grid(row=0, column=1,padx=50)

        btn_editar = Button(frame_btn, text="Modificar", width=15, font=("Robot",15),bg="#e6c885")
        btn_editar.grid(row=0, column=2,padx=50)
        
        btn_eliminar = Button(frame_btn, text="Eliminar", width=15,font=("Robot",15),bg="#e6c885")
        btn_eliminar.grid(row=0, column=3, padx=50)

        btn_volver = Button(frame_btn, text="Volver", width=15 ,font=("Robot",15), bg="#e6c885")
        btn_volver.grid(row=0, column=4, padx=50)

    #AGREGAR NUEVA FICHA 
    def agregar_ficha(self):        
        ventana_agregar = Toplevel(self)
        ventana_agregar.title("Agregar ficha")
        ventana_agregar.config(bg="#e4c09f") 
        ventana_agregar.resizable(False,False)
        ventana_agregar.geometry("1370x700+0+0")

        frame_agregar = LabelFrame(ventana_agregar, text="Agregar ficha", font= ("Robot", 12),padx=10, pady=10, bg="#c9c2b2")
        frame_agregar.pack(padx=10, pady=5)

        #FRAME DE DATOS DEL PACIENTE
        frame_paciente = LabelFrame(frame_agregar, text="Datos del paciente", font=("Robot", 10), padx=10, pady=5, bg="#c9c2b2")
        frame_paciente.pack(fill="x")
        #buscador de pacientes
        frame_busqueda = Frame(frame_paciente, bg="#c9c2b2")
        frame_busqueda.pack(fill="x", pady=5)
        Label(frame_busqueda, text="Buscar:", bg="#c9c2b2",font=("Robot", 13)).grid(row=0, column=1, padx=5, pady=2, sticky= W)
        self.buscar_paciente = Entry(frame_busqueda, width=20,font=("Robot",12))
        self.buscar_paciente.grid(row=0, column=2, padx=5, pady=2, sticky= W)
        img_buscar = Image.open("buscar1.png").resize((20, 20), Image.Resampling.LANCZOS)
        img_buscar = ImageTk.PhotoImage(img_buscar)
        btn_buscar = Button(frame_busqueda, image=img_buscar, width=25, height=25,bg="#e6c885", command=lambda: self.buscar_elemento("paciente"))
        btn_buscar.grid(row=0, column=3, sticky= W)
        btn_buscar.image = img_buscar

        frame_busqueda.columnconfigure(4, weight=2)
        frame_busqueda.columnconfigure(5, weight=2)

        btn_nuevo_paciente = Button(frame_busqueda, text="Agregar Paciente", font=("Robot", 11, "bold"),bg="#e6c885")
        btn_nuevo_paciente.grid(row = 0, column=6, padx=15)

        #Frame para los datos del paciente
        self.frame_datos_pacientes = Label(frame_paciente, bg="#c9c2b2", font=("Robot", 10))
        self.frame_datos_pacientes.pack(pady=5)

        campos_arriba = ["Nombre", "Apellido", "DNI"]
        campos_abajo = ["Obra Social", "Número de Afiliado"]
        entradas_pacientes = {}
        for i, campos_arriba in enumerate(campos_arriba):
            Label(self.frame_datos_pacientes, text=campos_arriba + ":", bg="#c9c2b2", font=("Robot", 12), justify=LEFT).grid(row=0, column=i, padx=10, sticky=W)
            entry = Entry(self.frame_datos_pacientes, width=40, font=("Robot", 12))
            entry.grid(row=1, column=i, padx=10)
            entradas_pacientes[campos_arriba] = entry
        for j, campos_abajo in enumerate(campos_abajo):
            Label(self.frame_datos_pacientes, text=campos_abajo + ":", bg="#c9c2b2", font=("Robot", 12), justify=LEFT).grid(row=2, column=j, padx=10, sticky=W)
            entry = Entry(self.frame_datos_pacientes, width=40, font=("Robot", 12))
            entry.grid(row=3, column=j, padx=10)
            entradas_pacientes[campos_abajo] = entry

        #Frame para los datos del MEDICO
        frame_medico = LabelFrame(frame_agregar, text="Datos del médico", font=("Robot", 10), bg="#c9c2b2")
        frame_medico.pack()

        #buscador de médico
        frame_busqueda_medico = Frame(frame_medico, bg="#c9c2b2")
        frame_busqueda_medico.pack(fill="x", pady=5)
        Label(frame_busqueda_medico, text="Buscar:", bg="#c9c2b2",font=("Robot", 13)).grid(row=0, column=1, padx=5, pady=2, sticky= W)
        self.buscar_medico = Entry(frame_busqueda_medico, width=20,font=("Robot",12))
        self.buscar_medico.grid(row=0, column=2, padx=5, pady=2, sticky= W)
        img_buscar = Image.open("buscar1.png").resize((20, 20), Image.Resampling.LANCZOS)
        img_buscar = ImageTk.PhotoImage(img_buscar)
        btn_buscar = Button(frame_busqueda_medico, image=img_buscar, width=25, height=25,bg="#e6c885")
        btn_buscar.grid(row=0, column=3, sticky= W)
        btn_buscar.image = img_buscar

        frame_busqueda_medico.columnconfigure(4, weight=2)
        frame_busqueda_medico.columnconfigure(5, weight=2)

        btn_nuevo_medico = Button(frame_busqueda_medico, text="Agregar Médico", font=("Robot", 11, "bold"),bg="#e6c885")
        btn_nuevo_medico.grid(row = 0, column=6, padx=15)

        #Frame para los datos del medico
        frame_datos_medico = Label(frame_medico, bg="#c9c2b2", font=("Robot", 10))
        frame_datos_medico.pack(pady=5)

        campos_medico = ["Nombre del médico", "Apellido del médico", "Especialidad", "Tipo de matrícula", "Matrícula"]
        entradas_medico = {}
        for m, campo in enumerate(campos_medico):
            Label(frame_datos_medico, text=campo + ":", bg="#c9c2b2", font=("Robot", 12), justify=LEFT).grid(row=0, column=m, padx=8)
            entry = Entry(frame_datos_medico, width=25, font=("Robot", 12))
            entry.grid(row=1, column=m, padx=8)
            entradas_medico[campo] = entry

        #Frame para los datos del tratamiento
        frame_tratamiento = LabelFrame(frame_agregar, text="Tratamiento", font=("Robot", 10), bg="#c9c2b2") 
        frame_tratamiento.pack(fill="x")

        buscar_tratamiento = Frame(frame_tratamiento, bg="#c9c2b2")
        buscar_tratamiento.pack(fill="x", pady=5)
        Label(buscar_tratamiento, text="Buscar:", bg="#c9c2b2",font=("Robot", 13)).grid(row=0, column=1, padx=5, pady=2, sticky= W)
        self.buscar_tratamiento = Entry(buscar_tratamiento, width=20,font=("Robot",12))
        self.buscar_tratamiento.grid(row=0, column=2, padx=5, pady=2, sticky= W)
        img_buscar = Image.open("buscar1.png").resize((20, 20), Image.Resampling.LANCZOS)
        img_buscar = ImageTk.PhotoImage(img_buscar)
        btn_buscar = Button(buscar_tratamiento, image=img_buscar, width=25, height=25,bg="#e6c885")
        btn_buscar.grid(row=0, column=3, sticky= W)
        btn_buscar.image = img_buscar

        buscar_tratamiento.columnconfigure(4, weight=2)
        buscar_tratamiento.columnconfigure(5, weight=2)

        btn_nuevo_tratamiento = Button(buscar_tratamiento, text="Agregar Tratamiento", font=("Robot", 11, "bold"),bg="#e6c885")
        btn_nuevo_tratamiento.grid(row = 0, column=6, padx=15)

        campos_tratamiento = ["Código", "Nombre del procedimiento", "Precio"]

        #Tabla para mostar los tratamientos
        frame_tabla_tratamientos = Frame(frame_tratamiento, bg="#c9c2b2", width= 500)  # Frame para contener la tabla y el scrollbar
        frame_tabla_tratamientos.pack(expand=True)
        
        estilo = ttk.Style()
        estilo.configure("Treeview", font=("Robot",11), rowheight=10)  # Cambia la fuente y el alto de las filas
        estilo.configure("Treeview.Heading", font=("Robot",14), padding= [0, 10])  # Cambia la fuente de las cabeceras
        
        #Treeview para mostrar la tabla de tratamientos dentro del frame_tabla
        self.arbol_ficha = ttk.Treeview(frame_tabla_tratamientos, columns=("Código", "Nombre", "Precio"), show='headings', height=16)
        self.arbol_ficha.pack(expand=True, fill="both")

        #Títulos de columnas
        self.arbol_ficha.heading("Código", text="Código")
        self.arbol_ficha.heading("Nombre", text="Nombre")
        self.arbol_ficha.heading("Precio", text="Precio")

        #Ancho de las columnas y datos centrados
        self.arbol_ficha.column("Código", anchor='center', width=200, stretch=False)
        self.arbol_ficha.column("Nombre", anchor='center', width=200, stretch=False)
        self.arbol_ficha.column("Precio", anchor='center', width=200, stretch=False)

        #Frame botones
        frame_botones = Frame(ventana_agregar, bg="#e4c09f")
        frame_botones.pack()

        btn_nueva_ficha = Button(frame_botones, text="Agregar", font=("Robot", 15),bg="#e6c885", width= 15)
        btn_nueva_ficha.grid(row = 0, column=0, columnspan=2, padx=20)

        btn_volver = Button(frame_botones, text="Volver", font=("Robot", 15),bg="#e6c885", width=15, command= ventana_agregar.destroy)
        btn_volver.grid(row = 0, column=3, columnspan=2, padx=20)

"""
    def guardar_nueva_ficha(self, entry, ventana):
        nombre = entry["Nombre"].get()      #Obtenemos los valores que el usuario ingresó.
        apellido = entry["Apellido"].get()
        dni = entry["DNI"].get()
        obra_social = entry["Obra social"].get()
        propietario = entry["Propietario del Plan"].get()
        telefono = entry["Teléfono"].get()
        nro_afiliado = entry["Número de Afiliado"].get()
        nombre_medico = entry["Nombre del médico"].get()
        apellido_medico = entry["Apellido del médico"].get()
        especialidad = entry ["Especialidad"].get()
        tipo_matricula = entry ["Tipo de matrícula"].get()
        matricula = entry ["Matrícula"].get()
        servicio = entry ["Servicio"].get()
        fecha = entry["Fecha de prestación médica"].get()
        codigo =entry["Código"].get()
        nombre_procedimiento=entry["Nombre del procedimiento"].get()
        precio=entry["Precio"].get()
        tipo_tratamiento=entry["Tipo de tratamiento"].get()
        siglas=entry["Siglas"].get()

        # Validar datos y agregar al Treeview
        if nombre and apellido and dni and obra_social and propietario and telefono and nro_afiliado and nombre_medico and apellido_medico and especialidad and tipo_matricula and matricula and servicio and fecha and codigo and nombre_procedimiento and precio and tipo_tratamiento and siglas:
            try:
                conexion = mysql.connector.connect(host="localhost", user="root", password="12345", database="recupero_obra_social")
                cursor = conexion.cursor()
                query = 
                INSERT INTO ficha (nombre, apellido, dni, obra_social, propietario, telefono, nro_afiliado, nombre_medico, apellido_medico, especialidad, tipo_matricula,
                matricula, servicio, fecha, codigo, nombre_procedimiento, precio, tipo_tratamiento, siglas)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                
                cursor.execute(query, (nombre, apellido, dni, obra_social, propietario, telefono, nro_afiliado,nombre_medico, apellido_medico, especialidad, tipo_matricula,
                matricula, servicio, fecha, codigo, nombre_procedimiento, precio, tipo_tratamiento, siglas))
                conexion.commit()
                messagebox.showinfo("Información", "Paciente agregado correctamente.")
                ventana.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al agregar la ficha: {err}")
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()
        else:
            messagebox.showwarning("Atención", "Complete todos los campos.")

    def ver_ficha(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione una ficha.")
            return
        
        ficha_seleccionada = self.tree.item(seleccion[0], 'values')   #Item= valor del elemento
        self.abrir_ventana_ficha(ficha_seleccionada,seleccion[0],modo="ver")

    def modificar_ficha(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione una ficha.")
            return
        
        ficha_seleccionada = self.tree.item(seleccion[0], 'values')
        self.abrir_ventana_ficha(ficha_seleccionada, seleccion[0],modo="modificar")    
    
    def abrir_ventana_ficha(self, ficha, id_seleccionado, modo="ver"):
        ventana = Toplevel(self)
        ventana.title("Detalles de la Ficha")
        ventana.config(bg="#e4c09f")
        ventana.resizable(False,False)
        ventana.geometry("+400+160")
        ventana.wm_geometry("+500+0")
        
        ventana.grid_columnconfigure(0, weight=1)
        ventana.grid_rowconfigure(0, weight=1)

        frame_detalles = LabelFrame(ventana, text="Detalles la ficha", font=("Robot", 10), padx=10, pady=10, bg="#c9c2b2")
        frame_detalles.grid(row=0, column=0, padx=10, pady=1, sticky="nsew")

        campos = ["Nombre" ,"Apellido", "DNI", "Obra social", "Propietario del Plan", "Teléfono",
         "Número de Afiliado", "Nombre del médico", "Apellido del médico","Especialidad","Tipo de matrícula", "Matrícula",
        "Servicio", "Fecha de prestación médica", "Código", "Nombre del procedimiento", "Precio", "Tipo de tratamiento", "Siglas"] #ejemplo
        id_fichas = ficha[0]
        #entradas ={}

        try:
            conexion = mysql.connector.connect(host="localhost", user="root", password="12345", database="recupero_obra_social")
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre, apellido, dni, obra_social, propietario, telefono, nro_afiliado, nombre_medico, apellido_medico, especialidad, tipo_matricula, matricula, servicio, fecha, codigo, nombre_procedimiento, precio, tipo_tratamiento, siglas  FROM paciente WHERE id_fichas = %s", (id_fichas,))
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

        vcqmd_letras = ventana.register(self.solo_letras)
        vcmd_numeros = ventana.register(self.solo_numeros)


        for i, campo in enumerate(campos):
            etiqueta = Label(frame_detalles, text=campo + ":", bg="#c9c2b2", font=("Robot", 10))
            etiqueta.grid(row=i, column=0, padx=10, pady=5)
            entry = Entry(frame_detalles, width=40)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry.insert(0, campos[i])
            entradas[campo] = entry
            

            if modo == "ver":
                entry.config(state="readonly")
                btn_editar = Button(ventana, text="Modificar", width=15, font=("Robot", 13), bg="#e6c885",
                                    command=lambda: self.activar_edicion(entradas, btn_guardar))
                btn_editar.grid(row=len(campos), column=0, pady=10)

    
                btn_guardar = Button(frame_detalles, text="Guardar Cambios", 
                                     command=lambda: self.guardar_cambios(entradas, ventana, id_seleccionado))
                btn_guardar.grid(row=len(campos), column=0, columnspan=2, padx=10, pady=10)
                btn_guardar.config(state="disabled")  # Iniciar como deshabilitado
                                

        if modo == "modificar":
            btn_modificar = Button(frame_detalles, text="Guardar Cambios", 
                                   command=lambda: self.guardar_cambios(entradas, ventana, id_seleccionado), bg="#e6c885")
            btn_modificar.grid(row=len(campos), column=0, columnspan=2, padx=10, pady=10)

    def activar_edicion(self, entradas, btn_guardar):
    # Habilitar la edición en las entradas
        for entry in entradas.values():
            entry.config(state="normal")  # Permitir edición en todos los Entry
        
        # Activar el botón "Guardar Cambios"
        btn_guardar.config(state="normal")  # Activar el botón directamente

    def guardar_cambios(self, entradas, ventana,seleccion):
        #base de datos
        #messagebox.showinfo("Información", "Cambios guardados correctamente.")# Obtener los nuevos valores de todas las entradas
        nuevos_valores = {campo: entradas[campo].get() for campo in entradas}
        id_ficha = self.tree.item(seleccion, 'values')[0]
        
        try:
            conexion = mysql.connector.connect(host="localhost", user="root", password="12345", database="recupero_obra_social")
            cursor = conexion.cursor()
            query = 
            UPDATE ficha
            SET nombre = %s, apellido = %s, dni = %s, obra_social = %s, propietario = %s, telefono = %s, nro_afiliado = %s, nombre_medico = %s, apellido_medico = %s, especialidad = %s, tipo_matricula = %s,
            matricula = %s, servicio = %s, fecha = %s, codigo = %s, nombre_procedimiento = %s, precio = %s, tipo_tratamiento = %s, siglas = %s
            WHERE id_ficha = %s
            cursor.execute(query, (
                nuevos_valores["Nombre"], nuevos_valores["Apellido"], nuevos_valores["DNI"], nuevos_valores["Obra Social"],
                nuevos_valores["Propietario del Plan"], nuevos_valores["Teléfono"],
                nuevos_valores["Número de Afiliado"], nuevos_valores["Nombre del médico"], nuevos_valores["Apellido del médico"],nuevos_valores["Especialidad"],
                nuevos_valores["Especialidad"],nuevos_valores["Tipo de matrícula"],nuevos_valores["Matrícula"], nuevos_valores["Servicio"],nuevos_valores["Fecha de prestación médica"],
                nuevos_valores["Código"],nuevos_valores["Nombre del procedimiento"],nuevos_valores["Precio"],nuevos_valores["Tipo de tratamiento"],
                nuevos_valores["Siglas"], id_ficha
            ))
            conexion.commit()
            
            # Actualizar los valores en el Treeview
            self.tree.item(seleccion, values=(id_ficha, *nuevos_valores.values()))
            
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

    def eliminar_ficha(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione un paciente para eliminar.")
            return
        
        ficha_seleccionada = self.tree.item(seleccion[0], "values")
        id_ficha = ficha_seleccionada[0]  # Asumiendo que el ID es el primer valor
        
        #Pregunta al usuario si está seguro de eliminar 
        respuesta = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar la ficha seleccionada?")
        if respuesta:  
            try:
                conexion= mysql.connector.connect(host="localhost", user="root", password="12345", database="recupero_obra_social")
                cursor = conexion.cursor()
                cursor.execute("UPDATE paciente SET activo = 0 WHERE id_paciente = %s", (id_ficha,))
                conexion.commit()
                messagebox.showinfo("Éxito", "ficha eliminada correctamente.")
                self.tree.delete(seleccion)
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al eliminar la ficha: {err}")
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()

    def buscar_ficha(self):
        busqueda = self.entrada_buscar.get().strip().lower() 
        if not busqueda:
            self.tree.delete(*self.tree.get_children())
            self.cargar_ficha()
            return

        try:
            conexion = mysql.connector.connect(host="localhost", user="root", password="12345", database="recupero_obra_social")
            cursor = conexion.cursor()
            query =
            SELECT id_ficha, nombre, apellido, dni, obra_social, propietario, telefono, nro_afiliado, nombre_medico, apellido_medico, especialidad, tipo_matricula,
            matricula, servicio, fecha, codigo, nombre_procedimiento, precio, tipo_tratamiento, siglas
            FROM ficha 
            WHERE LOWER(nombre) LIKE %s OR LOWER(apellido) LIKE %s OR dni LIKE %s
        
            like_pattern = f"%{busqueda}%"
            cursor.execute(query, (like_pattern, like_pattern, like_pattern))
            fichas = cursor.fetchall()
            
            self.tree.delete(*self.tree.get_children())
            for ficha in fichas:
                self.tree.insert("", "end", values=fichas)
            
            if not fichas:
                messagebox.showwarning("Atención", "No se encontró la ficha.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al buscar la ficha: {err}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()


        #Obtenemos búsqueda
        for item in self.tree.get_children():         #Recorre cada fila usando identificador en la lista devuelta por children
            valores = self.tree.item(item, 'values')  #Obtiene los valores de las columnas de la fila correspondiente al identificador item.
            nombre = valores[1].lower()
            apellido = valores[2].lower()
            dni = valores[0].lower()
            if busqueda in nombre or busqueda in dni or busqueda in apellido:
                self.tree.selection_set(item)         #Selecciona el tratamiento.
                self.tree.see(item)                   #Hace visible el tratamiento.
                ficha_encontrada = True
            else:
                self.tree.detach(item)                #Oculta los otros tratamientos.
       
            
        if not ficha_encontrada:

            messagebox.showwarning("Atención", "No se encontró la ficha.")

    def cargar_ficha(self):
        try:
            conexion = mysql.connector.connect(host="localhost", user="root", password="12345", database="recupero_obra_social")
            cursor = conexion.cursor()
            cursor.execute("SELECT id_ficha, nombre, apellido, dni, obra_social FROM ficha")
            fichas = cursor.fetchall()
            for ficha in fichas:
                self.tree.insert("", "end", values=ficha)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al cargar las fichas: {err}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
"""
ventana = Tk()
ventana.title("Gestion de Fichas")
ventana.resizable(False,False)
ventana.geometry("+0+0")
root = GestionFicha(ventana)
ventana.mainloop()