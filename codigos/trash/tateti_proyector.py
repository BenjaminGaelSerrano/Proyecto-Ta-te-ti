import pygame      
import random       
# Inicializar Pygame
pygame.init() 

ANCHO, ALTO = 700,700             # Define el ancho y alto de la ventana del juego.
pantalla = pygame.display.set_mode((ANCHO, ALTO))   # Crea la ventana con el tamaño especificado.
pygame.display.set_caption("TA-TE-TI")

#aca se deben definir colores
BLANCO = (255, 255, 255)  # Color blanco (para el fondo)
NEGRO = (0, 0, 0)         # Color negro (para las líneas del tablero)
AZUL= (0, 0, 255)
ROJOPUTO= (254, 0, 0)#AMARGO

# Calcular el tamaño de cada celda (para un tablero 3x3)
CELDA = ANCHO // 3  # Divide el ancho entre 3 para obtener el tamaño de cada celda (100 píxeles)
# NOTA: usamos "//" (división entera) para obtener un número entero en lugar de un decimal



# Crear una matriz (lista de listas) para guardar las coordenadas de cada celda
matriz = []  # Lista vacía donde guardaremos cada fila
for fila in range(3):  # Bucle para recorrer las 3 filas
    fila_celdas = []  # Lista vacía para las celdas de esta fila
    for col in range(3):  # Bucle para recorrer las 3 columnas
        x = col * CELDA  # Calcula la coordenada x de la celda
        y = fila * CELDA  # Calcula la coordenada y de la celda
        celda_rect = pygame.Rect(x, y, CELDA, CELDA)  # Crea un rectángulo con estas coordenadas y tamaño
        fila_celdas.append(celda_rect)  # Guarda la celda en la fila
    matriz.append(fila_celdas)  # Guarda la fila en la matriz
    lineas = []  # Lista para guardar las líneas dibujadas
    circulos = []


# Bucle principal del juego
reloj = pygame.time.Clock()   # Creamos un reloj para controlar la velocidad del juego.
ejecutando = True    # Variable para controlar si el juego sigue o termino.
while ejecutando:      # Bucle principal, se repite hasta que el jugador pierda o cierre la ventana. 
    
    
    reloj.tick(60)#limitamos el grafico a 60 fotogramas por segundo
    pantalla.fill(BLANCO)
    # Dibujar las líneas del tablero para hacer una matriz 3x3
    for i in range(1, 3):  # i toma los valores 1 y 2 (líneas divisorias)
        pygame.draw.line(pantalla, NEGRO, (i * CELDA, 0), (i * CELDA, ALTO), 3)  # Línea vertical
        pygame.draw.line(pantalla, NEGRO, (0, i * CELDA), (ANCHO, i * CELDA), 3)  # Línea horizontal
#                             puntoinicial(x,        y), pfinal(  x  ,   y      ),gorsor)  
    for centro in circulos:
        pygame.draw.circle(pantalla, ROJO, centro, CELDA//3, 3)  # Círculo de radio proporcional a la celda

    # Dibujar todas las líneas guardadas
    for linea in lineas:
        pygame.draw.line(pantalla, AZUL, linea[0], linea[1], 3)
    player=1
    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_q:
                ejecutando = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            #aca iria la variable que indicaria que jugador es cada uno! :V
            
            
            
            pos_mouse = pygame.mouse.get_pos()
            # Revisar si el clic está en la primera celda (0, 0)
            if pos_mouse[1] > 0 and pos_mouse[1] <= CELDA and pos_mouse[0] > 233 and pos_mouse[0] <= (ANCHO/3)*2 and player==-1:
                # Agregar coordenadas de la línea a la lista
                lineas.append(((CELDA//4, CELDA//4), (CELDA*3//4, CELDA*3//4)))  # Diagonal \
                lineas.append(((CELDA*3//4, CELDA//4), (CELDA//4, CELDA*3//4)))  # Diagonal /

            elif  pos_mouse[1] > 0 and pos_mouse[1] <= CELDA and pos_mouse[0] > 233 and pos_mouse[0] <= (ANCHO/3)*2 and player==-1:
                centro_circulo = (CELDA//2, CELDA//2)
                circulos.append(centro_circulo)
            player=player*-1
    pygame.display.flip()  # Actualiza la ventana

# Cuando el bucle termina, cerramos Pygame
pygame.quit()

# Al salir del juego, imprimimos las coordenadas de cada celda (para verificar)
print("Coordenadas de las celdas:")
for i, fila in enumerate(matriz):  # i es el número de fila (0,1,2)
    for j, celda in enumerate(fila):  # j es el número de columna (0,1,2)
        print(f"Celda ({i}, {j}): x={celda.x}, y={celda.y}, ancho={celda.width}, alto={celda.height}")
        
            

