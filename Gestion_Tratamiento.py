from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
from ConexionBD import obtener_conexion


class GestionTratamiento(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg="#e4c09f")
        self.master = master
        self.grid()
        self.createWidgets()
        self.actualizar_treeview()

    def solo_letras(self, char):
        return char.isalpha() or char == " "

    def solo_numeros(self, char):
        return char.isdigit()

    def createWidgets(self):
        frame_tratamientos = LabelFrame(self, text="Gestión de Tratamientos", font=("Robot",10),padx=10, pady=10, bg="#c9c2b2")
        frame_tratamientos.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        #Carga la imagen de fondo
        img_fondo = Image.open("fondo3.png")
        img_fondo = img_fondo.resize((900, 200), Image.Resampling.LANCZOS)
        self.img_fondo = ImageTk.PhotoImage(img_fondo)

        #Label para la imagen de fondo
        fondo_label = Label(frame_tratamientos, image=self.img_fondo)
        fondo_label.grid(row=0, column=0, columnspan=7)

        #Frame más chico para label y entry de búsqueda
        frame_busqueda = Frame(frame_tratamientos, bg="#e6c885")
        frame_busqueda.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="w")

        #Widgets de búsqueda dentro del frame más chico
        etiqueta_buscar = Label(frame_busqueda, text="Buscar:", bg="#e6c885",font=("Robot",13))
        etiqueta_buscar.grid(row=1, column=1, padx=5, pady=5)

        self.entrada_buscar = Entry(frame_busqueda,width="50",font=("Robot",11))
        self.entrada_buscar.grid(row=1, column=2, padx=5, pady=5)

        img_buscar = Image.open("buscar1.png").resize((30, 30), Image.Resampling.LANCZOS)
        img_buscar = ImageTk.PhotoImage(img_buscar)
        criterio_entry = Entry(self)
        criterio_entry.grid()
        btn_buscar = Button(frame_busqueda, image=img_buscar, width=30, height=30,bg="#e6c885", 
                            command=lambda:self.buscar_tratamiento(criterio_entry.get()))
        
        btn_buscar.grid(row=1, column=3)
        btn_buscar.image = img_buscar

        boton_agregar = Button(frame_tratamientos, text="Agregar   +", width=15, bg="#e6c885",font=("Robot",13),
                                command=self.agregar_tratamiento)
        boton_agregar.grid(row=1, column=5, padx=10, pady=10)

        #Para que siempre esté atrás de los widgets
        fondo_label.lower()

        #Frame para el Treeview y el scrollbar
        frame_tabla = Frame(frame_tratamientos, bg="#c9c2b2")  # Frame para contener la tabla y el scrollbar
        frame_tabla.grid(row=2, column=0, columnspan=6, padx=10, pady=10)
        
        stilo = ttk.Style()
        stilo.configure("Treeview", font=("Robot",11), rowheight=25)  # Cambia la fuente y el alto de las filas
        stilo.configure("Treeview.Heading", font=("Robot",14))  # Cambia la fuente de las cabeceras


        #Treeview para mostrar la tabla de tratamientos dentro del frame_tabla
        self.tree = ttk.Treeview(frame_tabla, columns=("codigo", "nombre", "precio"), show='headings', height=5)

        #Títulos de columnas
        self.tree.heading("codigo", text="Código")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("precio", text="Precio")

        #Ancho de las columnas y datos centrados
        self.tree.column("codigo", anchor='center', width=250)
        self.tree.column("nombre", anchor='center', width=350)
        self.tree.column("precio", anchor='center', width=250)

        #Ejemplo
        #self.tree.insert("", "end", values=("1234", "Tratamiento 1", "$100"))
        #self.tree.insert("", "end", values=("5678", "Tratamiento 2", "$150"))
        #self.tree.insert("", "end", values=("91011", "Tratamiento 3", "$200"))

        #Grid del frame_tabla
        self.tree.grid(row=0, column=0, sticky="nsew")

        #Scrollbar para la tabla dentro del frame_tabla
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')  #Se expande desde arriba hacia abajo
        self.tree.configure(yscrollcommand=scrollbar.set)

        frame_btn = Frame(frame_tratamientos,bg="#c9c2b2")
        frame_btn.grid(row=4, columnspan=6)

        #Botones(ver, modificar, eliminar)
        btn_ver = Button(frame_btn, text="Ver", width=15, font=("Robot",13),bg="#e6c885", 
                         command=self.ver_tratamiento)
        btn_ver.grid(row=4, column=1,padx=50)

        btn_editar = Button(frame_btn, text="Modificar", width=15, font=("Robot",13),bg="#e6c885",
                             command=self.modificar_tratamiento)
        btn_editar.grid(row=4, column=2,padx=50)
        
        btn_eliminar = Button(frame_btn, text="Eliminar", width=15,font=("Robot",13),bg="#e6c885",
                               command=self.eliminar_tratamiento)
        btn_eliminar.grid(row=4, column=3, padx=50)

    def agregar_tratamiento(self):
        ventana_agregar = Toplevel(self)
        ventana_agregar.title("Agregar Tratamiento")
        ventana_agregar.config(bg="#e4c09f") 
        ventana.resizable(False,False)

        frame_agregar = LabelFrame(ventana_agregar, text="Agregar Nuevo Tratamiento", font= ("Robot", 12),padx=10, pady=10, bg="#c9c2b2")
        frame_agregar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        campos = ["Código", "Nombre", "Precio", "Fecha Precio", "Tipo", "Siglas", "Descripción"]
        entradas = {}

        for i, campo in enumerate(campos):     #Devuelve índice y valor de cada elemento 
            etiquetas = Label(frame_agregar, text=campo + ":", bg="#c9c2b2", font=("Robot", 10))
            etiquetas.grid(row=i, column=0, padx=10, pady=5)
            if campo == "Tipo":
                entry_tipo = ttk.Combobox(frame_agregar, width=37, font=("Robot", 10), state="readonly")
                entry_tipo['values'] = ("Consulta", "Cirugía", "Terapia", "Examen", "Otro")
                entry_tipo.grid(row=i, column=1, padx=10, pady=5)
                entry_tipo.set("Consulta")
            else:
                entry = Entry(frame_agregar, width=40, font=("Robot", 10))
                entry.grid(row=i, column=1, padx=10, pady=5)
            entradas[campo] = entry

        btn_nuevo_tratamiento = Button(frame_agregar, text="Agregar", font=("Robot", 10),bg="#e6c885", 
                                       command=lambda: self.guardar_nuevo_tratamiento(entradas, ventana_agregar))
        btn_nuevo_tratamiento.grid(row=len(campos), column=0, columnspan=2, padx=10, pady=10)

    def ver_tratamiento(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione un tratamiento.")
            return
        
        tratamiento_seleccionado = self.tree.item(seleccion[0], 'values')   #Item= valor del elemento
        self.abrir_ventana_tratamiento(tratamiento_seleccionado,seleccion[0],modo="ver")

    def modificar_tratamiento(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione un tratamiento.")
            return
        
        tratamiento_seleccionado = self.tree.item(seleccion[0], 'values')
        self.abrir_ventana_tratamiento(tratamiento_seleccionado, seleccion[0],modo="modificar")    
    
    def abrir_ventana_tratamiento(self, tratamiento, id_seleccionado, modo="ver"):
        ventana = Toplevel(self)
        ventana.title("Detalles del Tratamiento")
        ventana.config(bg="#e4c09f")
        ventana.resizable(False,False)
        ventana.geometry("510x345+400+160")
        
        ventana.grid_columnconfigure(0, weight=1)
        ventana.grid_rowconfigure(0, weight=1)

        frame_detalles = LabelFrame(ventana, text="Detalles del Tratamiento", font=("Robot", 10), padx=10, pady=10, bg="#c9c2b2")
        frame_detalles.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        campos = ["Código", "Nombre", "Precio", "Fecha Precio", "Tipo", "Siglas", "Descripción"]
        valores = list(tratamiento) + ["Tipo Ejemplo", "Ejemplo Fecha Precio","Siglas Ejemplo", "Descripción"]  #ejemplo
        entradas ={}

        for i, campo in enumerate(campos):
            etiqueta = Label(frame_detalles, text=campo + ":", bg="#c9c2b2", font=("Robot", 10))
            etiqueta.grid(row=i, column=0, padx=10, pady=5)
            if campo == "Tipo":
                entry = ttk.Combobox(frame_detalles, width=37, font=("Robot", 10), state="readonly")
                entry['values'] = ("Consulta", "Cirugía", "Terapia", "Examen", "Otro")
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.set("Consulta")
                if modo == "ver":
                  entry.config(state="disabled")
            else:
                entry = Entry(frame_detalles, width=40)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(0, valores[i])
            entradas[campo] = entry
            

            if modo == "ver":
                entry.config(state="readonly")  
                
                btn_editar = Button(ventana, text="Modificar", width=15, font=("Robot", 13), bg="#e6c885",
                                    command=lambda: self.activar_edicion(entradas, btn_guardar))
                btn_editar.grid(row=len(campos), column=0, pady=10)

    
                btn_guardar = Button(frame_detalles, text="Guardar Cambios", 
                                     command=lambda: self.guardar_cambios(entradas, ventana))
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
        conexion = obtener_conexion()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return
        nuevos_valores = {campo: entradas[campo].get() for campo in entradas}
        self.tree.item(seleccion, values=list(nuevos_valores.values()))
        try:
            cursor = conexion.cursor()
            sql = "UPDATE tratamiento SET codigo=%s, nombre=%s, precio=%s, fecha_precio=%s, tipo_tratamiento=%s, siglas=%s, descripcion=%s WHERE codigo=%s"
            val = (nuevos_valores['Código'], 
                   nuevos_valores['Nombre'],
                   nuevos_valores['Precio'],
                   nuevos_valores['Fecha Precio'], 
                   nuevos_valores['Tipo'], 
                   nuevos_valores['Siglas'], 
                   nuevos_valores['Descripción'],
                   self.tree.item(seleccion, 'values')[0]
                   )
            cursor.execute(sql, val)
            conexion.commit()
            messagebox.showinfo("Información", "Tratamiento modificado correctamente.")
            ventana.destroy()
            self.actualizar_treeview()
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se pudo modificar el tratamiento: {error}")
        finally:
            cursor.close()
            conexion.close()

    def eliminar_tratamiento(self):
        conexion = obtener_conexion()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione un tratamiento para eliminar.")
            return
        tratamiento = self.tree.item(seleccion[0], 'values')[0]
        #Pregunta al usuario si está seguro de eliminar 
        respuesta = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar el tratamiento seleccionado?")
        if respuesta:
            try:
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM tratamiento WHERE codigo = %s", (tratamiento,))
                conexion.commit()
                messagebox.showinfo("Información", "Tratamiento eliminado correctamente.")
                self.actualizar_treeview()
            except mysql.connector.Error as error:
                messagebox.showerror("Error", f"No se pudo eliminar el tratamiento: {error}")
            finally:
                cursor.close()
                conexion.close()

    def guardar_nuevo_tratamiento(self, entry, ventana):
        conexion = obtener_conexion()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return
        codigo = entry["Código"].get()      #Obtenemos los valores que el usuario ingresó.
        nombre = entry["Nombre"].get()
        precio = entry["Precio"].get()
        fecha_precio = entry["Fecha Precio"].get()
        tipo_tratamiento = entry["Tipo"].get()
        siglas = entry["Siglas"].get()
        descripcion = entry["Descripción"].get()
        # Validar datos y agregar al Treeview
        if codigo and nombre and precio and fecha_precio and tipo_tratamiento and siglas and descripcion:
            try:
                cursor = conexion.cursor()
                sql = "INSERT INTO tratamiento (codigo, nombre, precio, fecha_precio, tipo_tratamiento, siglas, descripcion) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val = (codigo, nombre, precio, fecha_precio, tipo_tratamiento, siglas, descripcion)
                cursor.execute(sql, val)
                conexion.commit()
                messagebox.showinfo("Información", "Tratamiento agregado exitosamente")
                self.tree.insert("", 0, values=(codigo, nombre, precio))
                ventana.destroy()
                self.actualizar_treeview()
            except mysql.connector.Error as error:
                messagebox.showerror("Error", f"No se pudo agregar el tratamiento: {error}")
            finally:
                cursor.close()
                conexion.close()   
        else:
            messagebox.showwarning("Atención", "Complete todos los campos.")

    def actualizar_treeview(self):
        conexion = obtener_conexion()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT codigo, nombre, precio FROM tratamiento")
            tratamientos = cursor.fetchall()
            for tratamiento in tratamientos:
                self.tree.insert("", 0, values=tratamiento)
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se pudo recuperar los tratamientos: {error}")
        finally:
            cursor.close()
            conexion.close()

    def buscar_tratamiento(self, criterio):
        conexion = obtener_conexion()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Si el criterio está vacío, mostrar un mensaje y retornar
        if not criterio:
            messagebox.showinfo("Información", "Ingrese un criterio de búsqueda.")
            return

        try:
            cursor = conexion.cursor()
            sql = "SELECT codigo, nombre, precio FROM tratamiento WHERE nombre LIKE %s"
            val = ('%' + criterio + '%',)
            cursor.execute(sql, val)
            tratamientos = cursor.fetchall()

            # Verificar si se encontraron tratamientos
            if len(tratamientos) == 0:
                messagebox.showinfo("Información", "No se encontraron tratamientos con ese criterio.")
            else:
                # Insertar los tratamientos en el Treeview si se encontraron resultados
                for tratamiento in tratamientos:
                    self.tree.insert("", "end", values=tratamiento)
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se pudo recuperar los tratamientos: {error}")
        finally:
            cursor.close()
            conexion.close()

    #def cargar_tratamiento(self):
        #self.tree.insert("", "end", values=("1234", "Tratamiento 1", "$100"))
        #self.tree.insert("", "end", values=("5678", "Tratamiento 2", "$150"))
        #self.tree.insert("", "end", values=("91011", "Tratamiento 3", "$200"))

ventana = Tk()
ventana.title("Gestion de Tratamientos")
ventana.resizable(False,False)
ventana.geometry("+200+80")
root = GestionTratamiento(ventana)
ventana.mainloop()
