##
# Si se pasan dos parámetros opcionales el orden es siempre Estado Fecha.
# Se supone que no se pasan más argumentos que los opcionales.
##
from datetime import datetime
from sys import argv
from csv import DictReader

# Guardamos los argumentos pasados por consola
archivo, dni, salida, tipo, *opcionales = argv[1:]
# Le da un formato a la fecha actual
fecha = datetime.now().strftime("%Y-%m-%d")
estado = ''
fecha_inicio = ''
fecha_final = ''

#############
# Funciones #
#############
def filtro_basico(row):
	return (row['DNI'] == dni) and (row['Tipo'] == tipo)

def filtro_estado(row):
	return filtro_basico(row) and (row['Estado'] == estado)

def filtro_fecha(row):
	fecha_origen = datetime.strptime(row['FechaOrigen'], "%d-%m-%Y")
	return filtro_basico(row) and (fecha_inicio < fecha_origen) and (fecha_final > fecha_origen)

def filtro_ambos(row):
	return filtro_estado(row) and filtro_fecha(row)
# Posibles expresiones para filtrar el archivo
expresiones = {
	"Basico": filtro_basico,
	"Estado": filtro_estado,
	"Fecha": filtro_fecha,
	"Ambos": filtro_ambos
}

def get_expresion():
	""" Retorna las expresiones a utilizar según los parámetros ingresados """
	if estado:
		if fecha_final: # Ingresó Estado y Fecha
			return "Ambos"
		return "Estado" # Ingresó solo Estado
	elif fecha_final:
		return "Fecha" # Ingresó solo Fecha
	return "Basico" # No ingresó ninguno

def filtrar_archivo(archivo):
	""" Filtra el archivo dado dependiendo de los parámetros opcionales """
	expresion = get_expresion()
	# Retornamos una lista filtrada según la expresión retornada por get_expresion
	return [row for row in archivo if expresiones[expresion](row)]

def chequear_fecha(num):
	""" Chequea que el parámetro de fecha ingresado sea válido """
	resultado = opcionales[num].split(":")
	if len(resultado) == 2:
		fecha_inicio = datetime.strptime(resultado[0], "%d-%m-%Y")
		fecha_final = datetime.strptime(resultado[1], "%d-%m-%Y")
		# Si las fechas estan bien retorna una tupla
		return fecha_inicio, fecha_final

#############
# Principal #
#############
with open(archivo) as file:
	reader = DictReader(file)
	# Se chequean los opcionales
	if len(opcionales):
		if opcionales[0] in ['PENDIENTE', 'APROBADO', 'RECHAZADO']:
			estado = opcionales[0]
			if len(opcionales) == 2:
				fecha_inicio, fecha_final = chequear_fecha(1) 
		else:
			fecha_inicio, fecha_final = chequear_fecha(0)

	# Error si se repite codigo de cheque
	filtrado = filtrar_archivo(reader)
	nros_cheque = [elem["NroCheque"] for elem in filtrado]
	if len(nros_cheque) != len(set(nros_cheque)):
		raise ValueError("No pueden haber números de cheque repetidos para un mismo DNI.")

	if salida == 'PANTALLA':
		for row in filtrado:
			print(row)
	elif salida == 'CSV':
		# Abre o crea el archivo csv
		with open(f'{dni}-{fecha}.csv', 'w') as archivo:
			# Escribe el header en el archivo
			archivo.write('NumeroCuentaDestino,Valor,FechaOrigen,FechaPago\n')
			for row in filtrado:
				fila = f'{row["NumeroCuentaDestino"]},{row["Valor"]},{row["FechaOrigen"]},{row["FechaPago"]}\n'
				archivo.write(fila)
	else:
		print('Tipo de salida no valido')