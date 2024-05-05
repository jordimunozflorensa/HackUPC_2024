import pandas as pd
from tsp import obtener_nombres_camino as tonc
from sa import obtener_nombres_camino as sonc

def decidir_alg(nombre_csv):
    df = pd.read_csv(nombre_csv)
    if len(df) < 16:
        # print("El archivo es pequeño, se usará el algoritmo de fuerza bruta")
        return tonc(nombre_csv)
    else:
        # print("El archivo es muy grande, se usará el algoritmo de recocido simulado")
        return sonc(nombre_csv)
    