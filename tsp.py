import csv
import itertools
import numpy as np
from scipy.spatial.distance import pdist, squareform

def leer_lista_productos(archivo):
    """Lee el archivo CSV de la lista de productos y devuelve una lista de localizaciones."""
    localizaciones = []
    with open(archivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            localizaciones.append(list(map(int, row['localizacion'].strip('[]').split(','))))
        #print(localizaciones)
    return localizaciones

def calcular_distancias(localizaciones):
    """Calcula las distancias entre todas las localizaciones."""
    distancias = squareform(pdist(localizaciones, metric='cityblock'))
    #print(distancias)
    return distancias

def tsp_travelling_salesman(distancias):
    """Resuelve el problema del travelling salesman."""
    n = distancias.shape[0]
    menor_costo = np.inf
    mejor_camino = None
    for camino in itertools.permutations(range(n)):
        costo = sum(distancias[camino[i-1], camino[i]] for i in range(n))
        if costo < menor_costo:
            menor_costo = costo
            mejor_camino = camino
    return mejor_camino, menor_costo

def tsp_fast_travelling_salesman(distancias):
    n = distancias.shape[0]
    dp = [[10000000000000] * 20 for _ in range(1 << 20)]

    dp[1][0] = 0

    for msk in range(2, 1 << n):
        for v in range(n):
            if not msk & (1 << v):
                continue
            for u in range(n):
                if msk & (1 << u):
                    dp[msk][v] = min(dp[msk][v], dp[msk - (1 << v)][u] + distancias[u][v])
        
    sol = 10000000000000
    for i in range(1, n):
        sol = min(sol, dp[(1 << n) - 1][i] + distancias[i][0])

    return sol

# Leer la lista de productos y calcular las distancias
localizaciones = leer_lista_productos('lista_productos.csv')
distancias = calcular_distancias(localizaciones)

# Resolver el problema del travelling salesman
menor_costo = tsp_fast_travelling_salesman(distancias)

#print("Mejor camino:", mejor_camino)
print("Menor costo:", menor_costo)