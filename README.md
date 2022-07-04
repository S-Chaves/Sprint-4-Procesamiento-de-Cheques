# Sprint 4 Procesamiento de Cheques
Este proyecto permite filtrar archivos csv de cheques según los parámetros ingresados a través de la terminal.

## Como Ejecutar
El archivo se ejecuta utilizando python3 seguido del nombre de este, además de los parámetros obligatorios u opcionales para los filtros.
Los parámetros deben estar en el orden indicado abajo, y si se ingresan ambos opcionales el orden debe ser Estado Fecha.

### Parámetros
- Nombre del archivo csv.
- DNI del cliente donde se filtraran.
- Salida: PANTALLA o CSV.
- Tipo de cheque: EMITIDO o DEPOSITADO.
- Estado del cheque: PENDIENTE, APROBADO, RECHAZADO. (Opcional)
- Rango fecha: dd-mm-yyyy:dd-mm-yyyy. (Opcional)

## Ejemplos
```
python3 listado_cheques.py archivo.csv 28500037 PANTALLA DEPOSITADO
```
```
python3 listado_cheques.py archivo.csv 42312556 CSV EMITIDO APROBADO
```
```
python3 listado_cheques.py archivo.csv 31391126 PANTALLA EMITIDO 03-05-2010:01-04-2012
```
```
python3 listado_cheques.py archivo.csv 33102161 CSV EMITIDO RECHAZADO 13-02-2008:08-12-2020
```
