#Geovan Yassil Perez Encarnacion


import pygame
import sys
from scripts.mapa import MAP_DATA, TAMANO_CELDA

def test_mapa():
    pygame.init()
    # Aqui hice una ventana normal, no pantalla completa aún
    pantalla = pygame.display.set_mode((1280, 720))
    reloj = pygame.time.Clock()
    
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
        
        pantalla.fill((0,0,0))
        # Dibuje solo los muros para probar la estructura
        for f, fila in enumerate(MAP_DATA):
            for c, val in enumerate(fila):
                if val == 1:
                    pygame.draw.rect(pantalla, (50,50,50), (c*TAMANO_CELDA, f*TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
        
        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    test_mapa()