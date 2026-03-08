# Nombre: Geovan Yassil Perez Encarnacion
# Matricula: 24-EISN-2-037

import pygame
from scripts.mapa import TAMANO_CELDA, MAP_DATA

# Esta es la clase que representa al jugador (el robot)
class Jugador:
    def __init__(self, x, y):
        self.pos = [x, y]
        try:
            self.img = pygame.image.load("assets/images/robot.png").convert_alpha()
            self.img = pygame.transform.scale(self.img, (TAMANO_CELDA, TAMANO_CELDA))
        except: self.img = None

 # Funcion para mover al jugador en el mapa
    def mover(self, dx, dy):
        nueva_x = self.pos[0] + dx
        nueva_y = self.pos[1] + dy
        if 0 <= nueva_x < len(MAP_DATA[0]) and 0 <= nueva_y < len(MAP_DATA):
            if MAP_DATA[nueva_y][nueva_x] != 1: # 1 es muro
                self.pos = [nueva_x, nueva_y]
                
                # Funcion para dibujar al jugador en la pantalla

    def dibujar(self, sur, t):
        if self.img: sur.blit(self.img, (self.pos[0]*t, self.pos[1]*t))
        else: pygame.draw.rect(sur, (0,255,0), (self.pos[0]*t, self.pos[1]*t, t, t))