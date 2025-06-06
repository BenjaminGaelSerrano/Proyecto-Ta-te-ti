import cv2, pygame, numpy as np, sys

# ---- Inicialización ----
cap = cv2.VideoCapture(1, cv2.CAP_V4L2)  # fuerza backend v4l2 (Linux)
if not cap.isOpened():
    print("No se pudo abrir la cámara. ¿Está en uso o sin permisos?")
    sys.exit(1)                           # aborta solo si la cámara no existe

pygame.init()
W, H = 640, 480
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Ta-Te-Ti con detección de verde")
clock = pygame.time.Clock()
# ---- Colores y tablero ----
WHITE, RED, BLUE = (255, 255, 255), (255, 0, 0), (0, 0, 255)
lower_red1 = np.array([0, 70, 50])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 70, 50])
upper_red2 = np.array([180, 255, 255])
LINE, LW = (0, 255, 0), 4
board = [["" for _ in range(3)] for _ in range(3)]
turn, cd = "X", 0
cell_w, cell_h = W // 3, H // 3

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

def detectar_rojo(f):
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)
    conts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if conts:
        c = max(conts, key=cv2.contourArea)
        if cv2.contourArea(c) > 1000:
            M = cv2.moments(c)
            if M["m00"]:
                return int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"])
    return None



# ---- Loop principal ----
running = True
while running:
    ok, frame = cap.read()
    if not ok:           # la cámara falló a mitad de ejecución:
        continue         # seguí intentando sin cerrar la ventana

    # --- detección y jugada ---
    pos = detectar_rojo(frame) if cd == 0 else None
    if pos:
        x, y = pos       
        col, row = x * 3 // W, y * 3 // H
        if board[row][col] == "":
            board[row][col] = turn
            turn = "O" if turn == "X" else "X"
            cd = 30      # cooldown para evitar doble clic

    cd = max(cd-1, 0)

   # --- dibujar cámara ---
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (W, H))

# Usamos make_surface y giramos
    frame = pygame.surfarray.make_surface(frame)
    frame = pygame.transform.rotate(frame, -90)
    screen.blit(frame, (0, 0))



    draw_board()
    pygame.display.flip()

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False

    clock.tick(30)

cap.release()
pygame.quit()
