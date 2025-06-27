import pygame

pygame.init()

# Tamaño de pantalla
ANCHO, ALTO = 700, 700
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("TA-TE-TI")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)  # X
ROJO = (255, 0, 0)  # O
VERDE = (0, 200, 0)  # Para mostrar línea ganadora

CELDA = ANCHO // 3

# Inicialización
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont(None, 60)


# ----------- FUNCIONES --------------

def crear_tablero():
    return [[0 for _ in range(3)] for _ in range(3)]


def crear_matriz_rect():
    matriz = []
    for fila in range(3):
        fila_celdas = []
        for col in range(3):
            x = col * CELDA
            y = fila * CELDA
            celda_rect = pygame.Rect(x, y, CELDA, CELDA)
            fila_celdas.append(celda_rect)
        matriz.append(fila_celdas)
    return matriz


def dibujar_tablero():
    pantalla.fill(BLANCO)
    for i in range(1, 3):
        pygame.draw.line(pantalla, NEGRO, (i * CELDA, 0), (i * CELDA, ALTO), 3)
        pygame.draw.line(pantalla, NEGRO, (0, i * CELDA), (ANCHO, i * CELDA), 3)


def dibujar_figuras():
    for (f, c), lineas_x in lineas.items():
        for linea in lineas_x:
            pygame.draw.line(pantalla, AZUL, linea[0], linea[1], 3)
    for (f, c), centro in circulos.items():
        pygame.draw.circle(pantalla, ROJO, centro, CELDA // 3, 3)


def verificar_victoria(tablero):
    # Filas y columnas
    for i in range(3):
        if tablero[i][0] == tablero[i][1] == tablero[i][2] != 0:
            return (tablero[i][0], ((0, i), (2, i)))  # fila
        if tablero[0][i] == tablero[1][i] == tablero[2][i] != 0:
            return (tablero[0][i], ((i, 0), (i, 2)))  # columna
    # Diagonales
    if tablero[0][0] == tablero[1][1] == tablero[2][2] != 0:
        return (tablero[0][0], ((0, 0), (2, 2)))
    if tablero[0][2] == tablero[1][1] == tablero[2][0] != 0:
        return (tablero[0][2], ((2, 0), (0, 2)))
    return None


def mostrar_mensaje(texto):
    render = fuente.render(texto, True, VERDE)
    rect = render.get_rect(center=(ANCHO // 2, ALTO // 2))
    pantalla.blit(render, rect)


def reiniciar_juego():
    global estado_tablero, lineas, circulos, ganador, player
    estado_tablero = crear_tablero()
    lineas = {}
    circulos = {}
    ganador = None
    player = 1


# ----------- VARIABLES DEL JUEGO -------------

estado_tablero = crear_tablero()
matriz = crear_matriz_rect()
lineas = {}
circulos = {}
player = 1
ganador = None

# -------------- BUCLE PRINCIPAL -----------------

ejecutando = True
while ejecutando:
    reloj.tick(60)
    dibujar_tablero()
    dibujar_figuras()

    # Mostrar mensaje si alguien ganó
    if ganador:
        mostrar_mensaje(f"Ganó {'X' if ganador == 1 else 'O'} - R para reiniciar")

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_q:
                ejecutando = False
            elif evento.key == pygame.K_r:
                reiniciar_juego()

        if evento.type == pygame.MOUSEBUTTONDOWN and not ganador:
            pos_mouse = pygame.mouse.get_pos()
            fila = pos_mouse[1] // CELDA
            col = pos_mouse[0] // CELDA

            if 0 <= fila < 3 and 0 <= col < 3:
                rect = matriz[fila][col]

                # Borrar lo que había antes (permitir sobreescritura)
                if (fila, col) in lineas:
                    del lineas[(fila, col)]
                if (fila, col) in circulos:
                    del circulos[(fila, col)]

                if player == 1:
                    margen = 20
                    lineas[(fila, col)] = [
                        ((rect.left + margen, rect.top + margen), (rect.right - margen, rect.bottom - margen)),
                        ((rect.right - margen, rect.top + margen), (rect.left + margen, rect.bottom - margen))
                    ]
                    estado_tablero[fila][col] = 1
                else:
                    circulos[(fila, col)] = rect.center
                    estado_tablero[fila][col] = -1

                # Verificamos si alguien ganó
                resultado = verificar_victoria(estado_tablero)
                if resultado:
                    ganador, coords = resultado
                else:
                    player *= -1  # Cambiar de turno

    pygame.display.flip()

pygame.quit()
