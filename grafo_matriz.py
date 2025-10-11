import numpy as np
from typing import List, Optional
from grafo import Grafo

class GrafoMatriz(Grafo):
    def __init__(self, direcionado: bool, ponderado: bool):
        super().__init__(direcionado, ponderado)
        self.matriz: np.ndarray = np.array([], dtype=np.float32).reshape(0, 0)

    def inserir_vertice(self, label: str) -> bool:
        self.vertices.append(label)
        n = len(self.vertices)
        
        if n == 1:
            self.matriz = np.zeros((1, 1), dtype=np.float32)
        else:
            self.matriz = np.pad(self.matriz, ((0, 1), (0, 1)), mode='constant', constant_values=0)
        return True

    def remover_vertice(self, indice: int) -> bool:
        if indice < 0 or indice >= len(self.vertices):
            return False
        
        self.vertices.pop(indice)
        self.matriz = np.delete(self.matriz, indice, axis=0)
        self.matriz = np.delete(self.matriz, indice, axis=1)
        return True

    def imprimir_grafo(self) -> None:
        print("  ", end="")
        for vertice in self.vertices:
            print(f"{vertice:>5}", end="")
        print()
        
        for i in range(len(self.vertices)):
            print(f"{self.vertices[i]:<2}", end="")
            for j in range(len(self.vertices)):
                valor = self.matriz[i, j]
                if self.ponderado:
                    print(f"{valor:>5.1f}" if valor != 0 else "    0", end="")
                else:
                    print(f"{int(valor):>5d}" if valor != 0 else "    0", end="")
            print()

    def inserir_aresta(self, origem: int, destino: int, peso: float = 1) -> bool:
        if origem < 0 or destino < 0 or origem >= len(self.vertices) or destino >= len(self.vertices):
            return False
        
        self.matriz[origem, destino] = peso if self.ponderado else 1
        if not self.direcionado:
            self.matriz[destino, origem] = peso if self.ponderado else 1
        return True

    def remover_aresta(self, origem: int, destino: int) -> bool:
        if origem < 0 or destino < 0 or origem >= len(self.vertices) or destino >= len(self.vertices):
            return False
        
        self.matriz[origem, destino] = 0
        if not self.direcionado:
            self.matriz[destino, origem] = 0
        return True

    def existe_aresta(self, origem: int, destino: int) -> bool:
        if origem < 0 or destino < 0 or origem >= len(self.vertices) or destino >= len(self.vertices):
            return False
        return self.matriz[origem, destino] != 0

    def peso_aresta(self, origem: int, destino: int) -> Optional[float]:
        if not self.existe_aresta(origem, destino):
            return None
        return self.matriz[origem, destino]

    def retornar_vizinhos(self, vertice: int) -> List[int]:
        if vertice < 0 or vertice >= len(self.vertices):
            return []
        
        vizinhos = []
        for i in range(len(self.vertices)):
            if self.matriz[vertice, i] != 0:
                vizinhos.append(i)
        return vizinhos