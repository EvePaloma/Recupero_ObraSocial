from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

class GestionTratamiento(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg="#e4c09f")
        self.master = master
        self.grid()
        self.createWidgets()

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
        etiqueta_buscar = Label(frame_busqueda, text="Buscar:", bg="#e6c885",font=("Robot",15))
        etiqueta_buscar.grid(row=1, column=1, padx=5, pady=5)

        self.entrada_buscar = Entry(frame_busqueda,width="50")
        self.entrada_buscar.grid(row=1, column=2, padx=5, pady=5)

        img_buscar = Image.open("buscar1.png").resize((30, 30), Image.Resampling.LANCZOS)
        img_buscar = ImageTk.PhotoImage(img_buscar)
        btn_buscar = Button(frame_busqueda, image=img_buscar, width=30, height=30,bg="#e6c885", command=self.buscar_tratamiento)
        btn_buscar.grid(row=1, column=3)
        btn_buscar.image = img_buscar

        boton_agregar = Button(frame_tratamientos, text="Agregar   +", width=15, bg="#e6c885",font=("Robot",15), command=self.agregar_tratamiento)
        boton_agregar.grid(row=1, column=6, padx=10, pady=10)

        #Para que siempre esté atrás de los widgets
        fondo_label.lower()

        #Frame para el Treeview y el scrollbar
        frame_tabla = Frame(frame_tratamientos, bg="#c9c2b2")  # Frame para contener la tabla y el scrollbar
        frame_tabla.grid(row=2, column=0, columnspan=6, padx=10, pady=10, sticky="nsew")
        
        stilo = ttk.Style()
        stilo.configure("Treeview", font=("Robot",12), rowheight=25)  # Cambia la fuente y el alto de las filas
        stilo.configure("Treeview.Heading", font=("Robot",15))  # Cambia la fuente de las cabeceras


        #Treeview para mostrar la tabla de tratamientos dentro del frame_tabla
        self.tree = ttk.Treeview(frame_tabla, columns=("codigo", "procedimiento", "precio"), show='headings', height=5)

        #Títulos de columnas
        self.tree.heading("codigo", text="Código")
        self.tree.heading("procedimiento", text="Procedimiento")
        self.tree.heading("precio", text="Precio")

        #Ancho de las columnas y datos centrados
        self.tree.column("codigo", anchor='center', width=150)
        self.tree.column("procedimiento", anchor='center', width=250)
        self.tree.column("precio", anchor='center', width=150)

        #Ejemplo
        self.tree.insert("", "end", values=("1234", "Tratamiento 1", "$100"))
        self.tree.insert("", "end", values=("5678", "Tratamiento 2", "$150"))
        self.tree.insert("", "end", values=("91011", "Tratamiento 3", "$200"))

        #Grid del frame_tabla
        self.tree.grid(row=0, column=0, sticky="nsew")

        #Scrollbar para la tabla dentro del frame_tabla
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')  #Se expande desde arriba hacia abajo
        self.tree.configure(yscrollcommand=scrollbar.set)

        #Botones(ver, modificar, eliminar)
        btn_ver = Button(frame_tratamientos, text="Ver", width=15, font=("Robot",12),bg="#e6c885", command=self.ver_tratamiento)
        btn_ver.grid(row=3, column=2)

        btn_editar = Button(frame_tratamientos, text="Modificar", width=15, font=("Robot",12),bg="#e6c885", command=self.modificar_tratamiento)
        btn_editar.grid(row=3, column=3)
        
        btn_eliminar = Button(frame_tratamientos, text="Eliminar", width=15,font=("Robot",12),bg="#e6c885", command=self.eliminar_tratamiento)
        btn_eliminar.grid(row=3, column=4, padx=40)

    

ventana = Tk()
ventana.title("Gestion de Tratamientos")
ventana.resizable(False,False)
root = GestionTratamiento(ventana)
ventana.mainloop()
