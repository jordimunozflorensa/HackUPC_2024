import pandas as pd
import random
import math

# Función para leer un archivo CSV y devolver un DataFrame de Pandas
def read_csv(filename):
    df = pd.read_csv(filename)
    return df

# Función para calcular la distancia de Manhattan entre dos puntos
def manhattan_distance(loc1, loc2):
    return sum(abs(x - y) for x, y in zip(loc1, loc2))

# Función para calcular la distancia total recorrida en un orden dado de visitas a las localizaciones
def total_distance(order, localizaciones):
    total = manhattan_distance(localizaciones[0], localizaciones[order[0]])  # Distancia desde el punto de inicio al primero en el orden
    for i in range(len(order) - 1):
        total += manhattan_distance(localizaciones[order[i]], localizaciones[order[i+1]])  # Distancia entre cada par de localizaciones en el orden
    total += manhattan_distance(localizaciones[order[-1]], localizaciones[0])  # Distancia de regreso desde el último punto al punto de inicio
    return total

# Función que implementa el algoritmo de recocido simulado para resolver el problema del viajante
def simulated_annealing(localizaciones, T_max=1000, T_min=1, max_iter=10000, alpha=0.99):
    n = len(localizaciones)
    current_order = list(range(n))  # Genera un orden inicial aleatorio de visitas
    random.shuffle(current_order)
    current_cost = total_distance(current_order, localizaciones)  # Calcula el costo inicial
    best_order = current_order.copy()  # Inicializa el mejor orden encontrado
    best_cost = current_cost  # Inicializa el mejor costo encontrado

    T = T_max
    for _ in range(max_iter):
        T *= alpha
        if T < T_min:
            break
        i, j = random.sample(range(n), 2)  # Selecciona dos índices aleatorios para intercambiar
        new_order = current_order.copy()
        new_order[i], new_order[j] = new_order[j], new_order[i]  # Realiza un movimiento aleatorio
        new_cost = total_distance(new_order, localizaciones)  # Calcula el costo del nuevo orden
        delta_cost = new_cost - current_cost  # Calcula el cambio de costo
        # Acepta el nuevo orden si es mejor o con una cierta probabilidad si es peor
        if delta_cost < 0 or random.random() < math.exp(-delta_cost / T):
            current_order = new_order
            current_cost = new_cost
            # Actualiza el mejor orden y costo si el nuevo es mejor
            if current_cost < best_cost:
                best_order = current_order.copy()
                best_cost = current_cost
    
    # Devuelve el mejor orden y costo encontrado
    return [0] + best_order + [0], best_cost

def cojer_nombres(filename, mejor_camino):
    # Leer el archivo CSV
    df = pd.read_csv(filename)
    
    # Crear un diccionario para mapear los índices de fila a los nombres correspondientes
    index_to_name = {index: row['name'] for index, row in df.iterrows()}
    
    # Crear una lista de nombres de acuerdo a los índices del mejor camino
    best_path_names = [index_to_name[index-1] for index in mejor_camino]
    
    return best_path_names

# Función principal del programa
def obtener_nombres_camino(nombre_csv):
    df = read_csv(nombre_csv)  # Lee el archivo CSV proporcionado
    localizaciones = [eval(loc) for loc in df['localizacion']]  # Extrae las coordenadas de localización del DataFrame
    start_location = [0, 0, 0]  # Define el punto de inicio
    localizaciones.insert(0, start_location)  # Inserta el punto de inicio en la lista de localizaciones
    mejor_camino, menor_costo = simulated_annealing(localizaciones)  # Aplica el algoritmo de recocido simulado
    mejor_camino = [x for x in mejor_camino if x != 0]  # Elimina los puntos de inicio y fin del mejor camino

    mejor_camino = cojer_nombres(nombre_csv, mejor_camino)

    return mejor_camino
    # print("Mejor orden de visitas:", mejor_camino)  # Imprime el mejor orden de visitas encontrado
    # print("Costo total:", menor_costo)  # Imprime el costo total del mejor camino encontrado

# print(obtener_nombres_camino('lista_productos.csv'))  # Llama a la función principal con el nombre del archivo CSV
