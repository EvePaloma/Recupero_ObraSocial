import mysql
import mysql.connector as mysql_connector
from tkinter import messagebox


def obtener_conexion():
    try:
        conexion = mysql_connector.connect(
                host="localhost",
                user="root", #PONER SU PROPIO USUARIO
                password="12345", #PONER SU PROPIA CLAVE
                database="recupero_obra_social")
        print("Conexión exitosa")
        return conexion
    except mysql_connector.Error as err:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {err}")
        return None
    

def insertar_paciente_bd(nombre, apellido, dni, obrasocial, propietario, sexo, telefonopaciente, numeroafiliado):
    conexion = obtener_conexion()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        sql = "INSERT INTO paciente (nombre, apellido, dni, obra_social,proietario,sexo,telefono,nro_afiliado,) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (nombre, apellido, dni, obrasocial, propietario, sexo, telefonopaciente, numeroafiliado)
        cursor.execute(sql, val)
        conexion.commit()
        messagebox.showinfo("Éxito", "Registro insertado correctamente.")
    except mysql_connector.Error as err:
        messagebox.showerror("Error", f"Error al insertar en la base de datos: {err}")
    finally:
        conexion.close()

    #nombre, apellido, dni, obrasocial, obrasocialsec, propietario, fechanac, sexo, telefonopaciente, contactoemergencia, numeroafiliado)
def actualizar_paciente(nombre, apellido, dni, obrasocial, propietario, sexo, telefonopaciente,  numeroafiliado):
    
    conexion = obtener_conexion()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        sql = "UPDATE paciente SET nombre=%s, apellido=%s, telefono=%s, documento=%s WHERE id=%s"
        val = (nombre, apellido, dni, obrasocial, propietario, sexo, telefonopaciente, numeroafiliado)
        cursor.execute(sql, val)
        conexion.commit()
        messagebox.showinfo("Éxito", "Registro actualizado correctamente.")
    except mysql_connector.Error as err:
        messagebox.showerror("Error", f"Error al actualizar en la base de datos: {err}")
    finally:
        conexion.close()