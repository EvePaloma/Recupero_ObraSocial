from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from Gestion_Tratamiento import *   
from Gestion_obra_social import *
from Gestion_Medico_completa import *
from Gestion_Pacientes import *

class MENU(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg="#e4c09f", height=700, width=1366)
        self.master = master
        master.geometry("+0+0")
        self.pack_propagate(False)
        self.pack(expand=True)
        self.create_widgets()
        self.master.protocol("WM_DELETE_WINDOW", lambda: None)

    def abrir_paciente(self):
        self.master.destroy()
        ventana = Tk()
        ventana.wm_title("Gestión de Pacientes")
        ventana.wm_resizable(0,0)
        ventana.geometry("+0+0")
        entradas = GestionPaciente(ventana)
        entradas.mainloop()

    def abrir_tratamiento(self):
        self.master.destroy()
        ventana = Tk()
        ventana.wm_title("Gestión de Tratamientos")
        ventana.wm_resizable(0,0)
        ventana.geometry("+0+0")
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
        ventana_principal = Frame(self, bg="#e4c09f")
        ventana_principal.pack(fill="both", expand=True, pady= 15)

        frame_btn = Frame(ventana_principal, bg="#e4c09f")
        frame_btn.grid(row=0, column=0, padx=10, pady=(10, 0),sticky="ne")

        btn_cerrar_sesion = Button(frame_btn, text="Cerrar Sesión", font=("Roboto", 15), width= 15, bg="#c9c2b2", command=self.volver_login)
        btn_cerrar_sesion.grid(row=0, column=0, pady=(0, 10))

        menu = LabelFrame(ventana_principal, padx=20, pady=20, bg="#c9c2b2", height=530, width=1200)
        menu.grid(row=0, column=0, pady= 80, padx= 110)
        menu.grid_propagate(False)


        label_menu = Frame(menu, bg="#c9c2b2")
        label_menu.pack(pady= 15)

        menu_label = Label(label_menu, text="Menú Principal", font=("Roboto", 20), bg="#c9c2b2", width=67)
        menu_label.grid(row=0, column=0, padx=(0,10), pady=(0, 10))

        frame_botones = Frame(menu, bg="#c9c2b2")
        frame_botones.pack(pady= 15)

        btn_paciente = Button(frame_botones, text="Gestión de Paciente", font=("Roboto", 15), bg="#e4c09f", height=2, width=96,command=self.abrir_paciente)
        btn_paciente.grid(row=2, column=0, pady=(0, 20))

        btn_medico = Button(frame_botones, text="Gestión de Médico", font=("Roboto", 15), bg="#e4c09f", height=2, width=96,command=self.abrir_medico)
        btn_medico.grid(row=3, column=0, pady=(0, 20))

        btn_obra_social = Button(frame_botones, text="Gestión de Obra Social", font=("Roboto", 15), bg="#e4c09f", height=2, width=96, command=self.abrir_obra_social)
        btn_obra_social.grid(row=4, column=0, pady=(0, 20))

        btn_tratamiento = Button(frame_botones, text="Gestión de Tratamiento", font=("Roboto", 15), bg="#e4c09f", height=2, width=96,command=self.abrir_tratamiento)
        btn_tratamiento.grid(row=5, column=0, pady=(0, 20))    

        """btn_ficha = Button(menu, text="Gestión de Ficha Médica", font=("Roboto", 15), bg="#e4c09f", width=96)
        btn_ficha.grid(row=6, column=0, pady=(0, 20))"""


if __name__ == "__main__":
    ventana = Tk()
    ventana.wm_title("Menú Recupero de Obra Social")
    ventana.wm_resizable(0,0)
    menu = MENU(ventana)
    menu.mainloop()