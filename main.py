# Nombre: Geovan Yassil Perez Encarnacion
# Matricula: 24-EISN-2-037

import pygame
import sys
from scripts.mapa import MAP_DATA, TAMANO_CELDA
from scripts.jugador import Jugador
from scripts.enemigo import Enemigo

def juego():
    pygame.init()
    # Ventana de desarrollo
    pantalla = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Rescate IA - Geovan Perez")
    reloj = pygame.time.Clock()

    # Inicialización de objetos
    robot = Jugador(1, 1)
    # Definimos rutas simples para los drones
    enemigos = [
        Enemigo(28, 1, [(28, 1), (15, 1)]),
        Enemigo(1, 13, [(1, 13), (10, 13)]),
        Enemigo(15, 7, [(15, 7), (20, 7)])
    ]

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP: robot.mover(0, -1)
                if e.key == pygame.K_DOWN: robot.mover(0, 1)
                if e.key == pygame.K_LEFT: robot.mover(-1, 0)
                if e.key == pygame.K_RIGHT: robot.mover(1, 0)

        # Logica de enemigos
        for ene in enemigos:
            ene.actualizar(robot.pos, MAP_DATA)

        pantalla.fill((20, 20, 20)) # Fondo gris casi negro

        # 1. dibujamos el laberinto (Sin imagenes)
        for f, fila in enumerate(MAP_DATA):
            for c, val in enumerate(fila):
                rect = (c * TAMANO_CELDA, f * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)
                if val == 1: # MUROS
                    pygame.draw.rect(pantalla, (100, 100, 100), rect) # Rectangulo gris
                    pygame.draw.rect(pantalla, (50, 50, 50), rect, 2) # Borde
                elif val == 2: # PERSONAS
                    pygame.draw.circle(pantalla, (255, 200, 0), (rect[0]+32, rect[1]+32), 15)
                elif val == 3: # ZONA SEGURA
                    pygame.draw.rect(pantalla, (0, 150, 0), rect)

        # 2. dibujamos jugadory enemigos (Formas basicas)
        robot.dibujar(pantalla, TAMANO_CELDA)
        for ene in enemigos:
            ene.dibujar(pantalla, TAMANO_CELDA)

        pygame.display.flip()
        reloj.tick(15)

if __name__ == "__main__":
    juego()