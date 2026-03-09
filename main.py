# Nombre: Geovan Yassil Perez Encarnacion
# Matricula: 24-EISN-2-037

import pygame
import sys
from scripts.mapa import MAP_DATA, TAMANO_CELDA
from scripts.jugador import Jugador
from scripts.enemigo import Enemigo

class JuegoRescate:
    def __init__(self):
        pygame.init()
        # Pantalla completa
        self.pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.ancho, self.alto = self.pantalla.get_size()
        pygame.display.set_caption("Sistema de Rescate IA - Geovan Perez")
        
        # Las imagenes del juego
        self.img_muro = self.cargar_grafico("assets/images/muro.png")
        self.img_persona = self.cargar_grafico("assets/images/persona.png")
        self.img_zona = self.cargar_grafico("assets/images/zona segura.png")
        
        # FONDO PARA EL MENU
        try:
            self.img_fondo = pygame.image.load("assets/images/fondo_menu.png").convert()
            self.img_fondo = pygame.transform.scale(self.img_fondo, (self.ancho, self.alto))
        except:
            self.img_fondo = None

        # Sonido y Musica
        try:
            pygame.mixer.music.load("assets/music/bg.mp3")
            pygame.mixer.music.play(-1)
            self.sonido_victoria = pygame.mixer.Sound("assets/sounds/rescate.wav")
            self.sonido_derrota = pygame.mixer.Sound("assets/sounds/perdiste.wav")
        except:
            self.sonido_victoria = self.sonido_derrota = None

        self.fuente_tit = pygame.font.SysFont("Arial", 60, bold=True)
        self.fuente_ui = pygame.font.SysFont("Arial", 30, bold=True)
        self.reloj = pygame.time.Clock()
        self.reiniciar()

    def cargar_grafico(self, ruta):
        try:
            img = pygame.image.load(ruta).convert_alpha()
            return pygame.transform.scale(img, (TAMANO_CELDA, TAMANO_CELDA))
        except: return None

    def reiniciar(self):
        self.protagonista = Jugador(1, 1)
        # Rutas de patrulla para los 3 drones
        r1 = [(28, 1), (15, 1)]
        r2 = [(1, 13), (10, 13)]
        r3 = [(15, 7), (20, 7), (20, 10), (15, 10)]
        
        self.enemigos = [
            Enemigo(28, 1, r1),
            Enemigo(1, 13, r2),
            Enemigo(15, 7, r3)
        ]
        self.inventario = 0 
        self.puntos = 0   
        self.mapa_actual = [fila[:] for fila in MAP_DATA]
        
        # Sobrevivientes extra
        puntos_ext = [(5, 5), (25, 12), (15, 2), (2, 8), (28, 13), (1, 7)]
        for px, py in puntos_ext:
            if self.mapa_actual[py][px] == 0: self.mapa_actual[py][px] = 2

        self.estado = "MENU"

    def ventana_interactiva(self, titulo, sub, color, sonido=None):
        pygame.mixer.music.stop()
        if sonido: sonido.play()
        while True:
            self.pantalla.fill(color)
            t1 = self.fuente_tit.render(titulo, True, (255,255,255))
            t2 = self.fuente_ui.render("1. " + sub, True, (200,200,200))
            t3 = self.fuente_ui.render("2. SALIR", True, (200,200,200))
            self.pantalla.blit(t1, (self.ancho//2-t1.get_width()//2, self.alto//3))
            self.pantalla.blit(t2, (self.ancho//2-t2.get_width()//2, self.alto//2))
            self.pantalla.blit(t3, (self.ancho//2-t3.get_width()//2, self.alto//2 + 60))
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_1: 
                        pygame.mixer.music.play(-1)
                        return
                    if e.key == pygame.K_2: pygame.quit(); sys.exit()

    def jugar(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE: self.ventana_interactiva("PAUSA", "CONTINUAR", (40,40,80))
                if e.key in [pygame.K_w, pygame.K_UP]: self.protagonista.mover(0, -1)
                if e.key in [pygame.K_s, pygame.K_DOWN]: self.protagonista.mover(0, 1)
                if e.key in [pygame.K_a, pygame.K_LEFT]: self.protagonista.mover(-1, 0)
                if e.key in [pygame.K_d, pygame.K_RIGHT]: self.protagonista.mover(1, 0)

        for ene in self.enemigos:
            ene.actualizar(self.protagonista.pos, self.mapa_actual)
            if list(self.protagonista.pos) == list(ene.posicion):
                self.ventana_interactiva("¡ATRAPADO!", "REINTENTAR", (120,0,0), self.sonido_derrota)
                self.reiniciar()
                return

        rx, ry = self.protagonista.pos
        if self.mapa_actual[ry][rx] == 2 and self.inventario < 1:
            self.mapa_actual[ry][rx] = 0
            self.inventario = 1
        
        if self.mapa_actual[ry][rx] == 3 and self.inventario > 0:
            self.puntos += 1
            self.inventario = 0
            if not any(2 in fila for fila in self.mapa_actual):
                self.ventana_interactiva("¡LA MISIÓN HA SIDO UN ÉXITO!", "JUGAR DE NUEVO", (0,100,0), self.sonido_victoria)
                self.reiniciar()
                return
        self.dibujar()

    def dibujar(self):
         # Dibujo mapa, jugador y enemigos
        self.pantalla.fill((20, 20, 20))
        blink = (pygame.time.get_ticks() // 500) % 2 == 0
        for f, fila in enumerate(self.mapa_actual):
            for c, val in enumerate(fila):
                rect = (c*TAMANO_CELDA, f*TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)
                if val == 1 and self.img_muro: self.pantalla.blit(self.img_muro, rect[:2])
                elif val == 2 and self.img_persona: self.pantalla.blit(self.img_persona, rect[:2])
                elif val == 3:
                    if self.img_zona:
                        cx = rect[0] + (TAMANO_CELDA - self.img_zona.get_width()) // 2
                        cy = rect[1] + (TAMANO_CELDA - self.img_zona.get_height()) // 2
                        self.pantalla.blit(self.img_zona, (cx, cy))
                    if blink: pygame.draw.rect(self.pantalla, (0, 255, 0), rect, 3)

        self.protagonista.dibujar(self.pantalla, TAMANO_CELDA)
        for ene in self.enemigos: ene.dibujar(self.pantalla, TAMANO_CELDA)
        
        txt = f"RESCATADOS: {self.puntos} | CARGADO: {'SÍ' if self.inventario else 'NO'}"
        self.pantalla.blit(self.fuente_ui.render(txt, True, (255,255,255)), (20, self.alto - 50))
        pygame.display.flip()

    def ejecutar(self):
        while True:
            if self.estado == "MENU":
                # Dibujamos el fondo si existe, si no, pantalla negra
                if self.img_fondo:
                    self.pantalla.blit(self.img_fondo, (0, 0))
                else:
                    self.pantalla.fill((0,0,0))
                
                # Sombra para que se vea mejor
                titulo_texto = "Rescate Inteligente: Robot Explorador"
                subtitulo_texto = "OPRIMIR EL ESPACIO PARA COMENZAR"
                
                m1_sombra = self.fuente_tit.render(titulo_texto, True, (0,0,0))
                m1 = self.fuente_tit.render(titulo_texto, True, (255,255,255))
                m2 = self.fuente_ui.render(subtitulo_texto, True, (200,200,200))
                
                # Posicion de los textos
                self.pantalla.blit(m1_sombra, (self.ancho//2-m1.get_width()//2 + 2, self.alto//2-50 + 2))
                self.pantalla.blit(m1, (self.ancho//2-m1.get_width()//2, self.alto//2-50))
                self.pantalla.blit(m2, (self.ancho//2-m2.get_width()//2, self.alto//2+30))
                
                pygame.display.flip()
                for e in pygame.event.get():
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE: self.estado = "JUGANDO"
                    if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            else: self.jugar()
            self.reloj.tick(15)

if __name__ == "__main__":
    JuegoRescate().ejecutar()

