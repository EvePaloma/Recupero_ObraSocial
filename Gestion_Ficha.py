from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
from ConexionBD import *
from datetime import datetime

class GestionFicha(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg="#e4c09f", width= 1370, height=700)
        self.master = master
        self.pack_propagate(False)
        self.pack(expand=True)
        self.createWidgets()
        self.actualizar_treeview()

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

    def conexion_bd_os(self, id):
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM obra_social WHERE id_obra_social = %s", (id,))
            obra_social = cursor.fetchall()
            print(obra_social)
            return obra_social
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se pudo recuperar la obra social: {error}")
        finally:
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
    def volver_inicio(self):
        self.ventana_agregar.destroy()
        self.master.deiconify()

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
    
    #Función para generar el inicio
    def createWidgets(self):
        frame_fichas = LabelFrame(self, text="Gestión de Fichas", bg="#c9c2b2", height=800, width=1250)
        frame_fichas.pack_propagate(False)
        frame_fichas.pack(expand=True)

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
        frame_tabla.pack(expand=True, fill= "x", padx= 25)
        
        stilo = ttk.Style()
        stilo.configure("Inicio.Treeview", font=("Robot",11), rowheight=21)  # Cambia la fuente y el alto de las filas
        stilo.configure("Inicio.Treeview.Heading", font=("Robot",14), padding= [0, 5])  # Cambia la fuente de las cabeceras
        
        #Treeview para mostrar la tabla de tratamientos dentro del frame_tabla
        self.tree = ttk.Treeview(frame_tabla, columns=("DNI", "Nombre" ,"Apellido", "Obra Social", "Fecha prestación", "Total"), show='headings', height=15, style = "Inicio.Treeview")
        self.tree.pack(expand=True, fill="both")

        #Títulos de columnas
        self.tree.heading("DNI", text="DNI")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("Obra Social", text="Obra Social")
        self.tree.heading("Fecha prestación", text="Fecha prestación")
        self.tree.heading("Total", text="Total")

        #Ancho de las columnas y datos centrados
        self.tree.column("DNI", anchor='center', width=150)
        self.tree.column("Nombre", anchor='center', width=200)
        self.tree.column("Apellido", anchor='center', width=200)
        self.tree.column("Obra Social", anchor='center', width=300)
        self.tree.column("Fecha prestación", anchor='center', width=200)
        self.tree.column("Total", anchor='center', width=150)

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
        btn_ver = Button(frame_btn, text="Ver", width=15, font=("Robot",15),bg="#e6c885", command= self.ver_ficha)
        btn_ver.grid(row=0, column=1,padx=50)

        btn_editar = Button(frame_btn, text="Modificar", width=15, font=("Robot",15),bg="#e6c885")
        btn_editar.grid(row=0, column=2,padx=50)
        
        btn_eliminar = Button(frame_btn, text="Eliminar", width=15,font=("Robot",15),bg="#e6c885", command= self.eliminar_ficha)
        btn_eliminar.grid(row=0, column=3, padx=50)

        btn_volver = Button(frame_btn, text="Volver", width=15 ,font=("Robot",15), bg="#e6c885")
        btn_volver.grid(row=0, column=4, padx=50)

    #AGREGAR NUEVA FICHA 
    def agregar_ficha(self):
        self.master.withdraw()        
        self.ventana_agregar = Toplevel(self.master)
        self.ventana_agregar.title("Agregar ficha")
        self.ventana_agregar.config(bg="#e4c09f") 
        self.ventana_agregar.resizable(False,False)
        self.ventana_agregar.geometry("1370x700+0+0")

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

        btn_nuevo_paciente = Button(frame_busqueda, text="Agregar Paciente", font=("Robot", 11, "bold"),bg="#e6c885")
        btn_nuevo_paciente.grid(row = 0, column=6, padx=15)

        #Frame para los datos del PACIENTE
        self.frame_datos_pacientes = Label(frame_paciente, bg="#c9c2b2", font=("Robot", 10))
        self.frame_datos_pacientes.pack(pady=5)

        campos_arriba = ["Nombre", "Apellido", "DNI"]
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
        frame_medico = LabelFrame(frame_agregar, text="Datos del médico", font=("Robot", 10), bg="#c9c2b2")
        frame_medico.pack(fill="x")

        #buscador de médico
        frame_busqueda_medico = Frame(frame_medico, bg="#c9c2b2")
        frame_busqueda_medico.pack(fill="x", pady=5)
        Label(frame_busqueda_medico, text="Buscar:", bg="#c9c2b2",font=("Robot", 13)).grid(row=0, column=1, padx=5, pady=2, sticky= W)
        self.buscar_medico = Entry(frame_busqueda_medico, width=20,font=("Robot",12))
        self.buscar_medico.grid(row=0, column=2, padx=5, pady=2, sticky= W)
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

        btn_nuevo_medico = Button(frame_busqueda_medico, text="Agregar Médico", font=("Robot", 11, "bold"),bg="#e6c885")
        btn_nuevo_medico.grid(row = 0, column=6, padx=15)

        #Frame para los datos del medico
        self.frame_datos_medico = Label(frame_medico, bg="#c9c2b2", font=("Robot", 10))
        self.frame_datos_medico.pack(pady=5, fill="x")

        campos_medico = ["Nombre del médico", "Apellido del médico", "Matrícula"]
        for m, campo in enumerate(campos_medico):
            Label(self.frame_datos_medico, text=campo + ":", bg="#c9c2b2", font=("Robot", 12), justify=LEFT).grid(row=0, column=m, padx=8, sticky=W)
            entry = Entry(self.frame_datos_medico, width=28, font=("Robot", 12))
            entry.grid(row=1, column=m, padx=8, sticky=W)
            entry.config(state="readonly")

        #Frame para los datos del TRATAMIENTOS
        frame_tratamiento = LabelFrame(frame_agregar, text="Tratamiento", font=("Robot", 10), bg="#c9c2b2") 
        frame_tratamiento.pack(fill="x")

        campos_tratamiento = ["Código", "Nombre del procedimiento", "Precio"]

        #Tabla para mostar los tratamientos
        frame_tabla_tratamientos = Frame(frame_tratamiento, bg="#c9c2b2", width= 500)  # Frame para contener la tabla y el scrollbar
        frame_tabla_tratamientos.grid(row= 0, column=0, padx= 20, pady= 5)

        Label(frame_tabla_tratamientos, text="Tratamientos aplicados", font=("Robot", 12), bg="#c9c2b2").pack(pady=5)
        
        estilo = ttk.Style()
        estilo.configure("Treeview", font=("Robot",10), rowheight=13)  # Cambia la fuente y el alto de las filas
        estilo.configure("Treeview.Heading", font=("Robot",12), padding= [0, 10])  # Cambia la fuente de las cabeceras
        
        #Treeview para mostrar la tabla de tratamientos dentro del frame_tabla
        self.arbol_ficha = ttk.Treeview(frame_tabla_tratamientos, columns=("Código", "Nombre", "Precio", "Cantidad"), show='headings', height=16, style = "Treeview")
        self.arbol_ficha.pack(expand=True, fill="both")

        #Títulos de columnas
        self.arbol_ficha.heading("Código", text="Código")
        self.arbol_ficha.heading("Nombre", text="Nombre")
        self.arbol_ficha.heading("Precio", text="Precio")
        self.arbol_ficha.heading("Cantidad", text="Cantidad")

        #Ancho de las columnas y datos centrados
        self.arbol_ficha.column("Código", anchor='center', width=150, stretch=False)
        self.arbol_ficha.column("Nombre", anchor='center', width=200, stretch=False)
        self.arbol_ficha.column("Precio", anchor='center', width=200, stretch=False)
        self.arbol_ficha.column("Cantidad", anchor='center', width=100, stretch=False)

        #Frame para los botones de agregar y eliminar tratamientos
        frame_botones_tratamiento = Frame(frame_tratamiento, bg="#c9c2b2")
        frame_botones_tratamiento.grid(row=0, column=1, columnspan=2, padx=30)

        btn_nuevo_t = Button(frame_botones_tratamiento, text="Nuevo Tratamiento", font=("Robot", 11, "bold"),bg="#e6c885", height=2, width=20)
        btn_nuevo_t.pack(pady=8)

        btn_agregar_t = Button(frame_botones_tratamiento, text="Agregar Tratamiento", font=("Robot", 11, "bold"),bg="#e6c885", height=2, width=20, command= self.mostrar_tratamientos)
        btn_agregar_t.pack(pady=8)

        btn_eliminar_t = Button(frame_botones_tratamiento, text="Eliminar Tratamiento", font=("Robot", 11, "bold"),bg="#e6c885", height=2, width=20, command= self.eliminar_tratamiento_a_ficha)
        btn_eliminar_t.pack(pady=8)

        self.total_var = StringVar()
        self.entry_total = Entry(frame_botones_tratamiento, textvariable=self.total_var, font=("Robot", 15), state='readonly', width=8)
        self.entry_total.pack(pady=8)

        #Frame botones
        frame_botones = Frame(self.ventana_agregar, bg="#e4c09f")
        frame_botones.pack()

        btn_guardar_ficha = Button(frame_botones, text="Guardar", font=("Robot", 15),bg="#e6c885", width= 15, command= lambda: self.guardar_nueva_ficha(self.datos_ficha, self.ventana_agregar))
        btn_guardar_ficha.grid(row = 0, column=0, columnspan=2, padx=20)

        btn_volver = Button(frame_botones, text="Volver", font=("Robot", 15),bg="#e6c885", width=15, command= self.volver_inicio)
        btn_volver.grid(row = 0, column=3, columnspan=2, padx=20)

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
            print(resultado)
            return resultado[0]
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Consulta", f"No se pudo realizar la consulta a la base de datos: {err}. Error 2")
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return
    def obtener_unico(self, elemento, tabla):
        conexion = obtener_conexion()
        print(elemento)
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
    def buscar_elemento(self, tabla):
        if tabla == "paciente":
            elemento = self.buscar_paciente.get()
            if not elemento:
                messagebox.showwarning("Atención", "Ingrese un DNI para buscar.")
                ventana.lift()
                return
            if not elemento.isdigit():
                messagebox.showwarning("Atención", "Ingrese un DNI válido.")
                ventana.lift()
                return
            resultado = self.buscar_elemento_tabla(elemento, "paciente")
            print(resultado[0])
            if resultado[0] == 0:
                messagebox.showwarning("Atención", "No se encontró ningún paciente con ese DNI.")
                ventana.lift()
                return
            elif resultado[0] == 1:
                valores = self.obtener_unico(elemento, "paciente")
                campos_arriba = ["Nombre", "Apellido", "DNI"]
                campos_abajo = ["Obra Social", "Número de Afiliado"]
                print(valores)
                self.datos_ficha["Id_paciente"] = valores[0]
                for i, campos_arriba in enumerate(campos_arriba):
                    Label(self.frame_datos_pacientes, text=campos_arriba + ":", bg="#c9c2b2", font=("Robot", 12), justify=LEFT).grid(row=0, column=i, padx=10, sticky=W)
                    entry = Entry(self.frame_datos_pacientes, width=40, font=("Robot", 12))
                    entry.grid(row=1, column=i, padx=10)
                    if campos_arriba == "DNI":
                        entry.insert(0, valores[4])
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
                        print(valores[5])
                        nombre = self.conexion_bd_os(valores[5])
                        print(nombre)
                        entry.insert(0, nombre[0][1])
                        self.datos_ficha[campos_abajo] = valores[5]  #guarda el id de la obra social
                    elif campos_abajo == "Número de Afiliado":
                        entry.insert(0, valores[6])
                        self.datos_ficha[campos_abajo] = entry      #guarda el número de afiliado
                    entry.config(state="readonly")
                self.buscar_paciente.delete(0, END)
                if valores is None:
                    return
            else:
                messagebox.showwarning("Atención", "Se encontraron varios pacientes con ese DNI.")
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
            print(id_tratamiento, item_values, cantidad)
            self.arbol_ficha.insert("", "end", iid = id_tratamiento ,values= (item_values[1], item_values[0], item_values[2], cantidad))
            self.actualizar_total_precios()
    def eliminar_tratamiento_a_ficha(self):
        selected_item = self.arbol_ficha.selection()
        if selected_item:
            # Eliminar el elemento del Treeview de la ficha
            self.arbol_ficha.delete(selected_item)
            # Actualizar el total de precios
            self.actualizar_total_precios()

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

        self.ventana_tratamientos = Toplevel()
        self.ventana_tratamientos.title("Tratamientos")
        self.ventana_tratamientos.geometry("680x450")
        self.ventana_tratamientos.config(bg="#e4c09f")

        #Buscar tratamiento por nombre, codigo
        frame_busqueda = Frame(self.ventana_tratamientos, bg="#e6c885")
        frame_busqueda.pack()

        #Widgets de búsqueda dentro del frame más chico
        etiqueta_buscar = Label(frame_busqueda, text="Buscar:", bg="#e6c885",font=("Robot",11))
        etiqueta_buscar.grid(row=1, column=1, padx=5, pady=5)

        self.entrada_buscar = Entry(frame_busqueda,width="40",font=("Robot",10))
        self.entrada_buscar.grid(row=1, column=2, padx=5, pady=5)

        img_buscar = Image.open("buscar1.png").resize((25, 25), Image.Resampling.LANCZOS)
        img_buscar = ImageTk.PhotoImage(img_buscar)
        btn_buscar = Button(frame_busqueda, image=img_buscar, width=25, height=25,bg="#e6c885",command= buscar_tratamiento)
        
        btn_buscar.grid(row=1, column=3)
        btn_buscar.image = img_buscar

        # Crear el Treeview para ver los tratamientos
        stilo = ttk.Style()
        stilo.configure("Custom.Treeview", font=("Robot",11), rowheight=22)  # Cambia la fuente y el alto de las filas
        stilo.configure("Custom.Treeview.Heading", font=("Robot",14), padding= [0, 10])  # Cambia la fuente de las cabeceras

        self.tree_tratamiento = ttk.Treeview(self.ventana_tratamientos, columns=("Nombre", "Código", "Precio"), show='headings', style="Custom.Treeview")
        self.tree_tratamiento.heading("Nombre", text="Nombre")
        self.tree_tratamiento.heading("Código", text="Código")
        self.tree_tratamiento.heading("Precio", text="Precio")

        self.tree_tratamiento.column("Nombre", anchor='center', width=200, stretch=False)
        self.tree_tratamiento.column("Código", anchor='center', width=100, stretch=False)
        self.tree_tratamiento.column("Precio", anchor='center', width=100, stretch=False)
        self.tree_tratamiento.pack(pady=15)

        self.actualizar_treeview_tratamiento()

        self.cantidad_var = ttk.Combobox(self.ventana_tratamientos, values=[str(i) for i in range(1, 10)], state="readonly", width=8, height=2)
        self.cantidad_var.pack()
        self.cantidad_var.current(0)

        # Crear el frame para los botones
        frame_botones = Frame(self.ventana_tratamientos)
        frame_botones.pack(pady=10)

        # Botón Agregar
        btn_agregar = Button(frame_botones, text="Agregar", font=("Robot", 11, "bold"), bg="#e6c885", height=1, width=10, command= self.agregar_tratamiento_a_ficha)
        btn_agregar.grid(row=0, column=0, padx=10)

        # Botón Volver
        btn_volver = Button(frame_botones, text="Volver", font=("Robot", 11, "bold"), bg="#e6c885", height=1, width=10, command=self.ventana_tratamientos.destroy)
        btn_volver.grid(row=0, column=1, padx=10)

    #Funciones para conectar con la base de datos
    #Funciones para subir los datos en la base de datos
    def guardar_nueva_ficha(self, entry, ventana):
        conexion = obtener_conexion()
        
        id_paciente = self.datos_ficha["Id_paciente"]
        nombre = entry["Nombre"].get()      #Obtenemos los valores que el usuario ingresó.
        apellido = entry["Apellido"].get()
        dni = entry["DNI"].get()
        obra_social = self.datos_ficha["Obra Social"]
        nro_afiliado = entry["Número de Afiliado"].get()
        id_medico = self.datos_ficha["Id_medico"]
        nombre_medico = entry["Nombre del médico"].get()
        apellido_medico = entry["Apellido del médico"].get()
        matricula = entry ["Matrícula"].get()
        total = self.total_var.get()
        fecha = datetime.now()
        print(id_paciente, nombre, apellido, dni, obra_social, nro_afiliado, id_medico, nombre_medico, apellido_medico, matricula, total, fecha)

        # Validar datos y agregar al Treeview
        if nombre and apellido and dni and obra_social and nro_afiliado and nombre_medico and apellido_medico and matricula and total and fecha:
            try:
                cursor = conexion.cursor()
                sql = "INSERT INTO ficha (id_paciente, id_obra_social, nro_afiliado ,id_medico, fecha, total) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (id_paciente, obra_social, nro_afiliado, id_medico, fecha, total)
                cursor.execute(sql, val)
                conexion.commit()
                #Obtenemos el id de la ficha que acabamos de agregar
                ficha_id = cursor.lastrowid
                print("ID DE FICHA", ficha_id)
                for child in self.arbol_ficha.get_children():
                    id_tratamiento = child
                    tratamiento = self.arbol_ficha.item(child, 'values')
                    print("valores para agregar", id_tratamiento, tratamiento)
                    sql = "INSERT INTO detalle_ficha (id_ficha, id_tratamiento, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)"
                    val = (ficha_id, id_tratamiento, tratamiento[3], tratamiento[2])
                    cursor.execute(sql, val)
                    conexion.commit()
                messagebox.showinfo("Información", "Ficha agregada exitosamente")
                self.tree.insert("", 0, values=(dni, nombre, apellido, obra_social, fecha, total))
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
    
    #Ver obra social seleccionada
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

    def abrir_ventana_ficha(self, ficha, modo, seleccion=None):
        def activar_edicion(entradas, btn_guardar):
            btn_guardar.config(state="normal")
            btn_nuevo_t.config(state="normal")
            btn_agregar_t.config(state="normal")
            btn_eliminar_t.config(state="normal")
            btn_buscar1.config(state="normal")
            btn_buscar2.config(state="normal")
            self.buscar_paciente.config(state="normal")
            self.buscar_medico.config(state="normal")

        ventana = Toplevel(self)
        ventana.title("Detalles de ficha")
        ventana.config(bg="#e4c09f")
        ventana.resizable(False, False)
        ventana.geometry("1370x700+0+0")

        frame_detalles = LabelFrame(ventana, text="Detalles de ficha", font=("Robot", 12), bg="#c9c2b2")
        frame_detalles.pack(ipadx=20)

        frame_btns = Frame(ventana, bg="#e4c09f")
        frame_btns.pack()

        self.datos_ficha = {}  # Diccionario para guardar los datos de la ficha

        #FRAME DE DATOS DEL PACIENTE
        frame_paciente = LabelFrame(frame_detalles, text="Datos del paciente", font=("Robot", 10), padx=10, pady=5, bg="#c9c2b2")
        frame_paciente.pack(fill="x", ipadx=10)
        #buscador de pacientes

        frame_busqueda = Frame(frame_paciente, bg="#c9c2b2")
        frame_busqueda.pack(fill="x", pady=2)
        Label(frame_busqueda, text="Buscar:", bg="#c9c2b2",font=("Robot", 13)).grid(row=0, column=1, padx=5, pady=2, sticky= W)
        self.buscar_paciente = Entry(frame_busqueda, width=20,font=("Robot",12))
        self.buscar_paciente.grid(row=0, column=2, padx=5, pady=2, sticky= W)
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
        self.frame_datos_pacientes.pack(pady=10, padx=10, fill="x")

        campos_arriba = ["Nombre", "Apellido", "DNI"]
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
        frame_medico.pack(fill="x", pady=5)

        #buscador de médico
        frame_busqueda_medico = Frame(frame_medico, bg="#c9c2b2")
        frame_busqueda_medico.pack(fill="x", pady=5)
        Label(frame_busqueda_medico, text="Buscar:", bg="#c9c2b2",font=("Robot", 13)).grid(row=0, column=1, padx=5, pady=2, sticky= W)
        self.buscar_medico = Entry(frame_busqueda_medico, width=20,font=("Robot",12))
        self.buscar_medico.grid(row=0, column=2, padx=5, pady=2, sticky= W)
        self.buscar_medico.insert(0, "MATRÍCULA")  #Agrega marcador de posición
        self.buscar_medico.config(fg="gray")
        self.buscar_medico.bind("<FocusIn>", lambda event, e=self.buscar_medico: self.limpiar_marcador(e))
        self.buscar_medico.bind("<FocusOut>", lambda event, e=self.buscar_medico: self.restaurar_marcador(e))
        img_buscar = Image.open("buscar1.png").resize((20, 20), Image.Resampling.LANCZOS)
        img_buscar = ImageTk.PhotoImage(img_buscar)
        btn_buscar2 = Button(frame_busqueda_medico, image=img_buscar, width=25, height=25,bg="#e6c885", command=lambda: self.buscar_elemento("medico"))
        btn_buscar2.grid(row=0, column=3, sticky= W)
        btn_buscar2.image = img_buscar

        #Frame para los datos del medico
        self.frame_datos_medico = Label(frame_medico, bg="#c9c2b2", font=("Robot", 10))
        self.frame_datos_medico.pack(pady=10, padx = 10,fill="x")

        campos_medico = ["Nombre del médico", "Apellido del médico", "Matrícula"]
        valores_medico= list(self.recuperar_medico(ficha[4]))
        for m, campo in enumerate(campos_medico):
            Label(self.frame_datos_medico, text=campo + ":", bg="#c9c2b2", font=("Robot", 12), justify=LEFT).grid(row=0, column=m, padx=8, sticky=W)
            entry = Entry(self.frame_datos_medico, width=28, font=("Robot", 12))
            entry.grid(row=1, column=m, padx=8, sticky=W)
            entry.insert(0, str(valores_medico[0][m]).upper())
            self.datos_ficha[campo] = entry
            entry.config(state="readonly")

        #Frame para los datos del TRATAMIENTOS
        frame_tratamiento = LabelFrame(frame_detalles, text="Tratamiento", font=("Robot", 10), bg="#c9c2b2") 
        frame_tratamiento.pack(fill="x")

        campos_tratamiento = ["Código", "Nombre del procedimiento", "Precio"]

        #Tabla para mostar los tratamientos
        frame_tabla_tratamientos = Frame(frame_tratamiento, bg="#c9c2b2", width= 500)  # Frame para contener la tabla y el scrollbar
        frame_tabla_tratamientos.grid(row= 0, column=0, padx= 20, pady= 10)

        Label(frame_tabla_tratamientos, text="Tratamientos aplicados", font=("Robot", 12), bg="#c9c2b2").pack(pady=5)
        
        estilo = ttk.Style()
        estilo.configure("Treeview", font=("Robot",10), rowheight=15)  # Cambia la fuente y el alto de las filas
        estilo.configure("Treeview.Heading", font=("Robot",12), padding= [0, 10])  # Cambia la fuente de las cabeceras
        
        #Treeview para mostrar la tabla de tratamientos dentro del frame_tabla
        self.arbol_ficha = ttk.Treeview(frame_tabla_tratamientos, columns=("Código", "Nombre", "Precio", "Cantidad"), show='headings', height=10, style = "Treeview")
        self.arbol_ficha.pack(expand=True, fill="both")

        #Títulos de columnas
        self.arbol_ficha.heading("Código", text="Código")
        self.arbol_ficha.heading("Nombre", text="Nombre")
        self.arbol_ficha.heading("Precio", text="Precio")
        self.arbol_ficha.heading("Cantidad", text="Cantidad")

        #Ancho de las columnas y datos centrados
        self.arbol_ficha.column("Código", anchor='center', width=150, stretch=False)
        self.arbol_ficha.column("Nombre", anchor='center', width=200, stretch=False)
        self.arbol_ficha.column("Precio", anchor='center', width=200, stretch=False)
        self.arbol_ficha.column("Cantidad", anchor='center', width=100, stretch=False)

        self.ingresar_tratamientos_ver_ficha(seleccion)
        #Frame para los botones de agregar y eliminar tratamientos
        frame_botones_tratamiento = Frame(frame_tratamiento, bg="#c9c2b2")
        frame_botones_tratamiento.grid(row=0, column=1, columnspan=2, padx=30)

        btn_nuevo_t = Button(frame_botones_tratamiento, text="Nuevo Tratamiento", font=("Robot", 11, "bold"),bg="#e6c885", height=2, width=20)
        btn_nuevo_t.pack(pady=8)

        btn_agregar_t = Button(frame_botones_tratamiento, text="Agregar Tratamiento", font=("Robot", 11, "bold"),bg="#e6c885", height=2, width=20, command= self.mostrar_tratamientos)
        btn_agregar_t.pack(pady=8)

        btn_eliminar_t = Button(frame_botones_tratamiento, text="Eliminar Tratamiento", font=("Robot", 11, "bold"),bg="#e6c885", height=2, width=20, command= self.eliminar_tratamiento_a_ficha)
        btn_eliminar_t.pack(pady=8)

        self.total_var = StringVar()
        self.entry_total = Entry(frame_botones_tratamiento, textvariable=self.total_var, font=("Robot", 13), state='readonly')
        self.entry_total.pack(pady=8)
        self.actualizar_total_precios()

        if modo == "ver":
            btn_nuevo_t.config(state="disabled")
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
            btn_nuevo_t.config(state="normal")
            btn_agregar_t.config(state="normal")
            btn_eliminar_t.config(state="normal")
            btn_buscar1.config(state="normal")
            btn_buscar2.config(state="normal")
            self.buscar_paciente.config(state="normal")
            self.buscar_medico.config(state="normal")

            btn_guardar = Button(frame_btns, text="Guardar Cambios", width=15, font=("Robot", 13), bg="#e6c885", command=lambda: self.guardar_cambios(self.datos_ficha, ventana, seleccion))
            btn_guardar.grid(row=len(campos), column=0,  padx=40, pady=10)

            btn_cancelar = Button(frame_btns, text="Cancelar", width=15, font=("Robot", 13), bg="#e6c885", command=ventana.destroy)
            btn_cancelar.grid(row=len(campos), column=1, padx= 40, pady=10)
    
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

    def guardar_cambios(self, entradas, ventana, seleccion):
        conexion = obtener_conexion()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return

        dni = self.datos_ficha["DNI"].get()
        id_paciente = self.buscar_ids("paciente", dni)[0]
        id_obra_social = self.buscar_ids("obra_social", self.datos_ficha["Obra Social"].get())[0]
        nro_afiliado = self.datos_ficha["Número de Afiliado"].get()
        id_medico = self.buscar_ids("medico", self.datos_ficha["Matrícula"].get())[0]
        total = self.total_var.get()

        if dni and id_paciente and id_obra_social and nro_afiliado and id_medico and total:
            try:
                cursor = conexion.cursor()
                sql1 = "UPDATE ficha SET id_paciente = %s, id_obra_social = %s, nro_afiliado = %s, id_medico = %s, fecha = %s, total = %s WHERE id_ficha = %s"
                val1 = (id_paciente, id_obra_social, nro_afiliado, id_medico, datetime.now(), total, seleccion)
                cursor.execute(sql1, val1)

                # Obtener los tratamientos actuales de la ficha
                cursor.execute("SELECT id_tratamiento FROM detalle_ficha WHERE id_ficha = %s", (seleccion,))
                tratamientos_actuales = {row[0] for row in cursor.fetchall()}
                print(tratamientos_actuales)

                # Obtener los nuevos tratamientos de la interfaz
                nuevos_tratamientos = {}
                for child in self.arbol_ficha.get_children():
                    tratamiento = self.arbol_ficha.item(child, 'values')
                    id_tratamiento = int(child)
                    nuevos_tratamientos[id_tratamiento] = tratamiento
                
                print(nuevos_tratamientos)

                # Actualizar o agregar tratamientos
                for id_tratamiento, tratamiento in nuevos_tratamientos.items():
                    print(id_tratamiento, tratamiento)
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
                print(tratamientos_a_eliminar)
                for id_tratamiento in tratamientos_a_eliminar:
                    cursor.execute("DELETE FROM detalle_ficha WHERE id_ficha = %s AND id_tratamiento = %s", (seleccion, id_tratamiento))

                conexion.commit()
                messagebox.showinfo("Información", "Ficha actualizada exitosamente")
                self.actualizar_treeview()
            except Exception as e:
                conexion.rollback()
                messagebox.showerror("Error", f"Error al actualizar la ficha: {e}")
            finally:
                cursor.close()
                conexion.close()
        else:
            messagebox.showwarning("Atención", "Complete todos los campos.")

    #Funciones para eliminar las fichas, y los detalles de la misma
    def eliminar_ficha(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione un paciente para eliminar.")
            return
        
        id_ficha = seleccion[0]  # Asumiendo que el ID es el primer valor
        print(id_ficha)
        
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

    #Funciones para buscar fichas en la base de datos
    def buscar_ficha(self):
        busqueda = self.entrada_buscar.get().strip().upper() 
        if not busqueda:
            self.tree.delete(*self.tree.get_children())
            self.actualizar_treeview()
            return

        #evalua los dni que contengan ese número
        if busqueda.isdigit():
            tratamiento_encontrado = False
            for item in self.tree.get_children():
                valores = self.tree.item(item, 'values')
                dni = valores[0]

                if busqueda in dni:
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


"""

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