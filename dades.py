import pandas as pd

# Leer el archivo CSV
df = pd.read_csv('products.csv', sep=';')

# Función para obtener la parte antes del primer número y la parte después
def partir_nombre(nombre):
    nombre_sin_num = ""
    resto_nombre = ""
    for caracter in nombre:
        if caracter.isdigit():
            break
        nombre_sin_num += caracter
    resto_nombre = nombre[len(nombre_sin_num):].strip()
    return nombre_sin_num.strip(), resto_nombre.strip()

# Aplicar la función a la columna 'name' y dividir en dos nuevas columnas
df['name_med'], df['cantidad'] = zip(*df['name'].apply(partir_nombre))

# Guardar el DataFrame resultante en un nuevo archivo CSV
df.to_csv('medicaments.csv', index=False)
