import pandas as pd
from tsp import obtener_nombres_camino as tonc
from sa import obtener_nombres_camino as sonc

def decidir_alg(nombre_csv):
    df = pd.read_csv(nombre_csv)
    if len(df) < 16:
        return tonc(nombre_csv)
    else:
        return sonc(nombre_csv)