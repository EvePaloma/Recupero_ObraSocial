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
        for os in lista:
            self.tree.insert("", "0", iid=os[0], values= (os[1], os[2], os[7]))
        cursor.close()
        conexion.close()
    def actualizar_treeview_tratamiento(self):
        for item in self.tree_tratamiento.get_children():
            self.tree_tratamiento.delete(item)
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT nombre, codigo, precio FROM tratamiento where activo = 1")
        tratamientos = cursor.fetchall()

        # Insertar los datos en el Treeview
        for tratamiento in tratamientos:
            self.tree_tratamiento.insert("", "end", values=tratamiento)
        cursor.close()
        conexion.close()

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
        stilo.configure("Inicio.Treeview", font=("Robot",11), rowheight=22)  # Cambia la fuente y el alto de las filas
        stilo.configure("Inicio.Treeview.Heading", font=("Robot",14), padding= [0, 10])  # Cambia la fuente de las cabeceras
        
        #Treeview para mostrar la tabla de tratamientos dentro del frame_tabla
        self.tree = ttk.Treeview(frame_tabla, columns=("DNI", "Nombre" ,"Apellido", "Obra Social", "Fecha prestación", "Total"), show='headings', height=16, style = "Inicio.Treeview")
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
        self.ventana_agregar = Toplevel(self)
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
        entradas_pacientes = {}
        for i, campos_arriba in enumerate(campos_arriba):
            Label(self.frame_datos_pacientes, text=campos_arriba + ":", bg="#c9c2b2", font=("Robot", 12), justify=LEFT).grid(row=0, column=i, padx=10, sticky=W)
            entry = Entry(self.frame_datos_pacientes, width=40, font=("Robot", 12))
            entry.grid(row=1, column=i, padx=10)
            entry.config(state="readonly")
            entradas_pacientes[campos_arriba] = entry
        for j, campos_abajo in enumerate(campos_abajo):
            Label(self.frame_datos_pacientes, text=campos_abajo + ":", bg="#c9c2b2", font=("Robot", 12), justify=LEFT).grid(row=2, column=j, padx=10, sticky=W)
            entry = Entry(self.frame_datos_pacientes, width=40, font=("Robot", 12))
            entry.grid(row=3, column=j, padx=10)
            entry.config(state="readonly")
            entradas_pacientes[campos_abajo] = entry

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
        entradas_medico = {}
        for m, campo in enumerate(campos_medico):
            Label(self.frame_datos_medico, text=campo + ":", bg="#c9c2b2", font=("Robot", 12), justify=LEFT).grid(row=0, column=m, padx=8, sticky=W)
            entry = Entry(self.frame_datos_medico, width=28, font=("Robot", 12))
            entry.grid(row=1, column=m, padx=8, sticky=W)
            entry.config(state="readonly")
            entradas_medico[campo] = entry

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
        self.entry_total = Entry(frame_botones_tratamiento, textvariable=self.total_var, font=("Robot", 13), state='readonly')
        self.entry_total.pack(pady=8)

        #Frame botones
        frame_botones = Frame(self.ventana_agregar, bg="#e4c09f")
        frame_botones.pack()

        btn_guardar_ficha = Button(frame_botones, text="Guardar", font=("Robot", 15),bg="#e6c885", width= 15, command= lambda: self.guardar_nueva_ficha(self.datos_ficha, self.ventana_agregar))
        btn_guardar_ficha.grid(row = 0, column=0, columnspan=2, padx=20)

        btn_volver = Button(frame_botones, text="Volver", font=("Robot", 15),bg="#e6c885", width=15, command= self.ventana_agregar.destroy)
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
            return resultado
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
            if resultado[0] == 0:
                messagebox.showwarning("Atención", "No se encontró ningún paciente con ese DNI.")
                ventana.lift()
                return
            elif resultado[0] == 1:
                paciente = self.obtener_unico(elemento, "paciente")
                campos_arriba = ["Nombre", "Apellido", "DNI"]
                campos_abajo = ["Obra Social", "Número de Afiliado"]
                valores = list(paciente[0])
                self.datos_ficha["Id_paciente"] = valores[0]
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
                        self.datos_ficha[campos_abajo] = valores[6]  #guarda el id de la obra social
                    elif campos_abajo == "Número de Afiliado":
                        entry.insert(0, valores[7])
                        self.datos_ficha[campos_abajo] = entry      #guarda el número de afiliado
                    entry.config(state="readonly")
                self.buscar_paciente.delete(0, END)
                if paciente is None:
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
                medico = self.obtener_unico(elemento, "medico")
                campos_medico = ["Nombre del médico", "Apellido del médico", "Matrícula"]
                valores = list(medico[0])
                self.datos_ficha["Id_medico"] = valores[0]
                for m, campo in enumerate(campos_medico):
                    Label(self.frame_datos_medico, text=campo + ":", bg="#c9c2b2", font=("Robot", 12), justify=LEFT).grid(row=0, column=m, padx=8, sticky= W)
                    entry = Entry(self.frame_datos_medico, width=28, font=("Robot", 12))
                    entry.grid(row=1, column=m, padx=8)
                    entry.insert(0, valores[m+1])
                    entry.config(state="readonly")
                    self.datos_ficha[campo] = entry # Guarda la entrada en un diccionario
                self.buscar_medico.delete(0, END)
                if medico is None:
                    return
    
    #Funciones para agregar, eliminar y calcular el total de los tratamientos en la ficha
    def actualizar_total_precios(self):
            total = 0.0
            for child in self.arbol_ficha.get_children():
                precio = float(self.arbol_ficha.item(child, 'values')[2])
                cantidad = int(self.arbol_ficha.item(child, 'values')[3])
                total += precio * cantidad
            self.total_var.set(f"{total:.2f}")
    def agregar_tratamiento_a_ficha(self):
        # Obtener el elemento seleccionado
        selected_item = self.tree_tratamiento.selection()
        if selected_item:
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
            self.arbol_ficha.insert("", "end", values= (item_values[0], item_values[1], item_values[2], cantidad))
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

        # Validar datos y agregar al Treeview
        if nombre and apellido and dni and obra_social and nro_afiliado and nombre_medico and apellido_medico and matricula and total:
            try:
                cursor = conexion.cursor()
                sql = "INSERT INTO ficha (id_paciente, id_medico, fecha, total) VALUES (%s, %s, %s, %s)"
                val = (id_paciente, id_medico, datetime.now(), total)
                cursor.execute(sql, val)
                conexion.commit()
                cursor.close()
                messagebox.showinfo("Información", "Ficha agregada exitosamente")
                self.tree.insert("", 0, values=(dni, nombre, apellido, obra_social, datetime.now().strftime("%d/%m/%Y"), total))
                ventana.destroy()
                self.actualizar_treeview()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al agregar la ficha: {err}")
            finally:
                conexion.close()
        else:
            messagebox.showwarning("Atención", "Complete todos los campos.")

"""
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