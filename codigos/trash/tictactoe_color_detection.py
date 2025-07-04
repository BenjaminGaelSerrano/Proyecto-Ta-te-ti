import cv2
import pygame
import numpy as np

# Inicialización de cámara y Pygame
cap = cv2.VideoCapture(0)
pygame.init()

# Tamaño de ventana
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ta-Te-Ti con detección de color verde")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LINE_COLOR = (0, 255, 0)
LINE_WIDTH = 4

# Tablero
turn = "X"
board = [["" for _ in range(3)] for _ in range(3)]
cell_w = width // 3
cell_h = height // 3

# Función para dibujar el tablero y fichas
def draw_board():
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (0, i * cell_h), (width, i * cell_h), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * cell_w, 0), (i * cell_w, height), LINE_WIDTH)
    for y in range(3):
        for x in range(3):
            if board[y][x] == "X":
                pygame.draw.line(screen, RED, (x * cell_w + 20, y * cell_h + 20), ((x+1) * cell_w - 20, (y+1) * cell_h - 20), LINE_WIDTH)
                pygame.draw.line(screen, RED, ((x+1) * cell_w - 20, y * cell_h + 20), (x * cell_w + 20, (y+1) * cell_h - 20), LINE_WIDTH)
            elif board[y][x] == "O":
                pygame.draw.circle(screen, BLUE, (x * cell_w + cell_w // 2, y * cell_h + cell_h // 2), min(cell_w, cell_h)//2 - 20, LINE_WIDTH)

# Detección de color verde
def detectar_verde(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_green = np.array([40, 70, 70])
    upper_green = np.array([80, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest) > 1000:
            M = cv2.moments(largest)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                return cx, cy
    return None

# Loop principal
clock = pygame.time.Clock()
running = True
cooldown = 0

while running:
    ret, frame = cap.read()
    if not ret:
        break

    coords = detectar_verde(frame)

    if coords and cooldown == 0:
        try:
            x, y = coords

            # Espejar horizontal para que coincida con el movimiento del jugador
            x = width - x

            # Calcular columna y fila
            col = x * 3 // width
            row = y * 3 // height

            if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == "":
                board[row][col] = turn
                turn = "O" if turn == "X" else "X"
                cooldown = 30

        except Exception as e:
            print("Error al procesar coordenadas:", e)

    if cooldown > 0:
        cooldown -= 1

    # Mostrar cámara en Pygame
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_rgb = cv2.flip(frame_rgb, 1)
    frame_rgb = cv2.resize(frame_rgb, (width, height))
    frame_rgb = np.transpose(frame_rgb, (1, 0, 2))
    frame_surface = pygame.surfarray.make_surface(frame_rgb)
    screen.blit(frame_surface, (0, 0))

    draw_board()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(30)

cap.release()
pygame.quit()
