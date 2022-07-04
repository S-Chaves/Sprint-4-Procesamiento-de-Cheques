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
def filtro_fecha(row, fecha_inicio, fecha_final):
	""" Chequea que la fecha de origen se encuentre entre fecha_inicio y fecha_final """
	if fecha_inicio == '':
		return False
	# Se transforma la fecha en string a objeto fecha
	fecha_origen = datetime.strptime(row['FechaOrigen'], "%d-%m-%Y")
	return fecha_inicio < fecha_origen and fecha_final > fecha_origen

def filtrar_archivo(archivo):
	""" Filtra el archivo dado dependiendo de los parámetros opcionales """
	filtrado = []
	for row in archivo:
		dni_tipo = row['DNI'] == dni and row['Tipo'] == tipo
		filtro_estado = row['Estado'] == estado

		if dni_tipo and estado: # Ingresó estado
			if filtro_estado: # Chequeamos que el estado pase el filtro
				if filtro_fecha(row, fecha_inicio, fecha_final): # Ingresó estado y fecha
					filtrado.append(row)
				elif not fecha_inicio: # Ingresó solo estado
					filtrado.append(row)
		elif dni_tipo and fecha_inicio: # Ingresó solo fecha
			if filtro_fecha(row, fecha_inicio, fecha_final):
				filtrado.append(row)
		elif dni_tipo: # No ingreso estado ni fecha
			filtrado.append(row)
	return filtrado

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