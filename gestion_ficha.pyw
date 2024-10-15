from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

personas = {
    1: {
        "nombre": "Ana",
        "apellido": "Martínez",
        "dni": "34567890",
        "obra_social": "OSDE",
        "nro_obra_social": "123456789"
    },
    2: {
        "nombre": "Carlos",
        "apellido": "Pérez",
        "dni": "29876543",
        "obra_social": "Swiss Medical",
        "nro_obra_social": "987654321"
    },
    3: {
        "nombre": "Lucía",
        "apellido": "Gómez",
        "dni": "37654321",
        "obra_social": "Galeno",
        "nro_obra_social": "112233445"
    },
    4: {
        "nombre": "Jorge",
        "apellido": "Fernández",
        "dni": "30234567",
        "obra_social": "Medife",
        "nro_obra_social": "554433221"
    },
    5: {
        "nombre": "María",
        "apellido": "Rodríguez",
        "dni": "33221145",
        "obra_social": "OMINT",
        "nro_obra_social": "667788990"
    }
}

class ficha(Label):
    def __init__(self, master):
        Frame.__init__(self, master, bg="#e4c09f", height= 680, width=1200)
        self.master = master
        self.pack_propagate(False)
        self.pack(expand=True)
        self.createWidgets()

    def createWidgets(self):
        contenedor = Frame(self, padx=10, pady=10, bg="NavajoWhite3", height=600, width=800)
        contenedor.pack(expand=True)

        cont_paciente = LabelFrame(contenedor, text="Datos del Paciente", font=("Robot", 12), padx=10, pady=10, bg="#c9c2b2", width=800, height=300)
        cont_paciente.pack_propagate(False)
        cont_paciente.pack(expand=True, ipadx=18, ipady=18)
        
        cont_datos =Label(cont_paciente, width= 600, height= 300)
        cont_datos.pack(expand=True)

        # Entry para buscar
        self.entry_dni = Entry(cont_datos, width=30)
        self.entry_dni.grid(row= 0, column=0)
        self.entry_dni.bind('<KeyRelease>', self.actualizar_lista)

        self.entry_nombre = Entry(cont_datos, width=30, state="readonly")
        self.entry_nombre.grid( row=0 ,column=1)

        # Listbox para mostrar las coincidencias
        self.listbox = Listbox(cont_datos, width=30, height=5)
        self.listbox.pack(pady=5)  # Muestra el Listbox, ocultarlo inicialmente
        self.listbox.pack_forget()  # Ocultar inicialmente

        # Vincular el evento de selección al Listbox
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

    def actualizar_lista(self, evento):
        termino = self.entry_dni.get()
        self.listbox.delete(0, END)  # Limpiar la lista
        
        if termino:  # Mostrar el Listbox solo si hay un término de búsqueda
            #self.listbox.pack()  # Mostrar el Listbox
            self.listbox.place(x=self.entry_dni.winfo_x() - 12, y=self.entry_dni.winfo_y() - 11)
            # Buscar coincidencias en los datos de 'personas'
            for clave, valor in personas.items():
                if termino in valor['dni']:
                    self.listbox.insert(END, valor['dni'])
            
            # Si no hay coincidencias, ocultar la lista
            if self.listbox.size() == 0:
                self.listbox.pack_forget()  # Ocultar si no hay resultados
        else:
            self.listbox.pack_forget()  # Ocultar si no hay término de búsqueda

    def on_select(self, evento):
        # Obtener la selección actual
        seleccion = self.listbox.curselection()
        if seleccion:
            index = seleccion[0]
            dni_seleccionado = self.listbox.get(index)
            
            # Actualizar el Entry con el DNI seleccionado
            self.entry_dni.delete(0, END)
            self.entry_dni.insert(0, dni_seleccionado)
            
            # Rellenar el Entry de nombre con el nombre correspondiente
            for clave, valor in personas.items():
                if valor['dni'] == dni_seleccionado:
                    self.entry_nombre.config(state="normal")
                    self.entry_nombre.delete(0, END)
                    self.entry_nombre.insert(0, valor['nombre'])
                    self.entry_nombre.config(state="readonly")
                    break
            
            # Ocultar el Listbox después de la selección
            self.listbox.pack_forget()
