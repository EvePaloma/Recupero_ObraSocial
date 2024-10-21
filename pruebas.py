from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from ConexionBD import *

class Gestion_Obra_Social(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg="#e4c09f", height= 680, width=1300)
        self.master = master
        self.pack_propagate(False)
        self.pack(expand=True)
        self.createWidgets()
        self.actualizar_lista_os()

    #Ingresar datos en la tabla de obras sociales
    def actualizar_lista_os(self):
        self.tree.delete(*self.tree.get_children())
        lista_os = obtener_datos("obra_social", ["nombre", "siglas", "cuit"])
        print(lista_os)
        for os in lista_os:
            self.tree.insert("", END, values=os)

    #al seleccionar una opción en la compo, retorna el id
    def on_seleccion(self, event):
        seleccion = self.combo_afip.get()
        self.id_seleccionado = datos_afip[seleccion]
        return self.id_seleccionado

    #Funciones que AGREGAN obra social
    def agregar_OS(self):
        ventana_agregar = Toplevel(self)
        ventana_agregar.title("Agregar Tratamiento")
        ventana_agregar.config(bg="#e4c09f") 
        ventana_agregar.resizable(False,False)
        ventana_agregar.geometry("+380+150")

        frame_agregar = LabelFrame(ventana_agregar, text="Agregar Nueva Obra Social", font= ("Robot", 12),padx=10, pady=10, bg="#c9c2b2")
        frame_agregar.pack(expand=True)

        campos = ["Nombre", "Siglas", "Teléfono", "Detalle", "Domicilio Casa Central", "Domicilio Carlos Paz", "CUIT", "Carácter de AFIP"]
        entradas = {}

        for i, campo in enumerate(campos):     #Devuelve índice y valor de cada elemento 
            Label(frame_agregar, text=campo + ":", bg="#c9c2b2", font=("Robot", 12)).grid(row=i, column=0, padx=10, pady=5, sticky=W)
            #Ingresa los elementos en la combo box y devuelve el valor de la seleccion
            if campo == "Carácter de AFIP":
                lista_afip = obtener_datos("afip", ["id_afip", "nombre"])
                # Crear un diccionario para buscar el ID por el nombre
                datos_afip = {dato[1]: dato[0] for dato in lista_afip} 
                self.combo_afip = ttk.Combobox(frame_agregar, width=49, font=("Robot", 10), state="readonly")
                self.combo_afip['values'] = list(datos_afip.keys())
                self.combo_afip.grid(row=i, column=1, padx=10, pady=5)
                self.combo_afip.set(self.combo_afip['values'][0])  # Seleccionar el primer valor por defecto
                self.combo_afip.bind("<<ComboboxSelected>>", self.on_seleccion) 
            else:
                entry = Entry(frame_agregar, width=40, font=("Robot", 12))
                entry.grid(row=i, column=1, padx=10, pady=5)
            entradas[campo] = entry

        btn_nueva_os = Button(frame_agregar, text="Agregar", font=("Robot", 12),bg="#e6c885", width= 15, command=lambda: self.guardar_nueva_OS(entradas, ventana_agregar))
        btn_nueva_os.grid(row=len(campos), column=0, columnspan=2, padx=10, pady=10)
    
    def guardar_nueva_OS(self, entry, ventana):
        nombre = entry["Nombre"].get()
        siglas = entry["Siglas"].get()
        telefono = entry["Teléfono"].get()
        detalle = entry["Detalle"].get()
        domicilio_cc = entry["Domicilio Casa Central"].get()
        domicilio_cp = entry["Domicilio Carlos Paz"].get()
        cuit = entry["CUIT"].get()
        id_afip = entry["Carácter de AFIP"].get()

        # Validar datos y agregar a la base de datos
        if nombre and siglas and telefono and cuit and id_afip:
            insertar_os(nombre, siglas, telefono, detalle, domicilio_cc, domicilio_cp, cuit, id_afip)
        else:
            messagebox.showwarning("Atención", "Por favor, complete todos los campos.")
    
    #Funciones que VEN y MODIFICAN obra social
    def ver_OS(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione un tratamiento.")
            return

        # Usamos el primer elemento seleccionado (ID oculto)
        id_seleccionado = seleccion[0]
        
        # Obtenemos el tratamiento usando el ID
        tratamiento_seleccionado = self.obtener_tratamiento_por_id(id_seleccionado)

        if tratamiento_seleccionado:
            # Abrimos la ventana sin mostrar el ID
            tratamiento_reducido = tratamiento_seleccionado[0:]  # Aquí excluimos el ID
            self.abrir_ventana_tratamiento(tratamiento_reducido, modo="ver",seleccion=id_seleccionado)  # Excluimos el ID
        else:
            messagebox.showerror("Error", "No se pudo obtener el tratamiento.")
    
    def modificar_OS(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione una obra social.")
            return
        
        tratamiento_seleccionado = self.tree.item(seleccion[0], 'values')
        self.abrir_ventana_OS(tratamiento_seleccionado, seleccion[0],modo="modificar")

    def abrir_ventana_OS(self, id_seleccionado, modo="ver"):
        def guardar_cambios(entradas, ventana, seleccion):
            #base de datos
            #messagebox.showinfo("Información", "Cambios guardados correctamente.")# Obtener los nuevos valores de todas las entradas
            nuevos_valores = {campos: entradas[campos].get() for campos in entradas}
            self.tree.item(seleccion, values=list(nuevos_valores.values()))
            # Mostrar mensaje de confirmación
            messagebox.showinfo("Información", "Cambios guardados correctamente.")
            # Cerrar la ventana después de guardar
            ventana.destroy()

        def activar_edicion(entradas, btn_guardar):
            # Habilitar la edición en las entradas
            for entry in entradas.values():
                entry.config(state="normal")  # Permitir edición en todos los Entry
            # Activar el botón "Guardar Cambios"
            btn_guardar.config(state="normal")  # Activar el botón directamente

        ventana = Toplevel(self)
        ventana.title("Detalles de la Obra Social")
        ventana.config(bg="#e4c09f")
        ventana.resizable(False,False)
        ventana.geometry("+400+160")
        
        ventana.grid_columnconfigure(0, weight=1)
        ventana.grid_rowconfigure(0, weight=1)

        frame_detalles = LabelFrame(ventana, text="Detalles de la Obra Social", font=("Robot", 10), padx=10, pady=10, bg="#c9c2b2")
        frame_detalles.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        campos = ["Nombre", "Siglas", "Teléfono", "Detalle", "Domicilio Casa Central", "Domicilio Carlos Paz", "CUIT", "Carácter de AFIP"]
        columnas = ["nombre", "siglas", "telefono", "detalle", "domicilio_central", "domicilio_cp", "cuit", "id_afip"]

        datos = obtener_datos("obra_social", columnas, f"nombre = '{id_seleccionado[0]}' and cuit = '{id_seleccionado[2]}'")
        
        entradas ={}
        for i in datos:     #Devuelve índice y valor de cada elemento 
            valor = campos[i]
            Label(frame_detalles, text=valor + ":", bg="#c9c2b2", font=("Robot", 12)).grid(row=i, column=0, padx=10, pady=5, sticky=W)
            #Ingresa los elementos en la combo box y devuelve el valor de la seleccion
            if campos == "Carácter de AFIP":
                lista_afip = obtener_datos("afip", ["id_afip", "nombre"])
                # Crear un diccionario para buscar el ID por el nombre
                datos_afip = {dato[1]: dato[0] for dato in lista_afip} 
                self.combo_afip = ttk.Combobox(frame_detalles, width=49, font=("Robot", 10), state="readonly")
                self.combo_afip['values'] = list(datos_afip.keys())
                self.combo_afip.grid(row=i, column=1, padx=10, pady=5)
                id_afip = datos
                nombre_afip = (nombre for nombre, id_ in datos_afip.items() if id_ == id_afip)
                self.combo_afip.set(nombre_afip)
            else:
                entry = Entry(frame_detalles, width=40, font=("Robot", 12))
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(0, datos[i])  # Insertar el valor actual
                entry.config(state="readonly" if modo == "ver" else "normal")  # Configurar el estado según el modo
            entradas[valor] = entry
            
            if modo == "ver":
                entry.config(state="readonly")
                
                btn_editar = Button(ventana, text="Modificar", width=15, font=("Robot", 13), bg="#e6c885", command=lambda: activar_edicion(entradas, btn_guardar))
                btn_editar.grid(row=len(campos), column=0, pady=10)
    
                btn_guardar = Button(frame_detalles, text="Guardar Cambios", command=lambda: guardar_cambios(entradas, ventana))
                btn_guardar.grid(row=len(campos), column=0, columnspan=2, padx=10, pady=10)
                btn_guardar.config(state="disabled")  # Iniciar como deshabilitado
                                

        if modo == "modificar":
            btn_modificar = Button(frame_detalles, text="Guardar Cambios", command=lambda: self.guardar_cambios(entradas, ventana, id_seleccionado))
            btn_modificar.grid(row=len(campos), column=0, columnspan=2, padx=10, pady=10)

    #Función que ELIMINA obra social
    def eliminar_OS(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione una obra social para eliminar.")
            return
        #Pregunta al usuario si está seguro de eliminar 
        respuesta = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar la obra social seleccionado?")
        if respuesta:  
            self.tree.delete(seleccion)
            messagebox.showinfo("Atención", "Obra social eliminada correctamente.")
        else:
            messagebox.showinfo("Atención", "Eliminación cancelada.")

    def cargar_tratamiento(self):
        self.tree.insert("", "end", values=("1234", "Tratamiento 1", "$100"))
        self.tree.insert("", "end", values=("5678", "Tratamiento 2", "$150"))
        self.tree.insert("", "end", values=("91011", "Tratamiento 3", "$200"))
        
    #Funciones que buscan obra social
    def buscar_OS(self):
        busqueda = self.entrada_buscar.get().strip().lower()
        tratamiento_encontrado = False
    
        if not busqueda:
            self.tree.delete(*self.tree.get_children())
            self.cargar_tratamiento()
        #Obtenemos búsqueda
        for item in self.tree.get_children():         #Recorre cada fila usando identificador en la lista devuelta por children
            valores = self.tree.item(item, 'values')  #Obtiene los valores de las columnas de la fila correspondiente al identificador item.
            nombre = valores[0].lower()
            siglas = valores[1].lower()
            if busqueda in nombre or siglas:
                self.tree.selection_set(item)         #Selecciona el tratamiento.
                self.tree.see(item)                   #Hace visible el tratamiento.
                tratamiento_encontrado = True
            else:
                self.tree.detach(item)                #Oculta los otros tratamientos
            
        if not tratamiento_encontrado:
            #self.tree.delete(*self.tree.get_children())
            #self.cargar_tratamiento()
            messagebox.showwarning("Atención", "No se encontró la obra social.")

    def createWidgets(self):
        contenedor_total = Frame(self, padx=10, pady=10, bg="#e4c09f")
        contenedor_total.pack()

        #primer frame, contiene la imagen y el titulo de la ventana
        contenedor_titulo = Frame(contenedor_total, bg="#e4c09f")
        contenedor_titulo.pack()

        # Cargar la imagen de fondo
        img_fondo = Image.open("fondo3.png")
        img_fondo = img_fondo.resize((1000, 130), Image.Resampling.LANCZOS)
        self.img_fondo = ImageTk.PhotoImage(img_fondo)

        # Crear un Label para la imagen de fondo
        fondo_label = Label(contenedor_titulo, image=self.img_fondo)
        fondo_label.pack(expand=True, fill="both")

        # Crear un Label para el texto y colocarlo encima del Label de la imagen
        texto_label = Label(contenedor_titulo, text="Obras Sociales", font=("Robot", 25), bg="Black", fg="White")
        texto_label.place(relx=0.5, rely=0.5, anchor="center")

        #segundo frame, contiene el buscador y el boton de agregar
        #buscador de os
        frame_busqueda = Frame(contenedor_total, bg="#e4c09f")
        frame_busqueda.pack(fill= "x")
        #separa el campo de busqueda del botón
        frame_busqueda.columnconfigure(4, weight=1)

        #Widgets de búsqueda dentro del frame más chico
        Label(frame_busqueda, text="Buscar:", bg="#e6c885",font=("Robot",15)).grid(row=1, column=1, padx=5, pady=5, sticky= W)

        self.entrada_buscar = Entry(frame_busqueda,width="50",font=("Robot",13))
        self.entrada_buscar.grid(row=1, column=2, padx=5, pady=5, sticky= W)

        img_buscar = Image.open("buscar1.png").resize((30, 30), Image.Resampling.LANCZOS)
        img_buscar = ImageTk.PhotoImage(img_buscar)
        btn_buscar = Button(frame_busqueda, image=img_buscar, width=30, height=30,bg="#e6c885")
        btn_buscar.grid(row=1, column=3, sticky= W)
        btn_buscar.image = img_buscar

        boton_agregar = Button(frame_busqueda, text="Agregar   +", width=15, bg="#e6c885", activebackground="chartreuse4", font=("Robot",15), command=self.agregar_OS)
        boton_agregar.grid(row=1, column=5, padx=10, pady=10, sticky= E)


        #Tercer frame, contiene la tabla de OS
        #Frame para el Treeview y el scrollbar
        frame_tabla = Frame(contenedor_total, bg="#e4c09f", height= 500, width= 1000)  # Frame para contener la tabla y el scrollbar
        frame_tabla.pack(expand=True)
        
        stilo = ttk.Style()
        stilo.configure("Treeview", font=("Robot",11), rowheight=22)  # Cambia la fuente y el alto de las filas
        stilo.configure("Treeview.Heading", font=("Robot",14), padding= [0, 10])  # Cambia la fuente de las cabeceras
        
        #Treeview para mostrar la tabla de tratamientos dentro del frame_tabla
        self.tree = ttk.Treeview(frame_tabla, columns=("Nombre", "Siglas", "CUIT"), show='headings', height=16)
        self.tree.grid(row=0, column=0, sticky="nsew")

        #Títulos de columnas
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Siglas", text="Siglas")
        self.tree.heading("CUIT", text="CUIT")

        #Ancho de las columnas y datos centrados
        self.tree.column("Nombre", anchor='center', width=450, stretch=False)
        self.tree.column("Siglas", anchor='center', width=300, stretch=False)
        self.tree.column("CUIT", anchor='center', width=300, stretch=False)        

        #Scrollbar para la tabla dentro del frame_tabla
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')  #Se expande desde arriba hacia abajo
        self.tree.configure(yscrollcommand=scrollbar.set)

        #Cuarto frame, contiene los botones de ver, modificar y eliminar
        frame_btn = Frame(contenedor_total, bg= "#e4c09f")
        frame_btn.pack(pady= 8 )

        #Botones(ver, modificar, eliminar)
        btn_ver = Button(frame_btn, text="Ver", width=15, font=("Robot",15),bg="#e6c885", command=self.ver_OS)
        btn_ver.grid(row=0, column=1,padx=50)

        btn_editar = Button(frame_btn, text="Modificar", width=15, font=("Robot",15),bg="#e6c885", command=self.modificar_OS)
        btn_editar.grid(row=0, column=2,padx=50)
        
        btn_eliminar = Button(frame_btn, text="Eliminar", width=15,font=("Robot",15),bg="#e6c885", command=self.eliminar_OS)
        btn_eliminar.grid(row=0, column=3, padx=50)

        #Para que siempre esté atrás de los widgets
        fondo_label.lower()

ventana = Tk()
ventana.title("Gestion de Tratamientos")
ventana.resizable(False,False)
ventana.geometry("+30+15")
root = Gestion_Obra_Social(ventana)
ventana.mainloop()