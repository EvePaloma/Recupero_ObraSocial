from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from Menu import *

class Login(Frame):
    def __init__(self, master):
        super().__init__(master,bg="#e4c09f")
        self.master = master
        self.pack()
        self.usuario = ()
        self.contraseña = ()
        self.usuarios = {}
        self.create_widgets()
        
    
    def create_widgets(self):
        img_fondo = Image.open("fondo3.png")
        img_fondo = img_fondo.resize((700, 100), Image.Resampling.LANCZOS)
        self.img_fondo = ImageTk.PhotoImage(img_fondo)

        imagen = Label(self, image=self.img_fondo, padx=10, pady=10)
        imagen.pack(pady=(20, 20))

        contenedor = LabelFrame(self, text="Inicio de Sesión", padx=100, pady=100, bg="#c9c2b2")
        contenedor.pack()

        label_usario = Label(contenedor, text="Ingrese usuario", padx=10, pady=10,font=("Robot",13), bg="#c9c2b2")
        label_usario.pack()
        self.usario = Entry(contenedor, font=("Robot",13), width=30)
        self.usario.pack()

        label_contraseña = Label(contenedor, text="Ingrese contraseña", padx=10, pady=10,font=("Robot",13), bg="#c9c2b2")
        label_contraseña.pack()
        self.contraseña = Entry(contenedor, font=("Robot",13), width=30)
        self.contraseña.pack()

        login = Button(contenedor, text="Ingresar", command=self.check_login, font=("Robot",13), bg="#e4c09f")
        login.pack(pady=(20, 0))

        crear_usuario = Label(contenedor, text="Crear Usuario", font=("Roboto", 10), fg="black", cursor="hand2", bg="#c9c2b2")
        crear_usuario.pack(pady=(10, 0))

        crear_usuario.bind("<Enter>", lambda e: crear_usuario.config(fg="blue", font=("Roboto", 10, "underline")))
        crear_usuario.bind("<Leave>", lambda e: crear_usuario.config(fg="black", font=("Roboto", 10)))
        crear_usuario.bind("<Button-1>", lambda e: self.pedir_admin_login())

    

    def check_login(self):
        if self.usario.get() == "admin" and self.contraseña.get() == "*":
            self.abrir_menu()
        else:
            messagebox.showerror("Login", "Usuario o contraseña incorrectos")

    def abrir_menu(self):
        self.master.destroy()
        ventana = Tk()
        ventana.wm_title("Menú Recupero de Obra Social")
        ventana.wm_resizable(0,0)
        ventana.geometry("+30+15")
        menu = MENU(ventana)
        menu.mainloop()

    def pedir_admin_login(self):
        admin_login = Toplevel(self.master)
        admin_login.title("Login Administrador")
        admin_login.geometry("300x200")

        label_usario = Label(admin_login, text="Usuario Admin:", padx=10, pady=10)
        label_usario.pack()
        admin_usario_entry = Entry(admin_login)
        admin_usario_entry.pack(pady=(0, 10))

        label_contraseña = Label(admin_login, text="Contraseña Admin:", padx=10, pady=10)
        label_contraseña.pack()
        admin_contraseña_entry = Entry(admin_login, show="*")
        admin_contraseña_entry.pack(pady=(0, 10))

        crear_btn = Button(admin_login, text="Iniciar Sesión", 
                           command=lambda: self.verificar_admin(admin_usario_entry.get(), admin_contraseña_entry.get(), admin_login))
        crear_btn.pack()

    def verificar_admin(self, usuario, contraseña, window):
        if usuario == "admin" and contraseña == "admin":  
            window.destroy()  
            self.crear_usuario()  
        else:
            messagebox.showerror("Error", "Credenciales de administrador incorrectas.")

    def crear_usuario(self):
        crear_usuario = Toplevel(self.master)
        crear_usuario.title("Crear Usuario")
        crear_usuario.geometry("300x200")

        label_usario = Label(crear_usuario, text="Nuevo Usuario:", padx=10, pady=10)
        label_usario.pack()
        nuevo_usario_entry = Entry(crear_usuario)
        nuevo_usario_entry.pack(pady=(0, 10))

        label_contraseña = Label(crear_usuario, text="Contraseña:", padx=10, pady=10)
        label_contraseña.pack()
        nuevo_contraseña_entry = Entry(crear_usuario, show="*")
        nuevo_contraseña_entry.pack(pady=(0, 10))

        crear_btn = Button(crear_usuario, text="Crear", 
                           command=lambda: self.guardar_usuario(nuevo_usario_entry.get(), nuevo_contraseña_entry.get(), crear_usuario))
        crear_btn.pack()

    def guardar_usuario(self, usuario, contraseña, ventana):
        if usuario and contraseña:
            if usuario in self.usuarios:
                messagebox.showerror("Error", "El usuario ya existe.")
            else:
                self.usuarios[usuario] = contraseña
                messagebox.showinfo("Éxito", "Usuario creado exitosamente.")
                ventana.destroy()
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")


ventana = Tk()
ventana.configure(bg="#e4c09f") 
ventana.title("Inicio de Sesión")
ventana.geometry("900x600")
root = Login(ventana)
ventana.mainloop()