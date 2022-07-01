from datetime import datetime
from sys import argv
from csv import DictReader
# Guardo los argumentos pasados por consola
archivo, dni, salida, tipo, *opcionales = argv[1:]
# Le da un formato a la fecha
fecha = datetime.strftime("%d-%m-%Y") ## Cambiar formato ##

with open(archivo) as file:
	reader = DictReader(file)
    ## Leer opcionales ##
    ## Error si se repite codigo de cheque ##
	if (salida == 'PANTALLA'):
		for row in reader:
			# Si el el dni y el tipo son iguales los imprime en pantalla
			if(row['DNI'] == dni and row['Tipo'] == tipo):
				print(row)
	elif (salida == 'CSV'):
		# Abre o crea el archivo csv
		with open(f'{dni}-{fecha}.csv', 'w') as f:
			# Escribe el header en el archivo
			f.write('NumeroCuentaDestino,Valor,FechaOrigen,FechaPago\n')
			for row in reader:
				# Si el el dni y el tipo son iguales los agrega al archivo
				if(row['DNI'] == dni and row['Tipo'] == tipo):
					f.write(
						f'{row["NumeroCuentaDestino"]},{row["Valor"]},{row["FechaOrigen"]},{row["FechaPago"]}')
	else:
		print('Tipo de salida no valido')