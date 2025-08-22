import numpy as np
from typing import List, Optional, Union

class Grafo:
    def __init__(self, direcionado: bool, ponderado: bool):
        self.direcionado = direcionado
        self.ponderado = ponderado
        self.vertices: List[str] = []

    def inserir_vertice(self, label: str) -> bool:
        raise NotImplementedError

    def remover_vertice(self, indice: int) -> bool:
        raise NotImplementedError

    def label_vertice(self, indice: int) -> str:
        if indice < 0 or indice >= len(self.vertices):
            raise IndexError("Índice fora do intervalo")
        return self.vertices[indice]

    def imprimir_grafo(self) -> None:
        raise NotImplementedError

    def inserir_aresta(self, origem: int, destino: int, peso: float = 1) -> bool:
        raise NotImplementedError

    def remover_aresta(self, origem: int, destino: int) -> bool:
        raise NotImplementedError

    def existe_aresta(self, origem: int, destino: int) -> bool:
        raise NotImplementedError

    def peso_aresta(self, origem: int, destino: int) -> Optional[float]:
        raise NotImplementedError

    def retornar_vizinhos(self, vertice: int) -> List[int]:
        raise NotImplementedError


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
            # Adiciona nova linha e coluna
            new_row = np.zeros((1, n-1), dtype=np.float32)
            self.matriz = np.vstack([self.matriz, new_row])
            new_col = np.zeros((n, 1), dtype=np.float32)
            self.matriz = np.hstack([self.matriz, new_col])
        return True

    def remover_vertice(self, indice: int) -> bool:
        if indice < 0 or indice >= len(self.vertices):
            return False
        
        self.vertices.pop(indice)
        self.matriz = np.delete(self.matriz, indice, axis=0)  # Remove linha
        self.matriz = np.delete(self.matriz, indice, axis=1)  # Remove coluna
        return True

    def imprimir_grafo(self) -> None:
        print("  ", end="")
        for vertice in self.vertices:
            print(f"{vertice:>5}", end="")
        print()
        
        for i in range(len(self.vertices)):
            print(f"{self.vertices[i]:<2}", end="")
            linha_formatada = []
            for valor in self.matriz[i]:
                if self.ponderado:
                    linha_formatada.append(f"{valor:>5.1f}")
                else:
                    linha_formatada.append(f"{int(valor):>5d}")
            print("".join(linha_formatada))

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
        if origem < 0 or destino < 0 or origem >= len(self.vertices) or destino >= len(self.vertices):
            return None
        return self.matriz[origem, destino] if self.matriz[origem, destino] != 0 else None

    def retornar_vizinhos(self, vertice: int) -> List[int]:
        if vertice < 0 or vertice >= len(self.vertices):
            return []
        
        vizinhos = np.where(self.matriz[vertice] != 0)[0].tolist()
        return vizinhos


class GrafoLista(Grafo):
    class Aresta:
        def __init__(self, destino: int, peso: float = 1):
            self.destino = destino
            self.peso = peso

        def __repr__(self):
            return f"(→{self.destino} [{self.peso}])"

    def __init__(self, direcionado: bool, ponderado: bool):
        super().__init__(direcionado, ponderado)
        self.lista_adj: List[List[GrafoLista.Aresta]] = []

    def inserir_vertice(self, label: str) -> bool:
        self.vertices.append(label)
        self.lista_adj.append([])
        return True

    def remover_vertice(self, indice: int) -> bool:
        if indice < 0 or indice >= len(self.vertices):
            return False
        
        self.vertices.pop(indice)
        self.lista_adj.pop(indice)
        
        # Remove todas as referências ao vértice removido e ajusta índices
        for lista in self.lista_adj:
            lista[:] = [aresta for aresta in lista if aresta.destino != indice]
            for aresta in lista:
                if aresta.destino > indice:
                    aresta.destino -= 1
        return True

    def imprimir_grafo(self) -> None:
        for i, arestas in enumerate(self.lista_adj):
            print(f"{self.vertices[i]}: ", end="")
            print(" ".join(str(aresta) for aresta in arestas))

    def inserir_aresta(self, origem: int, destino: int, peso: float = 1) -> bool:
        if origem < 0 or destino < 0 or origem >= len(self.vertices) or destino >= len(self.vertices):
            return False
        
        peso_final = peso if self.ponderado else 1
        # Verifica se a aresta já existe para atualizar o peso
        for aresta in self.lista_adj[origem]:
            if aresta.destino == destino:
                aresta.peso = peso_final
                break
        else:
            self.lista_adj[origem].append(self.Aresta(destino, peso_final))
        
        if not self.direcionado:
            for aresta in self.lista_adj[destino]:
                if aresta.destino == origem:
                    aresta.peso = peso_final
                    break
            else:
                self.lista_adj[destino].append(self.Aresta(origem, peso_final))
        return True

    def remover_aresta(self, origem: int, destino: int) -> bool:
        if origem < 0 or destino < 0 or origem >= len(self.vertices) or destino >= len(self.vertices):
            return False
        
        # Remove origem → destino
        self.lista_adj[origem] = [a for a in self.lista_adj[origem] if a.destino != destino]
        
        if not self.direcionado:
            # Remove destino → origem
            self.lista_adj[destino] = [a for a in self.lista_adj[destino] if a.destino != origem]
        return True

    def existe_aresta(self, origem: int, destino: int) -> bool:
        if origem < 0 or destino < 0 or origem >= len(self.vertices) or destino >= len(self.vertices):
            return False
        return any(aresta.destino == destino for aresta in self.lista_adj[origem])

    def peso_aresta(self, origem: int, destino: int) -> Optional[float]:
        if origem < 0 or destino < 0 or origem >= len(self.vertices) or destino >= len(self.vertices):
            return None

        for aresta in self.lista_adj[origem]:
            if aresta.destino == destino:
                return aresta.peso if aresta.peso != 0 else None
        return None

    def retornar_vizinhos(self, vertice: int) -> List[int]:
        if vertice < 0 or vertice >= len(self.vertices):
            return []
        return [aresta.destino for aresta in self.lista_adj[vertice]]


if __name__ == "__main__":
    print("=== Grafo Matriz com NumPy ===")
    g = GrafoMatriz(direcionado=False, ponderado=True)
    g.inserir_vertice("Rio")
    g.inserir_vertice("SP")
    g.inserir_vertice("BH")
    
    g.inserir_aresta(0, 1, 430)
    g.inserir_aresta(1, 2, 586)
    g.inserir_aresta(0, 2, 600)
    
    g.imprimir_grafo()
    
    print("\nVizinhos do Rio:", [g.label_vertice(v) for v in g.retornar_vizinhos(0)])
    print("Peso da aresta Rio-SP:", g.peso_aresta(0, 1))

    print("\n=== Grafo Lista ===")
    g2 = GrafoLista(direcionado=True, ponderado=False)
    g2.inserir_vertice("A")
    g2.inserir_vertice("B")
    g2.inserir_vertice("C")
    
    g2.inserir_aresta(0, 1)
    g2.inserir_aresta(1, 2)
    g2.inserir_aresta(0, 2)
    
    g2.imprimir_grafo()
    print("\nVizinhos de A:", [g2.label_vertice(v) for v in g2.retornar_vizinhos(0)])
