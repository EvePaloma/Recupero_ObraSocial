import mysql.connector
from tkinter import messagebox

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="Gaspar",
            password="yarco7mysql",
            database="hospital"
        )
        return conexion
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al conectar con la base de datos: {err}")
        return None

def insertar_medico(nombre, apellido, matricula, telefono, documento):
    conexion = obtener_conexion()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        sql = "INSERT INTO medico (nombre, apellido, matricula, telefono, documento) VALUES (%s, %s, %s, %s, %s)"
        val = (nombre, apellido, matricula, telefono, documento)
        cursor.execute(sql, val)
        conexion.commit()
        messagebox.showinfo("Éxito", "Registro insertado correctamente.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al insertar en la base de datos: {err}")
    finally:
        conexion.close()

def actualizar_medico(id_medico, nombre, apellido, matricula, telefono, documento):
    conexion = obtener_conexion()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        sql = "UPDATE medico SET nombre=%s, apellido=%s, matricula=%s, telefono=%s, documento=%s WHERE id=%s"
        val = (nombre, apellido, matricula, telefono, documento, id_medico)
        cursor.execute(sql, val)
        conexion.commit()
        messagebox.showinfo("Éxito", "Registro actualizado correctamente.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al actualizar en la base de datos: {err}")
    finally:
        conexion.close()