ventana = Tk()
ventana.title("ficha")
ventana.resizable(False,False)
ventana.geometry("+30+15")
root = ficha(ventana)
ventana.mainloop()
"""
class Gestion_Fichas(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg="#e4c09f", height= 680, width=1300)
        self.master = master
        self.pack_propagate(False)
        self.pack(expand=True)
        self.createWidgets()

#Funciones que AGREGAN ficha
    def agregar_OS(self):
        ventana_agregar = Toplevel(self)
        ventana_agregar.title("Agregar Tratamiento")
        ventana_agregar.config(bg="#e4c09f") 
        ventana_agregar.resizable(False,False)
        ventana_agregar.geometry("+380+150")

        #datos del paciente
        frame_paciente = LabelFrame(ventana_agregar, text="Agregar Nueva Ficha", font= ("Robot", 12),padx=10, pady=10, bg="#c9c2b2")
        frame_paciente.pack(expand=True)

        frame_agregar = LabelFrame(ventana_agregar, text="Agregar Nueva Obra Social", font= ("Robot", 12),padx=10, pady=10, bg="#c9c2b2")
        frame_agregar.pack(expand=True)

        campos = ["Nombre", "Siglas", "CUIT", "Carácter de AFIP", "Domicilio Casa Central", "Domicilio Carlos Paz", "Mail", "Teléfono", "Detalle"]
        entradas = {}

        for i, campo in enumerate(campos):     #Devuelve índice y valor de cada elemento 
            Label(frame_agregar, text=campo + ":", bg="#c9c2b2", font=("Robot", 12)).grid(row=i, column=0, padx=10, pady=5, sticky=W)
            entry = Entry(frame_agregar, width=40, font=("Robot", 12))
            entry.grid(row=i, column=1, padx=10, pady=5)
            entradas[campo] = entry

        btn_nueva_os = Button(frame_agregar, text="Agregar", font=("Robot", 12),bg="#e6c885", width= 15, command=lambda: self.guardar_nueva_OS(entradas, ventana_agregar))
        btn_nueva_os.grid(row=len(campos), column=0, columnspan=2, padx=10, pady=10)
    
    def guardar_nueva_OS(self, entry, ventana):
        nombre = entry["Nombre"].get()
        siglas = entry["Siglas"].get()
        cuit = entry["CUIT"].get()
        caracter = entry["Carácter de AFIP"].get()
        domicilio_cc = entry["Domicilio Casa Central"].get()
        domicilio_cp = entry["Domicilio Carlos Paz"].get()
        mail = entry["Mail"].get()
        telefono = entry["Teléfono"].get()
        detalle = entry["Detalle"].get()

        # Validar datos y agregar al Treeview
        if nombre and siglas and cuit and caracter and domicilio_cc and domicilio_cp and mail and telefono and detalle:
            self.tree.insert("", "end", valors=(nombre, siglas, cuit))
            messagebox.showinfo("Información", "Obra social agregado correctamente.")
            ventana.destroy()
        else:
            messagebox.showwarning("Atención", "Complete todos los campos.")

    #Funciones que VEN y MODIFICAN obra social
    def ver_OS(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione una obra social.")
            return
        
        os_seleccion = self.tree.item(seleccion[0], 'valors')   #Item= valor del elemento
        self.abrir_ventana_OS(os_seleccion,seleccion[0],modo="ver")
    
    def modificar_OS(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione una obra social.")
            return
        
        tratamiento_seleccionado = self.tree.item(seleccion[0], 'valors')
        self.abrir_ventana_OS(tratamiento_seleccionado, seleccion[0],modo="modificar")

    def abrir_ventana_OS(self, obra_social, id_seleccionado, modo="ver"):
        def guardar_cambios(entradas, ventana, seleccion):
            #base de datos
            #messagebox.showinfo("Información", "Cambios guardados correctamente.")# Obtener los nuevos valores de todas las entradas
            nuevos_valores = {campo: entradas[campo].get() for campo in entradas}
            self.tree.item(seleccion, valors=list(nuevos_valores.valors()))
            
            # Mostrar mensaje de confirmación
            messagebox.showinfo("Información", "Cambios guardados correctamente.")
            
            # Cerrar la ventana después de guardar
            ventana.destroy()
        def activar_edicion(entradas, btn_guardar):
            # Habilitar la edición en las entradas
            for entry in entradas.valors():
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

        campos = ["Nombre", "Siglas", "CUIT", "Carácter de AFIP", "Domicilio Casa Central", "Domicilio Carlos Paz", "Mail", "Teléfono", "Detalle"]
        valores = list(obra_social) + ["Caracter ejemplo", "Domicilio Central ejemplo", " ", "Mail ejemplo", "354156542", "Detallin"]  #ejemplo
        entradas ={}

        for i, campo in enumerate(campos):
            Label(frame_detalles, text=campo + ":", bg="#c9c2b2", font=("Robot", 10)).grid(row=i, column=0, padx=10, pady=5)
            entry = Entry(frame_detalles, width=40)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry.insert(0, valores[i])
            entradas[campo] = entry
            

            if modo == "ver":
                entry.config(state="readonly")
                btn_editar = Button(ventana, text="Modificar", width=15, font=("Robot", 13), bg="#e6c885",
                                    command=lambda: activar_edicion(entradas, btn_guardar))
                btn_editar.grid(row=len(campos), column=0, pady=10)

    
                btn_guardar = Button(frame_detalles, text="Guardar cambios", command= lambda:guardar_cambios(entradas, ventana))
                btn_guardar.grid(row=len(campos), column=0, columnspan=2, padx=10, pady=10)
                btn_guardar.config(state="disabled")  # Iniciar como deshabilitado
                                
        if modo == "modificar":
            btn_modificar = Button(frame_detalles, text="Guardar Cambios", command= lambda:guardar_cambios(entradas, ventana, id_seleccionado))
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
        self.tree.insert("", "end", valors=("1234", "Tratamiento 1", "$100"))
        self.tree.insert("", "end", valors=("5678", "Tratamiento 2", "$150"))
        self.tree.insert("", "end", valors=("91011", "Tratamiento 3", "$200"))
        
    #Funciones que buscan obra social
    def buscar_OS(self):
        busqueda = self.entrada_buscar.get().strip().lower()
        tratamiento_encontrado = False
    
        if not busqueda:
            self.tree.delete(*self.tree.get_children())
            self.cargar_tratamiento()
        #Obtenemos búsqueda
        for item in self.tree.get_children():         #Recorre cada fila usando identificador en la lista devuelta por children
            valores = self.tree.item(item, 'valors')  #Obtiene los valores de las columnas de la fila correspondiente al identificador item.
            nombre = valores[0].lower()
            siglas = valores[1].lower()
            if busqueda in nombre or siglas in obra_social:
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
        texto_label = Label(contenedor_titulo, text="FICHAS", font=("Robot", 25), bg="Black", fg="White")
        texto_label.place(relx=0.5, rely=0.5, anchor="center")

        #segundo frame, contiene el buscador y el boton de agregar
            #buscador de fichas
        frame_busqueda = Frame(contenedor_total, bg="#e4c09f")
        frame_busqueda.pack(fill= "x")
            #separa el campo busqueda del resto de la ventana
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

        boton_agregar = Button(frame_busqueda, text="Agregar   +", width=15, bg="chartreuse3", activebackground="chartreuse4", font=("Robot",15), command=self.agregar_OS)
        boton_agregar.grid(row=1, column=5, padx=10, pady=10, sticky= E)

        #Tercer frame, contiene la tabla de OS
            #Frame para el Treeview y el scrollbar
        frame_tabla = Frame(contenedor_total, bg="#e4c09f", height= 500, width= 1000)  # Frame para contener la tabla y el scrollbar
        frame_tabla.pack(expand=True)
        
        stilo = ttk.Style()
        stilo.configure("Treeview", font=("Robot",11), rowheight=22)  # Cambia la fuente y el alto de las filas
        stilo.configure("Treeview.Heading", font=("Robot",14), padding= [0, 10])  # Cambia la fuente de las cabeceras
        
        #Treeview para mostrar la tabla de tratamientos dentro del frame_tabla
        self.tree = ttk.Treeview(frame_tabla, columns=("Código", "Paciente", "Doc. Paciente"), show='headings', height=16)
        self.tree.grid(row=0, column=0, sticky="nsew")

        #Títulos de columnas
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Siglas", text="Siglas")
        self.tree.heading("CUIT", text="CUIT")

        #Ancho de las columnas y datos centrados
        self.tree.column("Nombre", anchor='center', width=450, stretch=False)
        self.tree.column("Siglas", anchor='center', width=300, stretch=False)
        self.tree.column("CUIT", anchor='center', width=300, stretch=False)

        
        #Ejemplo
        self.tree.insert("", "end", valors=("1234", "OS 1", "7455"))
        self.tree.insert("", "end", valors=("5678", "Tratamiento 2", "2456"))
        self.tree.insert("", "end", valors=("91011", "Tratamiento 3", "522"))
        

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
ventana.mainloop()"""