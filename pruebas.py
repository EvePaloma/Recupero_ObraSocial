from ConexionBD import *

id_seleccionado = "GEA"

campos = ["Nombre", "Siglas", "Teléfono", "Detalle", "Domicilio Casa Central", "Domicilio Carlos Paz", "CUIT", "Carácter de AFIP"]
columnas = ["nombre", "siglas", "telefono", "detalle", "domicilio_central", "domicilio_cp", "cuit", "id_afip"]

datos = obtener_datos("obra_social", columnas, f"nombre = '{id_seleccionado}'")

print(datos)