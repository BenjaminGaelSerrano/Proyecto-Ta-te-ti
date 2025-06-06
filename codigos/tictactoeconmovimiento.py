import cv2
import pygame
import numpy as np
import time

# ---- Inicialización ----
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("No se pudo abrir la cámara.")
    exit()

pygame.init()
W, H = 640, 480
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Ta-Te-Ti con detección de color (foto)")
clock = pygame.time.Clock()

# ---- Colores y tablero ----
WHITE, RED, BLUE = (255, 255, 255), (255, 0, 0), (0, 0, 255)
LINE, LW = (0, 255, 0), 4
board = [["" for _ in range(3)] for _ in range(3)]
turn = "X"
cell_w, cell_h = W // 3, H // 3

analyze_frame = None
analyze_start_time = 0
analyze_duration = 2  # segundos para mostrar la foto antes de analizar

def draw_board():
    for i in range(1, 3):
        pygame.draw.line(screen, LINE, (0, i*cell_h), (W, i*cell_h), LW)
        pygame.draw.line(screen, LINE, (i*cell_w, 0), (i*cell_w, H), LW)
    for r in range(3):
        for c in range(3):
            cx, cy = c*cell_w + cell_w//2, r*cell_h + cell_h//2
            if board[r][c] == "X":
                pygame.draw.line(screen, RED, (c*cell_w+20, r*cell_h+20),
                                 ((c+1)*cell_w-20, (r+1)*cell_h-20), LW)
                pygame.draw.line(screen, RED, ((c+1)*cell_w-20, r*cell_h+20),
                                 (c*cell_w+20, (r+1)*cell_h-20), LW)
            elif board[r][c] == "O":
                pygame.draw.circle(screen, BLUE, (cx, cy), min(cell_w, cell_h)//2 - 20, LW)

def detectar_color(frame, lower, upper):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    conts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if conts:
        c = max(conts, key=cv2.contourArea)
        if cv2.contourArea(c) > 1000:
            M = cv2.moments(c)
            if M["m00"]:
                return int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"])
    return None

def mostrar_imagen(frame, screen, W, H):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_rgb = cv2.flip(frame_rgb, 1)
    frame_rgb = cv2.resize(frame_rgb, (W, H))
    surface = pygame.surfarray.make_surface(frame_rgb)
    screen.blit(surface, (0, 0))

lower_red1 = np.array([0, 70, 70])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 70, 70])
upper_red2 = np.array([180, 255, 255])

running = True
while running:
    ok, frame = cap.read()
    if not ok:
        continue

    if analyze_frame is None:
        mostrar_imagen(frame, screen, W, H)

        pos1 = detectar_color(frame, lower_red1, upper_red1)
        pos2 = detectar_color(frame, lower_red2, upper_red2)
        pos = pos1 if pos1 else pos2

        if pos:
            print("Color detectado, sacando foto para analizar...")
            analyze_frame = frame.copy()
            analyze_start_time = time.time()
    else:
        # Mostrar la foto sacada
        mostrar_imagen(analyze_frame, screen, W, H)
        elapsed = time.time() - analyze_start_time

        if elapsed >= analyze_duration:
            print("Analizando foto...")
            pos1 = detectar_color(analyze_frame, lower_red1, upper_red1)
            pos2 = detectar_color(analyze_frame, lower_red2, upper_red2)
            pos = pos1 if pos1 else pos2

            if pos:
                x, y = pos
                x = W - x
                col, row = x * 3 // W, y * 3 // H
                print(f"Jugada detectada en fila {row}, columna {col}")

                if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == "":
                    board[row][col] = turn
                    turn = "O" if turn == "X" else "X"
            else:
                print("No se detectó color en la foto.")

            analyze_frame = None

    draw_board()
    pygame.display.flip()

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False

    clock.tick(30)

cap.release()
pygame.quit()
