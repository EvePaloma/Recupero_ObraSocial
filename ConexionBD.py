import mysql.connector
from tkinter import messagebox

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
                host="localhost",
                user="root", #PONER SU PROPIO USUARIO
                password="", #PONER SU PROPIA CLAVE
                database="recupero_obra_social")
        print("Conexión exitosa")
        return conexion
    except mysql.connector.Error as err:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {err}")
        return None

def obtener_datos(nombre_tabla, lista_datos_buscar, filtro = None):
    conexion = obtener_conexion()  # Llama a la función que establece la conexión
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return
    try:
        cursor = conexion.cursor()  # Crea el cursor
        if filtro:
            sentencia = f"SELECT {', '.join(lista_datos_buscar)} FROM {nombre_tabla} WHERE {filtro}"
            cursor.execute(sentencia)  # Ejecuta la consulta
        else:
            campos = ", ".join(lista_datos_buscar)
            sentencia = f"SELECT {campos} FROM {nombre_tabla}"  # Inicia la sentencia SQL
            cursor.execute(sentencia)  # Ejecuta la consulta
        
        datos = cursor.fetchall()  # Obtén todos los resultados
        cursor.close()  # Cierra el cursor
        conexion.close()  # Cierra la conexión a la base de datos
        return datos  # Devuelve los datos obtenidos
    except mysql.connector.Error as err:
        messagebox.showerror("Error de Consulta", f"No se pudo realizar la consulta a la base de datos: {err}")
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
        return []  # Devuelve una lista vacía en caso de error
    
def insertar_os(nombre, siglas, telefono, detalle, domicilio_cc, domicilio_cp, cuit, id_afip):
    conexion = obtener_conexion()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return
    try:
        cursor = conexion.cursor() 
        sentencia = "INSERT INTO obra_social (nombre, siglas, telefono, detalle, domicilio_central, domicilio_cp, cuit, id_afip) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        valores = (nombre, siglas, telefono, detalle, domicilio_cc, domicilio_cp, cuit, id_afip)
        cursor.execute(sentencia, valores)
        conexion.commit()
        messagebox.showinfo("Éxito", "Obra Social insertado correctamente.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al insertar en la base de datos: {err}")