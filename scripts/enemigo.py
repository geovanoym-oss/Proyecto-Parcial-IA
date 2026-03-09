# Nombre: Geovan Yassil Perez Encarnacion
# Matricula: 24-EISN-2-037

import pygame
from scripts.ruta_int import a_star # Algoritmo para calcular la mejor ruta
from scripts.arbol_comportamiento import bt_drone # Decide si patrulla o persigue

class Enemigo:
    def __init__(self, x, y, ruta_puntos):
        self.posicion = [x, y]
        self.puntos = ruta_puntos
        self.indice = 0
        self.pasos = 0
        self.bloqueado = 0
        try:
            self.imagen = pygame.image.load("assets/images/dron.png").convert_alpha()
            self.imagen = pygame.transform.scale(self.imagen, (64, 64))
        except: self.imagen = None

    def actualizar(self, pos_jugador, mapa):
        self.pasos += 1

           # Se mueve cada ciertos ciclos para no hacerlo demasiado rápido
        if self.pasos >= 3:
            estado = bt_drone(self.posicion, pos_jugador)
            destino = pos_jugador if estado == "PERSEGUIR" else self.puntos[self.indice]

              # Calcular camino usando A*
            camino = a_star(mapa, self.posicion, destino)
            
            if camino and len(camino) > 0:
                self.posicion = list(camino[0])
                self.bloqueado = 0
            else:
                self.bloqueado += 1

            dist = abs(self.posicion[0] - destino[0]) + abs(self.posicion[1] - destino[1])
            if dist == 0 or self.bloqueado > 5:
                if estado != "PERSEGUIR":
                    self.indice = (self.indice + 1) % len(self.puntos)
                self.bloqueado = 0
            self.pasos = 0

    def dibujar(self, sur, t):
        # Dibuja la imagen del enemigo o un cuadro rojo si no hay imagen
        if self.imagen: sur.blit(self.imagen, (self.posicion[0]*t, self.posicion[1]*t))
        else: pygame.draw.rect(sur, (255,0,0), (self.posicion[0]*t, self.posicion[1]*t, t, t))