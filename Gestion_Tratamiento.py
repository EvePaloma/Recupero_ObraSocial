from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
from ConexionBD import obtener_conexion
from datetime import datetime



class GestionTratamiento(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, bg="#e4c09f", height=780, width=1366)
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
        img_fondo = img_fondo.resize((1310, 200), Image.Resampling.LANCZOS)
        self.img_fondo = ImageTk.PhotoImage(img_fondo)

        #Label para la imagen de fondo
        fondo_label = Label(frame_tratamientos, image=self.img_fondo)
        fondo_label.grid(row=0, column=0, columnspan=7)

        #Frame más chico para label y entry de búsqueda
        frame_busqueda = Frame(frame_tratamientos, bg="#e6c885")
        frame_busqueda.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        style = ttk.Style()
        style.theme_use("default")
        style.map("Custom.TCombobox",  fieldbackground=[("active", "white")],   # Fondo blanco en modo de solo lectura
                                        background=[("active", "white")],          # Fondo blanco al desplegar el menú
                                        selectbackground=[("focus", "white")],     # Fondo blanco cuando una opción está seleccionada
                                        selectforeground=[("focus", "black")])    # Text
        self.combo_activos = ttk.Combobox(frame_busqueda, width=10, font=("Robot", 14), state="readonly", style="Custom.TCombobox")
        self.combo_activos['values'] = ("Activos", "Inactivos", "Todos")
        self.combo_activos.set("Activos")
        self.combo_activos.grid(row=1, column=4, padx=20, pady=3)
        self.combo_activos.bind("<<ComboboxSelected>>", lambda event: self.actualizar_treeview())

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
        stilo.configure("Treeview", font=("Robot",11), rowheight=26)  # Cambia la fuente y el alto de las filas
        stilo.configure("Treeview.Heading", font=("Robot",14))  # Cambia la fuente de las cabeceras


        #Treeview para mostrar la tabla de tratamientos dentro del frame_tabla
        self.tree = ttk.Treeview(frame_tabla, columns=("codigo", "nombre", "precio"), show='headings', height=11)

        #Títulos de columnas
        self.tree.heading("codigo", text="Código")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("precio", text="Precio")

        #Ancho de las columnas y datos centrados
        self.tree.column("codigo", anchor='center', width=400)
        self.tree.column("nombre", anchor='center', width=480)
        self.tree.column("precio", anchor='center', width=400)

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

    def solo_numeros(self, num):
        return num.isdigit()

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
            if campo == "Estado":
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
        

    def agregar_tratamiento(self):
        ventana_agregar = Toplevel(self)
        ventana_agregar.title("Agregar Tratamiento")
        ventana_agregar.config(bg="#e4c09f") 
        ventana_agregar.resizable(False,False)
        ventana_agregar.geometry("455x345+400+160")
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

            if campo == "Precio":
                solo_num = ventana_agregar.register(self.solo_numeros)
                entry.config(validate="key", validatecommand=(solo_num, "%S"))

            #Configura marcador de posición para el campo "Fecha Precio"
            if campo == "Fecha Precio":
                entry.insert(0, "AAAA-MM-DD")  #Agrega marcador de posición
                entry.config(fg="gray")
                entry.bind("<FocusIn>", lambda event, e=entry: self.limpiar_marcador(e))
                entry.bind("<FocusOut>", lambda event, e=entry: self.restaurar_marcador(e))

        frame_btns = Frame(ventana_agregar, bg="#e4c09f")
        frame_btns.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        btn_nuevo_tratamiento = Button(frame_btns, text="Agregar", font=("Robot", 13),bg="#e6c885", width=15, 
                                       command=lambda:self.validar_campos(entradas,ventana_agregar) and self.guardar_nuevo_tratamiento(entradas,ventana_agregar))
        btn_nuevo_tratamiento.grid(row=len(campos), column=0, padx=40, pady=10)

        btn_volver = Button(frame_btns, text="Volver", font=("Robot", 13),bg="#e6c885", width=15,
                            command=ventana_agregar.destroy)
        btn_volver.grid(row=len(campos), column=1, pady=10)


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
        ventana.geometry("510x360+400+160")
        ventana.protocol("WM_DELETE_WINDOW", lambda: None)
        
        ventana.grid_columnconfigure(0, weight=2)
        ventana.grid_rowconfigure(0, weight=2)

        frame_detalles = LabelFrame(ventana, text="Detalles del Tratamiento", font=("Robot", 10), padx=10, pady=10, bg="#c9c2b2")
        frame_detalles.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        campos = ["Código", "Nombre", "Precio", "Fecha Precio", "Siglas", "Descripción", "Estado"]
        valores = list(tratamiento)
        entradas = {}

        for i, campo in enumerate(campos):
            etiqueta = Label(frame_detalles, text=campo + ":", bg="#c9c2b2", font=("Robot", 10))
            etiqueta.grid(row=i, column=0, padx=10, pady=5)
            if campo == "Estado":
                lista = self.conectar_tabla("estado")
                print(lista)
                # Crear un diccionario para buscar el ID por el nombre
                self.datos_tabla_1 = {dato[1]: dato[0] for dato in lista} 
                self.combo_valores_2 = ttk.Combobox(frame_detalles, width=38, font=("Robot", 10), state="disabled")
                self.combo_valores_2['values'] = list(self.datos_tabla_1.keys())
                self.combo_valores_2.grid(row=i, column=1, padx=10, pady=5)
                #se ingresa en la combo como valor inicial el nombre del caracter de afip o de estado
                valor_a_buscar = valores[i+1]
                clave_encontrada = next((clave for clave, valor in self.datos_tabla_1.items() if valor == valor_a_buscar), None)
                self.combo_valores_2.set(clave_encontrada)
            else:
                entry = Entry(frame_detalles, width=40, font=("Robot", 10))
                entry.grid(row=i, column=1, padx=10, pady=5)
                if i + 1 < len(valores):
                    entry.insert(0,str(valores[i + 1]).upper()) 
            entradas[campo] = entry

        if modo == "ver":
                for entry in entradas.values():
                    entry.config(state="readonly")

                self.combo_valores_2.config(state="disabled")
                
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
            self.combo_valores_2.config(state="readonly")
            self.combo_valores_2.bind("<<ComboboxSelected>>", lambda event: self.on_seleccion("Estado"))
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
        self.combo_valores_2.config(state="readonly")

    
    def validar_campos(self, entradas,ventana_agregar):
        campos_vacios = []
        for campo, entrada in entradas.items():
            valor = entrada.get().strip()
            if not valor:
                campos_vacios.append(campo)
        if campos_vacios:
            messagebox.showwarning("Advertencia", f"Los siguientes campos están vacíos: {', '.join(campos_vacios)}.\nPor favor complételos.")
            ventana_agregar.lift()
            return False

        for campo, entrada in entradas.items():
            valor = entrada.get().strip()
            if campo == "Precio":
                try:
                    precio = float(valor)
                    if precio <= 0:
                        messagebox.showerror("El precio debe ser mayor que 0.")
                        ventana_agregar.lift()
                except ValueError:
                    messagebox.showerror("Error", "El campo 'Precio' debe ser un número válido.")
                    ventana_agregar.lift()
                    return False
            elif campo == "Fecha Precio":
                if not self.fecha_valida(valor):
                    messagebox.showerror("Error", "El campo 'Fecha Precio' debe tener el formato 'YYYY-MM-DD'.")
                    ventana_agregar.lift()
                    return False
                
            elif campo == "Código":
                if not self.validar_repetidos(valor):
                    messagebox.showerror("Error", "El tratamiento con ese código ya existe.")
                    ventana_agregar.lift()
                    return False
        
        return True

    def limpiar_marcador(self, entry):
        if entry.get() == "AAAA-MM-DD":
            entry.delete(0, "end")
            entry.config(fg="black")

    def restaurar_marcador(self,entry):
        if not entry.get():
            entry.insert(0, "AAAA-MM-DD")
            entry.config(fg="gray")

    def validar_repetidos(self, codigo):
        conexion = obtener_conexion()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return
        try:
            cursor = conexion.cursor()
            sentencia = "SELECT COUNT(*) FROM tratamiento WHERE codigo = %s"
            cursor.execute(sentencia, (codigo,))
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

    def guardar_cambios(self, entradas, ventana,seleccion):
        conexion = obtener_conexion()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return
        nuevos_valores = {campo: entradas[campo].get().upper() for campo in entradas}
        nuevos_valores["Estado"] = self.on_seleccion("Estado")
       
        if seleccion:
            try:
                cursor = conexion.cursor()
                sql = "UPDATE tratamiento SET codigo=%s, nombre=%s, precio=%s, fecha_precio=%s, siglas=%s, descripcion=%s, activo=%s WHERE id_tratamiento=%s"
                val = (
                    nuevos_valores['Código'], 
                    nuevos_valores['Nombre'],
                    nuevos_valores['Precio'],
                    nuevos_valores['Fecha Precio'], 
                    nuevos_valores['Siglas'], 
                    nuevos_valores['Descripción'],
                    nuevos_valores['Estado'],
                    seleccion  #Usa el ID original del tratamiento que estás modificando
                )

                cursor.execute(sql, val)
                conexion.commit()
                messagebox.showinfo("Información", "Tratamiento modificado correctamente.")
                ventana.destroy()
                self.actualizar_treeview()
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

        #tratamiento_seleccionado = self.tree.item(seleccion[0], "values")
        id_tratamiento = seleccion[0]  # Asumiendo que el ID es el primer valor
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


    def guardar_nuevo_tratamiento(self, entry,ventana_agregar):
        if not self.validar_campos(entry,ventana_agregar):
            return
        
        conexion = obtener_conexion()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return
        codigo = entry["Código"].get().upper()      #Obtenemos los valores que el usuario ingresó.
        nombre = entry["Nombre"].get().upper()
        precio = entry["Precio"].get()
        fecha_precio = entry["Fecha Precio"].get()
        siglas = entry["Siglas"].get().upper()
        descripcion = entry["Descripción"].get().upper()
        if codigo and nombre and precio and fecha_precio and siglas and descripcion:
            try:
                cursor = conexion.cursor()
                sql = "INSERT INTO tratamiento (codigo, nombre, precio, fecha_precio, siglas, descripcion) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (codigo, nombre, precio, fecha_precio, siglas, descripcion)
                cursor.execute(sql, val)
                conexion.commit()
                messagebox.showinfo("Información", "Tratamiento agregado exitosamente")
                self.tree.insert("", 0, values=(codigo, nombre, precio))
                self.actualizar_treeview()
                ventana_agregar.destroy()
            except mysql.connector.Error as error:
                messagebox.showerror("Error", f"No se pudo agregar el tratamiento: {error}")  
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
            cursor.execute("SELECT * FROM tratamiento where activo = 1")
        elif seleccion == "Inactivos":
            cursor.execute("SELECT * FROM tratamiento where activo = 0")
        elif seleccion == "Todos":
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
        busqueda = self.entrada_buscar.get().strip().upper()

        if not busqueda:
            self.tree.delete(*self.tree.get_children())
            self.actualizar_treeview()
            return

        tratamiento_encontrado = False

        for item in self.tree.get_children():
            valores = self.tree.item(item, 'values')
            codigo = valores[0].upper()
            nombre = valores[1].upper()

            if busqueda in codigo or busqueda in nombre:
                tratamiento_encontrado = True
            else:
                self.tree.delete(item)

        if not tratamiento_encontrado:
            messagebox.showwarning("Atención", "No se encontró el tratamiento.")
            self.tree.delete(*self.tree.get_children())
            self.actualizar_treeview()

    def fecha_valida(self,fecha):
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return True
        except ValueError:
            return False


    def volver_menu_principal(self):
        from Menu import MENU
        self.master.destroy()
        ventana = Tk()
        ventana.wm_title("Menú Recupero de Obra Social")
        ventana.wm_resizable(0,0)
        ventana.geometry("+0+0")
        menu = MENU(ventana)
        menu.mainloop()

        

'''ventana = Tk()
ventana.title("Gestion de Tratamientos")
ventana.resizable(False,False)
ventana.geometry("+1+1")
root = GestionTratamiento(ventana)
ventana.mainloop()'''
