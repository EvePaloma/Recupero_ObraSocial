import mysql.connector
from tkinter import messagebox

    
    # Datos de conexión a la base de datos (reemplázalos con tus datos)
def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
                host="localhost",
                user="root", #PONER SU PROPIO USUARIO
                password="123", #PONER SU PROPIA CLAVE
                database="recupero_obra_social")
        print("Conexión exitosa")
        return conexion
    except mysql.connector.Error as err:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {err}")
        return None


