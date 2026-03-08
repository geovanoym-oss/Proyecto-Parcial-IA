# Nombre: Geovan Yassil Perez Encarnacion
# Matricula: 24-EISN-2-037


import pygame
import sys
from scripts.mapa import MAP_DATA, TAMANO_CELDA
from scripts.jugador import Jugador

def juego():
    pygame.init()
        # Creo la ventana del juego con un tamaño de 1280x720
    pantalla = pygame.display.set_mode((1280, 720))
    robot = Jugador(1, 1) # Creo al jugador

      # Bucle principal del juego 
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP: robot.mover(0, -1)
                if e.key == pygame.K_DOWN: robot.mover(0, 1)
                if e.key == pygame.K_LEFT: robot.mover(-1, 0)
                if e.key == pygame.K_RIGHT: robot.mover(1, 0)

        pantalla.fill((0,0,0))
        # Dibujo del mapa y jugador
        robot.dibujar(pantalla, TAMANO_CELDA)
        pygame.display.flip()

if __name__ == "__main__":
    juego()