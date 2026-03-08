# Nombre: Geovan Yassil Perez Encarnacion
# Matricula: 24-EISN-2-037

import heapq

def a_star(mapa, inicio, fin):
      # Convertimos a tupla para poder usarlos como claves en los diccionarios
    inicio, fin = tuple(inicio), tuple(fin)
    frontera = []
    heapq.heappush(frontera, (0, inicio))
    procedencia = {inicio: None}
    costo_acumulado = {inicio: 0}

    while frontera:
        actual = heapq.heappop(frontera)[1]
        if actual == fin: break

 # movimientos posibles (arriba, abajo, derecha, izquierda)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            vecino = (actual[0] + dx, actual[1] + dy)
            if 0 <= vecino[1] < len(mapa) and 0 <= vecino[0] < len(mapa[0]):
                if mapa[vecino[1]][vecino[0]] == 1: continue
                
                nuevo_costo = costo_acumulado[actual] + 1
                
                    # si encontramos un camino mejor lo actualizamos
                if vecino not in costo_acumulado or nuevo_costo < costo_acumulado[vecino]:
                    costo_acumulado[vecino] = nuevo_costo
                    prioridad = nuevo_costo + abs(fin[0]-vecino[0]) + abs(fin[1]-vecino[1])
                    heapq.heappush(frontera, (prioridad, vecino))
                    procedencia[vecino] = actual

    camino = []
    actual = fin
    while actual in procedencia and procedencia[actual] is not None:
        camino.append(actual)
        actual = procedencia[actual]
    camino.reverse()
    return camino