# Nombre: Geovan Yassil Perez Encarnacion
# Matricula: 24-EISN-2-037


# Nodos base del Behavior Tree

class Nodo:
    def ejecutar(self):
        pass


# Nodo Selector

class Selector(Nodo):
    def __init__(self, hijos):
        self.hijos = hijos

    def ejecutar(self):
        for hijo in self.hijos:
            resultado = hijo.ejecutar()
            if resultado:
                return resultado
        return None


# Nodo de Condicion

class JugadorCerca(Nodo):
    def __init__(self, pos_drone, pos_jugador, distancia=6):
        self.pos_drone = pos_drone
        self.pos_jugador = pos_jugador
        self.distancia = distancia

    def ejecutar(self):
        d = abs(self.pos_drone[0] - self.pos_jugador[0]) + abs(self.pos_drone[1] - self.pos_jugador[1])
        return d < self.distancia

# Nodo de la Accion de Perseguir

class AccionPerseguir(Nodo):
    def ejecutar(self):
        return "PERSEGUIR"
    
# Nodo de la Accion de Patrullar

class AccionPatrullar(Nodo):
    def ejecutar(self):
        return "PATRULLAR"


# Arbol de comportamiento

def bt_drone(pos_drone, pos_jugador):

    condicion = JugadorCerca(pos_drone, pos_jugador)
    perseguir = AccionPerseguir()
    patrullar = AccionPatrullar()

    if condicion.ejecutar():
        return perseguir.ejecutar()

    return patrullar.ejecutar()