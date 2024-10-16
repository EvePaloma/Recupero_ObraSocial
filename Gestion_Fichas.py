from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

class GestionFicha(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg="#e4c09f")
        self.master = master
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        frame_fichas = LabelFrame(self, text="Gestión de Fichas", font=("Robot",10),padx=10, pady=10, bg="#c9c2b2")
        frame_fichas.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        #Carga la imagen de fondo
        img_fondo = Image.open("fondo3.png")
        img_fondo = img_fondo.resize((900, 200), Image.Resampling.LANCZOS)
        self.img_fondo = ImageTk.PhotoImage(img_fondo)

        #Label para la imagen de fondo
        fondo_label = Label(frame_fichas, image=self.img_fondo)
        fondo_label.grid(row=0, column=0, columnspan=7)

        #Frame más chico para label y entry de búsqueda
        frame_busqueda = Frame(frame_fichas, bg="#e6c885")
        frame_busqueda.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="w")

        #Widgets de búsqueda dentro del frame más chico
        etiqueta_buscar = Label(frame_busqueda, text="Buscar:", bg="#e6c885",font=("Robot",13))
        etiqueta_buscar.grid(row=1, column=1, padx=5, pady=5)

        self.entrada_buscar = Entry(frame_busqueda,width="50",font=("Robot",11))
        self.entrada_buscar.grid(row=1, column=2, padx=5, pady=5)

        img_buscar = Image.open("buscar1.png").resize((30, 30), Image.Resampling.LANCZOS)
        img_buscar = ImageTk.PhotoImage(img_buscar)
        btn_buscar = Button(frame_busqueda, image=img_buscar, width=30, height=30,bg="#e6c885", 
                            command=self.buscar_ficha)
        btn_buscar.grid(row=1, column=3)
        btn_buscar.image = img_buscar

        boton_agregar = Button(frame_fichas, text="Agregar   +", width=15, bg="#e6c885",font=("Robot",13),
                                command=self.agregar_ficha)
        boton_agregar.grid(row=1, column=5, padx=10, pady=10)

        #Para que siempre esté atrás de los widgets
        fondo_label.lower()

        #Frame para el Treeview y el scrollbar
        frame_tabla = Frame(frame_fichas, bg="#c9c2b2")  # Frame para contener la tabla y el scrollbar
        frame_tabla.grid(row=2, column=0, columnspan=6, padx=10, pady=10)
        
        stilo = ttk.Style()
        stilo.configure("Treeview", font=("Robot",11), rowheight=25)  # Cambia la fuente y el alto de las filas
        stilo.configure("Treeview.Heading", font=("Robot",14))  # Cambia la fuente de las cabeceras


        #Treeview para mostrar la tabla de tratamientos dentro del frame_tabla
        self.tree = ttk.Treeview(frame_tabla, columns=("DNI", "Nombre y apellido", "Servicio", "Fecha prestación medica", "Código"), show='headings', height=5)

        #Títulos de columnas
       
        self.tree.heading("DNI", text="DNI")
        self.tree.heading("Nombre y apellido", text="Nombre y Apellido")
        self.tree.heading("Servicio", text="Servicio")
        self.tree.heading("Fecha prestación medica", text="Fecha prestación medica")
        self.tree.heading("Código", text="Código")

        #Ancho de las columnas y datos centrados
        self.tree.column("DNI", anchor='center', width=250)
        self.tree.column("Nombre y apellido", anchor='center', width=350)
        self.tree.column("Servicio", anchor='center', width=250)
        self.tree.column("Fecha prestación medica", anchor='center', width=250)
        self.tree.column("Código", anchor='center', width=250)

        #Ejemplo
        self.tree.insert("", "end", values=("DNI", "Sabrina Carpenter", "Estudio", "12-05-2024", "342"))
        self.tree.insert("", "end", values=("29319319", "María Gomez", "Resonancia", "30-08-2024", "421"))
        self.tree.insert("", "end", values=("1661617", "José Perez", "Fisioterapia", "12-10-2024", "23"))

        #Grid del frame_tabla
        self.tree.grid(row=0, column=0, sticky="nsew")

        #Scrollbar para la tabla dentro del frame_tabla
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')  #Se expande desde arriba hacia abajo
        self.tree.configure(yscrollcommand=scrollbar.set)

        frame_btn = Frame(frame_fichas,bg="#c9c2b2")
        frame_btn.grid(row=4, columnspan=6)

        #Botones(ver, modificar, eliminar)
        btn_ver = Button(frame_btn, text="Ver", width=15, font=("Robot",13),bg="#e6c885", 
                         command=self.ver_ficha)
        btn_ver.grid(row=4, column=1,padx=50)

        btn_editar = Button(frame_btn, text="Modificar", width=15, font=("Robot",13),bg="#e6c885",
                             command=self.modificar_ficha)
        btn_editar.grid(row=4, column=2,padx=50)
        
        btn_eliminar = Button(frame_btn, text="Eliminar", width=15,font=("Robot",13),bg="#e6c885",
                               command=self.eliminar_paciente)
        btn_eliminar.grid(row=4, column=3, padx=50)

    def agregar_ficha(self):
        ventana_agregar = Toplevel(self)
        ventana_agregar.title("Agregar ficha")
        ventana_agregar.config(bg="#e4c09f") 
        ventana_agregar.resizable(False,False)

        frame_agregar = LabelFrame(ventana_agregar, text="Agregar ficha", font= ("Robot", 12),padx=10, pady=10, bg="#c9c2b2")
        frame_agregar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


        campos = ["Nombre y Apellido del paciente", "DNI", "Obra social", "Obra Social Secundaria", "Propietario del Plan", "Fecha de Nacimiento", "Número de Afiliado", "Nombre y apellido del médico","Especialidad","Tipo de matrícula", "Matrícula","Servicio", "Fecha de prestación médica", "Código", "Nombre del procedimiento", "Precio", "Tipo de tratamiento", "Siglas"]
        entradas = {}

        for i, campo in enumerate(campos):     #Devuelve índice y valor de cada elemento 
            etiquetas = Label(frame_agregar, text=campo + ":", bg="#c9c2b2", font=("Robot", 10))
            etiquetas.grid(row=i, column=0, padx=10, pady=5)
            entry = Entry(frame_agregar, width=40, font=("Robot", 10))
            entry.grid(row=i, column=1, padx=10, pady=5)
            entradas[campo] = entry

        btn_nueva_ficha = Button(frame_agregar, text="Agregar", font=("Robot", 10),bg="#e6c885", 
                                       command=lambda: self.guardar_nueva_ficha(entradas, ventana_agregar))
        btn_nueva_ficha.grid(row=len(campos), column=0, columnspan=2, padx=10, pady=10)

    def ver_ficha(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione una ficha.")
            return
        
        paciente_seleccionado = self.tree.item(seleccion[0], 'values')   #Item= valor del elemento
        self.abrir_ventana_ficha(paciente_seleccionado,seleccion[0],modo="ver")

    def modificar_ficha(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione una ficha.")
            return
        
        ficha_seleccionada = self.tree.item(seleccion[0], 'values')
        self.abrir_ventana_ficha(ficha_seleccionada, seleccion[0],modo="modificar")    
    
    def abrir_ventana_ficha(self, tratamiento, id_seleccionado, modo="ver"):
        ventana = Toplevel(self)
        ventana.title("Detalles de la Ficha")
        ventana.config(bg="#e4c09f")
        ventana.resizable(False,False)
        ventana.geometry("700x705+400+160")
        
        ventana.grid_columnconfigure(0, weight=1)
        ventana.grid_rowconfigure(0, weight=1)

        frame_detalles = LabelFrame(ventana, text="Detalles del Paciente", font=("Robot", 10), padx=10, pady=10, bg="#c9c2b2")
        frame_detalles.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        campos = ["Nombre y Apellido del paciente", "DNI", "Obra social", "Obra Social Secundaria", "Propietario del Plan", 
        "Fecha de Nacimiento", "Número de Afiliado", "Nombre y apellido del médico","Especialidad","Tipo de matrícula", "Matrícula",
        "Servicio", "Fecha de prestación médica", "Código", "Nombre del procedimiento", "Precio", "Tipo de tratamiento", "Siglas"] #ejemplo
        entradas ={}


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
                                   command=lambda: self.guardar_cambios(entradas, ventana, id_seleccionado))
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
        self.tree.item(seleccion, values=list(nuevos_valores.values()))
        
        # Mostrar mensaje de confirmación
        messagebox.showinfo("Información", "Cambios guardados correctamente.")
        
        # Cerrar la ventana después de guardar
        ventana.destroy()

    def eliminar_paciente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione una ficha para eliminar.")
            return
        #Pregunta al usuario si está seguro de eliminar 
        respuesta = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar la ficha seleccionada?")
        if respuesta:  
            self.tree.delete(seleccion)
            messagebox.showinfo("Atención", "Ficha eliminada correctamente.")
        else:
            messagebox.showinfo("Atención", "Eliminación cancelada.")

    def guardar_nueva_ficha(self, entry, ventana):
        nombre = entry["Nombre y Apellido del paciente"].get()      #Obtenemos los valores que el usuario ingresó.
        dni = entry["DNI"].get()
        obrasocial = entry["Obra social"].get()
        obrasocialsec = entry["Obra Social Secundaria"].get()
        propietario = entry["Propietario del Plan"].get()
        fechanac = entry["Fecha de Nacimiento"].get()
        numeroafiliado = entry["Número de Afiliado"].get()
        nombre_medico = entry["Nombre y apellido del médico"].get()
        especialidad = entry ["Especialidad"].get()
        tipomatricula = entry ["Tipo de matrícula"].get()
        servicio = entry ["Servicio"].get()
        fechaprestacion = entry["Fecha de prestación médica"].get()
        codigo =entry["Código"].get()
        nombreprocedimiento=entry["Nombre del procedimiento"].get()
        precio=entry["Precio"].get()
        tipotratamiento=entry["Tipo de tratamiento"].get()
        siglas=entry["Siglas"].get()
        # Validar datos y agregar al Treeview
        if nombre and dni and obrasocial and obrasocialsec and propietario and fechanac and numeroafiliado and nombre_medico and especialidad and tipomatricula and servicio and fechaprestacion and codigo and nombreprocedimiento and precio and tipotratamiento and siglas:
            self.tree.insert("", "end", values=(nombre, dni, obrasocial, propietario, fechanac, numeroafiliado, nombre_medico, especialidad, tipomatricula, servicio, fechaprestacion, codigo, nombreprocedimiento,precio,tipotratamiento, siglas))
            messagebox.showinfo("Información", "Paciente agregado correctamente.")
            ventana.destroy()
        else:
            messagebox.showwarning("Atención", "Complete todos los campos.")

    def buscar_ficha(self):
        busqueda = self.entrada_buscar.get().strip().lower()
        paciente_encontrado = False
    
        if not busqueda:
            self.tree.delete(*self.tree.get_children())
            self.cargar_ficha()
        #Obtenemos búsqueda
        for item in self.tree.get_children():         #Recorre cada fila usando identificador en la lista devuelta por children
            valores = self.tree.item(item, 'values')  #Obtiene los valores de las columnas de la fila correspondiente al identificador item.
            nombre = valores[1].lower()
            dni = valores[0].lower()
            if busqueda in nombre or busqueda in dni:
                self.tree.selection_set(item)         #Selecciona el tratamiento.
                self.tree.see(item)                   #Hace visible el tratamiento.
                paciente_encontrado = True
            else:
                self.tree.detach(item)                #Oculta los otros tratamientos.
       
            
        if not paciente_encontrado:

            messagebox.showwarning("Atención", "No se encontró el paciente.")

    def cargar_ficha(self):
        self.tree.insert("", "end", values=("DNI", "Sabrina Carpenter", "Estudio", "12-05-2024", "342"))
        self.tree.insert("", "end", values=("29319319", "María Gomez", "Resonancia", "30-08-2024", "421"))
        self.tree.insert("", "end", values=("1661617", "José Perez", "Fisioterapia", "12-10-2024", "23"))

ventana = Tk()
ventana.title("Gestion de Fichas")
ventana.resizable(False,False)
ventana.geometry("+200+80")
root = GestionFicha(ventana)
ventana.mainloop()