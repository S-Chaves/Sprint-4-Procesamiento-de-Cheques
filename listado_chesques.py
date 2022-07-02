##
# - Suponemos que si hay dos params opcionales el primero es estado y el segundo es fecha
# - Suponemos que si pasa solo fecha no va a pasar más parámetros?
# Si podemos suponer que va a poner todo bien se hace más facil
##
from datetime import datetime
from sys import argv
from csv import DictReader

# Guardo los argumentos pasados por consola
archivo, dni, salida, tipo, *opcionales = argv[1:]
# Le da un formato a la fecha actual
fecha = datetime.now().strftime("%Y-%m-%d") ## "%Y-%m-%d %H/%M/%S"
estado = ''
fecha_inicio = ''
fecha_final = ''

#############
# Funciones #
#############
def filtro_estado(row, estado):
	return row['Estado'] == estado ## Podría no existir ##

def filtro_fecha(row, fecha_inicio, fecha_final):
	""" Chequea que la fecha de origen se encuentre entre fecha_inicio y fecha_final """
	if fecha_inicio == "":
		return False
	# Transformo la fecha en string a objeto fecha
	fecha_origen = datetime.strptime(row['FechaOrigen'], "%d-%m-%Y")
	return fecha_inicio < fecha_origen and fecha_final > fecha_origen

def write_archivo(elem, file):
	file.write(elem)
# Guardamos las funciones en un diccionario para acceder facilmente
funciones = {
	"PANTALLA": print,
	"CSV": write_archivo
}

def chequear_opcionales(row, archivo = ''):
	""" Chequea que parámetro opcional se ingreso y filtra según sea necesario """
	dni_tipo = row['DNI'] == dni and row['Tipo'] == tipo
	if dni_tipo and estado: # Ingresó estado
		if filtro_estado(row, estado): # Chequeamos que el estado pase el filtro
			if filtro_fecha(row, fecha_inicio, fecha_final): # Chequeamos que la fecha pase el filtro
				funciones[salida](row, archivo)
			elif not fecha_inicio: # Entra si no puso fecha o no paso el filtro
				funciones[salida](row, archivo)
	elif dni_tipo and fecha_inicio: # Ingresó fecha
		if filtro_fecha(row, fecha_inicio, fecha_final): # Chequeamos que la fecha pase el filtro
				funciones[salida](row, archivo)
	elif dni_tipo: # No ingreso estado ni fecha
		funciones[salida](row, archivo)

def chequear_fecha(num):
	""" Chequea que el parámetro de fecha ingresado sea válido """
	resultado = opcionales[num].split(":")
	if len(resultado) == 2: ## ¿Sabemos que vamos a recibir solo parámetros válidos? ##
		fecha_inicio = datetime.strptime(resultado[0], "%d-%m-%Y")
		fecha_final = datetime.strptime(resultado[1], "%d-%m-%Y")
		# Si las fechas estan bien retorna una tupla
		return fecha_inicio, fecha_final

#############
# Principal #
#############
with open(archivo) as file:
	reader = DictReader(file)
	
	if len(opcionales):
		if opcionales[0] in ['PENDIENTE', 'APROBADO', 'RECHAZADO']:
			estado = opcionales[0]
			## Podría estar acá en vez de afuera, porque afuera si hay fecha y otra cosa cualquiera entra igual. Todo depende de que asumimos ##
			if len(opcionales) == 2:
				fecha_inicio, fecha_final = chequear_fecha(1) 
		else:
			fecha_inicio, fecha_final = chequear_fecha(0)
	# if len(opcionales) == 2:
	# 			fecha_inicio, fecha_final = chequear_fecha(1)

	## Error si se repite codigo de cheque ##
	if salida == 'PANTALLA':
		for row in reader:
			chequear_opcionales(row)
	elif salida == 'CSV':
		# Abre o crea el archivo csv
		with open(f'{dni}-{fecha}.csv', 'w') as archivo:
			# Escribe el header en el archivo
			archivo.write('NumeroCuentaDestino,Valor,FechaOrigen,FechaPago\n')
			for row in reader:
				fila = f'{row["NumeroCuentaDestino"]},{row["Valor"]},{row["FechaOrigen"]},{row["FechaPago"]}\n'
				chequear_opcionales(fila, archivo)
	else:
		print('Tipo de salida no valido')