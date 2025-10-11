from typing import List, Optional
from grafo import Grafo

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
        
        for i, arestas in enumerate(self.lista_adj):
            self.lista_adj[i] = [a for a in arestas if a.destino != indice]
            for aresta in self.lista_adj[i]:
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
        self.remover_aresta(origem, destino)
        self.lista_adj[origem].append(self.Aresta(destino, peso_final))
        
        if not self.direcionado:
            self.remover_aresta(destino, origem)
            self.lista_adj[destino].append(self.Aresta(origem, peso_final))
            
        return True

    def remover_aresta(self, origem: int, destino: int) -> bool:
        if origem < 0 or destino < 0 or origem >= len(self.vertices) or destino >= len(self.vertices):
            return False
        
        self.lista_adj[origem] = [a for a in self.lista_adj[origem] if a.destino != destino]
        
        if not self.direcionado:
            self.lista_adj[destino] = [a for a in self.lista_adj[destino] if a.destino != origem]
            
        return True

    def existe_aresta(self, origem: int, destino: int) -> bool:
        if origem < 0 or destino < 0 or origem >= len(self.vertices) or destino >= len(self.vertices):
            return False
        return any(aresta.destino == destino for aresta in self.lista_adj[origem])

    def peso_aresta(self, origem: int, destino: int) -> Optional[float]:
        if not self.existe_aresta(origem, destino):
            return None
            
        for aresta in self.lista_adj[origem]:
            if aresta.destino == destino:
                return aresta.peso
        return None

    def retornar_vizinhos(self, vertice: int) -> List[int]:
        if vertice < 0 or vertice >= len(self.vertices):
            return []
        return [aresta.destino for aresta in self.lista_adj[vertice]]