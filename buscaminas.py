import random
import os
import sys

class Buscaminas:
    def __init__(self, filas=8, columnas=8, minas=10):
        self.filas = filas
        self.columnas = columnas
        self.minas = minas
        self.tablero = [[' ' for _ in range(columnas)] for _ in range(filas)]
        self.tablero_visible = [[' ' for _ in range(columnas)] for _ in range(filas)]
        self.minas_ubicadas = set()
        self.juego_terminado = False
        self.victoria = False
        self._colocar_minas()

    def _colocar_minas(self):
        while len(self.minas_ubicadas) < self.minas:
            f = random.randint(0, self.filas - 1)
            c = random.randint(0, self.columnas - 1)
            if (f, c) not in self.minas_ubicadas:
                self.minas_ubicadas.add((f, c))
                self.tablero[f][c] = '*'

        # Calcular números
        for f in range(self.filas):
            for c in range(self.columnas):
                if self.tablero[f][c] == '*':
                    continue
                conte_minas = 0
                for df in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nf, nc = f + df, c + dc
                        if 0 <= nf < self.filas and 0 <= nc < self.columnas:
                            if self.tablero[nf][nc] == '*':
                                conte_minas += 1
                if conte_minas > 0:
                    self.tablero[f][c] = str(conte_minas)

    def imprimir_tablero(self, revelar=False):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("   " + " ".join([str(i) for i in range(self.columnas)]))
        print("  +" + "--" * self.columnas + "+")
        for f in range(self.filas):
            fila_str = ""
            for c in range(self.columnas):
                valor = self.tablero_visible[f][c]
                if revelar:
                    valor = self.tablero[f][c]
                fila_str += valor + " "
            print(f"{f} | {fila_str}|")
        print("  +" + "--" * self.columnas + "+")

    def descubrir(self, f, c):
        if not (0 <= f < self.filas and 0 <= c < self.columnas):
            print("Coordenadas fuera de rango.")
            return

        if self.tablero_visible[f][c] != ' ':
            print("Casilla ya descubierta.")
            return

        if (f, c) in self.minas_ubicadas:
            self.juego_terminado = True
            self.victoria = False
            return

        self.tablero_visible[f][c] = self.tablero[f][c]

        if self.tablero[f][c] == ' ':
            # Revelar adyacentes vacíos recursivamente
            cola = [(f, c)]
            visitados = set([(f, c)])
            while cola:
                cf, cc = cola.pop(0)
                for df in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nf, nc = cf + df, cc + dc
                        if 0 <= nf < self.filas and 0 <= nc < self.columnas:
                            if (nf, nc) not in visitados and self.tablero_visible[nf][nc] == ' ':
                                self.tablero_visible[nf][nc] = self.tablero[nf][nc]
                                visitados.add((nf, nc))
                                if self.tablero[nf][nc] == ' ':
                                    cola.append((nf, nc))

    def verificar_victoria(self):
        casillas_descubiertas = 0
        for f in range(self.filas):
            for c in range(self.columnas):
                if self.tablero_visible[f][c] != ' ':
                    casillas_descubiertas += 1
        if casillas_descubiertas == (self.filas * self.columnas) - self.minas:
            self.juego_terminado = True
            self.victoria = True

def main():
    print("Bienvenido al Buscaminas de Consola!")
    try:
        filas = int(input("Filas (defaulf 8): ") or 8)
        cols = int(input("Columnas (default 8): ") or 8)
        minas = int(input("Minas (default 10): ") or 10)
    except ValueError:
        filas, cols, minas = 8, 8, 10
    
    juego = Buscaminas(filas, cols, minas)
    
    while not juego.juego_terminado:
        juego.imprimir_tablero()
        try:
            entrada = input("Ingresa fila y columna (ej: 3 4) o 's' para salir: ")
            if entrada.lower() == 's':
                break
            partes = entrada.split()
            if len(partes) != 2:
                continue
            f, c = int(partes[0]), int(partes[1])
            juego.descubrir(f, c)
            juego.verificar_victoria()
        except ValueError:
            pass
        except KeyboardInterrupt:
            sys.exit()

    juego.imprimir_tablero(revelar=True)
    if juego.victoria:
        print("\n¡FELICIDADES! ¡Has ganado! 🎉")
    else:
        print("\n¡BOOM! Has pisado una mina. Fin del juego. 💥")

if __name__ == "__main__":
    main()
