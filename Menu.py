from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from Gestion_Tratamiento import *   
from Gestion_obra_social import *
from Gestion_Medico_completa import *

class MENU(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg="#e4c09f", height=780, width=1366)
        self.master = master
        self.pack_propagate(False)
        self.pack(expand=True)
        self.grid()
        self.create_widgets()
        self.master.protocol("WM_DELETE_WINDOW", lambda: None)

    def abrir_tratamiento(self):
        self.master.destroy()
        ventana = Tk()
        ventana.wm_title("Gestión de Tratamientos")
        ventana.wm_resizable(0,0)
        ventana.geometry("+2+15")
        entradas = GestionTratamiento(ventana)
        entradas.mainloop()

    def abrir_obra_social(self):
        self.master.destroy()
        ventana = Tk()
        ventana.wm_title("Gestion de Obras Sociales")
        ventana.wm_resizable(0,0)
        ventana.geometry("+0+0")
        root = Gestion_Obra_Social(ventana)
        ventana.mainloop()

    def abrir_medico(self):
        self.master.destroy()
        ventana = Tk()
        ventana.wm_title("Gestión de Médicos")
        ventana.wm_resizable(0,0)
        ventana.geometry("+0+0")
        entradas = Gestionmedico(ventana)
        entradas.mainloop()

    def volver_login(self):
        self.master.destroy()
        from Login import Login
        
    def create_widgets(self):
        frame_btn = Frame(self, bg="#e4c09f")
        frame_btn.grid(row=0, column=0, padx=10, pady=(10, 0),sticky="ne")

        btn_cerrar_sesion = Button(frame_btn, text="Cerrar Sesión", font=("Roboto", 13), bg="#c9c2b2", command=self.volver_login)
        btn_cerrar_sesion.grid(row=0, column=0, pady=(0, 10))

        menu = LabelFrame(self, text="Menú", padx=20, pady=20, bg="#c9c2b2", height=500, width=1140)
        menu.grid(row=0, column=0, padx=80, pady= 80)
        menu.grid_propagate(False)

        label_menu = LabelFrame(menu, font=("Roboto", 20), bg="#c9c2b2")
        label_menu.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        menu_label = Label(label_menu, text="Menú Principal", font=("Roboto", 20), bg="#c9c2b2", width=67)
        menu_label.grid(row=0, column=0, padx=(0,10), pady=(0, 10))

        btn_paciente = Button(menu, text="Gestión de Paciente", font=("Roboto", 15), bg="#e4c09f", width=96)
        btn_paciente.grid(row=2, column=0, pady=(0, 20))

        btn_medico = Button(menu, text="Gestión de Médico", font=("Roboto", 15), bg="#e4c09f", width=96,command=self.abrir_medico)
        btn_medico.grid(row=3, column=0, pady=(0, 20))

        btn_obra_social = Button(menu, text="Gestión de Obra Social", font=("Roboto", 15), bg="#e4c09f", width=96, command=self.abrir_obra_social)
        btn_obra_social.grid(row=4, column=0, pady=(0, 20))

        btn_tratamiento = Button(menu, text="Gestión de Tratamiento", font=("Roboto", 15), bg="#e4c09f", width=96,command=self.abrir_tratamiento)
        btn_tratamiento.grid(row=5, column=0, pady=(0, 20))    

        btn_ficha = Button(menu, text="Gestión de Ficha Médica", font=("Roboto", 15), bg="#e4c09f", width=96)
        btn_ficha.grid(row=6, column=0, pady=(0, 20))


if __name__ == "__main__":
    ventana = Tk()
    ventana.wm_title("Menú Recupero de Obra Social")
    ventana.wm_resizable(0,0)
    ventana.geometry("+30+15")
    menu = MENU(ventana)
    menu.mainloop()