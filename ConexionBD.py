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
        return conexion
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

'''    
def insertar_tratamiento(codigo, nombre, precio, fecha_precio, id_tipo_tratamiento, siglas, descripcion):
    try:
        sql = "INSERT INTO tratamiento (codigo, nombre, precio, fecha_precio, id_tipo_tratamiento, siglas, descripcion) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (codigo, nombre, precio, fecha_precio, id_tipo_tratamiento, siglas, descripcion)  # Ajuste del orden
        mycursor.execute(sql, val)
        conexion.commit()
        messagebox.showinfo("Éxito", "Registro insertado correctamente.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al insertar en la base de datos: {err}")
    finally:
        conexion.close()

def actualizar_tratamiento(id_tratamiento, codigo, nombre, precio, fecha_precio, tipo_tratamiento, siglas, descripcion):
    try:
        sql = "UPDATE tratamiento SET codigo=%s, nombre=%s, precio=%s, fecha_precio=%s, id_tipo_tratamiento=%s, siglas=%s, descripcion=%s WHERE id=%s"
        val = (codigo, nombre, precio, fecha_precio, tipo_tratamiento, siglas, descripcion, id_tratamiento)  # Agregando `id_tratamiento` al final
        mycursor.execute(sql, val)
        conexion.commit()
        messagebox.showinfo("Éxito", "Registro actualizado correctamente.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al actualizar en la base de datos: {err}")
    finally:
        conexion.close()'''

