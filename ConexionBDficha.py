import mysql.connector as mysql_connector
from tkinter import messagebox

def obtener_conexion():
    try:
        conexion = mysql_connector.connect(
            host="localhost",
            user="root",  # PONER SU PROPIO USUARIO
            password="12345",  # PONER SU PROPIA CLAVE
            database="recupero_obra_social"
        )
        print("Conexión exitosa")
        return conexion
    except mysql_connector.Error as err:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {err}")
        return None

def insertar_ficha_bd(nombre, apellido, dni, obra_social, propietario, telefono, nro_afiliado, nombre_medico, apellido_medico, especialidad, tipo_matricula, matricula, servicio, fecha, codigo, nombre_procedimiento, precio, tipo_tratamiento, siglas):
    conexion = obtener_conexion()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        sql = """
        INSERT INTO paciente (nombre, apellido, dni, obra_social, propietario, telefono, nro_afiliado, nombre_medico, apellido_medico, especialidad, tipo_matricula, matricula, servicio, fecha, codigo, nombre_procedimiento, precio, tipo_tratamiento, siglas)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        val = (nombre, apellido, dni, obra_social, propietario, telefono, nro_afiliado, nombre_medico, apellido_medico, especialidad, tipo_matricula, matricula, servicio, fecha, codigo, nombre_procedimiento, precio, tipo_tratamiento, siglas)
        cursor.execute(sql, val)
        conexion.commit()
        messagebox.showinfo("Éxito", "Registro insertado correctamente.")
    except mysql_connector.Error as err:
        messagebox.showerror("Error", f"Error al insertar en la base de datos: {err}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def actualizar_ficha(nombre, apellido, dni, obra_social, propietario, telefono, nro_afiliado, nombre_medico, apellido_medico, especialidad, tipo_matricula, matricula, servicio, fecha, codigo, nombre_procedimiento, precio, tipo_tratamiento, siglas):
    
    conexion = obtener_conexion()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        sql = "UPDATE paciente SET nombre=%s, apellido=%s, telefono=%s, documento=%s WHERE id=%s"
        val = (nombre, apellido, dni, obra_social, propietario, telefono, nro_afiliado, nombre_medico, apellido_medico, especialidad, tipo_matricula, matricula, servicio, fecha, codigo, nombre_procedimiento, precio, tipo_tratamiento, siglas)
        cursor.execute(sql, val)
        conexion.commit()
        messagebox.showinfo("Éxito", "Registro actualizado correctamente.")
    except mysql_connector.Error as err:
        messagebox.showerror("Error", f"Error al actualizar en la base de datos: {err}")
    finally:
        conexion.close()