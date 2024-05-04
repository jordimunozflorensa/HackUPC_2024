import csv
import random

# Leer el archivo CSV original
productos = []
with open('products.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        productos.append(row)

# Crear la lista de productos con cantidades y localizaciones aleatorias
productos_lista = []
for _ in range(random.randint(20,20)):
    producto = random.choice(productos)
    cantidad = random.randint(1, 7)
    localizacion = [random.randint(1, 20), random.randint(1, 20), random.randint(1, 20)]
    productos_lista.append({'name': producto['name'], 'cantidad': cantidad, 'localizacion': localizacion})

# Escribir la lista de productos en un nuevo archivo CSV
with open('lista_productos.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['name', 'cantidad', 'localizacion']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for producto in productos_lista:
        writer.writerow(producto)
