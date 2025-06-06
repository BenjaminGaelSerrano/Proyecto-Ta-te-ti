import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración
ANCHO, ALTO = 400, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Esquivar Asteroides")

# Colores
FONDO = (10, 10, 50)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# Jugador
jugador = pygame.Rect(200, 550, 60, 40)
velocidad_jugador = 5

# Asteroide
asteroide = pygame.Rect(random.randint(0, ANCHO - 50), 0, 50, 50)
velocidad_asteroide = 5

# Bucle del juego
reloj = pygame.time.Clock()
ejecutando = True

while ejecutando:
    reloj.tick(180)
    pantalla.fill(FONDO)

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == pygame.MOUSEBUTTONDOWN:  # Si se hace click con el mouse
            pos_mouse = pygame.mouse.get_pos()     # Obtiene la posición del mouse
            jugador.center = pos_mouse            # Mueve el jugador a la posición del mouse

    # Movimiento del asteroide
    asteroide.y += velocidad_asteroide
    if asteroide.top > ALTO:
        asteroide.x = random.randint(0, ANCHO - asteroide.width)
        asteroide.y = 0

    # Colisión
    if jugador.colliderect(asteroide):
        print("¡Game Over!")
        ejecutando = False

    # Dibujar jugador y asteroide
    pygame.draw.rect(pantalla, BLANCO, jugador)
    pygame.draw.rect(pantalla, ROJO, asteroide)

    pygame.display.flip()

pygame.quit()
