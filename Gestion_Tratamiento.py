from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
from ConexionBD import obtener_conexion



class GestionTratamiento(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, bg="#e4c09f", height=780, width=1300)
        self.master = master
        self.pack_propagate(False)
        self.pack(expand=True)
        self.grid()
        self.createWidgets()
        self.actualizar_treeview()
        self.master.protocol("WM_DELETE_WINDOW", lambda: None)


    def createWidgets(self):
        frame_tratamientos = LabelFrame(self, text="Gestión de Tratamientos", font=("Robot",10),padx=10, pady=10, bg="#c9c2b2")
        frame_tratamientos.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        #Carga la imagen de fondo
        img_fondo = Image.open("fondo3.png")
        img_fondo = img_fondo.resize((1250, 200), Image.Resampling.LANCZOS)
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
        btn_buscar = Button(frame_busqueda, image=img_buscar, width=30, height=30,bg="#e6c885", 
                            command=self.buscar_tratamiento)
        
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
        self.tree = ttk.Treeview(frame_tabla, columns=("codigo", "nombre", "precio"), show='headings', height=10)

        #Títulos de columnas
        self.tree.heading("codigo", text="Código")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("precio", text="Precio")

        #Ancho de las columnas y datos centrados
        self.tree.column("codigo", anchor='center', width=350)
        self.tree.column("nombre", anchor='center', width=450)
        self.tree.column("precio", anchor='center', width=350)

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

        btn_volver = Button(frame_btn, text="Volver", width=15,font=("Robot",13),bg="#e6c885",
                            command=self.volver_menu_principal)
        btn_volver.grid(row=4, column=4, padx=50)


    def agregar_tratamiento(self):
        def validar_campos(entradas):
            campos_vacios = []
            for campo, entrada in entradas.items():
                valor = entrada.get().strip()
                if not valor:
                    campos_vacios.append(campo)
                elif campo == "Precio":
                    try:
                        float(valor)
                    except ValueError:
                        messagebox.showerror("Error", "El campo 'Precio' debe ser un número válido.")
                        return False
            
            if campos_vacios:
                messagebox.showwarning("Advertencia", f"Los siguientes campos están vacíos: {', '.join(campos_vacios)}.\nPor favor complételos.")
                return False
            else:
                messagebox.showinfo("Éxito","Tratamiento agregado correctamente.")
                return True
        ventana_agregar = Toplevel(self)
        ventana_agregar.title("Agregar Tratamiento")
        ventana_agregar.config(bg="#e4c09f") 
        ventana_agregar.resizable(False,False)
        ventana_agregar.geometry("455x310+400+160")
        ventana_agregar.protocol("WM_DELETE_WINDOW", lambda: None)

        frame_agregar = LabelFrame(ventana_agregar, text="Agregar Nuevo Tratamiento", font= ("Robot", 12),padx=10, pady=10, bg="#c9c2b2")
        frame_agregar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        campos = ["Código", "Nombre", "Precio", "Fecha Precio", "Siglas", "Descripción"]
        entradas = {}

        for i, campo in enumerate(campos):     #Devuelve índice y valor de cada elemento 
            etiquetas = Label(frame_agregar, text=campo + ":", bg="#c9c2b2", font=("Robot", 10))
            etiquetas.grid(row=i, column=0, padx=10, pady=5)
            entry = Entry(frame_agregar, width=40, font=("Robot", 10))
            entry.grid(row=i, column=1, padx=10, pady=5)
            entradas[campo] = entry



        btn_nuevo_tratamiento = Button(frame_agregar, text="Agregar", font=("Robot", 13),bg="#e6c885", width=15, 
                                       command=lambda:validar_campos(entradas) and  self.guardar_nuevo_tratamiento(entradas, ventana_agregar))
        btn_nuevo_tratamiento.grid(row=len(campos), column=0, columnspan=2, padx=10, pady=10)

        btn_volver = Button(frame_agregar, text="Volver", font=("Robot", 13),bg="#e6c885", width=15,
                            command=ventana_agregar.destroy)
        btn_volver.grid(row=len(campos), column=2, padx=10, pady=10)


    def ver_tratamiento(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione un tratamiento.")
            return
        id_seleccionado = seleccion[0]
        tratamiento_seleccionado = self.obtener_tratamiento_por_id(id_seleccionado)

        if tratamiento_seleccionado:
            tratamiento_reducido = tratamiento_seleccionado[0:]  
            self.abrir_ventana_tratamiento(tratamiento_reducido, modo="ver",seleccion=id_seleccionado)  
        else:
            messagebox.showerror("Error", "No se pudo obtener el tratamiento.")


    def modificar_tratamiento(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione un tratamiento.")
            return
        id_seleccionado = seleccion[0]
        tratamiento_seleccionado = self.obtener_tratamiento_por_id(id_seleccionado)
        if tratamiento_seleccionado:
            tratamiento_reducido = tratamiento_seleccionado[0:]  
            self.abrir_ventana_tratamiento(tratamiento_reducido, modo="modificar", seleccion=id_seleccionado)
        else:
            messagebox.showerror("Error", "No se pudo obtener el tratamiento para modificar.")


    def abrir_ventana_tratamiento(self, tratamiento,modo, seleccion=None):           
        ventana = Toplevel(self)
        ventana.title("Detalles del Tratamiento")
        ventana.config(bg="#e4c09f")
        ventana.resizable(False, False)
        ventana.geometry("510x345+400+160")
        ventana.protocol("WM_DELETE_WINDOW", lambda: None)
        
        ventana.grid_columnconfigure(0, weight=2)
        ventana.grid_rowconfigure(0, weight=2)

        frame_detalles = LabelFrame(ventana, text="Detalles del Tratamiento", font=("Robot", 10), padx=10, pady=10, bg="#c9c2b2")
        frame_detalles.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        campos = ["Código", "Nombre", "Precio", "Fecha Precio", "Siglas", "Descripción"]
        valores = list(tratamiento)
        entradas = {}

        for i, campo in enumerate(campos):
            etiqueta = Label(frame_detalles, text=campo + ":", bg="#c9c2b2", font=("Robot", 10))
            etiqueta.grid(row=i, column=0, padx=10, pady=5)
            entry = Entry(frame_detalles, width=40, font=("Robot", 10))
            entry.grid(row=i, column=1, padx=10, pady=5)
            if i + 1 < len(valores):
                entry.insert(0,str(valores[i + 1])) 
                entradas[campo] = entry

        if modo == "ver":
                for entry in entradas.values():
                    entry.config(state="readonly")
                
                frame_btns = Frame(ventana, bg="#e4c09f")
                frame_btns.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

                btn_editar = Button(frame_btns, text="Modificar", width=15, font=("Robot", 13), bg="#e6c885",
                                    command=lambda: self.activar_edicion(entradas,btn_guardar))
                btn_editar.grid(row=len(campos), column=0, padx=10,pady=10)

                btn_guardar = Button(frame_btns, text="Guardar Cambios", width=15, font=("Robot", 13), bg="#e6c885", 
                                    command=lambda: self.guardar_cambios(entradas, ventana, seleccion))
                btn_guardar.grid(row=len(campos), column=1, padx=10,pady=10)
                btn_guardar.config(state="disabled")  

                btn_volver = Button(frame_btns, text="Volver", width=15, font=("Robot", 13), bg="#e6c885",
                                    command=ventana.destroy)
                btn_volver.grid(row=len(campos), column=2, padx=10,pady=10)

        if modo == "modificar":
            frame_btns = Frame(ventana, bg="#e4c09f")
            frame_btns.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

            btn_guardar = Button(frame_btns, text="Guardar Cambios", width=15, font=("Robot", 13), bg="#e6c885",
                                command=lambda: self.guardar_cambios(entradas, ventana, seleccion))
            btn_guardar.grid(row=len(campos), column=0,  padx=60, pady=10)

            btn_cancelar = Button(frame_btns, text="Cancelar", width=15, font=("Robot", 13), bg="#e6c885",
                                command=ventana.destroy)
            btn_cancelar.grid(row=len(campos), column=1, pady=10)


    def activar_edicion(self, entradas, btn_guardar):
        for entry in entradas.values():
            entry.config(state="normal")  
        btn_guardar.config(state="normal") 


    def guardar_cambios(self, entradas, ventana,seleccion):
        conexion = obtener_conexion()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return
        nuevos_valores = {campo: entradas[campo].get() for campo in entradas}
        print(nuevos_valores)
        if seleccion:
            try:
                cursor = conexion.cursor()
                sql = "UPDATE tratamiento SET codigo=%s, nombre=%s, precio=%s, fecha_precio=%s, siglas=%s, descripcion=%s WHERE id_tratamiento=%s"
                val = (
                    nuevos_valores['Código'], 
                    nuevos_valores['Nombre'],
                    nuevos_valores['Precio'],
                    nuevos_valores['Fecha Precio'], 
                    nuevos_valores['Siglas'], 
                    nuevos_valores['Descripción'],
                    seleccion  #Usa el ID original del tratamiento que estás modificando
                )

                if any(value is None for value in val[:-1]):
                    messagebox.showerror("Error", "Hay campos vacíos que no pueden ser actualizados.")
                    return
                cursor.execute(sql, val)
                conexion.commit()
                print(f"Filas afectadas: {cursor.rowcount}")  #Muestra cuántas filas se actualizaron
                messagebox.showinfo("Información", "Tratamiento modificado correctamente.")
                ventana.destroy()
                self.actualizar_treeview()
                messagebox.showerror("Error", "No se pudo modificar el tratamiento: ")
                messagebox.showinfo("Éxito", "Tratamiento actualizado correctamente.")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Ocurrió un error al actualizar el tratamiento: {err}")
            finally:
                cursor.close()
                conexion.close()


    def eliminar_tratamiento(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione un tratamiento.")
            return

        tratamiento_seleccionado = self.tree.item(seleccion[0], "values")
        id_tratamiento = tratamiento_seleccionado[0]  # Asumiendo que el ID es el primer valor

        respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este tratamiento?")
        if respuesta:
            try:
                conexion = obtener_conexion()
                cursor = conexion.cursor()
                cursor.execute("UPDATE tratamiento SET activo = 0 WHERE id_tratamiento = %s", (id_tratamiento,))
                conexion.commit()
                messagebox.showinfo("Éxito", "Tratamiento eliminado correctamente.")
                self.tree.delete(seleccion[0])  # Eliminar de la interfaz
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al eliminar el tratamiento: {err}")
            finally:
                if conexion.is_connected():
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
        siglas = entry["Siglas"].get()
        descripcion = entry["Descripción"].get()
        #Validar datos y agregar al Treeview
        if codigo and nombre and precio and fecha_precio  and siglas and descripcion:
            try:
                cursor = conexion.cursor()
                sql = "INSERT INTO tratamiento (codigo, nombre, precio, fecha_precio, siglas, descripcion) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (codigo, nombre, precio, fecha_precio, siglas, descripcion)
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
        for item in self.tree.get_children():
            self.tree.delete(item)
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM tratamiento")
        tratamientos = cursor.fetchall()
        for tratamiento in tratamientos:
            self.tree.insert("", "0", iid=tratamiento[0], values=tratamiento[1:])
        
        cursor.close()
        conexion.close()
    

    def cargar_tratamientos(self):
        #Obtener tratamientos de la base de datos
        tratamientos = self.obtener_tratamientos() 

        for tratamiento in tratamientos:
            self.tree.insert('', 'end', iid=tratamiento[0], values=(tratamiento[1], tratamiento[2], tratamiento[3]))  # Mostrar solo los campos deseados


    def obtener_tratamiento_por_id(self, id_tratamiento):
        conexion = obtener_conexion()
        try:
            sql = "SELECT * FROM tratamiento WHERE id_tratamiento = %s"
            cursor = conexion.cursor()
            cursor.execute(sql, (id_tratamiento,))
            tratamiento = cursor.fetchone()
            if tratamiento is None:
               messagebox.showwarning("Advertencia", "No se encontró ningún tratamiento con ese ID.")
            
            return tratamiento
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se pudo recuperar el tratamiento: {error}")
        finally:
            cursor.close()
            conexion.close()


    def buscar_tratamiento(self):
        busqueda = self.entrada_buscar.get().strip().lower()

        if not busqueda:
            self.tree.delete(*self.tree.get_children())
            self.actualizar_treeview()
            return

        tratamiento_encontrado = False

        for item in self.tree.get_children():
            valores = self.tree.item(item, 'values')
            codigo = valores[0].lower()
            nombre = valores[1].lower()

            if busqueda in codigo or busqueda in nombre:
                tratamiento_encontrado = True
            else:
                self.tree.delete(item)

        if not tratamiento_encontrado:
            messagebox.showwarning("Atención", "No se encontró el tratamiento.")
            self.tree.delete(*self.tree.get_children())
            self.actualizar_treeview()


    def volver_menu_principal(self):
        from Menu import MENU
        self.master.destroy()
        ventana = Tk()
        ventana.wm_title("Menú Recupero de Obra Social")
        ventana.wm_resizable(0,0)
        ventana.geometry("+30+15")
        menu = MENU(ventana)
        menu.mainloop()

        

'''ventana = Tk()
ventana.title("Gestion de Tratamientos")
ventana.resizable(False,False)
ventana.geometry("+30+15")
root = GestionTratamiento(ventana)
ventana.mainloop()'''
