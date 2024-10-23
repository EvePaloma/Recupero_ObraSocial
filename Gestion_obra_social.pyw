from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
from ConexionBD import obtener_conexion

class Gestion_Obra_Social(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg="#e4c09f", height=700, width=1350)
        self.master = master
        self.pack_propagate(False)
        self.pack(expand=True)
        self.createWidgets()
        self.actualizar_treeview()
        # Sobrescribe el protocolo de cierre de la ventana
        self.master.protocol("WM_DELETE_WINDOW", lambda: None)

    def volver_menu_principal(self):
        from Menu import MENU
        self.master.destroy()
        ventana = Tk()
        ventana.wm_title("Menú Recupero de Obra Social")
        ventana.wm_resizable(0,0)
        ventana.geometry("+30+15")
        menu = MENU(ventana)
        menu.mainloop()

    def solo_letras_numeros(self, char):
        return char.isalpha() or char == " " or char.isdigit()
    def solo_numeros(self, char):
        return char.isdigit()
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
            if campo == "Carácter de AFIP":
                seleccion = self.combo_valores.get()
                if seleccion in self.datos_tabla:
                    self.dato_afip = self.datos_tabla[seleccion]
                    return self.dato_afip
                else:
                    raise ValueError(f"Selección '{seleccion}' no encontrada en datos_tabla.")
            elif campo == "Estado":
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

    def actualizar_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM obra_social where activo = 1")
        lista = cursor.fetchall()
        for os in lista:
            self.tree.insert("", "0", iid=os[0], values=os[1:])
        cursor.close()
        conexion.close()

    def obtener_obra_social_por_id(self, id_obra_social):
        conexion = obtener_conexion()
        try:
            sql = "SELECT * FROM obra_social WHERE id_obra_social = %s"
            cursor = conexion.cursor()
            cursor.execute(sql, (id_obra_social,))
            obra_social = cursor.fetchone()
            if obra_social is None:
                messagebox.showwarning("Advertencia", "No se encontró ningún obra_social con ese ID.")
            return obra_social
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se pudo recuperar el obra_social: {error}")
        finally:
            cursor.close()
            conexion.close()

    def createWidgets(self):
        contenedor_total = Frame(self, bg="#c9c2b2", height= 800)
        self.pack_propagate(False)
        contenedor_total.pack(expand=True, fill= "y")

        #primer frame, contiene la imagen y el titulo de la ventana
        contenedor_titulo = Frame(contenedor_total, bg="#c9c2b2")
        contenedor_titulo.pack(pady= 10)

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
        frame_busqueda = Frame(contenedor_total, bg="#c9c2b2")
        frame_busqueda.pack(fill= "x", padx = 5)
        #separa el campo de busqueda del botón
        frame_busqueda.columnconfigure(4, weight=1)

        #Widgets de búsqueda dentro del frame más chico
        Label(frame_busqueda, text="Buscar:", bg="#c9c2b2",font=("Robot",15)).grid(row=1, column=1, padx=5, pady=2, sticky= W)

        self.entrada_buscar = Entry(frame_busqueda,width="50",font=("Robot",13))
        self.entrada_buscar.grid(row=1, column=2, padx=5, pady=2, sticky= W)

        img_buscar = Image.open("buscar1.png").resize((30, 30), Image.Resampling.LANCZOS)
        img_buscar = ImageTk.PhotoImage(img_buscar)
        btn_buscar = Button(frame_busqueda, image=img_buscar, width=40, height=30,bg="#e6c885", command=self.buscar_obra_social)
        btn_buscar.grid(row=1, column=3, sticky= W)
        btn_buscar.image = img_buscar

        boton_agregar = Button(frame_busqueda, text="Agregar  +", width=15, bg="#e6c885",font=("Robot",15), command=self.agregar_obra_social)
        boton_agregar.grid(row=1, column=5, padx=10, pady=3, sticky= E)
        #Para que siempre esté atrás de los widgets
        fondo_label.lower()

        #Tercer frame, contiene la tabla de OS
        #Frame para el Treeview y el scrollbar
        frame_tabla = Frame(contenedor_total, bg="#c9c2b2", width= 1000)  # Frame para contener la tabla y el scrollbar
        frame_tabla.pack(expand=True)
        
        stilo = ttk.Style()
        stilo.configure("Treeview", font=("Robot",11), rowheight=22)  # Cambia la fuente y el alto de las filas
        stilo.configure("Treeview.Heading", font=("Robot",14), padding= [0, 10])  # Cambia la fuente de las cabeceras
        
        #Treeview para mostrar la tabla de tratamientos dentro del frame_tabla
        self.tree = ttk.Treeview(frame_tabla, columns=("nombre", "siglas", "cuit"), show='headings', height=16)
        self.tree.grid(row=0, column=0, sticky="nsew")

        #Títulos de columnas
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("siglas", text="Siglas")
        self.tree.heading("cuit", text="CUIT")

        #Ancho de las columnas y datos centrados
        self.tree.column("nombre", anchor='center', width=450, stretch=False)
        self.tree.column("siglas", anchor='center', width=300, stretch=False)
        self.tree.column("cuit", anchor='center', width=300, stretch=False)        

        #Scrollbar para la tabla dentro del frame_tabla
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')  #Se expande desde arriba hacia abajo
        self.tree.configure(yscrollcommand=scrollbar.set)

        #Cuarto frame, contiene los botones de ver, modificar y eliminar
        frame_btn = Frame(contenedor_total, bg= "#c9c2b2")
        frame_btn.pack(ipady= 10)

        #Botones(ver, modificar, eliminar)
        btn_ver = Button(frame_btn, text="Ver", width=15, font=("Robot",15), bg="#e6c885", command=self.ver_obra_social)
        btn_ver.grid(row=0, column=1,padx=50)

        btn_editar = Button(frame_btn, text="Modificar", width=15, font=("Robot",15), bg="#e6c885", command=self.modificar_obra_social)
        btn_editar.grid(row=0, column=2,padx=50)
        
        btn_eliminar = Button(frame_btn, text="Eliminar", width=15,font=("Robot",15), bg="#e6c885", command=self.eliminar_obra_social)
        btn_eliminar.grid(row=0, column=3, padx=50)

        btn_volver = Button(frame_btn, text="Volver", width=15 ,font=("Robot",15), bg="#e6c885", command=self.volver_menu_principal)
        btn_volver.grid(row=0, column=4, padx=50)

    #Agregar pbra social a la base de datos.
    def agregar_obra_social(self):
        ventana_agregar = Toplevel(self)
        ventana_agregar.title("Agregar Obra Social")
        ventana_agregar.config(bg="#e4c09f") 
        ventana_agregar.resizable(False,False)
        ventana_agregar.geometry("700x400+400+160")

        validar_letynum = ventana_agregar.register(self.solo_letras_numeros)
        validar_numeros = ventana_agregar.register(self.solo_numeros)

        frame_agregar = LabelFrame(ventana_agregar, text="Agregar Nueva Obra Social", font= ("Robot", 12),padx=10, pady=10, bg="#c9c2b2")
        frame_agregar.pack(padx=10, pady=10, fill="both", expand=True)

        frame_btns = Frame(ventana_agregar, bg="#e4c09f")
        frame_btns.pack(pady=3)

        campos = ["Nombre", "Siglas", "Teléfono", "Detalle", "Domicilio Casa Central", "Domicilio Carlos Paz", "CUIT", "Carácter de AFIP"]
        entradas = {}

        for i, campo in enumerate(campos):     #Devuelve índice y valor de cada elemento 
            Label(frame_agregar, text=campo + ":", bg="#c9c2b2", font=("Robot", 12)).grid(row=i, column=0, padx=10, pady=5, sticky=W)
            #Ingresa los elementos en la combo box y devuelve el valor de la seleccion
            if campo == "Carácter de AFIP":
                lista = self.conectar_tabla("afip")
                # Crear un diccionario para buscar el ID por el nombre
                self.datos_tabla = {dato[1]: dato[0] for dato in lista} 
                self.combo_valores = ttk.Combobox(frame_agregar, width=49, font=("Robot", 10), state="readonly")
                self.combo_valores['values'] = list(self.datos_tabla.keys())
                self.combo_valores.grid(row=i, column=1, padx=10, pady=5)
                self.combo_valores.set(self.combo_valores['values'][0])  # Seleccionar el primer valor por defecto
                self.combo_valores.bind("<<ComboboxSelected>>", lambda event: self.on_seleccion("Carácter de AFIP")) 
            else:
                entry = Entry(frame_agregar, width=40, font=("Robot", 12))
                if campo in ["Nombre", "Siglas"]:
                    entry.config(validate="key", validatecommand=(validar_letynum, '%S'))
                elif campo in ["Teléfono", "CUIT"]:
                    entry.config(validate="key", validatecommand=(validar_numeros, '%S'))
                entry.grid(row=i, column=1, padx=10, pady=5)
            entradas[campo] = entry

        btn_nueva_obra_social = Button(frame_btns, text="Agregar", width=15, font=("Robot", 13),bg="#e6c885", command=lambda: self.guardar_nueva_obra_social(entradas, ventana_agregar))
        btn_nueva_obra_social.grid(row=len(campos), column=0, padx=40, pady=10)
        
        btn_cancelar = Button(frame_btns, text="Cancelar", width=15, font=("Robot", 13), bg="#e6c885", command=ventana_agregar.destroy)
        btn_cancelar.grid(row=len(campos), column=1, padx= 40, pady=10)
    
    def guardar_nueva_obra_social(self, entry, ventana):
        conexion = obtener_conexion()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return

        nombre = entry["Nombre"].get().upper()
        siglas = entry["Siglas"].get().upper()
        telefono = entry["Teléfono"].get()
        detalle = entry["Detalle"].get().upper()
        domicilio_central = entry["Domicilio Casa Central"].get().upper()
        domicilio_cp = entry["Domicilio Carlos Paz"].get().upper()
        cuit = entry["CUIT"].get()
        id_afip = self.dato_afip
        print(nombre, siglas, telefono, detalle, domicilio_central, domicilio_cp, cuit, id_afip)

        # Validar datos y agregar al Treeview
        if nombre and siglas and telefono and cuit:
            try:
                cursor = conexion.cursor()
                sql = "INSERT INTO obra_social (nombre, siglas, telefono, detalle, domicilio_central, domicilio_cp, cuit, id_afip) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (nombre, siglas, telefono, detalle, domicilio_central, domicilio_cp, cuit, id_afip)
                cursor.execute(sql, val)
                conexion.commit()
                messagebox.showinfo("Información", "Obra social agregada exitosamente")
                self.tree.insert("", 0, values=(nombre, siglas, cuit))
                ventana.destroy()
                self.actualizar_treeview()
            except mysql.connector.Error as error:
                messagebox.showerror("Error", f"No se pudo agregar el obra social: {error}")
            finally:
                cursor.close()
                conexion.close()
        else:
            messagebox.showwarning("Atención", "Complete todos los campos.")

    #Ver datos de las obras sociales
    def ver_obra_social(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione una obra social.")
            return

        # Usamos el primer elemento seleccionado (ID oculto)
        id_seleccionado = seleccion[0]
        
        # Obtenemos el obra_social usando el ID
        obra_social_seleccionada = self.obtener_obra_social_por_id(id_seleccionado)

        if obra_social_seleccionada:
            # Abrimos la ventana sin mostrar el ID
            obra_social_reducido = obra_social_seleccionada[0:]  # Aquí excluimos el ID
            self.abrir_ventana_obra_social(obra_social_reducido, modo="ver", seleccion=id_seleccionado)  # Excluimos el ID
        else:
            messagebox.showerror("Error", "No se pudo obtener el obra_social.")
    
    #Ver y/o modificar el elemento seleccionado
    def abrir_ventana_obra_social(self, obra_social, modo, seleccion=None):
        def activar_edicion(entradas, btn_guardar):
            for entry in entradas.values():
                entry.config(state="normal")
            btn_guardar.config(state="normal")
            self.combo_valores.config(state="readonly")
            self.combo_valores_2.config(state="readonly")  

        ventana = Toplevel(self)
        ventana.title("Detalles de obra social")
        ventana.config(bg="#e4c09f")
        ventana.resizable(False, False)
        ventana.geometry("600x450+400+160")
        print(obra_social)

        validar_letynum = ventana.register(self.solo_letras_numeros)
        validar_numeros = ventana.register(self.solo_numeros)

        frame_detalles = LabelFrame(ventana, text="Detalles de obra social", font=("Robot", 10), padx=10, pady=10, bg="#c9c2b2")
        frame_detalles.pack(padx=10, pady=10)

        frame_btns = Frame(ventana, bg="#e4c09f")
        frame_btns.pack(pady=8, padx=10)

        campos = ["Nombre", "Siglas", "Teléfono", "Detalle", "Domicilio Casa Central", "Domicilio Carlos Paz", "CUIT", "Carácter de AFIP", "Estado"]
        valores = list(obra_social)
        entradas = {}

        for i, campo in enumerate(campos):
            Label(frame_detalles, text=campo + ":", bg="#c9c2b2", font=("Robot", 10)).grid(row=i, column=0, padx=10, pady=5, sticky=W)
            if campo == "Carácter de AFIP":
                lista = self.conectar_tabla("afip")
                print(lista) 
                # Crear un diccionario para buscar el ID por el nombre
                self.datos_tabla = {dato[1]: dato[0] for dato in lista} 
                self.combo_valores = ttk.Combobox(frame_detalles, width=38, font=("Robot", 10), state="disabled")
                self.combo_valores['values'] = list(self.datos_tabla.keys())
                self.combo_valores.grid(row=i, column=1, padx=10, pady=5)
                #se ingresa en la combo como valor inicial el nombre del caracter de afip o de estado
                valor_a_buscar = valores[i+1]
                clave_encontrada = next((clave for clave, valor in self.datos_tabla.items() if valor == valor_a_buscar), None)
                self.combo_valores.set(clave_encontrada)
            elif campo == "Estado":
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
                if campo in ["Nombre", "Siglas"]:
                    entry.config(validate="key", validatecommand=(validar_letynum, '%S'))
                if campo in ["Teléfono", "CUIT"]:
                    entry.config(validate="key", validatecommand=(validar_numeros, '%S'))
                entry.grid(row=i, column=1, padx=10, pady=5)
                if i + 1 < len(valores):
                    entry.insert(0,str(valores[i + 1]))
            entradas[campo] = entry

        if modo == "ver":
            for entry in entradas.values():
                entry.config(state="readonly")

            self.combo_valores.config(state="disabled")
            self.combo_valores_2.config(state="disabled")

            btn_editar = Button(frame_btns, text="Modificar", width=15, font=("Robot", 13), bg="#e6c885", command=lambda: activar_edicion(entradas,btn_guardar))
            btn_editar.grid(row = 0, column=0, padx=25,pady=10)

            btn_guardar = Button(frame_btns, text="Guardar Cambios", width=15, font=("Robot", 13), bg="#e6c885", command=lambda: self.guardar_cambios(entradas, ventana, seleccion))
            btn_guardar.grid(row = 0, column=1, padx=25,pady=10)
            btn_guardar.config(state="disabled")  # Iniciar como deshabilitado

            btn_editar = Button(frame_btns, text="Cancelar", width=15, font=("Robot", 13), bg="#e6c885", command=ventana.destroy)
            btn_editar.grid(row = 0, column=2, padx=25,pady=10)

        if modo == "modificar":
            self.combo_valores.config(state="readonly")
            self.combo_valores_2.config(state="readonly")
            self.combo_valores.bind("<<ComboboxSelected>>", self.on_seleccion("Carácter de AFIP"))
            self.combo_valores_2.bind("<<ComboboxSelected>>", lambda event: self.on_seleccion("Estado"))

            btn_guardar = Button(frame_btns, text="Guardar Cambios", width=15, font=("Robot", 13), bg="#e6c885", command=lambda: self.guardar_cambios(entradas, ventana, seleccion))
            btn_guardar.grid(row=len(campos), column=0,  padx=40, pady=10)

            btn_cancelar = Button(frame_btns, text="Cancelar", width=15, font=("Robot", 13), bg="#e6c885", command=ventana.destroy)
            btn_cancelar.grid(row=len(campos), column=1, padx= 40, pady=10)
    
    def guardar_cambios(self, entradas, ventana, seleccion):
        conexion = obtener_conexion()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return
        nuevos_valores = {campo: entradas[campo].get().upper() for campo in entradas}
        nuevos_valores['Carácter de AFIP'] = self.on_seleccion("Carácter de AFIP")
        nuevos_valores['Estado'] = self.on_seleccion("Estado")
        print("nuevos valores ", nuevos_valores)
        # Asegúrate de que 'seleccion' no sea None y tenga un valor válido
        if seleccion:
            try:
                cursor = conexion.cursor()
                sql = "UPDATE obra_social SET nombre = %s, siglas = %s, telefono = %s, detalle = %s, domicilio_central = %s, domicilio_cp = %s, cuit = %s, id_afip = %s, activo = %s WHERE id_obra_social=%s"
                val = (
                    nuevos_valores['Nombre'], 
                    nuevos_valores['Siglas'],
                    nuevos_valores['Teléfono'],
                    nuevos_valores['Detalle'], 
                    nuevos_valores['Domicilio Casa Central'], 
                    nuevos_valores['Domicilio Carlos Paz'],
                    nuevos_valores['CUIT'],
                    nuevos_valores['Carácter de AFIP'],
                    nuevos_valores['Estado'],
                    seleccion  # Usa el ID original del obra_social que estás modificando
                )
                obligatorios = ['nombre', 'siglas', 'telefono', 'cuit', 'id_afip']

                if any(elemento  == "" for elemento in obligatorios):
                    messagebox.showerror("Error", "Hay campos obligatorios vacíos.")
                    return
                cursor.execute(sql, val)
                conexion.commit()
                messagebox.showinfo("Información", "Obra social modificada correctamente.")
                ventana.destroy()
                self.actualizar_treeview()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Ocurrió un error al actualizar la obra social: {err}")
            finally:
                cursor.close()
                conexion.close()

    def modificar_obra_social(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione una obra social.")
            return
        # Usamos el primer elemento seleccionado (ID oculto)
        id_seleccionado = seleccion[0]
        # Aquí obtenemos los valores del obra_social usando el ID
        obra_social_seleccionado = self.obtener_obra_social_por_id(id_seleccionado)
        if obra_social_seleccionado:
            # Abrimos la ventana sin mostrar el ID
            obra_social_reducido = obra_social_seleccionado[0:]  # Aquí excluimos el ID
            self.abrir_ventana_obra_social(obra_social_reducido, modo="modificar", seleccion=id_seleccionado)
        else:
            messagebox.showerror("Error", "No se pudo obtener la obra social para modificar.")
    
    #Se elimina la obra social seleccionada, se pasa de activo a inactivo
    def eliminar_obra_social(self):
        conexion = obtener_conexion()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione una obra social para eliminar.")
            return

        id_seleccion = seleccion[0]
        #Pregunta al usuario si está seguro de eliminar 
        respuesta = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar la obra social seleccionada?")
        if respuesta:
            try:
                cursor = conexion.cursor()
                cursor.execute("UPDATE obra_social SET activo = 0 WHERE id_obra_social = %s", (id_seleccion,))
                conexion.commit()
                messagebox.showinfo("Información", "obra social eliminada correctamente.")
                self.actualizar_treeview()
            except mysql.connector.Error as error:
                messagebox.showerror("Error", f"No se pudo eliminar la obra social: {error}")
            finally:
                cursor.close()
                conexion.close()

    def buscar_obra_social(self):
        busqueda = self.entrada_buscar.get().strip().upper()

        if not busqueda:
            self.tree.delete(*self.tree.get_children())
            self.actualizar_treeview()
            return

        coincidencias = []

        for item in self.tree.get_children():
            valores = self.tree.item(item, 'values')
            nombre = valores[1].upper()
            siglas = valores[2].upper()

            if busqueda in nombre or busqueda in siglas:
                coincidencias.append(valores)

        if not coincidencias:
            messagebox.showwarning("Atención", "No se encontró la obra social.")
            self.tree.delete(*self.tree.get_children())
            self.actualizar_treeview()
        else:
            self.tree.delete(*self.tree.get_children())
            for valores in coincidencias:
                self.tree.insert('', 'end', values=valores)

"""ventana = Tk()
ventana.title("Gestion de obra_socials")
ventana.resizable(False,False)
ventana.geometry("+0+0")
root = Gestion_Obra_Social(ventana)
ventana.mainloop()"""