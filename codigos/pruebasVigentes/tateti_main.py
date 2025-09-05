import pygame
import sys
import numpy as np

class TatetiBoard:
    def __init__(self):
        pygame.init()
        self.ANCHO = 600
        self.ALTO = 600
        self.FILAS = 3
        self.COLUMNAS = 3
        self.TAMAÑO_CASILLA = self.ANCHO // self.COLUMNAS
        
        # Colores
        self.BLANCO = (255, 255, 255)
        self.NEGRO = (0, 0, 0)
        self.ROJO = (255, 0, 0)
        self.AZUL = (0, 0, 255)
        self.GRIS = (128, 128, 128)
        
        # Configurar pantalla
        self.screen = pygame.display.set_mode((self.ANCHO, self.ALTO))
        pygame.display.set_caption("Ta-Te-Ti Automatizado")
        
        # Tablero (0 = vacío, 1 = X, 2 = O)
        self.tablero = np.zeros((3, 3), dtype=int)
        
        # Turno actual (1 = X, 2 = O)
        self.turno_actual = 1
        
        # Estado del juego
        self.juego_terminado = False
        self.ganador = None

    def dibujar_tablero(self):
        """Dibuja el tablero de ta-te-ti"""
        self.screen.fill(self.BLANCO)
        
        # Dibujar líneas del tablero
        for i in range(1, self.FILAS):
            # Líneas horizontales
            pygame.draw.line(self.screen, self.NEGRO, 
                           (0, i * self.TAMAÑO_CASILLA), 
                           (self.ANCHO, i * self.TAMAÑO_CASILLA), 3)
            # Líneas verticales
            pygame.draw.line(self.screen, self.NEGRO, 
                           (i * self.TAMAÑO_CASILLA, 0), 
                           (i * self.TAMAÑO_CASILLA, self.ALTO), 3)

    def dibujar_x(self, fila, columna):
        """Dibuja una X en la casilla especificada"""
        x_centro = columna * self.TAMAÑO_CASILLA + self.TAMAÑO_CASILLA // 2
        y_centro = fila * self.TAMAÑO_CASILLA + self.TAMAÑO_CASILLA // 2
        offset = self.TAMAÑO_CASILLA // 3
        
        # Dibujar las dos líneas de la X
        pygame.draw.line(self.screen, self.ROJO,
                        (x_centro - offset, y_centro - offset),
                        (x_centro + offset, y_centro + offset), 8)
        pygame.draw.line(self.screen, self.ROJO,
                        (x_centro + offset, y_centro - offset),
                        (x_centro - offset, y_centro + offset), 8)

    def dibujar_o(self, fila, columna):
        """Dibuja un O en la casilla especificada"""
        x_centro = columna * self.TAMAÑO_CASILLA + self.TAMAÑO_CASILLA // 2
        y_centro = fila * self.TAMAÑO_CASILLA + self.TAMAÑO_CASILLA // 2
        radio = self.TAMAÑO_CASILLA // 3
        
        pygame.draw.circle(self.screen, self.AZUL, 
                         (x_centro, y_centro), radio, 8)

    def dibujar_simbolos(self):
        """Dibuja todos los símbolos en el tablero"""
        for fila in range(3):
            for columna in range(3):
                if self.tablero[fila][columna] == 1:  # X
                    self.dibujar_x(fila, columna)
                elif self.tablero[fila][columna] == 2:  # O
                    self.dibujar_o(fila, columna)

    def colocar_simbolo(self, fila, columna):
        """Coloca un símbolo en la casilla especificada"""
        if fila < 0 or fila >= 3 or columna < 0 or columna >= 3:
            print(f"⚠️  Coordenadas fuera de rango: ({fila}, {columna})")
            return False
            
        if self.tablero[fila][columna] != 0:
            print(f"⚠️  Casilla ({fila}, {columna}) ya está ocupada")
            return False
            
        if self.juego_terminado:
            print("⚠️  El juego ya terminó")
            return False
        
        self.tablero[fila][columna] = self.turno_actual
        simbolo = "X" if self.turno_actual == 1 else "O"
        print(f"✅ {simbolo} colocado en casilla ({fila}, {columna})")
        
        # Verificar si hay ganador
        if self.verificar_ganador():
            self.juego_terminado = True
            self.ganador = self.turno_actual
            print(f"🎉 ¡Ganó el jugador {simbolo}!")
        elif self.tablero_lleno():
            self.juego_terminado = True
            print("🤝 ¡Empate!")
        else:
            # Cambiar turno
            self.turno_actual = 2 if self.turno_actual == 1 else 1
            siguiente_simbolo = "X" if self.turno_actual == 1 else "O"
            print(f"🔄 Turno del jugador {siguiente_simbolo}")
        
        return True

    def verificar_ganador(self):
        """Verifica si hay un ganador"""
        # Verificar filas
        for fila in range(3):
            if (self.tablero[fila][0] == self.tablero[fila][1] == 
                self.tablero[fila][2] != 0):
                return True
        
        # Verificar columnas
        for columna in range(3):
            if (self.tablero[0][columna] == self.tablero[1][columna] == 
                self.tablero[2][columna] != 0):
                return True
        
        # Verificar diagonales
        if (self.tablero[0][0] == self.tablero[1][1] == 
            self.tablero[2][2] != 0):
            return True
        if (self.tablero[0][2] == self.tablero[1][1] == 
            self.tablero[2][0] != 0):
            return True
        
        return False

    def tablero_lleno(self):
        """Verifica si el tablero está lleno"""
        return not np.any(self.tablero == 0)

    def reiniciar_juego(self):
        """Reinicia el juego"""
        self.tablero = np.zeros((3, 3), dtype=int)
        self.turno_actual = 1
        self.juego_terminado = False
        self.ganador = None
        print("🔄 Juego reiniciado. Turno del jugador X")

    def mostrar_estado(self):
        """Muestra el estado actual del tablero en consola"""
        print("\n--- Estado del Tablero ---")
        for i, fila in enumerate(self.tablero):
            fila_str = ""
            for j, celda in enumerate(fila):
                if celda == 0:
                    fila_str += " - "
                elif celda == 1:
                    fila_str += " X "
                else:
                    fila_str += " O "
                if j < 2:
                    fila_str += "|"
            print(fila_str)
            if i < 2:
                print("-----------")
        print("-------------------------\n")

    def actualizar_pantalla(self):
        """Actualiza la pantalla con el estado actual"""
        self.dibujar_tablero()
        self.dibujar_simbolos()
        
        # Mostrar mensaje de estado
        font = pygame.font.Font(None, 36)
        if self.juego_terminado:
            if self.ganador:
                simbolo = "X" if self.ganador == 1 else "O"
                texto = f"¡Ganó {simbolo}! Presiona R para reiniciar"
                color = self.ROJO if self.ganador == 1 else self.AZUL
            else:
                texto = "¡Empate! Presiona R para reiniciar"
                color = self.GRIS
        else:
            simbolo = "X" if self.turno_actual == 1 else "O"
            texto = f"Turno: {simbolo}"
            color = self.ROJO if self.turno_actual == 1 else self.AZUL
        
        text_surface = font.render(texto, True, color)
        text_rect = text_surface.get_rect(center=(self.ANCHO//2, self.ALTO + 30))
        
        # Extender la ventana temporalmente para mostrar el texto
        extended_screen = pygame.display.set_mode((self.ANCHO, self.ALTO + 60))
        extended_screen.fill(self.BLANCO)
        extended_screen.blit(self.screen, (0, 0))
        extended_screen.blit(text_surface, text_rect)
        
        pygame.display.flip()
        
        # Volver al tamaño original
        self.screen = pygame.display.set_mode((self.ANCHO, self.ALTO))

    def manejar_eventos(self):
        """Maneja los eventos de pygame"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r and self.juego_terminado:
                    self.reiniciar_juego()
                elif evento.key == pygame.K_s:  # Mostrar estado en consola
                    self.mostrar_estado()
        return True

# Función para integrar con tu sistema de detección
def procesar_deteccion_rojo(casilla, tablero_juego):
    """
    Procesa la detección de rojo y actualiza el tablero
    casilla: tupla (fila, columna) desde detectar_rojo_en_imagen()
    tablero_juego: instancia de TatetiBoard
    """
    if casilla is not None:
        fila, columna = casilla
        tablero_juego.colocar_simbolo(fila, columna)

# Ejemplo de uso
if __name__ == "__main__":
    juego = TatetiBoard()
    clock = pygame.time.Clock()
    
    print("🎮 Ta-Te-Ti Automatizado iniciado")
    print("📋 Controles:")
    print("   - R: Reiniciar juego (cuando termine)")
    print("   - S: Mostrar estado en consola")
    print("   - Cerrar ventana: Salir")
    
    running = True
    while running:
        running = juego.manejar_eventos()
        juego.actualizar_pantalla()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()