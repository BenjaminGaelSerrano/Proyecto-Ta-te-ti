import matplotlib.pyplot as plt
 
# Inicializamos tablero vacío
tablero = [["" for _ in range(3)] for _ in range(3)]
turno = "X"  # Empieza X
 
def jugar(fila, columna):
    global turno, tablero
    
    # Si la celda está vacía, colocar la marca
    if tablero[fila][columna] == "":
        tablero[fila][columna] = turno
        
        # Dibujar tablero
        fig, ax = plt.subplots(figsize=(4, 4))
 
        # Líneas verticales
        ax.plot([1, 1], [0, 3], color="black", linewidth=2)
        ax.plot([2, 2], [0, 3], color="black", linewidth=2)
 
        # Líneas horizontales
        ax.plot([0, 3], [1, 1], color="black", linewidth=2)
        ax.plot([0, 3], [2, 2], color="black", linewidth=2)
 
        # Ajustes
        ax.set_xlim(0, 3)
        ax.set_ylim(0, 3)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect("equal")
 
        # Dibujar las fichas actuales
        for f in range(3):
            for c in range(3):
                if tablero[f][c] != "":
                    x = c + 0.5
                    y = 2.5 - f
                    ax.text(x, y, tablero[f][c], fontsize=32,
                            ha="center", va="center", fontweight="bold")
 
        plt.show()
 
        # Cambiar turno
        turno = "O" if turno == "X" else "X"
    else:
        print("⚠️ Esa casilla ya está ocupada.")
 
# Ejemplo de uso:
jugar(0, 0)  # X arriba izquierda
jugar(1, 1)  # O en el centro
jugar(2, 2)  # X abajo derecha