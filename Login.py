from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox

class Login(Frame):
    def __init__(self, master):
        super().__init__(master,bg="#e4c09f")
        self.master = master
        self.pack()
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

        label_password = Label(contenedor, text="Ingrese contraseña", padx=10, pady=10,font=("Robot",13), bg="#c9c2b2")
        label_password.pack()
        self.password = Entry(contenedor, font=("Robot",13), width=30)
        self.password.pack()

        login = Button(contenedor, text="Ingresar", command=self.check_login, font=("Robot",13), bg="#e4c09f")
        login.pack(pady=(20, 0))

    def check_login(self):
        if self.usario.get() == "admin" and self.password.get() == "admin":
            messagebox.showinfo("Login", "Usuario o contraseña incorrectos")
        else:
            messagebox.showerror("Login", "Usuario o contraseña incorrectos")

ventana = Tk()
ventana.configure(bg="#e4c09f") 
ventana.title("Inicio de Sesión")
ventana.geometry("900x600")
root = Login(ventana)
ventana.mainloop()