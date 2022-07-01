from datetime import datetime
from sys import argv
from csv import DictReader
# Guardo los argumentos pasados por consola
archivo, dni, salida, tipo, *opcionales = argv[1:]
# Le da un formato a la fecha
fecha = datetime.now().strftime("%Y-%m-%d") ## "%Y-%m-%d %H/%M/%S"
estado = ''
fecha_inicio = ''
fecha_final = ''
hay_fecha = False

def chequear_estado(row, estado):
	if row['Estado'] == estado:
		return True
	return False

def chequear_fecha(row, fecha_inicio, fecha_final):
	if (fecha_inicio == "" or fecha_final == ""):
		return False
	fecha_origen = datetime.strptime(row['FechaOrigen'], "%d-%m-%Y")
	if fecha_inicio < fecha_origen and fecha_final > fecha_origen:
		return True
	return False

with open(archivo) as file:
	reader = DictReader(file)
	if len(opcionales) != 0:
		opciones_estado = ['PENDIENTE', 'APROBADO', 'RECHAZADO']
		if opcionales[0] in opciones_estado:
			estado = opcionales[0]
		else:
			resultado = opcionales[0].split(":")

			if len(resultado) == 2:
				fecha_inicio = datetime.strptime(resultado[0], "%d-%m-%Y")
				fecha_final = datetime.strptime(resultado[1], "%d-%m-%Y")
				hay_fecha = True
	if len(opcionales) == 2:
		resultado = opcionales[1].split(":")

		if len(resultado) == 2:
			fecha_inicio = datetime.strptime(resultado[0], "%d-%m-%Y")
			fecha_final = datetime.strptime(resultado[1], "%d-%m-%Y")
			hay_fecha = True

	## Error si se repite codigo de cheque ##
	if (salida == 'PANTALLA'):
		for row in reader:
			# Si el el dni y el tipo son iguales los imprime en pantalla
			dni_tipo = row['DNI'] == dni and row['Tipo'] == tipo
			if (dni_tipo and estado): # Ingresó estado
				if chequear_estado(row, estado): # Chequeamos que el estado sea el mismo
					if chequear_fecha(row, fecha_inicio, fecha_final): 
						print(row)
					elif not hay_fecha:
						print(row)
			elif (dni_tipo and hay_fecha): # Ingresó fecha
				if chequear_fecha(row, fecha_inicio, fecha_final): 
						print(row)
			elif dni_tipo: # No hay estado ni fecha
				print(row)
	
	elif (salida == 'CSV'):
		# Abre o crea el archivo csv
		with open(f'{dni}-{fecha}.csv', 'w') as archivo:
			# Escribe el header en el archivo
			archivo.write('NumeroCuentaDestino,Valor,FechaOrigen,FechaPago\n')
			for row in reader:
				fila = f'{row["NumeroCuentaDestino"]},{row["Valor"]},{row["FechaOrigen"]},{row["FechaPago"]}\n'
				dni_tipo = row['DNI'] == dni and row['Tipo'] == tipo
				if (dni_tipo and estado): # Ingresó estado
					if chequear_estado(row, estado): # Chequeamos que el estado sea el mismo
						if chequear_fecha(row, fecha_inicio, fecha_final): 
							archivo.write(fila)
						elif not hay_fecha:
								archivo.write(fila)
				elif (dni_tipo and hay_fecha): # Ingresó fecha
					if chequear_fecha(row, fecha_inicio, fecha_final): 
							archivo.write(fila)
				elif dni_tipo: # No hay estado ni fecha
					archivo.write(fila)
	else:
		print('Tipo de salida no valido')
