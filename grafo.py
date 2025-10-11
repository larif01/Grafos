from typing import List, Optional, Tuple, Dict
from collections import deque
import heapq

class Grafo:
    def __init__(self, direcionado: bool, ponderado: bool):
        self.direcionado = direcionado
        self.ponderado = ponderado
        self.vertices: List[str] = []

    # --- Métodos que as subclasses implementam ---
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

    # --- Algoritmos movidos para dentro de Grafo ---
    def bfs(self, origem: int = 0) -> List[int]:
        """Busca em Largura (ordem de visita)."""
        n = len(self.vertices)
        if origem < 0 or origem >= n:
            return []
        visitados = [False] * n
        ordem = []
        fila = deque([origem])
        visitados[origem] = True
        while fila:
            v = fila.popleft()
            ordem.append(v)
            for u in self.retornar_vizinhos(v):
                if not visitados[u]:
                    visitados[u] = True
                    fila.append(u)
        return ordem

    def dfs(self, origem: int = 0) -> List[int]:
        """Busca em Profundidade (ordem de visita)."""
        n = len(self.vertices)
        if origem < 0 or origem >= n:
            return []
        visitados = [False] * n
        ordem: List[int] = []
        def rec(v: int):
            visitados[v] = True
            ordem.append(v)
            for u in self.retornar_vizinhos(v):
                if not visitados[u]:
                    rec(u)
        rec(origem)
        return ordem

    def dijkstra(self, origem: int = 0) -> Tuple[List[Optional[float]], Dict[int, List[int]]]:
        """
        Dijkstra a partir de 'origem' (default 0).
        Retorna (distancias, caminhos), onde distancias[i] é:
          - distância mínima (float) se alcançável
          - None se inalcançável (evita 'inf' como você pediu)
        Caminhos inalcançáveis vêm como [].
        """
        n = len(self.vertices)
        if origem < 0 or origem >= n:
            return [], {}
        if not self.ponderado:
            # roda só quando ponderado=True
            return [], {}

        dist = [float('inf')] * n
        pred = [-1] * n
        visit = [False] * n
        dist[origem] = 0.0
        pq: List[Tuple[float, int]] = [(0.0, origem)]

        while pq:
            d_atual, v = heapq.heappop(pq)
            if visit[v]:
                continue
            visit[v] = True

            for u in self.retornar_vizinhos(v):
                peso = self.peso_aresta(v, u)
                if peso is None:
                    continue
                nd = d_atual + float(peso)
                if nd < dist[u]:
                    dist[u] = nd
                    pred[u] = v
                    heapq.heappush(pq, (nd, u))

        # Reconstrói caminhos e troca inf -> None
        caminhos: Dict[int, List[int]] = {}
        dist_out: List[Optional[float]] = []
        for i in range(n):
            if dist[i] == float('inf'):
                dist_out.append(None)  # <- nada de 'inf'
                caminhos[i] = []
            else:
                dist_out.append(dist[i])
                caminho = []
                a = i
                while a != -1:
                    caminho.append(a)
                    a = pred[a]
                caminhos[i] = list(reversed(caminho))
        return dist_out, caminhos
